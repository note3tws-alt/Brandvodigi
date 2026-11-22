#!/usr/bin/env python3
"""Step 12: never mention the look-alike Riyadh agency on the site (22 Nov 2026). Run after step 11.

Usage: python3 tools/build_step12_no_lookalike.py site-build

Hola, 22 Nov 2026: don't mention brandvo.sa anywhere on our site (they copied our logo).
Removes the About FAQ entry (HTML and FAQPage schema) and the llms.txt line, and replaces
them with a line Hola approved the same day that names no other agency (ORIGINAL below), as an
About FAQ (HTML + FAQPage schema) and an llms.txt key fact. Idempotent.
"""
import hashlib, json, re, sys
from pathlib import Path

site = Path(sys.argv[1])
ORIGINAL = ("Brandvo Digital Co. is the original Brandvo, founded in Kannur, Kerala. "
            "We are not affiliated with any other agency using a similar name.")
Q = "Is Brandvo Digital Co. connected to other agencies with a similar name?"
H3 = '<h3 class="mb-1 mt-9 font-display text-xl font-semibold leading-snug text-white">'

p = site / "about" / "index.html"
t = p.read_text()
t = re.sub(r'<h3 [^>]*>Is Brandvo Digital Co\. connected to brandvo\.sa\?</h3>\s*<p class="mt-5">[^<]*</p>\s*', "", t)
if Q not in t:
    anchor = H3 + "Do you work with businesses outside Kannur?</h3>"
    assert t.count(anchor) == 1
    t = t.replace(anchor, f'{H3}{Q}</h3>\n<p class="mt-5">{ORIGINAL}</p>\n' + anchor)
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
data = json.loads(m.group(1))
for n in data["@graph"]:
    if n.get("@type") == "FAQPage":
        qs = [q for q in n["mainEntity"] if "brandvo.sa" not in json.dumps(q).lower() and q["name"] != Q]
        i = next(k for k, q in enumerate(qs) if q["name"].startswith("Who founded")) + 1
        qs.insert(i, {"@type": "Question", "name": Q, "acceptedAnswer": {"@type": "Answer", "text": ORIGINAL}})
        n["mainEntity"] = qs
t = t.replace(m.group(0), '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>")
p.write_text(t)

l = site / "llms.txt"
lt = re.sub(r"- Not affiliated with brandvo\.sa[^\n]*\n", "", l.read_text())
lt = re.sub(r"- Brandvo Digital Co\. is the original Brandvo[^\n]*\n", "", lt)
lt = lt.replace("\n- Services: ", f"\n- {ORIGINAL}\n- Services: ", 1)
assert ORIGINAL in lt
l.write_text(lt)

for f in site.rglob("*"):
    if f.is_file() and f.suffix in (".html", ".js", ".txt", ".xml"):
        assert "brandvo.sa" not in f.read_text().lower(), f

manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
