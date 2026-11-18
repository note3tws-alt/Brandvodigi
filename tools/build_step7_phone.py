#!/usr/bin/env python3
"""Step 7: phone numbers (18 Nov 2026). Run after the other steps.

+91 62354 34787 is the calling number; +91 62820 70376 is WhatsApp only.
Fixes schema telephone, the contact-section tel: link, the "reach us on" line,
re-hashes the bundle and rewrites tools/deploy-manifest.json. Idempotent.

Usage: python3 tools/build_step7_phone.py site-build
"""
import hashlib, json, sys
from pathlib import Path

site = Path(sys.argv[1])
CALL, CALL_TEL = "+91 62354 34787", "+916235434787"
WA, WA_TEL = "+91 62820 70376", "+916282070376"
REPL = [
    (f'"telephone":"{WA}"', f'"telephone":"{CALL}"'),
    (f'href="tel:{WA_TEL}"', f'href="tel:{CALL_TEL}"'),
    (f'hover:text-white">{WA}</a>', f'hover:text-white">{CALL}</a>'),
    (f"You can also reach us on {WA}.", f"You can also call {CALL} or WhatsApp {WA}."),
    (f"{WA} (phone and WhatsApp)", f"{CALL} (calls), {WA} (WhatsApp)"),
    # bundle: contact list shows the calling number; inline line mentions both
    ('["phone",K.phone,`tel:${K.phone.replace(/\\s/g,"")}`,!1]', '["phone",K.footerPhone,`tel:${K.footerPhone.replace(/\\s/g,"")}`,!1]'),
    ('You can also reach us on ",K.phone,"."', 'You can also call ",K.footerPhone," or WhatsApp ",K.phone,"."'),
]
n = 0
for f in list(site.rglob("*.html")) + list(site.rglob("*.js")) + [site / "llms.txt"]:
    s = f.read_text(); t = s
    for a, b in REPL:
        t = t.replace(a, b)
    if t != s:
        f.write_text(t); n += 1
print("files changed:", n)

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

manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
