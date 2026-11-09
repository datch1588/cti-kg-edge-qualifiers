#!/usr/bin/env python3
"""Чи виконують збережені записи методу пʼять формальних умов прийняття (5) статті v6.33.

Записи: усі виходи методу, на яких спираються підрозділи 5.2–5.5 і новий набір 5.3:
- шість наборів повторного аудиту CTI_QUALIFIER_REAUDIT (keys/sources.json: v2-1, v2-2, v3-1, v3-2, v2-N, v3-N);
- 56 запусків CTI_CROSSDOC (W001–W056);
- запуски A2 і A3 CTI_FACTS_NEW (keys/runs_key.json).
Умови для кожного ребра: [r ∈ TE] – relation_type з 20 типів; [qₐ ∈ Q] – modality з M, polarity з Π, атрибуція, час
і контекст – рядки (порожній рядок = ⊥); [type(vs), type(vo) ∈ TV] – кінці ребра існують, їхні entity_type з 19 типів;
[P(a) ≠ ∅] – щонайменше один фрагмент role TARGET; [P(a) ⊑ D] – кожен фрагмент TARGET має doc_id документа, його
paragraph_id є в тексті документа, а цитата після squash() (як у analyze_q.py: кожна послідовність пробільних знаків
→ один пробіл, без крайніх пробілів) непорожня й міститься в так само стиснутому тексті цього абзацу з урахуванням
регістру. Для вузлів – тип з TV, щонайменше один фрагмент TARGET і та сама дослівність.
Окремо рахується дослівність без стискання пробілів (точний підрядок).
Запуск: python3 -I -B umovy_v633.py --m1 /mnt/project-files/metod1 --out <json>
"""
import argparse, collections, json, re
from pathlib import Path

TV = set("threat_actor malware malware_class vulnerability attack_technique tool organization person product "
         "technology campaign incident indicator country location event threat_category security_property other".split())
TE = set("USES EXPLOITS TARGETS AFFECTS DEVELOPS PROVIDES OPERATES LEADS MEMBER_OF PART_OF LOCATED_IN "
         "ATTRIBUTED_TO REPORTS_ON WARNS_ABOUT MITIGATES PROTECTS ENABLES DETECTS DISCOVERS SUPPORTS".split())
M = {"actual", "planned", "recommended", "possible", "conditional", "unknown"}
PI = {"positive", "negative"}
PARA = re.compile(r"^\[(D\d{4}:P\d{4})\] (.*)$", re.M)


def squash(s):
    return " ".join((s or "").split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m1", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    m1 = Path(a.m1)
    runs = []  # (набір, шлях виходу, тека тексту, doc_id)
    for s in json.loads((m1 / "doslid_pereaudyt_kvalifikatoriv_2026-11-04/keys/sources.json").read_text("utf-8")):
        t = s["target"]
        base = m1 / ("doslid_rag_v2/kit/data/targets" if t.startswith("T") else "doslid_kontrakt_v3_2026-10-28/data/targets_new")
        runs.append((s["set"], m1 / s["output"], base / t, t.split("_")[1]))
    X = m1 / "doslid_zlyttia_2026-11-04"
    for r, k in sorted(json.loads((X / "keys/runs_key.json").read_text("utf-8")).items()):
        runs.append(("crossdoc", X / "runs/outputs" / f"{r}.json", X / "data/targets" / k["target"], k["doc_id"]))
    F = m1 / "doslid_polia_novi_statti_2026-11-05"
    for r, k in sorted(json.loads((F / "keys/runs_key.json").read_text("utf-8")).items()):
        if k["system"] in ("A2", "A3"):
            runs.append(("new-" + k["system"], F / "runs/outputs" / f"{r}.json", F / "data/targets" / k["target"], k["doc_id"]))

    tot = collections.defaultdict(collections.Counter)
    fails = []
    for st, out, tdir, doc in runs:
        g = json.loads(out.read_text("utf-8"))
        paras = dict(PARA.findall((tdir / "target.txt").read_text("utf-8")))
        sq = {k: squash(v) for k, v in paras.items()}
        nodes = {n.get("id"): n for n in g.get("nodes") or []}
        c = tot[st]
        c["runs"] += 1

        def frag(item, kind):
            evs = [e for e in item.get("evidence") or [] if e.get("role") == "TARGET"]
            c[f"{kind}_non_target_evidence"] += sum(e.get("role") != "TARGET" for e in item.get("evidence") or [])
            ok_ne = bool(evs)
            ok_sq = ok_ne and all(e.get("doc_id") == doc and e.get("paragraph_id") in paras and squash(e.get("quote"))
                                  and squash(e.get("quote")) in sq[e.get("paragraph_id")] for e in evs)
            ok_ex = ok_ne and all(e.get("doc_id") == doc and e.get("paragraph_id") in paras and e.get("quote")
                                  and e.get("quote") in paras[e.get("paragraph_id")] for e in evs)
            c[f"{kind}_fragments"] += len(evs)
            return ok_ne, ok_sq, ok_ex

        for n in nodes.values():
            c["nodes"] += 1
            ne, sqv, ex = frag(n, "node")
            res = {"type": n.get("entity_type") in TV, "nonempty": ne, "verbatim": sqv}
            for k2, v in res.items():
                c[f"node_{k2}_ok"] += v
            c["node_exact_ok"] += ex
            if not all(res.values()):
                fails.append({"set": st, "run": out.name, "node": n.get("id"), **res})
        for e in g.get("edges") or []:
            c["edges"] += 1
            s, o = nodes.get(e.get("source")), nodes.get(e.get("target"))
            ne, sqv, ex = frag(e, "edge")
            res = {"rel": e.get("relation_type") in TE,
                   "qual": e.get("modality") in M and e.get("polarity") in PI and
                           all(isinstance(e.get(f, ""), str) for f in ("attribution", "event_time", "event_scope")),
                   "types": bool(s and o) and s.get("entity_type") in TV and o.get("entity_type") in TV,
                   "nonempty": ne, "verbatim": sqv}
            for k2, v in res.items():
                c[f"edge_{k2}_ok"] += v
            c["edge_all5_ok"] += all(res.values())
            c["edge_exact_ok"] += ex
            if not all(res.values()):
                fails.append({"set": st, "run": out.name, "edge": e.get("id"), **res})
    allc = collections.Counter()
    for c in tot.values():
        allc.update(c)
    res = {"by_set": {k: dict(v) for k, v in sorted(tot.items())}, "all": dict(allc), "failures": fails}
    Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res["all"], ensure_ascii=False, indent=1))
    print("невиконаних записів:", len(fails))
    for f in fails[:30]:
        print(f)


if __name__ == "__main__":
    main()
