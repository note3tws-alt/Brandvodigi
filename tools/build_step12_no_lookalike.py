#!/usr/bin/env python3
"""Step 12: never mention the look-alike Riyadh agency on the site (22 Nov 2026). Run after step 11.

Usage: python3 tools/build_step12_no_lookalike.py site-build

Hola, 22 Nov 2026: don't mention brandvo.sa anywhere on our site (they copied our logo).
Removes the About FAQ entry (HTML and FAQPage schema) and the llms.txt line. Idempotent.
"""
import hashlib, json, re, sys
from pathlib import Path

site = Path(sys.argv[1])
p = site / "about" / "index.html"
t = p.read_text()
t = re.sub(r'<h3 [^>]*>Is Brandvo Digital Co\. connected to brandvo\.sa\?</h3>\s*<p class="mt-5">[^<]*</p>\s*', "", t)
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
data = json.loads(m.group(1))
for n in data["@graph"]:
    if n.get("@type") == "FAQPage":
        n["mainEntity"] = [q for q in n["mainEntity"] if "brandvo.sa" not in json.dumps(q).lower()]
t = t.replace(m.group(0), '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>")
p.write_text(t)

l = site / "llms.txt"
l.write_text(re.sub(r"- Not affiliated with brandvo\.sa[^\n]*\n", "", l.read_text()))

for f in site.rglob("*"):
    if f.is_file() and f.suffix in (".html", ".js", ".txt", ".xml"):
        assert "brandvo.sa" not in f.read_text().lower(), f

manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
