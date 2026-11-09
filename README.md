# Data for: A method for constructing knowledge graphs with generative artificial intelligence to analyze cyber threat reports

D. V. Lande, V. S. Kuzminskyi. National Technical University of Ukraine "Igor Sikorsky Kyiv Polytechnic Institute".

Ukrainian title: «Метод формування графів знань для аналізу повідомлень про кіберзагрози за допомогою генеративного штучного інтелекту».

Package version 0.4.0 (2026-11-05). It supports the article accepted for publication in the journal "Artificial Intelligence" («Штучний інтелект», ISSN 2710-1673), 2026, No. 4. The accepted text keeps the section, equation and table numbering of draft v6.37, which is used below, and all 109 numbers checked by `scripts/recompute_article_numbers.py` are printed in it unchanged. The DOI of the article will be added after publication. Repository: https://github.com/datch1588/cti-kg-edge-qualifiers.

The article improves a method for constructing knowledge graphs of cyber threats from news reports with a language model: each edge is a claim of the source with modality, polarity, attribution, event time and event context; an edge is accepted only with a verbatim supporting fragment; records are merged only when the triple and all qualifiers match. This package holds the contracts, protocols, run inputs and outputs, audit files and verdicts, analysis results and fixation files of the experiments that the article reports, without the texts of the source documents.

## What changed since 0.3.0

- The article no longer reports the experiments with retrieval of additional passages (RAG, BM25), the four RAG/LLM graphs or the runs on Grok. Their files (`graphs/`, `audit/`, `retrieval/`, contract S1, the BM25 replay and the RAG conditions of the controlled experiment) are not in this version; package 0.3.0 keeps them.
- New studies: contract v3 (parts A and B) with the audit of part B by a model of another developer, part C (50 new documents, audits by Claude Opus 5.5 and Claude Sonnet 5.5), the re-audit of qualifiers and supporting fragments, the cross-document merge of 56 documents and the recheck of the acceptance conditions.
- The package is in English: this README, `CITATION.cff`, `LICENSE-DATA.md`, `provenance.tsv` (formerly `pokhodzhennia.tsv`) and the verification outputs. Folder and file names are English ASCII; the old and new names are in `provenance.tsv`. Protocols, reports, contracts, prompts and run inputs stay in Ukrainian, as they were fixed and run (see "Language of the files").
- `scripts/restore_quotes.py` replaces `vidnovyty_tsytaty.py` of 0.3.0: it also restores the quote references inside lines, new in this version. `scripts/recompute_article_numbers.py` recomputes key numbers of the article.

## Contents

| Folder | Article (v6.37) | Files | Content |
|---|---|---:|---|
| `contract/` | 3.3, 5.1 | 2 | extraction contracts v2 and v3 (in Ukrainian; byte-identical to what the model received) |
| `corpus/` | 5.1 | 2 | manifests of the corpus CTI_250_V1 (250 documents) and of the 671 InfoStream documents it was sampled from; no texts |
| `studies/repeat1_method_runs_2026-10-20/` | 5.2, 6.1, Table 2 (repeat 1) | 155 | Method runs of repeat 1 |
| `studies/ctinexus_comparison_repeat1_2026-10-27/` | 5.2, 6.1, Table 2 (repeat 1) | 213 | Comparison with CTINexus, repeat 1 |
| `studies/ablation_repeat2_2026-10-27/` | 5.2, 6.1, Table 2 (repeat 2) | 413 | Ablation and repeat 2 |
| `studies/wording_reaudit_2026-10-28/` | 5.2, 6.1 (second additional check) | 171 | Re-audit of the form from the relation wording |
| `studies/independent_audit_repeat2_2026-10-28/` | 5.2, 6.1 (dependence on the auditor) | 32 | Audit by a model of another developer, repeat 2 |
| `studies/contract_v3_parts_A_B_2026-10-28/` | 5.3, 6.2 (parts A and B) | 701 | Contract v3, parts A and B |
| `studies/independent_audit_part_B_2026-10-28/` | 5.3, 6.2 (part B) | 33 | Audit of part B by a model of another developer |
| `studies/part_C_new_documents_2026-11-05/` | 5.3, 6.2 (part C) | 526 | Part C, 50 new documents |
| `studies/qualifier_reaudit_2026-11-04/` | 5.4, 6.3, Table 3 | 245 | Re-audit of qualifiers and supporting fragments |
| `studies/cross_document_merge_2026-11-04/` | 5.5, 6.4 | 250 | Entity reconciliation and claim merging across 56 documents |
| `studies/acceptance_conditions_2026-11-05/` | 3.4 (condition (5)) | 2 | Recheck of the acceptance conditions |
| `scripts/` | | 3 | corpus sampling, quote restoration, recomputation of article numbers |
| `verification/` | | 2 | outputs of the scripts in `scripts/` |
| top level | | 6 | README.md, CITATION.cff, LICENSE, LICENSE-DATA.md, provenance.tsv, SHA256SUMS.txt |

In all: 2 756 files, 44 664 805 bytes.

Article sections (v6.37): 3.4 Steps of the method; 5.1 Corpus and contract versions; 5.2 Comparison with CTINexus and ablation; 5.3 Study of the effect of the modality rules (contract v3); 5.4 Evaluation of qualifiers and supporting fragments; 5.5 Entity reconciliation and claim merging across documents; 6.1 Comparison with CTINexus and ablation; 6.2 Results of the study of the effect of the modality rules; 6.3 Results of the evaluation of qualifiers and supporting fragments; 6.4 Results of entity reconciliation and claim merging across documents. Tables: Table 1. How the method differs from CTINexus and AttacKG+; Table 2. Comparison with CTINexus and ablation: blind model-based audit of records from 50 documents; Table 3. Repeated audit of the method’s records.

All systems and auditors ran on Claude Opus 5.5 unless stated otherwise. Run IDs are blind: the key that maps them to systems is not in the package (see "What is not included").

## Studies in `studies/`

### `repeat1_method_runs_2026-10-20/`: Method runs of repeat 1 (Sections 5.2, 6.1, Table 2 (repeat 1))

The 50 runs of the method with contract v2 that repeat 1 of the comparison with CTINexus uses (Section 5.2: "in the first run, the records of the method were taken from a separate launch performed earlier"). They are the condition NONE (the document and the contract only) of an earlier controlled experiment (CTI_RAG_CONTROLLED_V2, 2026-10-20). Only this condition is included: its other conditions, the audit of that experiment and its protocol concern retrieval of additional passages, which the article no longer reports. The fixation file `PROTOCOL_sha256.txt` of that experiment is included; it lists files that are not in the package.

Top-level files:

- `PROTOCOL_sha256.txt`: fixation file: SHA-256 of the files fixed at that stage

| Folder | Files | Content |
|---|---:|---|
| `data/` | 1 | manifest and documents of the study (texts and titles replaced by SHA-256) |
| `data/targets/*/` | 50 | manifest and documents of the study (texts and titles replaced by SHA-256) |
| `prompts/` | 2 | prompts and contracts, in Ukrainian, byte-identical to what the model received |
| `runs/` | 1 | run hashes and model names |
| `runs/inputs/` | 50 | run inputs: exactly what the model received (task text in Ukrainian); document texts replaced by SHA-256 |
| `runs/outputs/` | 50 | run outputs (JSON records of nodes and edges; quotes replaced by references) |

Quotes replaced by references: 2 105 (exact 2 105, other paragraph 0, not found verbatim 0).

### `ctinexus_comparison_repeat1_2026-10-27/`: Comparison with CTINexus, repeat 1 (Sections 5.2, 6.1, Table 2 (repeat 1))

CTINexus runs on the same 50 documents and the blind audit of the method and CTINexus records (study CTI_BASELINE_CTINEXUS). Includes the post hoc check on modality and negation markers in the relation wording (the first additional check of Section 5.2).

Top-level files:

- `AUDIT_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sha256_before_runs.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before runs, SHA-256 in `PROTOCOL_sha256_before_runs.txt`); edited after fixation, see "Files changed after fixation"
- `REPORT_uk.md`: report (in Ukrainian; written after the analysis)

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 4 | analysis results |
| `audit/` | 1 | audit check log and hashes of the inputs |
| `audit/inputs/` | 50 | blind audit files shown to the auditor (quotes replaced by references) |
| `audit/outputs/` | 50 | auditor verdicts (JSON) |
| `prompts/` | 4 | prompts and contracts, in Ukrainian, byte-identical to what the model received |
| `runs/inputs/` | 50 | run inputs: exactly what the model received (task text in Ukrainian); document texts replaced by SHA-256 |
| `runs/outputs/` | 50 | run outputs (JSON records of nodes and edges; quotes replaced by references) |

### `ablation_repeat2_2026-10-27/`: Ablation and repeat 2 (Sections 5.2, 6.1, Table 2 (repeat 2))

All three systems (the method with contract v2, CTINexus and the ablation) rerun on the 50 documents, 150 runs, and the blind audit of their records.

Top-level files:

- `AUDIT_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sha256_before_runs.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before runs, SHA-256 in `AUDIT_sha256_before_audit.txt`, `PROTOCOL_sha256_before_runs.txt`); edited after fixation, see "Files changed after fixation"

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 5 | analysis results |
| `audit/` | 2 | audit check log and hashes of the inputs |
| `audit/inputs/` | 50 | blind audit files shown to the auditor (quotes replaced by references) |
| `audit/outputs/` | 50 | auditor verdicts (JSON) |
| `prompts/` | 1 | prompts and contracts, in Ukrainian, byte-identical to what the model received |
| `runs/` | 1 | run hashes and model names |
| `runs/inputs/` | 150 | run inputs: exactly what the model received (task text in Ukrainian); document texts replaced by SHA-256 |
| `runs/outputs/` | 150 | run outputs (JSON records of nodes and edges; quotes replaced by references) |
| `scripts/` | 1 | scripts |

Quotes replaced by references: 4 146 (exact 4 146, other paragraph 0, not found verbatim 0).

### `wording_reaudit_2026-10-28/`: Re-audit of the form from the relation wording (Sections 5.2, 6.1 (second additional check))

The auditor evaluated the form of CTINexus records from the wording of the relation.

Top-level files:

- `PROTOCOL_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sha256_before_audit.txt`); edited after fixation, see "Files changed after fixation"
- `REPORT_uk.md`: report (in Ukrainian; written after the analysis)

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 2 | analysis results |
| `audit/` | 2 | audit check log and hashes of the inputs |
| `audit/inputs/` | 81 | blind audit files shown to the auditor (quotes replaced by references) |
| `audit/outputs/` | 81 | auditor verdicts (JSON) |
| `audit/outputs_rejected/` | 1 | audit output rejected by the check (kept as a record) |
| `prompts/` | 1 | prompts and contracts, in Ukrainian, byte-identical to what the model received |

### `independent_audit_repeat2_2026-10-28/`: Audit by a model of another developer, repeat 2 (Sections 5.2, 6.1 (dependence on the auditor))

457 of the 2761 records of repeat 2 and 30 control records, evaluated by GPT-6 Astra Pro (OpenAI) in ten files N01-N10; `answers/MODEL.txt` records the model and the run conditions.

Top-level files:

- `PROTOCOL_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sha256_before_audit.txt`); edited after fixation, see "Files changed after fixation"
- `README_for_author_uk.md`: instructions for the author on running the audit (in Ukrainian)
- `REPORT_uk.md`: report (in Ukrainian; written after the analysis)
- `answers_sha256.txt`: fixation file: SHA-256 of the files fixed at that stage
- `for_auditor_sha256.txt`: fixation file: SHA-256 of the files fixed at that stage

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 2 | analysis results |
| `answers/` | 11 | answers of the auditor of another developer |
| `for_auditor/` | 12 | files given to the auditor of another developer (quotes replaced by references) |
| `prompts/` | 1 | prompts and contracts, in Ukrainian, byte-identical to what the model received |

### `contract_v3_parts_A_B_2026-10-28/`: Contract v3, parts A and B (Sections 5.3, 6.2 (parts A and B))

Study CTI_CONTRACT_V3. Part A: the method with contract v3 on the 50 documents of Section 5.2, two runs per document (Y001-Y100). Part B: 25 new documents, one run each of the method with contracts v2 and v3, CTINexus and the ablation (Z001-Z100). Blind audit files S1T## and S2T## (part A, repeats 1 and 2) and S3N## (part B). `scripts/make_contracts_v3.py` builds contract v3 and the ablation contract from contract v2 and rules 8a.

Top-level files:

- `AUDIT_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sha256_before_runs.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before runs, SHA-256 in `AUDIT_sha256_before_audit.txt`, `PROTOCOL_sha256_before_runs.txt`); edited after fixation, see "Files changed after fixation"
- `REPORT_uk.md`: report (in Ukrainian; written after the analysis)

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 4 | analysis results |
| `audit/` | 2 | audit check log and hashes of the inputs |
| `audit/inputs/` | 125 | blind audit files shown to the auditor (quotes replaced by references) |
| `audit/outputs/` | 125 | auditor verdicts (JSON) |
| `data/` | 1 | manifest and documents of the study (texts and titles replaced by SHA-256) |
| `data/targets_new/*/` | 25 | manifest and documents of the study (texts and titles replaced by SHA-256) |
| `prompts/` | 12 | prompts and contracts, in Ukrainian, byte-identical to what the model received |
| `runs/` | 2 | run hashes and model names |
| `runs/inputs/` | 200 | run inputs: exactly what the model received (task text in Ukrainian); document texts replaced by SHA-256 |
| `runs/outputs/` | 200 | run outputs (JSON records of nodes and edges; quotes replaced by references) |
| `scripts/` | 1 | scripts |

Quotes replaced by references: 8 154 (exact 8 154, other paragraph 0, not found verbatim 0).

### `independent_audit_part_B_2026-10-28/`: Audit of part B by a model of another developer (Sections 5.3, 6.2 (part B))

Part B records evaluated by GPT-6 Astra Pro (OpenAI) in ten files N01-N10 (study CTI_INDEPENDENT_AUDIT_V3). The field `rows` of the analysis outputs is removed, because it maps the blind record IDs to the systems.

Top-level files:

- `PACK_sha256_before_results.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sha256_before_audit.txt`); edited after fixation, see "Files changed after fixation"
- `README_for_author_uk.md`: instructions for the author on running the audit (in Ukrainian)
- `REPORT_uk.md`: report (in Ukrainian; written after the analysis)
- `answers_sha256.txt`: fixation file: SHA-256 of the files fixed at that stage
- `for_auditor_sha256.txt`: fixation file: SHA-256 of the files fixed at that stage

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 2 | analysis results |
| `answers/` | 11 | answers of the auditor of another developer |
| `for_auditor/` | 12 | files given to the auditor of another developer (quotes replaced by references) |
| `prompts/` | 1 | prompts and contracts, in Ukrainian, byte-identical to what the model received |

### `part_C_new_documents_2026-11-05/`: Part C, 50 new documents (Sections 5.3, 6.2 (part C))

Study CTI_FACTS_NEW: the method with contracts v2 and v3 and the ablation, one run each on 50 new documents (F001-F150), the blind audit by Claude Opus 5.5 (S5F01-S5F50) and the second blind audit by Claude Sonnet 5.5 (`sonnet_reaudit/`). `sonnet_reaudit/first_attempts_not_clean/` keeps the three first attempts that were rerun (deviation 1 of the Sonnet protocol).

Top-level files:

- `AUDIT_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sha256_before_runs.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sonnet_reaudit_sha256.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sonnet_reaudit_uk.md`: protocol (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sonnet_reaudit_sha256.txt`); edited after fixation, see "Files changed after fixation"
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before runs, SHA-256 in `PROTOCOL_sha256_before_runs.txt`)
- `REPORT_uk.md`: report (in Ukrainian; written after the analysis)

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 1 | analysis results |
| `audit/` | 2 | audit check log and hashes of the inputs |
| `audit/inputs/` | 50 | blind audit files shown to the auditor (quotes replaced by references) |
| `audit/outputs/` | 50 | auditor verdicts (JSON) |
| `data/` | 2 | manifest and documents of the study (texts and titles replaced by SHA-256) |
| `data/targets/*/` | 50 | manifest and documents of the study (texts and titles replaced by SHA-256) |
| `prompts/` | 7 | prompts and contracts, in Ukrainian, byte-identical to what the model received |
| `runs/` | 1 | run hashes and model names |
| `runs/inputs/` | 150 | run inputs: exactly what the model received (task text in Ukrainian); document texts replaced by SHA-256 |
| `runs/outputs/` | 150 | run outputs (JSON records of nodes and edges; quotes replaced by references) |
| `sonnet_reaudit/` | 2 | second blind audit by Claude Sonnet 5.5 |
| `sonnet_reaudit/first_attempts_not_clean/` | 5 | first attempts that were rerun |
| `sonnet_reaudit/outputs/` | 50 | verdicts of the Sonnet audit |

Quotes replaced by references: 5 593 (exact 5 593, other paragraph 0, not found verbatim 0).

### `qualifier_reaudit_2026-11-04/`: Re-audit of qualifiers and supporting fragments (Sections 5.4, 6.3, Table 3)

Study CTI_QUALIFIER_REAUDIT: 4379 edge records and 927 nodes with alternative names from 75 documents, with 353 control records, in 118 audit files.

Top-level files:

- `ANALYSIS_sha256_before_results.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sha256_before_audit.txt`)

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 2 | analysis results |
| `audit/` | 2 | audit check log and hashes of the inputs |
| `audit/inputs/` | 118 | blind audit files shown to the auditor (quotes replaced by references) |
| `audit/outputs/` | 118 | auditor verdicts (JSON) |
| `prompts/` | 2 | prompts and contracts, in Ukrainian, byte-identical to what the model received |

Quotes replaced by references: 4 034 (exact 4 034, other paragraph 0, not found verbatim 0).

### `cross_document_merge_2026-11-04/`: Entity reconciliation and claim merging across 56 documents (Sections 5.5, 6.4)

Study CTI_CROSSDOC: 56 runs of the method with contract v3 (W001-W056), the candidate groups (`resolve/plan.json`), 14 resolver sessions (R01-R14) for the decisions same(v, v'), the merged graph (`graph/crossdoc.gexf`, `graph/crossdoc.json`) and the audit of merged nodes, unmerged candidate pairs, merged edges and form (15 files). The 56 documents were selected with the 0.3.0 graph `graphs/claude_llm.gexf`, which is not part of this package (see `data/manifest.json`).

Top-level files:

- `ANALYSIS_sha256_before_results.txt`: fixation file: SHA-256 of the files fixed at that stage
- `AUDIT_sha256_before_audit.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_sha256_before_runs.txt`: fixation file: SHA-256 of the files fixed at that stage
- `PROTOCOL_uk.md`: protocol (in Ukrainian; fixed before runs, SHA-256 in `PROTOCOL_sha256_before_runs.txt`)
- `RESOLVE_sha256_before_resolution.txt`: fixation file: SHA-256 of the files fixed at that stage

| Folder | Files | Content |
|---|---:|---|
| `analysis/` | 2 | analysis results |
| `audit/` | 2 | audit check log and hashes of the inputs |
| `audit/inputs/` | 15 | blind audit files shown to the auditor (quotes replaced by references) |
| `audit/outputs/` | 15 | auditor verdicts (JSON) |
| `data/` | 1 | manifest and documents of the study (texts and titles replaced by SHA-256) |
| `data/targets/*/` | 56 | manifest and documents of the study (texts and titles replaced by SHA-256) |
| `graph/` | 3 | merged graph and merge log |
| `prompts/` | 7 | prompts and contracts, in Ukrainian, byte-identical to what the model received |
| `resolve/` | 3 | audit check log and hashes of the inputs |
| `resolve/inputs/` | 14 | resolver inputs (quotes replaced by references) |
| `resolve/outputs/` | 14 | resolver decisions (JSON) |
| `runs/` | 1 | run hashes and model names |
| `runs/inputs/` | 56 | run inputs: exactly what the model received (task text in Ukrainian); document texts replaced by SHA-256 |
| `runs/outputs/` | 56 | run outputs (JSON records of nodes and edges; quotes replaced by references) |

Quotes replaced by references: 10 599 (exact 10 599, other paragraph 0, not found verbatim 0).

### `acceptance_conditions_2026-11-05/`: Recheck of the acceptance conditions (Sections 3.4 (condition (5)))

`acceptance_conditions_v633.json`: the recheck of the acceptance conditions of every node and edge (Eq. (5)) over all 406 method runs: 9780 nodes and 7395 edges, none rejected. The script `acceptance_conditions_v633.py` needs the blinding keys and the full document texts, so it cannot be rerun from the package.

Top-level files:

- `acceptance_conditions_v633.json`
- `acceptance_conditions_v633.py`

## Language of the files

The package text written for this release is in English. The files below were written in Ukrainian before or during the experiments and are kept byte for byte, since translating them would change content fixed by hash or content that the model actually received:

- Contracts and prompts (`contract/`, `studies/*/prompts/`) and run, audit and resolver inputs: in Ukrainian; byte-identical to what the model received (run inputs only have the document texts replaced by SHA-256 and quotes replaced by references).
- `studies/ablation_repeat2_2026-10-27/PROTOCOL_uk.md` (in Ukrainian; fixed before runs, SHA-256 in `AUDIT_sha256_before_audit.txt`, `PROTOCOL_sha256_before_runs.txt`); edited after fixation, see "Files changed after fixation"
- `studies/contract_v3_parts_A_B_2026-10-28/PROTOCOL_uk.md` (in Ukrainian; fixed before runs, SHA-256 in `AUDIT_sha256_before_audit.txt`, `PROTOCOL_sha256_before_runs.txt`); edited after fixation, see "Files changed after fixation"
- `studies/cross_document_merge_2026-11-04/PROTOCOL_uk.md` (in Ukrainian; fixed before runs, SHA-256 in `PROTOCOL_sha256_before_runs.txt`)
- `studies/ctinexus_comparison_repeat1_2026-10-27/PROTOCOL_uk.md` (in Ukrainian; fixed before runs, SHA-256 in `PROTOCOL_sha256_before_runs.txt`); edited after fixation, see "Files changed after fixation"
- `studies/independent_audit_part_B_2026-10-28/PROTOCOL_uk.md` (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sha256_before_audit.txt`); edited after fixation, see "Files changed after fixation"
- `studies/independent_audit_repeat2_2026-10-28/PROTOCOL_uk.md` (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sha256_before_audit.txt`); edited after fixation, see "Files changed after fixation"
- `studies/part_C_new_documents_2026-11-05/PROTOCOL_sonnet_reaudit_uk.md` (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sonnet_reaudit_sha256.txt`); edited after fixation, see "Files changed after fixation"
- `studies/part_C_new_documents_2026-11-05/PROTOCOL_uk.md` (in Ukrainian; fixed before runs, SHA-256 in `PROTOCOL_sha256_before_runs.txt`)
- `studies/qualifier_reaudit_2026-11-04/PROTOCOL_uk.md` (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sha256_before_audit.txt`)
- `studies/wording_reaudit_2026-10-28/PROTOCOL_uk.md` (in Ukrainian; fixed before the audit, SHA-256 in `PROTOCOL_sha256_before_audit.txt`); edited after fixation, see "Files changed after fixation"
- Reports `REPORT_uk.md` and `analysis/report_tables.md`: in Ukrainian; written after the analysis.
- Answers and reasons of the auditors: in Ukrainian, as the auditors wrote them.

## Files changed after fixation

Each study fixed its protocol, inputs and scripts by SHA-256 before the runs or the audit (files `*sha256*.txt`). The files below differ from the fixed version; the reason comes from the study files themselves.

- `studies/ctinexus_comparison_repeat1_2026-10-27/PROTOCOL_uk.md`, fixed in `PROTOCOL_sha256_before_runs.txt` as `f2dbf0ddec53…`: after the analysis, two entries (2026-10-27 15:28 and 21:05 UTC) on the post hoc checks `posthoc_modal_markers.py` and `posthoc_false_form_breakdown.py` were added to the section on deviations after fixation; the current version is not in the fixation files.
- `studies/ablation_repeat2_2026-10-27/PROTOCOL_uk.md`, fixed in `PROTOCOL_sha256_before_runs.txt` as `121db9e65686…`: item 1 (2026-10-27T21:18:24Z) on the fix of `check_r2.py` was added to the section on deviations; the current version is fixed in `AUDIT_sha256_before_audit.txt`, with a note that only that section changed.
- `doslid_ablyatsiia_povtor_2026-10-27/scripts/check_r2.py` (not in the package), fixed in `PROTOCOL_sha256_before_runs.txt` as `ef356850695d…`: by item 1 of the deviations (2026-10-27T21:18:24Z), the comparison of paths expanded by the symbolic link `/mnt/project-files` was fixed before the audit was built; the new hash is in the protocol and in `AUDIT_sha256_before_audit.txt`.
- `studies/wording_reaudit_2026-10-28/PROTOCOL_uk.md`, fixed in `PROTOCOL_sha256_before_audit.txt` as `904f776ee37c…`: two items were added to the deviations: the rejected audit attempt R1_T38 that the auditor corrected itself (2026-10-28T09:29Z) and the launch of the auditors in waves (no time given); the current version is not in the fixation files.
- `studies/independent_audit_repeat2_2026-10-28/PROTOCOL_uk.md`, fixed in `PROTOCOL_sha256_before_audit.txt` as `41e4386da26a…`: three items (2026-10-28T10:11Z, 10:16Z and 10:19Z) on saving the auditor's answers and the model name in `vidpovidi/MODEL.txt` (now `answers/MODEL.txt`) were added to the deviations; the current version is not in the fixation files.
- `studies/contract_v3_parts_A_B_2026-10-28/PROTOCOL_uk.md`, fixed in `AUDIT_sha256_before_audit.txt` as `8a96279dff1b…`: the version fixed before the audit already had deviation 1; deviations 2 (22:02:22Z) and 3 (22:17:28Z) were added later; the current version is not in the fixation files.
- `doslid_kontrakt_v3_2026-10-28/scripts/check_v3.py` (not in the package), fixed in `AUDIT_sha256_before_audit.txt` as `9b384840a885…`: by deviation 2 of the protocol (2026-10-28T22:02:22Z) only the pattern of the input file name in auditor transcripts was fixed (`[A-Z][A-Z0-9]*\d\.txt`), during the audit; the check rules did not change.
- `doslid_kontrakt_v3_2026-10-28/scripts/verify_synthetic_v3.py` (not in the package), fixed in `AUDIT_sha256_before_audit.txt` as `41cc0756a417…`: the fixed hash is the one deviation 1 of the protocol gives for this new script; the files do not say why the script changed afterwards.
- `studies/contract_v3_parts_A_B_2026-10-28/PROTOCOL_uk.md`, fixed in `PROTOCOL_sha256_before_runs.txt` as `ff501fddf85b…`: three items were added to the deviations after fixation: the interruption of the part B runs by the API usage limit (2026-10-28T21:37:51Z), the fix of the transcript path pattern in `check_v3.py` (22:02:22Z) and the order of work for the other-developer audit and the interim review (22:17:28Z); the current version is not in the fixation files.
- `doslid_kontrakt_v3_2026-10-28/scripts/check_v3.py` (not in the package), fixed in `PROTOCOL_sha256_before_runs.txt` as `9b384840a885…`: by deviation 2 of the protocol (2026-10-28T22:02:22Z) only the pattern of the input file name in auditor transcripts was fixed (`[A-Z][A-Z0-9]*\d\.txt`), during the audit; the check rules did not change.
- `studies/independent_audit_part_B_2026-10-28/PROTOCOL_uk.md`, fixed in `PROTOCOL_sha256_before_audit.txt` as `fd07a51ab6ab…`: three items (2026-10-30T07:35Z, 07:39Z and 08:00Z) on receiving the answers, the auditor model and the run conditions were added to the deviations; the current version is not in the fixation files.
- `studies/part_C_new_documents_2026-11-05/PROTOCOL_sonnet_reaudit_uk.md`, fixed in `PROTOCOL_sonnet_reaudit_sha256.txt` as `c68810b496d7…`: deviation 1 (three auditors S5F22, S5F35 and S5F50 edited their own output, each was rerun once; no time given) was added after fixation; the current version is not in the fixation files.

All other 1 827 fixation entries match the files of the study folders. The fixation hashes refer to the original files: a file whose document texts or quotes were replaced has a different SHA-256 in the package (its source SHA-256 is in `provenance.tsv`).

## What is not included

- Texts of the InfoStream documents: document texts, titles and passages are replaced by SHA-256; verbatim quotes and fragments are replaced by references (next section). The corpus file `dataset_250_articles.txt` is available from the authors.
- Blinding keys of all studies (`keys/`, the tables `records.csv`, the run check logs `runs/check.json` and `analysis/check_runs_AB.txt` that name the system of each run, the field `rows` of the analysis of the part B audit), because expert checks of the records of contract v3 and of part C are still in progress. Scripts that need these keys or the full texts are not included either, except `studies/contract_v3_parts_A_B_2026-10-28/scripts/make_contracts_v3.py` and the acceptance-condition script.
- Materials of the expert checks (instructions, rating forms, answers, keys).
- Third-party CTINexus content: its prompt template and demonstration set. In CTINexus run inputs they are replaced by marker lines `CTINEXUS_COMMIT`, `CTINEXUS_DEMOS` (names of the three demonstrations) and `REMOVED_SHA256`. The code is at https://github.com/peng-gao-lab/CTINexus, commit `0c688536d85eae72f6055723492b573b0a1ff865`.
- Archives, interim analyses and duplicate copies (e.g. the answers of the other-developer audit under their original upload names).
- The RAG-era material of package 0.3.0 (see "What changed since 0.3.0").

## How texts and quotes were replaced

The scheme is that of packages 0.2.0 and 0.3.0, with one addition for references inside lines.

- A document paragraph `[D0596:P0003] text` becomes `[D0596:P0003] sha256:<SHA-256 of the paragraph text>` (the text after the identifier and a space, without the line end, in UTF-8, as in the corpus file).
- `TITLE: title` becomes `TITLE_SHA256: <SHA-256>`; a title inside a line (`стаття: «title» (date)`) becomes `стаття: «TITLE_SHA256:<SHA-256>» (date)`. JSON fields `text`, `title` and `exact_text` become `text_sha256`, `title_sha256` and `exact_text_sha256`.
- In CTINexus run inputs, each line of the document after `Target report:` becomes `"CTI": sha256:<…>` or `sha256:<…>`.
- A quote in JSON (key `quote`, also in the `evidence_json` attribute of the GEXF graph) becomes `quote_ref` in the same place, for example `{"match": "exact", "paragraph_id": "D0290:P0026", "start": 0, "end": 101, "sha256": "3825ab2256064220b59ce00b52c22eaae8c045a4dc0a19fbc9869fe8fe393bae"}`. The quote is the characters `start` to `end` of the text of paragraph `paragraph_id` (Unicode code point offsets from 0, `end` excluded); `sha256` is the SHA-256 of the quote in UTF-8. `"match": "other_paragraph"` means that the quote is in another paragraph of the same document (named in the reference); `"match": "not_found"` means that the quote is not verbatim in the document, so only its `length` and `sha256` are given and it cannot be restored.
- A quote line of an audit file `[paragraph] «quote»` becomes `[paragraph] «@start-end sha256=…»`, `[paragraph] «@D0000:P0000:start-end sha256=…»` (another paragraph of the same document) or `[paragraph] «@not_found len=… sha256=…»`.
- New in 0.4.0, references inside lines: the fragment lists of the qualifier re-audit (`фрагменти: [D0595:P0026] «@s-e sha256=<h>»; [D0595:P0015] «@s-e sha256=<h>»`) and the fragment and paragraph lines of the merge study (`фрагмент [P0014]: «@D0006:P0014:s-e sha256=<h>»`, `абзац: «@D0006:P0014:s-e sha256=<h>»`). There the document is named only by its title, so the reference carries the full paragraph identifier. A paragraph excerpt cut at either end keeps the ellipsis inside the reference: `абзац: «…@D0006:P0014:s-e sha256=<h>…»`. The labels `фрагменти`, `фрагмент` and `абзац` are Ukrainian for fragments, fragment and paragraph; `стаття` is article.
- Everything else, including `SOURCE_URL`, `PUBLICATION_DATE`, the records and the verdicts, is unchanged.

Quotes replaced in this package: 34 631 (exact 34 631, other paragraph 0, not found verbatim 0), of which 28 380 in the new studies. Short text fragments remain outside the quotes: entity names, titles that the models extracted as entities, qualifier phrases and the reasons of the auditors. Fragments of 40 characters or more cover 7.41% of the corpus text; the longest is 158 characters.

## How to verify

1. File integrity: `sha256sum -c SHA256SUMS.txt`.
2. Restore the quotes from the corpus file (the package is not changed; a copy is written):

   ```
   python3 scripts/restore_quotes.py --corpus dataset_250_articles.txt --repo . --out ../restored
   ```

   Every restored quote is checked against its SHA-256; references `not_found` stay as they are.
3. Recompute the key numbers of the article from the package files:

   ```
   python3 scripts/recompute_article_numbers.py --repo . --out /tmp/article_numbers.json
   ```

   The result of the release build is `verification/article_numbers_v6.37.json`: 109 of 109 numbers match (Tables 2 and 3, Sections 3.4, 5.2, 6.1-6.4; bootstrap intervals are recomputed with an independent seed and a tolerance of 1.0 percentage point). Numbers that need the blinding keys are listed under `not_recomputed`.
4. Contracts: `python3 studies/contract_v3_parts_A_B_2026-10-28/scripts/make_contracts_v3.py --kit <copy of that study folder>` rebuilds contract v3 and the ablation contract from contract v2 and rules 8a (it writes into `prompts/` of the folder given).

The scripts need Python 3.9 or later and no third-party libraries.

## Provenance

`provenance.tsv` has one row per file: `package_path`; `original_path` (the file in the authors' working folders); `via_package_0.3.0` (the path in package 0.3.0 when the file was taken from it byte for byte); `renamed_from` (the former name inside the study folder when it was renamed); `action`; `source_sha256`; `package_sha256`. Study folders were renamed as follows:

- `studies/doslid_baza_ctinexus_2026-10-27/` in package 0.3.0 (working folder `doslid_baza_ctinexus_2026-10-27/`) → `studies/ctinexus_comparison_repeat1_2026-10-27/`
- `studies/doslid_ablyatsiia_povtor_2026-10-27/` in package 0.3.0 (working folder `doslid_ablyatsiia_povtor_2026-10-27/`) → `studies/ablation_repeat2_2026-10-27/`
- `studies/doslid_pereaudyt_formy_2026-10-28/` in package 0.3.0 (working folder `doslid_pereaudyt_formy_2026-10-28/`) → `studies/wording_reaudit_2026-10-28/`
- `studies/nezalezhnyi_audyt_2026-10-28/` in package 0.3.0 (working folder `nezalezhnyi_audyt_2026-10-28/`) → `studies/independent_audit_repeat2_2026-10-28/`
- `studies/doslid_rag_v2/` in package 0.3.0 (working folder `doslid_rag_v2/`; condition NONE only) → `studies/repeat1_method_runs_2026-10-20/`
- working folder `doslid_kontrakt_v3_2026-10-28/` → `studies/contract_v3_parts_A_B_2026-10-28/`
- working folder `nezalezhnyi_audyt_v3_2026-10-28/` → `studies/independent_audit_part_B_2026-10-28/`
- working folder `doslid_polia_novi_statti_2026-11-05/` → `studies/part_C_new_documents_2026-11-05/`
- working folder `doslid_pereaudyt_kvalifikatoriv_2026-11-04/` → `studies/qualifier_reaudit_2026-11-04/`
- working folder `doslid_zlyttia_2026-11-04/` → `studies/cross_document_merge_2026-11-04/`
- `v6.33_2026-11-05/skrypty/umovy_v633.py` and `v6.33_2026-11-05/obchyslennia/umovy.json` → `studies/acceptance_conditions_2026-11-05/`

## Licenses

Data: CC BY 4.0 (`LICENSE-DATA.md`). Scripts (`scripts/` and the `.py` files elsewhere): MIT (`LICENSE`). The rights to the texts of the source documents belong to their publishers.

## How to cite

Lande, D. V., & Kuzminskyi, V. S. (2026). Data for: A method for constructing knowledge graphs with generative artificial intelligence to analyze cyber threat reports (Version 0.4.0) [Data set]. https://github.com/datch1588/cti-kg-edge-qualifiers. See `CITATION.cff`; the article DOI will be added after publication.
