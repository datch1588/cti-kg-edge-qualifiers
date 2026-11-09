#!/usr/bin/env python3
"""Restore the verbatim quotes of this package from the corpus file CTI_250_V1.

Every quote from a corpus document that supports a node or an edge (and every paragraph shown to an auditor)
is replaced in this package by a reference to its place in a paragraph of the corpus document. Whoever has
received the corpus file `dataset_250_articles.txt` from the authors can put the quotes back with this script.
The package itself is not changed: the script writes a copy into a new folder.

    python3 scripts/restore_quotes.py --corpus dataset_250_articles.txt --repo . --out ../restored

Reference formats (see README, "How texts and quotes were replaced"); they are those of package 0.3.0, and
the script of package 0.3.0 (`scripts/vidnovyty_tsytaty.py` there) restores the first two kinds:
- JSON, including the `evidence_json` attribute of GEXF graphs: the key "quote" is replaced by the key
  "quote_ref": {"match": "exact", "paragraph_id": "D0344:P0010", "start": s, "end": e, "sha256": h}.
  The quote is the characters s to e of the paragraph text (Unicode code point offsets from 0, end
  excluded). "other_paragraph" is the same, but the paragraph differs from the one the record names.
  "not_found" means that the quote is not verbatim in the document; only "length" and "sha256" are known,
  so such a reference stays as it is.
- Text files, one quote per line: `[paragraph] «@s-e sha256=h»`, `[paragraph] «@D0344:P0011:s-e sha256=h»`
  (another paragraph of the same document) or `[paragraph] «@not_found len=n sha256=h»`.
- Text files, references inside a line (new in 0.4.0): the same `«@…»` tokens, several per line
  (`фрагменти: [D0595:P0026] «@s-e sha256=h»; [D0595:P0015] «@…»`) or after a label without the document
  part of the paragraph identifier (`фрагмент [P0014]: «@D0006:P0014:s-e sha256=h»`,
  `абзац: «@D0006:P0014:0-n sha256=h»`). A token without its own paragraph identifier takes the one in
  square brackets right before it. A paragraph excerpt that the auditor saw cut at either end keeps the
  ellipsis inside the token (`абзац: «…@D0006:P0014:s-e sha256=h…»`); it is put back around the quote.
The paragraph text is the line of the corpus file after `[D0344:P0010] `. The SHA-256 is computed from the
quote in UTF-8, and the script checks every restored quote against it.

Requires Python 3.9+ and no third-party libraries. Exit code: 0 if everything was restored or only
"not_found" references remain; 1 if a SHA-256 does not match or a paragraph is unknown. License: MIT.
"""
import argparse
import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

CORPUS_SHA256 = "c75f91835ed2f192398287d707795867184a4042c96b483b69c1e070c032b2c7"
RE_PARAGRAPH = re.compile(r"^\[(D\d{4}:P\d{4})\] (.*)$")
RE_REF = re.compile(r'"quote_ref"(\s*):(\s*)(\{[^{}]*\})')
RE_ATTR = re.compile(r"""(\svalue=)("[^"]*"|'[^']*')""")
RE_TOKEN = re.compile(r"(?:\[(D\d{4}:P\d{4})(?::W\d{4})?\] )?«(…?)@(?:(D\d{4}:P\d{4}):)?(\d+)-(\d+) "
                      r"sha256=([0-9a-f]{64})(…?)»")
RE_TOKEN_NF = re.compile(r"«…?@not_found len=\d+ sha256=[0-9a-f]{64}…?»")


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def escape_attr(s):
    """Escape an XML attribute value exactly as xml.etree.ElementTree does."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return s.replace("\r", "&#13;").replace("\n", "&#10;").replace("\t", "&#09;")


def unescape_attr(s):
    return re.sub(r"&(#\d+|#x[0-9a-fA-F]+|amp|lt|gt|quot|apos);", lambda m: html.unescape(m.group(0)), s)


class Restorer:
    def __init__(self, paragraphs):
        self.par = paragraphs
        self.restored = 0
        self.not_found = 0
        self.errors = []

    def quote(self, pid, s, e, h, where):
        t = self.par.get(pid)
        if t is None:
            self.errors.append(f"{where}: paragraph {pid} is not in the corpus file")
            return None
        q = t[s:e]
        if e > len(t) or sha(q) != h:
            self.errors.append(f"{where}: SHA-256 of the quote from {pid} [{s}:{e}] does not match")
            return None
        self.restored += 1
        return q

    def json_text(self, text, where):
        def sub(m):
            ref = json.loads(m.group(3))
            if ref.get("match") not in ("exact", "other_paragraph"):
                self.not_found += 1
                return m.group(0)
            q = self.quote(ref["paragraph_id"], ref["start"], ref["end"], ref["sha256"], where)
            if q is None:
                return m.group(0)
            return '"quote"' + m.group(1) + ":" + m.group(2) + json.dumps(q, ensure_ascii=False)
        return RE_REF.sub(sub, text)

    def gexf(self, text, where):
        """Attribute values in double quotes are escaped as xml.etree.ElementTree does (graphs of 0.3.0), values in
        single quotes as xml.sax.saxutils.quoteattr does (the merged graph of 0.4.0)."""
        def sub(m):
            raw = m.group(2)
            v = unescape_attr(raw[1:-1])
            if '"quote_ref"' not in v:
                return m.group(0)
            new = self.json_text(v, where)
            if raw[0] == "'":
                return m.group(1) + quoteattr(new)
            return m.group(1) + '"' + escape_attr(new) + '"'
        return RE_ATTR.sub(sub, text)

    def lines(self, text, where):
        def sub(m):
            pid = m.group(3) or m.group(1)
            if pid is None:
                self.errors.append(f"{where}: reference without a paragraph identifier")
                return m.group(0)
            q = self.quote(pid, int(m.group(4)), int(m.group(5)), m.group(6), where)
            if q is None:
                return m.group(0)
            prefix = m.group(0)[:m.group(0).index("«")]
            return prefix + "«" + m.group(2) + q + m.group(7) + "»"
        out = []
        for ln in text.split("\n"):
            self.not_found += len(RE_TOKEN_NF.findall(ln))
            out.append(RE_TOKEN.sub(sub, ln))
        return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Restore the verbatim quotes of the package from the corpus file.")
    ap.add_argument("--corpus", required=True, help="corpus file dataset_250_articles.txt")
    ap.add_argument("--repo", default=".", help="package folder (default: current folder)")
    ap.add_argument("--out", required=True, help="new folder for the copy of the package with quotes")
    a = ap.parse_args()
    corpus = Path(a.corpus).read_bytes()
    if hashlib.sha256(corpus).hexdigest() != CORPUS_SHA256:
        print("Warning: the SHA-256 of the corpus file differs from the expected one; every quote is still "
              "checked against its own SHA-256.")
    par = {}
    for ln in corpus.decode("utf-8").split("\n"):
        m = RE_PARAGRAPH.match(ln.rstrip("\r"))
        if m:
            par[m.group(1)] = m.group(2)
    repo, out = Path(a.repo).resolve(), Path(a.out).resolve()
    if out == repo or repo in out.parents:
        sys.exit("The --out folder must not be inside the package.")
    if out.exists() and any(out.iterdir()):
        sys.exit(f"The folder {out} is not empty.")
    r = Restorer(par)
    changed = 0
    for p in sorted(repo.rglob("*")):
        rel = p.relative_to(repo)
        if not p.is_file() or rel.parts[0] == ".git":
            continue
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = p.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            shutil.copyfile(p, dest)
            continue
        if p.suffix == ".json" and '"quote_ref"' in text:
            new = r.json_text(text, rel.as_posix())
        elif p.suffix == ".gexf" and ("&quot;quote_ref&quot;" in text or '"quote_ref"' in text):
            new = r.gexf(text, rel.as_posix())
        elif "«@" in text:
            new = r.lines(text, rel.as_posix())
        else:
            new = text
        if new != text:
            changed += 1
            dest.write_bytes(new.encode("utf-8"))
        else:
            shutil.copyfile(p, dest)
    print(f"Quotes restored: {r.restored}; files changed: {changed}; "
          f"not restored (not verbatim in the document): {r.not_found}; errors: {len(r.errors)}")
    for x in r.errors[:20]:
        print("  ", x)
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
