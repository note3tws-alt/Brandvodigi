#!/usr/bin/env python3
"""Step 4: use the full brand name "Brandvo Digital Co." everywhere (17 Nov 2026).

Usage: python3 tools/build_step4_brandname.py site-build [more .md files or dirs...]

Rewrites visible text, titles, alt text and aria labels. Leaves URLs, ids,
handles (brandvo_digital_co, Brandvo-Digital-Co-...) and the schema
alternateName alone. Re-hashes the JS bundle name and updates every HTML
reference, then rewrites tools/deploy-manifest.json for the site folder.
"""
import hashlib, json, os, re, sys
from pathlib import Path

FULL = "Brandvo Digital Co."
KEEP = '"alternateName":"Brandvo Digital"', '"alternateName": "Brandvo Digital"'


def fix(s):
    for i, k in enumerate(KEEP):
        s = s.replace(k, f"\0KEEP{i}\0")
    s = s.replace("BrandVo Digital", "Brandvo Digital")
    s = re.sub(r"Brandvo Digital [Cc]o\b\.?", "\0FULL\0", s)
    # "Brandvo Digital" or bare "Brandvo" used as a name (not in URLs, ids or handles)
    s = re.sub(r"(?<![\w/.@#-])Brandvo(?: Digital)?(?![\w-])", "\0FULL\0", s)
    # avoid "Co.." at the end of a sentence
    s = s.replace("\0FULL\0.", "Brandvo Digital Co.").replace("\0FULL\0", FULL)
    for i, k in enumerate(KEEP):
        s = s.replace(f"\0KEEP{i}\0", k)
    return s


def files(p):
    p = Path(p)
    if p.is_dir():
        return [f for f in p.rglob("*") if f.suffix in (".html", ".js", ".md", ".xml", ".json") and f.is_file()]
    return [p]


site = Path(sys.argv[1])
changed = 0
for target in sys.argv[1:]:
    for f in files(target):
        s = f.read_text()
        n = fix(s)
        if n != s:
            f.write_text(n)
            changed += 1
print("files changed:", changed)

# re-hash the bundle name so cached copies are never served
assets = site / "assets"
for js in assets.glob("index-bv*.js"):
    s = js.read_text()
    new = "index-bv" + hashlib.sha1(s.encode()).hexdigest()[:8] + ".js"
    if new != js.name:
        js.rename(assets / new)
        for h in site.rglob("*.html"):
            t = h.read_text()
            if js.name in t:
                h.write_text(t.replace("/assets/" + js.name, "/assets/" + new))
        print("bundle", js.name, "->", new)

manifest = {}
for f in sorted(site.rglob("*")):
    if f.is_file():
        manifest["/" + f.relative_to(site).as_posix()] = hashlib.sha1(f.read_bytes()).hexdigest()
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
