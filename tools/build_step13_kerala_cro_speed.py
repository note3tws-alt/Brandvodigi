#!/usr/bin/env python3
"""Step 13 (26 Nov 2026): low-risk Kerala-page, speed and accessibility fixes. Run after step 12.

Usage: python3 tools/build_step13_kerala_cro_speed.py site-build

1. Kerala landing page: adds a "Case study" section (Unicorn Bakes, figures as reported by the
   client and already published at /work/unicorn-bakes/) and a "Why businesses choose Brandvo"
   section built only from verifiable facts. Bumps dateModified and the sitemap lastmod.
2. Header logo: /logo-full.png was 1496x516 (48 KB) but is shown about 36 px tall. Resized to
   600x207 (same aspect ratio, still sharp at 3x). Same file name, so the JS bundle is untouched.
3. Footer copyright bar: text-white/40 failed WCAG AA contrast (3.7:1); now text-white/55.
4. /_headers: one-year immutable cache for /assets/* (all file names there are content hashed;
   step 4 re-hashes the JS bundle). If the CSS file is ever edited, rename it too.
Idempotent.
"""
import hashlib, json, re, sys
from pathlib import Path
from PIL import Image

site = Path(sys.argv[1])
TODAY = "2026-11-26"
H2 = ('<h2 id="{id}" class="mb-1 mt-14 font-display text-[1.65rem] font-semibold leading-tight '
      'tracking-tight text-white sm:text-[2rem]">{t}</h2>')
UL = '<ul class="mt-5 list-disc space-y-2.5 pl-6 marker:text-brand-magenta">'
LI = '<li class="pl-1"><strong class="font-semibold text-white">{b}</strong> {t}</li>'
A = '<a href="{h}" class="focus-ring rounded text-white underline decoration-brand-magenta decoration-2 underline-offset-4 transition-colors hover:text-brand-orange">{t}</a>'

CASE = (
    H2.format(id="case-study", t="Case study: ₹95 lakh in sales for a Payyanur bakery")
    + '\n<p class="mt-5">Unicorn Bakes is a pastry and cake shop in Payyanur. Over two years we worked on '
    "their branding, short-form content, influencer marketing with local food creators and Meta Ads "
    "aimed at WhatsApp and phone orders. The business reports <strong class=\"font-semibold text-white\">"
    "₹95 lakh in sales from ₹8 lakh in ad spend</strong>, roughly ₹11.9 in sales for every ₹1 spent on ads.</p>\n"
    '<p class="mt-5">The lesson for other Kerala businesses is not the budget. It is that a consistent brand, '
    "content planned around real occasions, trusted local voices and ads judged by orders rather than "
    "likes make each rupee work harder. "
    + A.format(h="/work/unicorn-bakes/", t="Read the full Unicorn Bakes case study")
    + ".</p>\n"
)
WHY = (
    H2.format(id="why-brandvo", t="Why businesses choose Brandvo Digital Co.")
    + "\n" + UL + "\n"
    + LI.format(b="One team from idea to enquiry.", t="Strategy, design, content, Meta Ads, SEO and websites "
                "sit with the same team, so the ad, the post and the landing page tell the same story.") + "\n"
    + LI.format(b="Measured on enquiries and sales.", t="We report on leads, cost per lead, WhatsApp chats, "
                "calls and orders, not on likes alone.") + "\n"
    + LI.format(b="People you can meet.", t="Our founder Muhammed Ansar and the team work from Payyanur in "
                "Kannur district. " + A.format(h="/about/#team", t="Meet the team") + ".") + "\n"
    + LI.format(b="Proof you can check.", t="Named clients and founders who speak for us on this page, plus "
                "a published case study with real figures.") + "\n"
    + LI.format(b="Honest about results.", t="Nobody can promise a Google position or a fixed number of "
                "leads. We promise a clear plan, transparent reporting and steady optimisation.") + "\n"
    + "</ul>\n"
)

# 1. Kerala page
p = site / "digital-marketing-agency-in-kerala" / "index.html"
t = p.read_text()
if 'id="case-study"' not in t:
    anchor = '<h2 id="how-we-work"'
    assert t.count(anchor) == 1
    t = t.replace(anchor, CASE + WHY + anchor)
t = re.sub(r'"dateModified":"\d{4}-\d\d-\d\d"', f'"dateModified":"{TODAY}"', t)
p.write_text(t)
sm = site / "sitemap.xml"
s = sm.read_text()
s = re.sub(r"(digital-marketing-agency-in-kerala/</loc><lastmod>)[\d-]+", r"\g<1>" + TODAY, s)
sm.write_text(s)

# 2. Header logo
logo = site / "logo-full.png"
im = Image.open(logo)
if im.width > 600:
    im.resize((600, round(600 * im.height / im.width)), Image.LANCZOS).save(logo, optimize=True)

# 3. Footer contrast (copyright bar only)
OLD = "gap-3 text-xs text-white/40 sm:flex-row"
for f in site.rglob("*.html"):
    h = f.read_text()
    if OLD in h:
        f.write_text(h.replace(OLD, "gap-3 text-xs text-white/55 sm:flex-row"))

# 4. Cache headers
(site / "_headers").write_text(
    "# Content-hashed build assets never change under the same name.\n"
    "/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n"
)

manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
