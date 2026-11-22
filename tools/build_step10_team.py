#!/usr/bin/env python3
"""Step 10: Team section (22 Nov 2026). Run after build_step9_priority_locations.py.

Usage: python3 tools/build_step10_team.py site-build

Requested by Hola on 22 Nov 2026:
- Founder: Muhammed Ansar, Social Media Manager.
- Co-founders: Akshay, Graphic & Content Creator; Abhishek Prakash, Marketing Head.
- Fathimath Thashreefa, Digital Marketing Specialist & Social Media Influencer.
Photos for all four came from Hola on 22 Nov 2026 (originals in assets/team/; the Akshay and
Abhishek photos arrived together, mapped as Abhishek = suit photo, Akshay = blue cardigan photo;
to swap, swap the source files in PHOTOS). A TEAM entry without "img" falls back to initials.

What it does:
1. Crops/resizes the two photos to 320x320 WebP under /images/team/.
2. Patches the bundle: a "Meet the team" section (#team) after the homepage About section,
   re-hashes the bundle, re-renders the homepage #root with Playwright.
3. About page: full names in "Who we are", a "Meet the team" section (#team), FAQ, meta.
4. Every page's Organization schema: founders with full names and job titles; About page
   gets Person nodes for all four. llms.txt team lines. Sitemap lastmod, deploy manifest.
Idempotent: re-running gives the same output.
"""
import hashlib, html, json, re, subprocess, sys, tempfile
from pathlib import Path

from PIL import Image

SITE = "https://brandvodigital.com"
TODAY = "2026-11-22"
site = Path(sys.argv[1])
ORG_ID = SITE + "/#organization"

TEAM = [
    {"n": "Muhammed Ansar", "i": "MA", "t": "Founder", "r": "Social Media Manager",
     "d": "Started Brandvo Digital Co. and leads social media for our clients: the content plan, the posting rhythm and what each month's results say.",
     "img": "/images/team/muhammed-ansar-founder-brandvo-digital-co.webp",
     "alt": "Muhammed Ansar, founder and social media manager at Brandvo Digital Co., Payyanur"},
    {"n": "Akshay", "i": "A", "t": "Co-founder", "r": "Graphic & Content Creator",
     "d": "Designs the posters, ad creatives and content that go out on our clients' pages, so every post looks like the same brand.",
     "img": "/images/team/akshay-graphic-content-creator-brandvo-digital-co.webp",
     "alt": "Akshay, co-founder and graphic and content creator at Brandvo Digital Co., Payyanur"},
    {"n": "Abhishek Prakash", "i": "AP", "t": "Co-founder", "r": "Marketing Head",
     "d": "Heads marketing strategy and campaign planning, keeping every plan tied to the enquiries and sales it is meant to bring.",
     "img": "/images/team/abhishek-prakash-marketing-head-brandvo-digital-co.webp",
     "alt": "Abhishek Prakash, co-founder and marketing head at Brandvo Digital Co., Payyanur"},
    {"n": "Fathimath Thashreefa", "i": "FT", "t": "Team", "r": "Digital Marketing Specialist & Social Media Influencer",
     "d": "Plans and runs digital campaigns, and as a creator herself she knows what makes people stop, watch and share.",
     "img": "/images/team/fathimath-thashreefa-digital-marketing-specialist-kannur.webp",
     "alt": "Fathimath Thashreefa, digital marketing specialist and social media influencer at Brandvo Digital Co., Kannur"},
]
JOB = {"Muhammed Ansar": "Founder & Social Media Manager", "Akshay": "Co-founder, Graphic & Content Creator",
       "Abhishek Prakash": "Co-founder & Marketing Head",
       "Fathimath Thashreefa": "Digital Marketing Specialist & Social Media Influencer"}
SEC_TITLE = ("The people behind ", "the work.")
SEC_TEXT = "You work directly with the people who plan, design and run your campaigns, from our office in Payyanur."

# ================================================================ 1. photos
PHOTOS = [("assets/team/muhammed-ansar-original.webp", (152, 40, 372, 260), TEAM[0]["img"]),
          ("assets/team/akshay-original.jpg", (465, 105, 785, 425), TEAM[1]["img"]),
          ("assets/team/abhishek-prakash-original.jpg", (15, 10, 410, 405), TEAM[2]["img"]),
          ("assets/team/fathimath-thashreefa-original.webp", (395, 250, 725, 580), TEAM[3]["img"])]
for srcf, box, url in PHOTOS:
    dest = site / url.lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        Image.open(srcf).convert("RGB").crop(box).resize((320, 320), Image.LANCZOS).save(dest, "WEBP", quality=82, method=6)


def rehash_bundle():
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


# ================================================================ 2. bundle: homepage team section
js = next((site / "assets").glob("index-bv*.js"))
s = js.read_text()
data = json.dumps(TEAM, ensure_ascii=False)
if "function Tm10(" in s:  # refresh the team data only
    s = re.sub(r"const Tm10D=\[.*?\];function Tm10\(", lambda m: "const Tm10D=" + data + ";function Tm10(", s, count=1, flags=re.S)
    js.write_text(s)
else:
    avatar = ('i.jsx("span",{className:"block shrink-0 rounded-full bg-gradient-to-br from-brand-indigo via-brand-magenta to-brand-orange",'
              'style:{width:88,height:88,padding:2},children:e.img?i.jsx("img",{src:e.img,alt:e.alt,width:320,height:320,loading:"lazy",decoding:"async",'
              'className:"h-full w-full rounded-full bg-ink-900 object-cover"}):i.jsx("span",{"aria-hidden":"true",'
              'className:"flex h-full w-full items-center justify-center rounded-full bg-ink-900 font-display text-2xl font-semibold text-white",children:e.i})})')
    card = ('i.jsxs(_e,{as:"li",delay:t*110,className:"glass flex flex-col p-6 sm:p-7",children:[' + avatar + ','
            'i.jsx("p",{className:"mt-5 text-xs uppercase tracking-[0.18em] text-white/45",children:e.t}),'
            'i.jsx("h3",{className:"mt-2 font-display text-lg font-semibold text-white",children:e.n}),'
            'i.jsx("p",{className:"mt-1 text-sm font-semibold text-brand-orange",children:e.r}),'
            'i.jsx("p",{className:"mt-3 text-[15px] leading-relaxed text-white/60",children:e.d})]},e.n)')
    comp = ('const Tm10D=' + data + ';function Tm10(){return i.jsx("section",{id:"team",className:"relative py-24 sm:py-32",'
            'children:i.jsxs("div",{className:"container-x",children:[i.jsx(es,{eyebrow:"Our Team",'
            f'title:i.jsxs(i.Fragment,{{children:[{json.dumps(SEC_TITLE[0])},i.jsx("span",{{className:"grad-text",children:{json.dumps(SEC_TITLE[1])}}})]}}),'
            f'text:{json.dumps(SEC_TEXT)},'
            'action:i.jsx("a",{href:"/about/#team",className:"focus-ring rounded text-sm font-semibold text-white underline decoration-brand-magenta decoration-2 underline-offset-4 transition-colors hover:text-brand-orange",children:"More about us"})}),'
            'i.jsx("ul",{className:"grid gap-5 sm:grid-cols-2 lg:grid-cols-4",children:Tm10D.map((e,t)=>' + card + ')})]})})}')
    anchor = "function es({eyebrow:e,"
    assert s.count(anchor) == 1
    s = s.replace(anchor, comp + anchor)
    old = "i.jsx(Tp,{}),i.jsx(Ap,{})"
    assert s.count(old) == 1
    s = s.replace(old, "i.jsx(Tp,{}),i.jsx(Tm10,{}),i.jsx(Ap,{})")
    js.write_text(s)
rehash_bundle()

with tempfile.TemporaryDirectory() as td:
    out = Path(td) / "pre.json"
    r = subprocess.run(["node", "tools/prerender.js", str(site), str(out), "/"], capture_output=True, text=True, timeout=180)
    print(r.stdout.strip())
    assert "errors: []" in r.stdout, r.stdout + r.stderr
    root = json.loads(out.read_text())["/"]["root"]
assert root.count("<h1") == 1 and 'id="team"' in root and "Fathimath Thashreefa" in root
home = site / "index.html"
t = home.read_text()
t, n = re.subn(r'<div id="root">.*?</div>\n  </body>', lambda m: '<div id="root">' + root + "</div>\n  </body>", t, flags=re.S)
assert n == 1
home.write_text(t)

# cards for static pages: same markup as the homepage, revealed
ul = re.search(r'<section id="team".*?(<ul class="grid.*?</ul>)', root, re.S).group(1)
ul = re.sub(r'\s*style="--d: ?\d+ms;?"', "", ul)
ul = ul.replace("reveal is-in ", "").replace("reveal ", "")

# ================================================================ 3. About page
A2 = "mb-1 mt-14 font-display text-[1.65rem] font-semibold leading-tight tracking-tight text-white sm:text-[2rem]"
p = site / "about" / "index.html"
t = p.read_text()
t = re.sub(r"<!--s10-->.*?<!--/s10-->", "", t, flags=re.S)
old_who = ('Brandvo Digital Co. was founded by <strong class="font-semibold text-white">Ansar</strong>, with <strong class="font-semibold text-white">Akshay</strong> '
           'and <strong class="font-semibold text-white">Abhishek</strong> as co-founders.')
new_who = ('Brandvo Digital Co. was founded by <strong class="font-semibold text-white">Muhammed Ansar</strong>, with <strong class="font-semibold text-white">Akshay</strong> '
           'and <strong class="font-semibold text-white">Abhishek Prakash</strong> as co-founders.')
t = t.replace(old_who, new_who)
assert new_who in t
block = (f'<!--s10--><h2 id="team" class="{A2}">Meet the team</h2>'
         f'<p class="mt-5">{html.escape(SEC_TEXT)}</p><div class="mt-8">{ul.replace("lg:grid-cols-4", "")}</div><!--/s10-->')
anchor = f'<h2 id="what-we-believe" class="{A2}">'
assert t.count(anchor) == 1
t = t.replace(anchor, block + anchor)
OLD_D = "founded by Ansar, with co-founders Akshay and Abhishek."
NEW_D = "founded by Muhammed Ansar, with co-founders Akshay and Abhishek Prakash."
t = t.replace(OLD_D, NEW_D)
OLD_FAQ = "Ansar is the founder, and Akshay and Abhishek are co-founders."
NEW_FAQ = ("Muhammed Ansar is the founder and social media manager. Akshay (graphic and content creator) and "
           "Abhishek Prakash (marketing head) are co-founders.")
t = t.replace(OLD_FAQ, NEW_FAQ)
p.write_text(t)

# ================================================================ 4. schema, llms.txt
def person(m, full=False):
    d = {"@type": "Person", "name": m["n"], "jobTitle": JOB[m["n"]]}
    if full:
        d["@id"] = SITE + "/about/#" + re.sub(r"[^a-z]+", "-", m["n"].lower()).strip("-")
        d["worksFor"] = {"@id": ORG_ID}
        if m.get("img"):
            d["image"] = SITE + m["img"]
    return d


FOUNDERS = json.dumps([person(m) for m in TEAM[:3]], ensure_ascii=False, separators=(",", ":"))
FOUNDER_RE = re.compile(r'"founder":\[\{"@type":"Person".*?\}\]')
nf = 0
for f in site.rglob("*.html"):
    t = f.read_text()
    t2 = FOUNDER_RE.sub(lambda m: '"founder":' + FOUNDERS, t)
    if t2 != t:
        f.write_text(t2)
        nf += 1
print("founder schema updated:", nf)

p = site / "about" / "index.html"
t = p.read_text()
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
data = json.loads(m.group(1))
g = [n for n in data["@graph"] if n.get("@type") != "Person"]
for n in g:
    if n.get("@type") == "AboutPage":
        n["dateModified"] = TODAY
g += [person(mm, True) for mm in TEAM]
data["@graph"] = g
t = t.replace(m.group(0), '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>")
p.write_text(t)

llms = (site / "llms.txt").read_text()
llms = re.sub(r"- Founder: .*\n(- Team: .*\n)?",
              "- Founder: Muhammed Ansar (social media manager). Co-founders: Akshay (graphic and content creator) and Abhishek Prakash (marketing head).\n"
              "- Team: Fathimath Thashreefa, digital marketing specialist and social media influencer.\n", llms, count=1)
llms = llms.replace(OLD_D, NEW_D)
(site / "llms.txt").write_text(llms)

# ================================================================ 5. sitemap, checks, manifest
sm = (site / "sitemap.xml").read_text()
for u in ["/", "/about/"]:
    loc = f"<loc>{SITE}{u}</loc>"
    sm = re.sub(re.escape(loc) + r"<lastmod>[^<]+", loc + f"<lastmod>{TODAY}", sm)
(site / "sitemap.xml").write_text(sm)

for f in [site / "index.html", site / "about" / "index.html"]:
    t = f.read_text()
    for src in re.findall(r'src="(/images/[^"]+)"', t):
        assert (site / src.lstrip("/")).exists(), src
    assert "Abhishek Prakash" in t and "Fathimath Thashreefa" in t, f

manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
