#!/usr/bin/env python3
"""Відтворення відбору корпусу CTI_250_V1 (250 з 671 документа InfoStream).

Процедура (стаття, підрозділ 5.1): документ належить до місяця за останньою датою формату
РРРР.ММ.ДД у записі; квоти місяців пропорційні кількості документів (метод найбільших остач);
у межах місяця документи впорядковуються за SHA-256 рядка «CTI_250_V1|DOC_ID» і беруться перші nₘ;
у корпусі відновлюється порядок вихідного масиву.

Без текстів скрипт працює за corpus/infostream_671_manifest.csv (стовпці doc_id і month) і
перевіряє стовпці in_corpus_250 та sample_position. Якщо задано --documents (documents.json,
надається на запит), місяці й SHA-256 текстів спершу перераховуються з текстів і звіряються з маніфестом.

Приклад:
    python3 scripts/sample_corpus.py --manifest corpus/infostream_671_manifest.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter

SEED = "CTI_250_V1"
DATE_RE = re.compile(r"(\d{4})\.(\d{2})\.(\d{2})")


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def quotas(counts: dict[str, int], total: int) -> dict[str, int]:
    n = sum(counts.values())
    exact = {m: total * c / n for m, c in counts.items()}
    q = {m: int(v) for m, v in exact.items()}
    for m in sorted(exact, key=lambda m: (-(exact[m] - q[m]), m))[: total - sum(q.values())]:
        q[m] += 1
    return q


def select(rows: list[dict], total: int) -> list[str]:
    counts = Counter(r["month"] for r in rows)
    q = quotas(counts, total)
    chosen = set()
    for m, k in q.items():
        ids = sorted((r["doc_id"] for r in rows if r["month"] == m), key=lambda i: sha256(f"{SEED}|{i}"))
        chosen.update(ids[:k])
    return [r["doc_id"] for r in rows if r["doc_id"] in chosen]  # порядок вихідного масиву


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manifest", required=True, help="corpus/infostream_671_manifest.csv")
    ap.add_argument("--documents", help="documents.json (необов'язково; надається на запит)")
    ap.add_argument("--total", type=int, default=250)
    a = ap.parse_args(argv)
    with open(a.manifest, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    problems = []
    if a.documents:
        with open(a.documents, encoding="utf-8") as f:
            docs = {d["id"]: d for d in json.load(f)}
        for r in rows:
            d = docs.get(r["doc_id"])
            if d is None:
                problems.append(f"{r['doc_id']}: немає в documents.json")
                continue
            y, mo, _ = DATE_RE.findall(d["text"])[-1]
            if f"{y}-{mo}" != r["month"]:
                problems.append(f"{r['doc_id']}: місяць {y}-{mo} ≠ {r['month']}")
            if sha256(d["text"]) != r["text_sha256"]:
                problems.append(f"{r['doc_id']}: SHA-256 тексту не збігається")
    for r in rows:
        if sha256(f"{SEED}|{r['doc_id']}") != r["selection_key_sha256"]:
            problems.append(f"{r['doc_id']}: ключ відбору не збігається")
    picked = select(rows, a.total)
    expected = [r["doc_id"] for r in sorted((r for r in rows if r["in_corpus_250"] == "1"),
                                             key=lambda r: int(r["sample_position"]))]
    month_q = quotas(Counter(r["month"] for r in rows), a.total)
    print(json.dumps({"documents": len(rows), "selected": len(picked), "monthly_quotas": dict(sorted(month_q.items())),
                      "matches_manifest_set": set(picked) == set(expected),
                      "matches_manifest_order": picked == expected, "problems": problems[:20],
                      "problems_total": len(problems)}, ensure_ascii=False, indent=1))
    return 0 if picked == expected and not problems else 1


if __name__ == "__main__":
    sys.exit(main())
