#!/usr/bin/env python3
"""Step 8: internal linking, hubs and service depth (19 Nov 2026). Run after build_step7_phone.py.

Usage: python3 tools/build_step8_linking.py site-build content/pages-2026-11-19

Approved by Hola on 19 Nov 2026 (options B, C, D of the Phase 1 plan):
- B  Homepage service cards link to their service pages (new SEO card added),
     footer lists every service, location, industry, the case study and About,
     breadcrumbs gain Services / Industries / Kerala levels, /services/ and
     /industries/ hub pages.
- C  Expanded copy for /services/social-media-marketing/, /services/performance-marketing/
     and /industries/real-estate/ (overwrites the step3 versions).
- D  New pages /services/lead-generation/, /services/local-seo/, /about/,
     /industries/food-and-restaurants/.

The homepage #root is re-rendered with Playwright from the patched bundle and the
new footer is copied into every page, so static pages and the SPA show the same
footer. Idempotent: re-running gives the same output.
"""
import hashlib, html, json, re, subprocess, sys, tempfile
from pathlib import Path

import markdown

SITE = "https://brandvodigital.com"
TODAY = "2026-11-19"
site, src = Path(sys.argv[1]), Path(sys.argv[2])
ORG_REF = {"@id": SITE + "/#organization", "@type": "ProfessionalService", "name": "Brandvo Digital Co.", "url": SITE + "/"}
MARK = "<!-- build_step8 -->"
OVERWRITE_OK = {"services/social-media-marketing", "services/performance-marketing", "industries/real-estate"}

CLS = {
    "h2": "mb-1 mt-14 font-display text-[1.65rem] font-semibold leading-tight tracking-tight text-white sm:text-[2rem]",
    "h3": "mb-1 mt-9 font-display text-xl font-semibold leading-snug text-white",
    "p": "mt-5",
    "ul": "mt-5 list-disc space-y-2.5 pl-6 marker:text-brand-magenta",
    "ol": "mt-5 list-decimal space-y-2.5 pl-6 marker:font-semibold marker:text-brand-orange",
    "li": "pl-1",
    "strong": "font-semibold text-white",
    "a": "focus-ring rounded text-white underline decoration-brand-magenta decoration-2 underline-offset-4 transition-colors hover:text-brand-orange",
}
CRUMB_A = "focus-ring rounded hover:text-white"


def esc(s):
    return html.escape(s, quote=True)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", s)).lower()).strip("-")


def style(body):
    body = re.sub(r"<h2>(.*?)</h2>", lambda m: f'<h2 id="{slugify(m.group(1))}" class="{CLS["h2"]}">{m.group(1)}</h2>', body)
    body = re.sub(r"<h3>(.*?)</h3>", lambda m: f'<h3 class="{CLS["h3"]}">{m.group(1)}</h3>', body)
    for tag in ["p", "ul", "ol", "li", "strong"]:
        body = body.replace(f"<{tag}>", f'<{tag} class="{CLS[tag]}">')
    body = re.sub(r'<a href="(https?://[^"]+)">', lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener noreferrer" class="{CLS["a"]}">', body)
    body = re.sub(r'<a href="((?:/|mailto:)[^"]*)">', lambda m: f'<a href="{m.group(1)}" class="{CLS["a"]}">', body)
    body = body.replace("<table>", '<div class="mt-7 overflow-x-auto rounded-2xl border border-white/10"><table class="w-full min-w-[560px] border-collapse text-left text-[15px] leading-6">').replace("</table>", "</table></div>")
    body = body.replace("<thead>\n<tr>", '<thead>\n<tr class="bg-white/[0.04]">').replace("<th>", '<th class="px-4 py-3 font-display text-sm font-semibold text-white">')
    body = re.sub(r"<tbody>(.*?)</tbody>", lambda m: "<tbody>" + m.group(1).replace("<tr>", '<tr class="border-t border-white/[0.07]">').replace("<td>", '<td class="px-4 py-3.5 align-top">') + "</tbody>", body, flags=re.S)
    assert "<a href" not in re.sub(r'<a href="[^"]+" (target|class)', "", body), "unstyled link"
    return body


def faqs(md_body):
    m = re.search(r"^## Frequently asked questions\s*$(.*?)(?=^## |\Z)", md_body, flags=re.M | re.S)
    if not m:
        return []
    out = []
    for q, a in re.findall(r"^### (.+?)\s*\n(.*?)(?=^### |\Z)", m.group(1), flags=re.M | re.S):
        a = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a.strip())
        a = re.sub(r"\*\*(.+?)\*\*", r"\1", a)
        out.append((q.strip(), " ".join(a.split())))
    return out


def crumb_ol(crumbs):
    items = []
    for i, (name, href) in enumerate(crumbs):
        if i:
            items.append('<li aria-hidden="true">/</li>')
        if href:
            items.append(f'<li><a href="{href}" class="{CRUMB_A}">{esc(name)}</a></li>')
        else:
            items.append(f'<li aria-current="page" class="text-white/70">{esc(name)}</li>')
    return f'<ol class="flex flex-wrap items-center gap-x-2 gap-y-1">{"".join(items)}</ol>'


def bc_ld(crumbs, url):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + (h or url)} for i, (n, h) in enumerate(crumbs)]}


def hero(crumbs, eyebrow, h1):
    return ('<header class="relative isolate overflow-x-clip pt-[72px]"><div aria-hidden="true" class="pointer-events-none absolute inset-0 -z-10">'
            '<div class="absolute -right-32 -top-40 h-[560px] w-[560px] rounded-full bg-brand-magenta/20 blur-[140px]"></div>'
            '<div class="absolute left-[4%] top-[30%] h-[380px] w-[380px] rounded-full bg-brand-indigo/25 blur-[130px]"></div></div>'
            '<div class="container-x max-w-3xl pb-10 pt-14 sm:pt-20"><nav aria-label="Breadcrumb" class="text-xs text-white/45">'
            f'{crumb_ol(crumbs)}</nav>'
            f'<p class="eyebrow mt-8">{esc(eyebrow)}</p>'
            f'<h1 class="h-display mt-4 text-[clamp(2rem,4.6vw,3.4rem)] leading-[1.08]">{esc(h1)}</h1></div></header>')


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


# ================================================================ 1. bundle: service cards + footer
SERVICES = [("Social Media Marketing", "/services/social-media-marketing/"), ("Meta Ads", "/services/meta-ads/"),
            ("Performance Marketing", "/services/performance-marketing/"), ("Lead Generation", "/services/lead-generation/"),
            ("SEO", "/services/seo/"), ("Local SEO", "/services/local-seo/"),
            ("Website Design", "/services/website-design/"), ("Branding & Creative", "/services/branding/"),
            ("All services", "/services/")]
INDUSTRIES = [("About Brandvo Digital Co.", "/about/"), ("Case study: Unicorn Bakes", "/work/unicorn-bakes/"),
              ("Real estate marketing", "/industries/real-estate/"), ("Healthcare marketing", "/industries/healthcare/"),
              ("Beauty & salon marketing", "/industries/beauty-and-salons/"), ("Restaurant & bakery marketing", "/industries/food-and-restaurants/"),
              ("All industries", "/industries/")]
LOCATIONS = [("Kerala", "kerala"), ("Kannur", "kannur"), ("Payyanur", "payyanur"), ("Thalassery", "thalassery"),
             ("Taliparamba", "taliparamba"), ("Kasaragod", "kasaragod"), ("Kanhangad", "kanhangad"), ("Kozhikode", "kozhikode"),
             ("Vadakara", "vadakara"), ("Wayanad", "wayanad"), ("Malappuram", "malappuram"), ("Palakkad", "palakkad"),
             ("Thrissur", "thrissur"), ("Kochi", "kochi"), ("Thiruvananthapuram", "trivandrum")]
LOC_LINKS = [(n, f"/digital-marketing-agency-in-{s}/") for n, s in LOCATIONS]
for _, u in SERVICES + INDUSTRIES + LOC_LINKS:
    assert (site / u.strip("/") / "index.html").exists() or (src / "x").parent.exists(), u  # new pages checked at the end

js = next((site / "assets").glob("index-bv*.js"))
s = js.read_text()
arr = lambda xs: "[" + ",".join(json.dumps([n, u], ensure_ascii=False) for n, u in xs) + "]"
if "Sx8=" not in s:
    # service cards: give every card a page, add SEO
    for title, page in [("Content Strategy", "/services/social-media-marketing/"), ("Reels & Short-Form", "/services/social-media-marketing/"),
                        ("Creative Design", "/services/branding/"), ("Branding", "/services/branding/"),
                        ("Lead Generation", "/services/lead-generation/"), ("Digital Strategy", "/services/"),
                        ("Website & Landing Pages", "/services/website-design/")]:
        old = f'title:"{title}",chips:'
        assert s.count(old) == 1, title
        s = s.replace(old, f'title:"{title}",page:"{page}",chips:')
    seo_card = ('{icon:"compass",title:"SEO & Local Search",page:"/services/seo/",chips:["Google Business Profile","Local rankings","Reviews"],'
                'text:"Get found on Google Search and Maps when nearby customers look for what you sell."},')
    anchor = '{icon:"pen",title:"Content Strategy",'
    assert s.count(anchor) == 1
    s = s.replace(anchor, seo_card + anchor)
    # footer data
    lx_start = s.index("const Lx=[")
    lx_end = s.index("]],cl=", lx_start) + 2
    s = s[:lx_start] + f"const Lx={arr(LOC_LINKS)},Sx8={arr(SERVICES)},Ix8={arr(INDUSTRIES)}" + s[lx_end:]
    li_map = lambda v: f'{v}.map(e=>i.jsx("li",{{children:i.jsx("a",{{href:e[1],className:Ot,children:e[0]}})}},e[1]))'
    old = 'Wn.slice(0,6).map(e=>i.jsx("li",{children:i.jsx("a",{href:e.page||"/#services",className:Ot,children:e.title})},e.title))'
    assert s.count(old) == 1
    s = s.replace(old, li_map("Sx8"))
    old = 'i.jsx("h3",{className:cl+" mt-8",children:"Locations & industries"}),i.jsx("ul",{className:"mt-4 space-y-2.5",children:' + li_map("Lx") + "})"
    assert s.count(old) == 1
    s = s.replace(old, 'i.jsx("h3",{className:cl+" mt-8",children:"Company & industries"}),i.jsx("ul",{className:"mt-4 space-y-2.5",children:' + li_map("Ix8") + "})")
    old = 'i.jsx("li",{children:K.location})]})]})'
    assert s.count(old) == 1
    s = s.replace(old, 'i.jsx("li",{children:K.location})]}),i.jsx("h3",{className:cl+" mt-8",children:"Kerala locations"}),'
                       'i.jsx("ul",{className:"mt-4 space-y-2.5",children:' + li_map("Lx") + "})]})")
    js.write_text(s)
rehash_bundle()

# ================================================================ 2. re-render homepage, take the footer
with tempfile.TemporaryDirectory() as td:
    out = Path(td) / "pre.json"
    r = subprocess.run(["node", "tools/prerender.js", str(site), str(out), "/"], capture_output=True, text=True, timeout=180)
    print(r.stdout.strip())
    assert "errors: []" in r.stdout, r.stdout + r.stderr
    pre = json.loads(out.read_text())["/"]
root = pre["root"]
assert root.count("<h1") == 1 and "Best Digital Marketing Agency in Kerala" in root
assert 'href="/services/seo/"' in root and 'href="/about/"' in root and "Kerala locations" in root
footer = root[root.index("<footer"): root.index("</footer>") + len("</footer>")]

home = site / "index.html"
t = home.read_text()
t, n = re.subn(r'<div id="root">.*?</div>\n  </body>', lambda m: '<div id="root">' + root + "</div>\n  </body>", t, flags=re.S)
assert n == 1
t = re.sub(r'\s*<meta name="keywords" content="[^"]*" />', "", t)
home.write_text(t)

# ================================================================ 3. new and expanded pages
tpl = (site / "digital-marketing-agency-in-kannur" / "index.html").read_text()
head_tpl = tpl[: tpl.index('<div id="root">') + len('<div id="root">')]
rest = tpl[len(head_tpl):]
chrome_top = rest[: rest.index('<main id="main">')]
end_tpl = rest[rest.index("<footer"):]
aside_html = rest[rest.index("<aside"): rest.index("</aside>") + len("</aside>")]


def make_head(title, desc, url, graph):
    h = head_tpl
    h = re.sub(r"<title>.*?</title>", "<title>" + esc(title) + "</title>", h)
    for attr, val in [('name="description"', desc), ('property="og:title"', title), ('property="og:description"', desc), ('property="og:url"', url)]:
        h, k = re.subn(r'<meta ' + attr + r' content="[^"]*" />', f'<meta {attr} content="{esc(val)}" />', h)
        assert k == 1, attr
    h, k = re.subn(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{url}" />', h)
    assert k == 1
    h, k = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: ld({"@context": "https://schema.org", "@graph": graph}), h, flags=re.S)
    assert k == 1
    return h


new = []
for f in sorted(src.glob("*.md")):
    fm_txt, body_md = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(), flags=re.S).groups()
    fm = dict(line.split(": ", 1) for line in fm_txt.splitlines() if ": " in line)
    kind, url = fm["kind"], fm["url"]
    full = SITE + url
    body = style(markdown.markdown(body_md.strip(), extensions=["tables", "sane_lists"]))
    name = fm["breadcrumb"].split(">")[-1].strip()
    if kind == "service":
        eyebrow, crumbs = "Services", [("Home", "/"), ("Services", "/services/"), (name, None)]
        main_ld = {"@type": "Service", "@id": full + "#service", "name": fm["h1"], "serviceType": name, "provider": ORG_REF,
                   "areaServed": [{"@type": "State", "name": "Kerala"}, {"@type": "Country", "name": "United Arab Emirates"}], "url": full}
        page_type = "WebPage"
    elif kind == "industry":
        eyebrow, crumbs = "Industries", [("Home", "/"), ("Industries", "/industries/"), (name, None)]
        main_ld = {"@type": "Service", "@id": full + "#service", "name": fm["h1"], "serviceType": name + " marketing", "provider": ORG_REF,
                   "areaServed": {"@type": "State", "name": "Kerala"}, "url": full}
        page_type = "WebPage"
    elif kind == "about":
        eyebrow, crumbs = "About", [("Home", "/"), ("About", None)]
        main_ld = None
        page_type = "AboutPage"
    else:  # hub
        eyebrow, crumbs = name, [("Home", "/"), (name, None)]
        links = re.findall(r"^##+ \[([^\]]+)\]\((/[^)]+)\)", body_md, flags=re.M)
        main_ld = {"@type": "ItemList", "@id": full + "#list", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + u} for i, (n, u) in enumerate(links)]}
        page_type = "CollectionPage"
    webpage = {"@type": page_type, "@id": full + "#webpage", "url": full, "name": fm["title"], "description": fm["metaDescription"],
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"}, "inLanguage": "en-IN",
               "dateModified": TODAY, "breadcrumb": {"@id": full + "#breadcrumb"}}
    if kind == "about":
        webpage["mainEntity"] = {"@id": SITE + "/#organization"}
    bc = dict(bc_ld(crumbs, url), **{"@id": full + "#breadcrumb"})
    graph = [webpage] + ([main_ld] if main_ld else []) + [bc]
    fq = faqs(body_md)
    assert fq, f"no FAQ in {f}"
    graph.append({"@type": "FAQPage", "@id": full + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]})
    main = ('<main id="main">' + hero(crumbs, eyebrow, fm["h1"]) +
            '<div class="container-x max-w-3xl pb-24"><article class="mt-4"><div class="text-[17px] leading-8 text-white/70">'
            + body + "</div></article>" + aside_html + "</div></main>")
    dest = site / url.strip("/") / "index.html"
    if dest.exists():
        assert MARK in dest.read_text() or url.strip("/") in OVERWRITE_OK, f"would overwrite {dest}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(make_head(fm["title"], fm["metaDescription"], full, graph) + chrome_top + main + end_tpl.replace("</body>", MARK + "\n  </body>", 1))
    new.append((kind, fm["h1"], url, fm["metaDescription"]))
    print("page", url, len(re.sub(r"<[^>]+>", " ", body).split()), "words", len(fq), "faqs")

# ================================================================ 4. breadcrumbs on existing static pages
def set_crumbs(path, crumbs):
    t = path.read_text()
    t, k = re.subn(r'(<nav aria-label="Breadcrumb" class="text-xs text-white/45">)<ol .*?</ol>', lambda m: m.group(1) + crumb_ol(crumbs), t, count=1, flags=re.S)
    if not k:
        return False
    url = "/" + path.parent.relative_to(site).as_posix().strip("/") + "/"
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, flags=re.S)
    data = json.loads(m.group(1))
    nodes = data.get("@graph", [data])
    bc = dict(bc_ld(crumbs, url))
    for i, node in enumerate(nodes):
        if node.get("@type") == "BreadcrumbList":
            if "@id" in node:
                bc["@id"] = node["@id"]
            nodes[i] = bc
            break
    else:
        nodes.append(bc)
    t = t.replace(m.group(0), ld(data if "@graph" in data else {"@context": "https://schema.org", "@graph": nodes}))
    path.write_text(t)
    return True


def last_crumb(t):
    m = re.search(r'aria-current="page" class="text-white/70">([^<]+)</li>', t)
    return html.unescape(m.group(1)) if m else None


fixed = 0
for p in sorted(site.rglob("index.html")):
    rel = p.parent.relative_to(site).as_posix()
    if rel == "." or rel.startswith("blog") or MARK in p.read_text():
        continue
    t = p.read_text()
    name = last_crumb(t)
    if not name:
        continue
    if rel.startswith("services/"):
        crumbs = [("Home", "/"), ("Services", "/services/"), (name, None)]
    elif rel.startswith("industries/"):
        crumbs = [("Home", "/"), ("Industries", "/industries/"), (name, None)]
    elif rel.startswith("work/"):
        crumbs = [("Home", "/"), ("About", "/about/"), (name, None)]
    elif rel.startswith("digital-marketing-agency-in-") and rel != "digital-marketing-agency-in-kerala":
        crumbs = [("Home", "/"), ("Kerala", "/digital-marketing-agency-in-kerala/"), (name, None)]
    else:
        continue
    fixed += set_crumbs(p, crumbs)
print("breadcrumbs updated:", fixed)

# ================================================================ 5. footer everywhere (static pages + prerendered SPA pages)
FOOT = re.compile(r"<footer .*?</footer>", re.S)
nf = 0
for p in site.rglob("*.html"):
    t = p.read_text()
    if "<footer" not in t:
        continue
    t2 = FOOT.sub(lambda m: footer, t, count=1)
    if t2 != t:
        p.write_text(t2)
        nf += 1
print("footers replaced:", nf)

# ================================================================ 6. Kerala pillar: link the new pages
S8 = re.compile(r"<!--s8-->.*?<!--/s8-->", re.S)
p = site / "digital-marketing-agency-in-kerala" / "index.html"
t = S8.sub("", p.read_text())
lis = "".join(f'<li class="{CLS["li"]}"><a href="{u}" class="{CLS["a"]}">{esc(h)}</a></li>' for k, h, u, d in new if k != "hub")
block = (f'<h2 id="more-from-brandvo-digital-co" class="{CLS["h2"]}">More from Brandvo Digital Co.</h2>'
         f'<p class="{CLS["p"]}">Browse <a href="/services/" class="{CLS["a"]}">all services</a> or <a href="/industries/" class="{CLS["a"]}">all industries</a>, or start here:</p>'
         f'<ul class="{CLS["ul"]}">{lis}</ul>')
assert t.count("<!--/s6--></div></article>") == 1
p.write_text(t.replace("<!--/s6--></div></article>", "<!--/s6--><!--s8-->" + block + "<!--/s8--></div></article>"))

# ================================================================ 7. sitemap, llms.txt, manifest
sm = (site / "sitemap.xml").read_text()
for k, h, u, d in new:
    loc = f"<loc>{SITE}{u}</loc>"
    if loc in sm:
        sm = re.sub(re.escape(loc) + r"<lastmod>[^<]+", loc + f"<lastmod>{TODAY}", sm)
    else:
        sm = sm.replace("</urlset>", f"  <url>{loc}<lastmod>{TODAY}</lastmod></url>\n</urlset>")
for u in ["/", "/digital-marketing-agency-in-kerala/"]:
    loc = f"<loc>{SITE}{u}</loc>"
    sm = re.sub(re.escape(loc) + r"<lastmod>[^<]+", loc + f"<lastmod>{TODAY}", sm)
(site / "sitemap.xml").write_text(sm)

llms = (site / "llms.txt").read_text()
llms = re.sub(r"\n## Services, industries and company\n.*?(?=\n## )", "", llms, flags=re.S)
llms = llms.replace("\n## Contact", "\n## Services, industries and company\n\n" +
                    "".join(f"- [{h}]({SITE}{u}): {d}\n" for k, h, u, d in new) + "\n## Contact", 1)
(site / "llms.txt").write_text(llms)

# every linked internal page must exist
missing = set()
for p in site.rglob("*.html"):
    for href in re.findall(r'href="(/[^"#?]*)"', p.read_text()):
        if href.startswith("/assets/") or "." in href.rsplit("/", 1)[-1]:
            continue
        if href in ("/", "/privacy", "/terms"):
            continue
        if not (site / href.strip("/") / "index.html").exists():
            missing.add((href, p.relative_to(site).as_posix()))
assert not missing, sorted(missing)[:20]

manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("pages:", len(new), "manifest files:", len(manifest))
