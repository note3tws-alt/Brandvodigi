#!/usr/bin/env python3
"""Step 11: Unicorn Bakes founder is Sreejith Ramesh (22 Nov 2026). Run after build_step10_team.py.

Usage: python3 tools/build_step11_unicorn_founder.py site-build

Hola, 22 Nov 2026: "change unicorn bakes founder to this guy Sreejith Ramesh", with a photo
(original in assets/testimonials/). The existing Unicorn Bakes testimonial quote stays the same;
only the person it is attributed to and the photo change. The old "Abhishek" attribution and the
old testimonial photo are removed everywhere (homepage testimonials, static pages).
Idempotent: re-running gives the same output.
"""
import hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path

from PIL import Image

site = Path(sys.argv[1])
NAME = "Sreejith Ramesh"
IMG = "/testimonials/sreejith-ramesh-unicorn-bakes.webp"
OLD_IMG = "/testimonials/abhishek-unicorn-bakes.webp"

# 1. photo: 4:5 like the other testimonial photos (320x400)
dest = site / IMG.lstrip("/")
if not dest.exists():
    Image.open("assets/testimonials/sreejith-ramesh-unicorn-bakes-original.jpg").convert("RGB").crop((14, 0, 166, 190)) \
        .resize((320, 400), Image.LANCZOS).save(dest, "WEBP", quality=85, method=6)
for f in ["abhishek-unicorn-bakes.webp", "abhishek-unicorn-bakes.jpg"]:
    (site / "testimonials" / f).unlink(missing_ok=True)

# 2. bundle testimonial
js = next((site / "assets").glob("index-bv*.js"))
s = js.read_text()
old = f'name:"Abhishek",role:"Founder",company:"Unicorn Bakes, Payyanur",image:"{OLD_IMG}"'
new = f'name:"{NAME}",role:"Founder",company:"Unicorn Bakes, Payyanur",image:"{IMG}"'
if old in s:
    js.write_text(s.replace(old, new))
assert new in js.read_text()
js = next((site / "assets").glob("index-bv*.js"))
s = js.read_text()
newname = "index-bv" + hashlib.sha1(s.encode()).hexdigest()[:8] + ".js"
if newname != js.name:
    js.rename(js.parent / newname)
    for h in site.rglob("*.html"):
        t = h.read_text()
        if js.name in t:
            h.write_text(t.replace("/assets/" + js.name, "/assets/" + newname))
    print("bundle", js.name, "->", newname)

# 3. static pages
REPL = [("— Abhishek, Founder, Unicorn Bakes", f"— {NAME}, Founder, Unicorn Bakes"),
        ("(Abhishek, Founder, Unicorn Bakes)", f"({NAME}, Founder, Unicorn Bakes)"),
        ('sales." — Abhishek, Founder<', f'sales." — {NAME}, Founder<'),
        ('sales." (Abhishek, Founder)<', f'sales." ({NAME}, Founder)<')]
for f in site.rglob("*.html"):
    if f == site / "index.html":
        continue
    t = f.read_text()
    t2 = t
    for a, b in REPL:
        t2 = t2.replace(a, b)
    if t2 != t:
        f.write_text(t2)
        print("updated", f.relative_to(site))

# 4. homepage re-render
with tempfile.TemporaryDirectory() as td:
    out = Path(td) / "pre.json"
    r = subprocess.run(["node", "tools/prerender.js", str(site), str(out), "/"], capture_output=True, text=True, timeout=180)
    assert "errors: []" in r.stdout, r.stdout + r.stderr
    root = json.loads(out.read_text())["/"]["root"]
assert root.count("<h1") == 1 and 'id="team"' in root
home = site / "index.html"
t = home.read_text()
t, n = re.subn(r'<div id="root">.*?</div>\n  </body>', lambda m: '<div id="root">' + root + "</div>\n  </body>", t, flags=re.S)
assert n == 1
home.write_text(t)

# 5. checks + manifest
for f in list(site.rglob("*.html")) + list(site.rglob("*.js")) + [site / "llms.txt"]:
    t = f.read_text()
    assert "abhishek-unicorn-bakes" not in t, f
    assert not re.search(r"Abhishek(?! Prakash)", t), f
manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
