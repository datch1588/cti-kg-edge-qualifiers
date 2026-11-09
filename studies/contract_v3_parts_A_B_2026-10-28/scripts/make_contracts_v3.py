#!/usr/bin/env python3
"""Контракти досліду CTI_CONTRACT_V3 (28.10.2026).

contract_v3_uk.txt  = contract_v2_uk.txt + блок правил 8а (prompts/rule_8a_uk.txt), вставлений одразу після правила 8.
                      Решта тексту v2 не змінюється.
contract_ablation_uk.txt = contract_v3 без блоку 8а і з тими самими чотирма замінами, що й 27.10
                      (doslid_ablyatsiia_povtor_2026-10-27/scripts/make_ablation_contract.py).
Скрипт перевіряє, що контракт абляції байт у байт збігається з контрактом абляції 27.10, тож виходи C від 27.10
відповідають тому самому контракту.
Запуск: python3 -I scripts/make_contracts_v3.py --kit .
"""
import argparse, hashlib
from pathlib import Path

ANCHOR = "Відмінні події, періоди або автори тверджень не зливаються автоматично.\n"
REPL = [
    ("modality: actual | planned | recommended | possible | conditional | unknown;\npolarity: positive | negative;\n", ""),
    ("Не перетворюй плани на здійснені дії, припущення на певність, заперечення на ствердження. ", ""),
    ('"modality": "...", "polarity": "...", ', ""),
    ("(source, relation_type, target, modality, polarity, event_time, attribution)", "(source, relation_type, target, event_time, attribution)"),
]


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--kit", default="."); a = ap.parse_args()
    p = Path(a.kit) / "prompts"
    v2 = (p / "contract_v2_uk.txt").read_text(encoding="utf-8")
    r8a = (p / "rule_8a_uk.txt").read_text(encoding="utf-8")
    assert r8a.startswith("8а. ") and r8a.endswith("\n")
    assert v2.count(ANCHOR) == 1 and v2.split(ANCHOR, 1)[1].startswith("9. ")
    v3 = v2.replace(ANCHOR, ANCHOR + r8a)
    assert v3.replace(r8a, "", 1) == v2
    (p / "contract_v3_uk.txt").write_text(v3, encoding="utf-8")
    ab = v3.replace(r8a, "", 1)
    for old, new in REPL:
        assert ab.count(old) == 1, old
        ab = ab.replace(old, new)
    old_ab = (p / "contract_ablation_2026-10-27_uk.txt").read_text(encoding="utf-8")
    assert ab == old_ab, "контракт абляції відрізняється від контракту 27.10"
    assert "modality" not in ab and "polarity" not in ab
    (p / "contract_ablation_uk.txt").write_text(ab, encoding="utf-8")
    for n, s in [("contract_v2_uk.txt", v2), ("rule_8a_uk.txt", r8a), ("contract_v3_uk.txt", v3), ("contract_ablation_uk.txt", ab)]:
        print(n, len(s), sha(s))


if __name__ == "__main__":
    main()
