#!/usr/bin/env python3
"""Recompute key numbers of the article from the files of this package and compare them with the article.

Article: D. V. Lande, V. S. Kuzminskyi. "A method for constructing knowledge graphs with generative artificial
intelligence to analyze cyber threat reports" (Ukrainian draft v6.37, 2026-11-05). The values printed in the
article are embedded below exactly as the article prints them (decimal comma, rounding to the printed digits).

What is recomputed and from which files:
- Subsection 6.1 and Table 2: per-document counts (`per_article`) in the analysis results of the CTINexus
  comparison (repeat 1) and of the ablation and repeat 2 study: records and correct records per document, the
  share of confirmed triples and of correct records (means over documents) and the false-form share of
  formula (8) (pooled over documents); differences between systems; the ratio of correct records per document.
  The intervals are read from the analysis outputs and, in addition, re-estimated here by an independent
  document bootstrap (10 000 resamples, own seed); an independent bound must lie within 1.0 percentage point
  of the printed bound (Monte Carlo tolerance).
- Subsection 6.2: the same for part B of the contract v3 study (`per_article`, set S3), and the pooled counts
  of the other-developer audit of part B and of part C (Ukrainian "частина В") with both auditors.
- Subsection 6.3 and Table 3: shares of the qualifier re-audit (numerator / denominator) with the bootstrap
  intervals of its analysis output.
- Subsection 6.4: counts of the 56-document graph and Wilson intervals, recomputed from k and n.
- Subsection 3.4 (step 4, condition (5)): totals of the re-check of the formal acceptance conditions.
Numbers that need the blinding keys or the document texts (for example, which documents hold the wrong
attributions) are not recomputed; they are listed in the output under "not_recomputed".

Only the Python 3.9+ standard library is needed. No document texts or quotes are needed.

    python3 scripts/recompute_article_numbers.py --repo . --out /tmp/article_numbers.json

Exit code: 0 if every recomputed number matches the article, 1 otherwise. License: MIT (see LICENSE).
"""
import argparse
import json
import math
import random
import sys
from pathlib import Path

S = "studies/"
R1 = S + "ctinexus_comparison_repeat1_2026-10-27/analysis/results.json"
R2 = S + "ablation_repeat2_2026-10-27/analysis/results.json"
R2_POST = S + "ablation_repeat2_2026-10-27/analysis/posthoc_review_checks_r2.json"
R2_FORM = S + "ablation_repeat2_2026-10-27/analysis/posthoc_form_errors.json"
WR = S + "wording_reaudit_2026-10-28/analysis/analysis_output.json"
IA2 = S + "independent_audit_repeat2_2026-10-28/analysis/independent_output.json"
V3 = S + "contract_v3_parts_A_B_2026-10-28/analysis/results.json"
IA3 = S + "independent_audit_part_B_2026-10-28/analysis/independent_output.json"
PC = S + "part_C_new_documents_2026-11-05/analysis/results.json"
PCS = S + "part_C_new_documents_2026-11-05/sonnet_reaudit/results.json"
QR = S + "qualifier_reaudit_2026-11-04/analysis/results.json"
XM = S + "cross_document_merge_2026-11-04/analysis/results.json"
AC = S + "acceptance_conditions_2026-11-05/acceptance_conditions_v633.json"

BOOT_REPS = 10000
BOOT_SEED = "cti-kg-edge-qualifiers 0.4.0 independent bootstrap"
BOOT_TOL_PP = 1.0
Z95 = 1.959963984540054


def fmt(x, nd=1):
    """Number as the article prints it: decimal comma, minus sign U+2212."""
    s = f"{x:.{nd}f}"
    if s.startswith("-"):
        s = "−" + s[1:]
        if float(s[1:].replace(",", ".")) == 0:
            s = s[1:]
    return s.replace(".", ",")


def fmt_ci(lo, hi, nd=1):
    return f"[{fmt(lo, nd)}; {fmt(hi, nd)}]"


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def boot(stat, docs, rng):
    vals = []
    n = len(docs)
    for _ in range(BOOT_REPS):
        v = stat([docs[rng.randrange(n)] for _ in range(n)])
        if v is not None:
            vals.append(v)
    return pct(vals, 0.025), pct(vals, 0.975)


def wilson(k, n, z=Z95):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


class PerDoc:
    """Per-document counts of one analysis output: per[doc][system] = {n, correct, triple_c, false_form, ...}."""

    def __init__(self, per):
        self.per = per

    def docs(self, *systems):
        return sorted(d for d, v in self.per.items() if all(v.get(s, {}).get("n", 0) > 0 for s in systems))

    def share(self, d, s, num="correct", den="n"):
        v = self.per[d][s]
        return v[num] / v[den] if v[den] else None

    def mean_share(self, docs, s, num="correct", den="n"):
        return mean([self.share(d, s, num, den) for d in docs])

    def mean_diff(self, docs, x, y, num="correct", den="n"):
        return mean([self.share(d, x, num, den) - self.share(d, y, num, den) for d in docs
                     if self.share(d, x, num, den) is not None and self.share(d, y, num, den) is not None])

    def pooled(self, docs, s, num="false_form", den="triple_c"):
        n = sum(self.per[d][s][den] for d in docs)
        return sum(self.per[d][s][num] for d in docs) / n if n else None

    def pooled_diff(self, docs, x, y, num="false_form", den="triple_c"):
        a, b = self.pooled(docs, x, num, den), self.pooled(docs, y, num, den)
        return None if a is None or b is None else a - b

    def total(self, docs, s, key):
        return sum(self.per[d][s][key] for d in docs)


class Checks:
    def __init__(self):
        self.rows = []
        self.not_recomputed = []

    def add(self, cid, section, quantity, article, computed, source, how="exact"):
        self.rows.append({"id": cid, "section": section, "quantity": quantity, "article": article,
                          "computed": computed, "source": source, "comparison": how,
                          "match": article == computed})

    def tol(self, cid, section, quantity, article_ci, lo, hi, source):
        """Independent bootstrap interval: each bound within BOOT_TOL_PP of the printed bound."""
        a = [float(x.replace("−", "-").replace(",", ".")) for x in article_ci.strip("[]").split("; ")]
        ok = abs(a[0] - lo * 100) <= BOOT_TOL_PP and abs(a[1] - hi * 100) <= BOOT_TOL_PP
        self.rows.append({"id": cid, "section": section, "quantity": quantity, "article": article_ci,
                          "computed": fmt_ci(lo * 100, hi * 100, 2), "source": source,
                          "comparison": f"independent bootstrap, tolerance {BOOT_TOL_PP} pp", "match": ok})


def pp(x):
    return fmt(x * 100)


def ci_pp(ci, sign=1):
    lo, hi = (ci[0] * 100, ci[1] * 100) if sign > 0 else (-ci[1] * 100, -ci[0] * 100)
    return fmt_ci(lo, hi)


def main():
    ap = argparse.ArgumentParser(description="Recompute key numbers of the article from the package files.")
    ap.add_argument("--repo", default=".", help="package folder (default: current folder)")
    ap.add_argument("--out", required=True, help="JSON file to write the comparison to")
    a = ap.parse_args()
    repo = Path(a.repo)

    def load(rel):
        return json.loads((repo / rel).read_text("utf-8"))

    C = Checks()
    rng = random.Random(BOOT_SEED)

    # ------------------------------------------------------------ 6.1 and Table 2
    r1, r2 = load(R1), load(R2)
    p1, p2 = PerDoc(r1["per_article"]), PerDoc(r2["per_article"])
    d1 = p1.docs("A", "B")
    d2ab = p2.docs("A", "B")
    d2ac = p2.docs("A", "C")
    d2cb = p2.docs("C", "B")
    all2 = sorted(p2.per)
    t2 = [  # system label, repeat, PerDoc, system key, documents for shares, all documents
        ("Method", 1, p1, "A", d1, sorted(p1.per),
         ("15,12", "14,46", "97,8", "95,6", "2,0")),
        ("Method", 2, p2, "A", p2.docs("A"), all2, ("15,72", "14,88", "99,1", "94,6", "3,6")),
        ("Ablation", 2, p2, "C", p2.docs("C"), all2, ("13,44", "12,56", "97,4", "92,0", "3,5")),
        ("CTINexus", 1, p1, "B", d1, sorted(p1.per), ("42,24", "37,30", "96,7", "87,3", "8,3")),
        ("CTINexus", 2, p2, "B", p2.docs("B"), all2, ("37,02", "33,04", "97,5", "88,0", "7,3")),
    ]
    for name, rep, p, s, ds, alld, art in t2:
        src = R1 if rep == 1 else R2
        cols = (("records per document", fmt(p.total(alld, s, "n") / len(alld), 2)),
                ("correct records per document", fmt(p.total(alld, s, "correct") / len(alld), 2)),
                ("triple confirmed, % (mean over documents)", pp(p.mean_share(ds, s, "triple_c"))),
                ("correct records, % (mean over documents)", pp(p.mean_share(ds, s))),
                ("false form, % (formula (8), pooled)", pp(p.pooled(ds, s))))
        for (q, v), av in zip(cols, art):
            C.add(f"T2.{name}.{rep}.{q.split(',')[0].split(' (')[0].replace(' ', '_')}", "6.1, Table 2",
                  f"{name}, repeat {rep}: {q}", av, v, f"{src} per_article")
    C.add("T2.ablation_documents", "6.1, Table 2", "ablation: documents with records", "49",
          str(len(p2.docs("C"))), f"{R2} per_article")

    v = p1.mean_diff(d1, "A", "B")
    C.add("6.1.diff_correct.r1", "6.1", "method − CTINexus, correct records, pp, repeat 1", "8,4", pp(v), R1)
    C.add("6.1.diff_correct.r1.ci", "6.1", "95% CI (analysis output)", "[4,4; 12,5]", ci_pp(r1["primary"]["ci95"]), R1)
    lo, hi = boot(lambda s: p1.mean_diff(s, "A", "B"), d1, rng)
    C.tol("6.1.diff_correct.r1.boot", "6.1", "95% CI, independent bootstrap", "[4,4; 12,5]", lo, hi, R1)
    v = p2.mean_diff(d2ab, "A", "B")
    C.add("6.1.diff_correct.r2", "6.1", "method − CTINexus, correct records, pp, repeat 2", "6,6", pp(v), R2)
    C.add("6.1.diff_correct.r2.ci", "6.1", "95% CI (analysis output)", "[2,3; 10,9]",
          ci_pp(r2["P2_share_correct_A_minus_B"]["ci95"]), R2)
    lo, hi = boot(lambda s: p2.mean_diff(s, "A", "B"), d2ab, rng)
    C.tol("6.1.diff_correct.r2.boot", "6.1", "95% CI, independent bootstrap", "[2,3; 10,9]", lo, hi, R2)
    v = p1.pooled_diff(d1, "B", "A")
    C.add("6.1.diff_ff.r1", "6.1", "CTINexus − method, false form, pp, repeat 1", "6,3", pp(v), R1)
    C.add("6.1.diff_ff.r1.ci", "6.1", "95% CI (analysis output, sign reversed)", "[3,0; 9,8]",
          ci_pp(r1["false_form"]["ci95"], -1), R1)
    lo, hi = boot(lambda s: p1.pooled_diff(s, "B", "A"), d1, rng)
    C.tol("6.1.diff_ff.r1.boot", "6.1", "95% CI, independent bootstrap", "[3,0; 9,8]", lo, hi, R1)
    v = p2.pooled_diff(d2ab, "B", "A")
    C.add("6.1.diff_ff.r2", "6.1", "CTINexus − method, false form, pp, repeat 2", "3,7", pp(v), R2)
    C.add("6.1.diff_ff.r2.ci", "6.1", "95% CI (analysis output)", "[0,1; 7,2]",
          ci_pp(r2["secondary"]["false_form_B_minus_A"]["ci95"]), R2)
    lo, hi = boot(lambda s: p2.pooled_diff(s, "B", "A"), d2ab, rng)
    C.tol("6.1.diff_ff.r2.boot", "6.1", "95% CI, independent bootstrap", "[0,1; 7,2]", lo, hi, R2)
    C.add("6.1.ratio_correct.r1", "6.1", "CTINexus / method, correct records per document, repeat 1", "2,6",
          fmt(p1.total(d1, "B", "correct") / p1.total(d1, "A", "correct")), R1)
    C.add("6.1.ratio_correct.r2", "6.1", "CTINexus / method, correct records per document, repeat 2", "2,2",
          fmt(p2.total(all2, "B", "correct") / p2.total(all2, "A", "correct")), R2)
    C.add("6.1.decoys.r1", "6.1", "control records rejected, repeat 1", "237 of 240",
          f"{r1['decoys']['not_correct']} of {r1['decoys']['n']}", R1)
    C.add("6.1.decoys.r2", "6.1", "control records rejected, repeat 2", "242 of 242",
          f"{r2['secondary']['decoys']['not_correct']} of {r2['secondary']['decoys']['n']}", R2)
    post = load(R2_POST)["r2"]["lenient_A-B_BASELINE"]
    C.add("6.1.sens_markers.r2", "6.1", "check 1 (modal markers count as correct), method − CTINexus, pp, repeat 2",
          "2,7 [−0,6; 5,9]", f"{fmt(post['diff'])} {fmt_ci(*post['ci'])}", R2_POST)
    w = load(WR)["R2"]["wording_A-B"]
    C.add("6.1.sens_wording.r2", "6.1", "check 2 (form by relation wording), method − CTINexus, pp, repeat 2",
          "2,3 [−0,9; 5,5]", f"{fmt(w['diff'])} {fmt_ci(*w['ci'])}", WR)
    ia2 = load(IA2)
    C.add("6.1.other_auditor.agree", "6.1", "agreement of the other-developer auditor with the main audit, %",
          "94,6", fmt(ia2["agreement_weighted"]["percent"]), IA2)
    C.add("6.1.other_auditor.diff", "6.1", "method − CTINexus by the other-developer auditor, pp",
          "4,8 [−1,1; 10,6]", f"{fmt(ia2['A-B']['diff'])} {fmt_ci(*ia2['A-B']['ci'])}", IA2)
    C.add("5.2.other_auditor.sample", "5.2", "records in the other-developer audit sample / all records of repeat 2",
          "457 of 2761", f"{sum(x['n'] for x in ia2['strata'].values())} of {sum(x['N'] for x in ia2['strata'].values())}", IA2)
    C.add("5.2.other_auditor.decoys", "5.2", "control records in the other-developer audit", "30",
          str(sum(x["n"] for x in ia2["decoys"].values())), IA2)
    v = p2.pooled_diff(d2ac, "C", "A")
    C.add("6.1.abl_ff", "6.1", "ablation − method, false form, pp", "−0,1", pp(v), R2)
    C.add("6.1.abl_ff.ci", "6.1", "95% CI (analysis output)", "[−3,2; 3,3]", ci_pp(r2["P1_false_form_C_minus_A"]["ci95"]), R2)
    lo, hi = boot(lambda s: p2.pooled_diff(s, "C", "A"), d2ac, rng)
    C.tol("6.1.abl_ff.boot", "6.1", "95% CI, independent bootstrap", "[−3,2; 3,3]", lo, hi, R2)
    v = p2.mean_diff(d2cb, "C", "B")
    C.add("6.1.abl_vs_ctinexus", "6.1", "ablation − CTINexus, correct records, pp", "4,1", pp(v), R2)
    C.add("6.1.abl_vs_ctinexus.ci", "6.1", "95% CI (analysis output)", "[0,2; 8,1]",
          ci_pp(r2["secondary"]["share_correct_C_minus_B"]["ci95"]), R2)
    lo, hi = boot(lambda s: p2.mean_diff(s, "C", "B"), d2cb, rng)
    C.tol("6.1.abl_vs_ctinexus.boot", "6.1", "95% CI, independent bootstrap", "[0,2; 8,1]", lo, hi, R2)
    C.add("6.1.nonactual_correct", "6.1", "correct method records with a form other than actual, positive (repeat 2)",
          "76", str(r2["secondary"]["counts"]["A"]["correct_nonactual"]), R2)
    fe = load(R2_FORM)
    C.add("6.1.false_forms", "6.1", "false forms of the method (repeat 2)", "28",
          str(fe["A"]["other_form_false_form"] + fe["A"]["actual_positive_false_form"]), R2_FORM)
    C.add("6.1.false_forms_nonactual", "6.1", "of them with modality other than actual", "28",
          str(sum(v["false_form"] for k, v in fe["A_other_form_by_label"].items() if not k.startswith("actual,"))), R2_FORM)
    C.add("6.1.false_forms_fact", "6.1", "of them where the document presents the relation as a fact", "26",
          str(fe["A_false_form_direction_manual"]["стаття подає як факт"]), R2_FORM)
    C.not_recomputed.append({"section": "6.1", "quantity": "75 of the 76 correct non-actual method records have no "
                             "correct counterpart in the ablation", "reason": "needs the blinding keys (record-level "
                             "system labels) of the ablation and repeat 2 study"})

    # ------------------------------------------------------------ 6.2, part B (set S3 of the contract v3 study)
    v3 = load(V3)
    p3 = PerDoc({d: x for d, x in v3["per_article"].items() if d.startswith("S3")})
    q1 = v3["Q1_false_form_A2_minus_A3"]["S3"]
    d3 = p3.docs("A2", "A3")
    C.add("6.2.B.docs", "6.2", "part B: documents with edges of both method variants", "24", str(len(d3)), V3)
    C.add("6.2.B.ff_v3", "6.2", "part B: false form, contract v3 (records with confirmed triple)", "1,7 % (7 of 405)",
          f"{pp(p3.pooled(d3, 'A3'))} % ({p3.total(d3, 'A3', 'false_form')} of {p3.total(d3, 'A3', 'triple_c')})", V3)
    C.add("6.2.B.ff_v2", "6.2", "part B: false form, contract v2", "7,5 % (25 of 335)",
          f"{pp(p3.pooled(d3, 'A2'))} % ({p3.total(d3, 'A2', 'false_form')} of {p3.total(d3, 'A2', 'triple_c')})", V3)
    C.add("6.2.B.Q1", "6.2", "part B: Q1, v2 − v3, false form, pp", "5,7 [0,9; 12,1]",
          f"{pp(p3.pooled_diff(d3, 'A2', 'A3'))} {ci_pp(q1['ci95'])}", V3)
    lo, hi = boot(lambda s: p3.pooled_diff(s, "A2", "A3"), d3, rng)
    C.tol("6.2.B.Q1.boot", "6.2", "part B: Q1 95% CI, independent bootstrap", "[0,9; 12,1]", lo, hi, V3)
    sec = v3["secondary"]["S3"]
    alld3 = sorted(p3.per)
    C.add("6.2.B.more_correct", "6.2", "part B: correct records per document, v3 − v2", "3,5 [2,2; 4,9]",
          f"{fmt(mean([p3.per[d]['A3']['correct'] - p3.per[d]['A2']['correct'] for d in alld3]))} "
          f"{fmt_ci(*sec['correct_per_article_A3_minus_A2']['ci95'])}", V3)
    tci = sec["triple_c_share_A3_minus_A2"]["ci95"]
    C.add("6.2.B.triple_share", "6.2", "part B: share of confirmed triples did not change significantly (CI covers 0)",
          "yes", "yes" if tci[0] <= 0 <= tci[1] else "no", V3)
    q2 = v3["Q2_share_correct_A3_minus_B"]["S3"]
    d3b = p3.docs("A3", "B")
    C.add("6.2.B.Q2", "6.2", "part B: Q2, correct records v3 vs CTINexus, % and difference, pp",
          "95,8 % vs 89,0 %, difference 6,8 [1,2; 11,6]",
          f"{pp(p3.mean_share(d3b, 'A3'))} % vs {pp(p3.mean_share(d3b, 'B'))} %, difference "
          f"{pp(p3.mean_diff(d3b, 'A3', 'B'))} {ci_pp(q2['ci95'])}", V3)
    lo, hi = boot(lambda s: p3.mean_diff(s, "A3", "B"), d3b, rng)
    C.tol("6.2.B.Q2.boot", "6.2", "part B: Q2 95% CI, independent bootstrap", "[1,2; 11,6]", lo, hi, V3)
    C.add("6.2.B.ratio", "6.2", "part B: CTINexus / v3, correct records per document", "2,0",
          fmt(p3.total(alld3, "B", "correct") / p3.total(alld3, "A3", "correct")), V3)
    q3 = v3["Q3_false_form_C_minus_A3"]["S3"]
    d3c = p3.docs("C", "A3")
    C.add("6.2.B.Q3", "6.2", "part B: Q3, ablation false form and ablation − v3, pp", "4,5 % (13 of 290), 2,8 [−0,9; 6,0]",
          f"{pp(p3.pooled(d3c, 'C'))} % ({p3.total(d3c, 'C', 'false_form')} of {p3.total(d3c, 'C', 'triple_c')}), "
          f"{pp(p3.pooled_diff(d3c, 'C', 'A3'))} {ci_pp(q3['ci95'])}", V3)
    lo, hi = boot(lambda s: p3.pooled_diff(s, "C", "A3"), d3c, rng)
    C.tol("6.2.B.Q3.boot", "6.2", "part B: Q3 95% CI, independent bootstrap", "[−0,9; 6,0]", lo, hi, V3)
    dec = [v3["Q1_false_form_A2_minus_A3"][s]["decision"] for s in ("S1", "S2")] + \
          [v3["Q2_share_correct_A3_minus_B"][s]["decision"] for s in ("S1", "S2")] + \
          [v3["Q3_false_form_C_minus_A3"]["S2"]["decision"]]
    C.add("6.2.A.same_answers", "6.2", "part A: the same answers to Q1–Q3 as part B (Q1, Q2 established; Q3 not)",
          "yes", "yes" if all("встановлено" in x and "не встановлено" not in x for x in dec[:4])
          and "не встановлено" in dec[4] else "no", V3)
    ia3 = load(IA3)
    iq = ia3["independent"]["Q1_false_form_A2_minus_A3"]
    C.add("6.2.B.other_auditor", "6.2", "part B, other-developer auditor: false form v3 vs v2, difference",
          "2,0 % (8 of 392) vs 10,0 % (33 of 330), 8,0 [2,6; 15,0], 24 documents",
          f"{pp(iq['A3'])} % ({iq['A3_false_form']} of {iq['A3_triple_c']}) vs {pp(iq['A2'])} % "
          f"({iq['A2_false_form']} of {iq['A2_triple_c']}), {pp(iq['diff'])} {ci_pp(iq['ci95'])}, "
          f"{iq['articles']} documents", IA3)
    C.add("6.2.B.other_auditor.items", "6.2", "part B, other-developer auditor: records rated, control records found",
          "584; 85 of 86", f"{ia3['items']}; {ia3['independent']['decoys']['caught_expected']} of "
          f"{ia3['independent']['decoys']['n']}", IA3)
    C.add("6.2.B.other_auditor.agree", "6.2", "part B: form agreement with the main audit (both confirmed the triple), %",
          "97,7", pp(ia3["agreement_with_main"]["form_both_triple_C"]["match"]), IA3)
    pc, pcs = load(PC), load(PCS)
    for lab, r, art in (("Opus", pc, "0,8 % (6 of 713) vs 9,4 % (62 of 662), difference 8,5 [4,8; 13,0], 48"),
                        ("Sonnet", pcs, "1,8 % (13 of 711) vs 7,4 % (49 of 660), difference 5,6 [1,6; 10,6], 48")):
        q = r["Q3_FF_A2_minus_A3"]
        C.add(f"6.2.C.Q1.{lab}", "6.2", f"part C, auditor {lab}: false form v3 vs v2, difference, documents", art,
              f"{pp(q['A3']['num'] / q['A3']['den'])} % ({q['A3']['num']} of {q['A3']['den']}) vs "
              f"{pp(q['A2']['num'] / q['A2']['den'])} % ({q['A2']['num']} of {q['A2']['den']}), difference "
              f"{pp(q['A2']['num'] / q['A2']['den'] - q['A3']['num'] / q['A3']['den'])} {ci_pp(q['ci95'])}, "
              f"{q['articles']}", PC if lab == "Opus" else PCS)
    for lab, r, art in (("Opus", pc, "3,3 [−0,8; 8,3], 49"), ("Sonnet", pcs, "−0,1 [−2,7; 3,0], 49")):
        q = r["Q4_FF_C_minus_A3"]
        C.add(f"6.2.C.Q3.{lab}", "6.2", f"part C, auditor {lab}: ablation − v3, false form, pp, documents", art,
              f"{pp(q['C']['num'] / q['C']['den'] - q['A3']['num'] / q['A3']['den'])} {ci_pp(q['ci95'])}, "
              f"{q['articles']}", PC if lab == "Opus" else PCS)

    # ------------------------------------------------------------ 5.4, 6.3 and Table 3
    qr = load(QR)
    g = qr["groups"]["усі"]

    def share_ci(key):
        x = g[key]
        if abs(x["p"] - x["num"] / x["den"]) > 1e-12:
            raise SystemExit(f"{QR}: p != num/den for {key}")
        return f"{x['den']}; {pp(x['num'] / x['den'])} {fmt_ci(x['lo'] * 100, x['hi'] * 100)}"
    for key, label, art in (
            ("2_атрибуція_C_серед_заповнених", "attribution correct", "1239; 93,9 [87,8; 98,3]"),
            ("2_атрибуція_M_серед_порожніх", "attribution missed", "3134; 3,3 [1,7; 5,1]"),
            ("3_час_C_серед_заповнених", "time correct", "567; 98,9 [97,2; 100,0]"),
            ("3_час_M_серед_порожніх", "time missed", "3806; 3,7 [1,8; 6,0]"),
            ("4_контекст_C_серед_заповнених", "context correct", "1099; 87,0 [78,9; 93,7]"),
            ("5_кваліфікатори_без_помилок_серед_трійки_C", "all filled fields correct", "4373; 95,1 [92,5; 97,3]"),
            ("6_фрагменти_S", "fragments support the whole record", "4205; 83,2 [78,4; 87,5]"),
            ("7_повне_строго_серед_усіх", "edge fully correct", "4379; 71,0 [66,0; 75,9]"),
            ("8_повне_без_пропусків_серед_усіх", "the same, omissions allowed", "4379; 86,9 [83,4; 90,1]"),
            ("9_альтернативні_назви_C", "alternative names correct", "927; 99,5 [98,8; 99,9]")):
        C.add("T3." + label.replace(" ", "_").replace(",", ""), "6.3, Table 3",
              f"{label}: records; share, % [95% CI]", art, share_ci(key), f"{QR} groups (all sets)")
    C.add("5.4.records", "5.4", "edge records and nodes with alternative names in the re-audit", "4379; 927",
          f"{g['edge_records']}; {g['node_records']}", QR)
    C.add("5.4.decoys", "5.4", "control records with a deliberately changed field", "353",
          str(sum(x["total"] for x in qr["decoys"].values())), QR)
    C.add("6.3.frag_P", "6.3", "fragments support neither the triple nor the form, %", "4,1",
          pp(g["6_фрагменти_P"]["num"] / g["6_фрагменти_P"]["den"]), QR)
    C.add("7.frag_not_S", "7", "records with correct triple and form whose fragments do not support the whole record, %",
          "16,8", pp(1 - g["6_фрагменти_S"]["num"] / g["6_фрагменти_S"]["den"]), QR)
    gv2, gv3 = qr["groups"]["v2"], qr["groups"]["v3"]
    k7, k8 = "7_повне_строго_серед_усіх", "8_повне_без_пропусків_серед_усіх"
    C.add("6.3.v3_vs_v2", "6.3", "fully correct records v3 vs v2; the same without omissions, %",
          "74,1 % vs 66,9 %; 90,2 % vs 82,7 %",
          f"{pp(gv3[k7]['num'] / gv3[k7]['den'])} % vs {pp(gv2[k7]['num'] / gv2[k7]['den'])} %; "
          f"{pp(gv3[k8]['num'] / gv3[k8]['den'])} % vs {pp(gv2[k8]['num'] / gv2[k8]['den'])} %", QR)
    det = {k: x["detected"] / x["evaluable"] for k, x in qr["decoys"].items()}
    other = [x for k, x in det.items() if k != "ctx_swap"]
    C.add("6.3.decoys", "6.3", "control records found by kind: range except replaced context; replaced context, %",
          "98,5–100,0; 83,0", f"{pp(min(other))}–{pp(max(other))}; {pp(det['ctx_swap'])}", QR)
    ag = qr["agreement_with_CTI_CONTRACT_V3"]["усі"]
    C.add("6.3.agreement", "6.3", "agreement with the audit of 6.2 on triple and form, %", "99,5; 99,1",
          f"{pp(ag['triple']['agreement'])}; {pp(ag['form_both_triple_C']['agreement'])}", QR)
    C.not_recomputed.append({"section": "6.3", "quantity": "wrong attributions concentrated in four documents (60 of 64 "
                             "records), the kinds of those documents and of the wrong contexts",
                             "reason": "needs the blinding key of the qualifier re-audit (record-level sources) and "
                             "the document texts"})

    # ------------------------------------------------------------ 6.4
    xm = load(XM)
    mn = xm["main"]

    def wil(x):
        lo, hi = wilson(x["k"], x["n"])
        return f"{x['k']} of {x['n']}, {pp(x['k'] / x['n'])} {fmt_ci(lo * 100, hi * 100)}"
    C.add("6.4.nodes", "6.4", "nodes; nodes joining several documents; of them specific entities", "1531; 187; 111",
          f"{xm['nodes']['total']}; {xm['nodes']['cross_doc']}; {xm['nodes']['cross_doc_by_kind']['resolved']}", XM)
    C.add("6.4.specific", "6.4", "specific cross-document nodes judged correct (Wilson)", "111 of 111, 100,0 [96,7; 100,0]",
          wil(mn["QB1_nodes_specific"]), XM)
    C.add("6.4.general", "6.4", "general-concept nodes checked and judged correct", "20 of 20",
          f"{mn['QB1_nodes_general']['k']} of {mn['QB1_nodes_general']['n']}", XM)
    C.add("6.4.pairs", "6.4", "unmerged candidate pairs that are the same entity (Wilson)", "19 of 146, 13,0 [8,5; 19,4]",
          wil(mn["QB1_pairs"]), XM)
    me = mn["QB1_pairs"]["missed_estimate"]
    C.add("6.4.pairs_missed", "6.4", "estimated missed merges among all unmerged candidate pairs", "56 [37; 84] of 430",
          f"{round(me['point'])} [{round(me['lo'])}; {round(me['hi'])}] of {mn['QB1_pairs']['population']}", XM)
    lo, hi = wilson(mn["QB1_pairs"]["k"], mn["QB1_pairs"]["n"])
    pop = mn["QB1_pairs"]["population"]
    C.add("6.4.pairs_missed.wilson", "6.4", "the same, recomputed as population × Wilson bounds", "56 [37; 84]",
          f"{round(pop * mn['QB1_pairs']['k'] / mn['QB1_pairs']['n'])} [{round(pop * lo)}; {round(pop * hi)}]", XM)
    C.add("6.4.audit_pairs", "6.4 (5.5)", "random unmerged candidate pairs given to the auditor", "150",
          str(xm["audit"]["items"]["pair"]["real"]), XM)
    tr = xm["triples"]
    C.add("6.4.triples", "6.4", "triples given by at least two documents; merged into one edge each", "39; 26",
          f"{tr['in_2plus_docs']}; {xm['edges']['cross_doc']}", XM)
    C.add("6.4.merges", "6.4", "merges judged correct (Wilson)", "26 of 26, 100,0 [87,1; 100,0]", wil(mn["QB2_merge"]), XM)
    C.add("6.4.not_merged", "6.4", "triples left as several edges; of them with different forms", "13; 3",
          f"{tr['in_2plus_docs'] - xm['edges']['cross_doc']}; {tr['different_forms_across_docs']}", XM)
    C.add("6.4.form_decoys", "6.4", "control records with a changed form found", "2 of 3",
          f"{xm['audit']['decoys']['form']['k']} of {xm['audit']['decoys']['form']['n']}", XM)
    C.add("6.4.contradictory", "6.4", "contradictory claims (positive and negative across documents)", "0",
          str(tr["positive_and_negative_across_docs"]), XM)
    C.not_recomputed.append({"section": "6.4", "quantity": "16 of the 19 same-entity pairs are general designations, "
                             "3 are specific entities (HM Government / UK government, Salt Typhoon, Volt Typhoon); "
                             "10 of the 13 unmerged triples differ in attribution, time or event context",
                             "reason": "needs the resolver and audit keys of the merge study"})

    # ------------------------------------------------------------ 3.4, condition (5)
    ac = load(AC)["by_set"]
    edges = sum(x["edges"] for x in ac.values())
    nodes = sum(x["nodes"] for x in ac.values())
    e_ok = sum(x["edge_all5_ok"] for x in ac.values())
    n_ok = sum(min(x["node_type_ok"], x["node_nonempty_ok"], x["node_verbatim_ok"]) for x in ac.values())
    C.add("3.4.records", "3.4 (step 4)", "method edge and node records re-checked against condition (5)", "7395; 9780",
          f"{edges}; {nodes}", AC)
    C.add("3.4.rejected", "3.4 (step 4)", "records that a checking program would reject", "0",
          str((edges - e_ok) + (nodes - n_ok)), AC)

    ok = all(r["match"] for r in C.rows)
    out = {"article": "Ukrainian draft v6.37 (2026-11-05)", "package_version": "0.4.0",
           "checks": len(C.rows), "matched": sum(r["match"] for r in C.rows), "all_match": ok,
           "bootstrap": {"resamples": BOOT_REPS, "seed": BOOT_SEED, "tolerance_pp": BOOT_TOL_PP},
           "results": C.rows, "not_recomputed": C.not_recomputed}
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", "utf-8")
    print(f"Checks: {len(C.rows)}; matched: {out['matched']}; not recomputed (need keys or texts): "
          f"{len(C.not_recomputed)}")
    for r in C.rows:
        if not r["match"]:
            print(f"  MISMATCH {r['id']}: article {r['article']!r}, computed {r['computed']!r}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
