#!/usr/bin/env python3
"""Контракт абляції: контракт v2 без полів modality і polarity та без речення, яке стосується лише їх.
Решта тексту (предикати, правила доказів, атрибуція, час і контекст події) — без змін.
Кожна заміна мусить знайтися в контракті рівно один раз.
Запуск: python3 -I scripts/make_ablation_contract.py --kit .
"""
import argparse
from pathlib import Path

REPL = [
    ("modality: actual | planned | recommended | possible | conditional | unknown;\npolarity: positive | negative;\n", ""),
    ("Не перетворюй плани на здійснені дії, припущення на певність, заперечення на ствердження. ", ""),
    ('"modality": "...", "polarity": "...", ', ""),
    ("(source, relation_type, target, modality, polarity, event_time, attribution)", "(source, relation_type, target, event_time, attribution)"),
]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--kit", default="."); a = ap.parse_args()
    k = Path(a.kit)
    s = (k / "prompts/contract_v2_uk.txt").read_text(encoding="utf-8")
    for old, new in REPL:
        assert s.count(old) == 1, old
        s = s.replace(old, new)
    (k / "prompts/contract_ablation_uk.txt").write_text(s, encoding="utf-8")
    print("ok", len(s))


if __name__ == "__main__":
    main()
