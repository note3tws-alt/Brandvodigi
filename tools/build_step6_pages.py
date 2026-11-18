#!/usr/bin/env python3
"""Step 6: regional SEO expansion (17 Nov 2026). Run after build_step5_aeo.py.

Usage: python3 tools/build_step6_pages.py site-build content/pages-2026-11

Adds static pages built from Markdown, using the chrome of an existing static
page (no JS bundle, same as build_step3 pages):
- kind: location -> /digital-marketing-agency-in-<town>/  (Service + areaServed)
- kind: service  -> /services/<slug>/                      (Service, Kerala)
- kind: article  -> /blog/<slug>/                          (BlogPosting)
Every page gets WebPage, BreadcrumbList and FAQPage JSON-LD.

Also: adds the new towns to the footer "Locations & industries" list (static
HTML and JS bundle), links the new pages from the Kerala, Kannur and Payyanur
pages, appends them to sitemap.xml and llms.txt, re-hashes the bundle name
and rewrites tools/deploy-manifest.json.
"""
import hashlib, html, json, re, sys
from pathlib import Path

import markdown

SITE = "https://brandvodigital.com"
TODAY = "2026-11-17"
site, src = Path(sys.argv[1]), Path(sys.argv[2])
ORG_REF = {"@id": SITE + "/#organization", "@type": "ProfessionalService", "name": "Brandvo Digital Co.", "url": SITE + "/"}

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
    body = re.sub(r'<a href="(/[^"]*)">', lambda m: f'<a href="{m.group(1)}" class="{CLS["a"]}">', body)
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


def hero(crumbs, eyebrow, h1, meta_line=None):
    items = []
    for i, (name, href) in enumerate(crumbs):
        if i:
            items.append('<li aria-hidden="true">/</li>')
        if href:
            items.append(f'<li><a href="{href}" class="focus-ring rounded hover:text-white">{esc(name)}</a></li>')
        else:
            items.append(f'<li aria-current="page" class="text-white/70">{esc(name)}</li>')
    ml = f'<p class="mt-6 text-sm text-white/50">{meta_line}</p>' if meta_line else ""
    return ('<header class="relative isolate overflow-x-clip pt-[72px]"><div aria-hidden="true" class="pointer-events-none absolute inset-0 -z-10">'
            '<div class="absolute -right-32 -top-40 h-[560px] w-[560px] rounded-full bg-brand-magenta/20 blur-[140px]"></div>'
            '<div class="absolute left-[4%] top-[30%] h-[380px] w-[380px] rounded-full bg-brand-indigo/25 blur-[130px]"></div></div>'
            '<div class="container-x max-w-3xl pb-10 pt-14 sm:pt-20"><nav aria-label="Breadcrumb" class="text-xs text-white/45">'
            f'<ol class="flex flex-wrap items-center gap-x-2 gap-y-1">{"".join(items)}</ol></nav>'
            f'<p class="eyebrow mt-8">{esc(eyebrow)}</p>'
            f'<h1 class="h-display mt-4 text-[clamp(2rem,4.6vw,3.4rem)] leading-[1.08]">{esc(h1)}</h1>{ml}</div></header>')


# ------------------------------------------------ template from an existing static page
tpl = (site / "digital-marketing-agency-in-kannur" / "index.html").read_text()
head_tpl = tpl[: tpl.index('<div id="root">') + len('<div id="root">')]
root = tpl[len(head_tpl):]
chrome_top = root[: root.index('<main id="main">')]
footer_and_end = root[root.index("<footer"):]
aside_html = root[root.index("<aside"): root.index("</aside>") + len("</aside>")]


def make_head(title, desc, url, graph):
    h = head_tpl
    h = re.sub(r"<title>.*?</title>", "<title>" + esc(title) + "</title>", h)
    for attr, val in [('name="description"', desc), ('property="og:title"', title), ('property="og:description"', desc), ('property="og:url"', url)]:
        h, n = re.subn(r'<meta ' + attr + r' content="[^"]*" />', f'<meta {attr} content="{esc(val)}" />', h)
        assert n == 1, attr
    h, n = re.subn(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{url}" />', h)
    assert n == 1
    if "/blog/" in url:
        h = h.replace('<meta property="og:type" content="website" />', '<meta property="og:type" content="article" />')
    h, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: ld({"@context": "https://schema.org", "@graph": graph}), h, flags=re.S)
    assert n == 1
    return h


new = []  # (kind, title-for-lists, url, desc, place)
for f in sorted(src.glob("*.md")):
    fm_txt, body_md = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(), flags=re.S).groups()
    fm = dict(line.split(": ", 1) for line in fm_txt.splitlines() if ": " in line)
    kind, url = fm["kind"], fm["url"]
    full = SITE + url
    body_md = re.sub(r"^# .+\n", "", body_md.lstrip(), count=1)
    body = style(markdown.markdown(body_md, extensions=["tables", "sane_lists"]))
    if kind == "location":
        place = fm["place"]
        eyebrow, crumbs = f"Digital marketing · {place}", [("Home", "/"), (f"Digital marketing in {place}", None)]
        area = {"@type": fm.get("areaType", "City"), "name": place, "containedInPlace": {"@type": "State", "name": "Kerala"}}
        main_ld = {"@type": "Service", "@id": full + "#service", "name": fm["h1"], "serviceType": "Digital marketing",
                   "provider": ORG_REF, "areaServed": area, "url": full}
        list_title = f"Digital marketing agency in {place}"
    elif kind in ("service", "industry"):
        name = fm["breadcrumb"].split(">")[-1].strip()
        eyebrow, crumbs = ("Services", [("Home", "/"), ("Services", "/#services"), (name, None)]) if kind == "service" else ("Industries", [("Home", "/"), (name + " marketing", None)])
        main_ld = {"@type": "Service", "@id": full + "#service", "name": fm["h1"], "serviceType": name, "provider": ORG_REF,
                   "areaServed": [{"@type": "State", "name": "Kerala"}, {"@type": "Country", "name": "United Arab Emirates"}], "url": full}
        list_title = name
    else:
        eyebrow, crumbs = "Guide", [("Home", "/"), ("Blog", "/blog/"), (fm["breadcrumb"].split(">")[-1].strip(), None)]
        main_ld = {"@type": "BlogPosting", "@id": full + "#article", "headline": fm["h1"], "description": fm["metaDescription"],
                   "datePublished": fm["date"], "dateModified": fm["date"], "inLanguage": "en-IN", "mainEntityOfPage": full,
                   "image": SITE + "/og-image.png", "author": ORG_REF, "publisher": ORG_REF}
        list_title = fm["h1"]
    bc_items = [(n, SITE + (h or url)) for n, h in crumbs if not (h and "#" in h)]
    bc = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": it} for i, (n, it) in enumerate(bc_items)]}
    webpage = {"@type": "WebPage", "@id": full + "#webpage", "url": full, "name": fm["title"], "description": fm["metaDescription"],
               "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"}, "inLanguage": "en-IN", "dateModified": TODAY}
    graph = [webpage, main_ld, bc]
    fq = faqs(body_md)
    assert fq, f"no FAQ in {f}"
    graph.append({"@type": "FAQPage", "@id": full + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]})
    meta_line = f'Brandvo Digital Co. · {fm["readMinutes"]} min read · Updated 17 Nov 2026' if kind == "article" else None
    main = ('<main id="main">' + hero(crumbs, eyebrow, fm["h1"], meta_line) +
            '<div class="container-x max-w-3xl pb-24"><article class="mt-4"><div class="text-[17px] leading-8 text-white/70">'
            + body + "</div></article>" + aside_html + "</div></main>")
    dest = site / url.strip("/") / "index.html"
    assert not dest.exists() or "build_step6" in dest.read_text(), f"would overwrite {dest}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(make_head(fm["title"], fm["metaDescription"], full, graph) + chrome_top + main + footer_and_end.replace("</body>", "<!-- build_step6 -->\n  </body>", 1))
    new.append((kind, list_title, url, fm["metaDescription"], fm.get("place")))
    print("page", url, len(fq), "faqs")

# ------------------------------------------------ homepage: keyword title and H1 (18 Nov 2026, approved by Hola)
HOME_TITLE = "Best Digital Marketing Agency in Kerala & Kannur | Brandvo Digital Co."
HOME_H1 = "Best Digital Marketing Agency in Kerala &amp; Kannur"
home = site / "index.html"
t = home.read_text()
t = t.replace("Digital Marketing Agency in Kerala | Brandvo Digital Co.", esc(HOME_TITLE).replace("&#x27;", "'"))
old_hero = re.search(r'<p class="eyebrow mb-6 animate-\[fadeUp_\.8s_both\]">Strategy[^<]*</p><h1 (class="h-display[^"]*")>(.*?)</h1>', t, flags=re.S)
if old_hero:
    t = t.replace(old_hero.group(0), f'<h1 class="eyebrow mb-6 animate-[fadeUp_.8s_both]">{HOME_H1}</h1><p {old_hero.group(1)}>{old_hero.group(2)}</p>')
assert t.count("<h1") == 1 and HOME_H1 in t
home.write_text(t)

# ------------------------------------------------ footer locations list (static HTML + bundle)
FOOT_A = "focus-ring rounded text-sm text-white/55 transition-colors hover:text-white"
extra_loc = [("Digital marketing in Thalassery", "/digital-marketing-agency-in-thalassery/"),
             ("Digital marketing in Kasaragod", "/digital-marketing-agency-in-kasaragod/"),
             ("Digital marketing in Kozhikode", "/digital-marketing-agency-in-kozhikode/")]
anchor = f'<li><a href="/digital-marketing-agency-in-payyanur/" class="{FOOT_A}">Digital marketing in Payyanur</a></li>'
add_li = "".join(f'<li><a href="{u}" class="{FOOT_A}">{n}</a></li>' for n, u in extra_loc)
patched = 0
for h in site.rglob("*.html"):
    t = h.read_text()
    if anchor in t and extra_loc[0][1] not in t.split(anchor, 1)[1][:600]:
        h.write_text(t.replace(anchor, anchor + add_li))
        patched += 1
print("footer patched:", patched)

js = next((site / "assets").glob("index-bv*.js"))
s = js.read_text()
old = '["Digital marketing in Payyanur","/digital-marketing-agency-in-payyanur/"],'
if extra_loc[0][1] not in s:
    assert s.count(old) == 1
    s = s.replace(old, old + "".join(f'["{n}","{u}"],' for n, u in extra_loc))
s = s.replace('"Digital Marketing Agency in Kerala | Brandvo Digital Co."', json.dumps(HOME_TITLE))
s = re.sub(r'i\.jsx\("p",\{className:"eyebrow mb-6 animate-\[fadeUp_\.8s_both\]",children:"Strategy[^"]*"\}\),i\.jsxs\("h1",\{className:"h-display animate-\[fadeUp_\.9s_\.08s_both\]',
           lambda m: 'i.jsx("h1",{className:"eyebrow mb-6 animate-[fadeUp_.8s_both]",children:"Best Digital Marketing Agency in Kerala & Kannur"}),'
                     'i.jsxs("p",{className:"h-display animate-[fadeUp_.9s_.08s_both]', s)
assert 'children:"Best Digital Marketing Agency in Kerala & Kannur"' in s and HOME_TITLE in s
js.write_text(s)
newname = "index-bv" + hashlib.sha1(s.encode()).hexdigest()[:8] + ".js"
if newname != js.name:
    js.rename(js.parent / newname)
    for h in site.rglob("*.html"):
        t = h.read_text()
        if js.name in t:
            h.write_text(t.replace("/assets/" + js.name, "/assets/" + newname))
    print("bundle", js.name, "->", newname)

# ------------------------------------------------ links from the existing location pages
def link_block(title, items):
    lis = "".join(f'<li class="{CLS["li"]}"><a href="{u}" class="{CLS["a"]}">{esc(n)}</a></li>' for n, u in items)
    return f'<h2 id="{slugify(title)}" class="{CLS["h2"]}">{esc(title)}</h2><ul class="{CLS["ul"]}">{lis}</ul>'

locs = [(t, u) for k, t, u, d, p in new if k == "location"]
svcs = [(t, u) for k, t, u, d, p in new if k == "service"]
arts = [(t, u) for k, t, u, d, p in new if k == "article"]
inds = [(t + " marketing", u) for k, t, u, d, p in new if k == "industry"]
# All 14 districts, linking the ones that have a page (existing step3 pages + new ones).
have = {u for _, u in locs} | {"/digital-marketing-agency-in-kannur/", "/digital-marketing-agency-in-payyanur/"}
DISTRICTS = [("Kasaragod", "/digital-marketing-agency-in-kasaragod/", "Kasaragod, Kanhangad"),
             ("Kannur", "/digital-marketing-agency-in-kannur/", "Kannur, Payyanur, Thalassery, Taliparamba"),
             ("Wayanad", "/digital-marketing-agency-in-wayanad/", "Kalpetta, Sulthan Bathery"),
             ("Kozhikode", "/digital-marketing-agency-in-kozhikode/", "Kozhikode, Vadakara"),
             ("Malappuram", "/digital-marketing-agency-in-malappuram/", "Manjeri, Perinthalmanna, Tirur"),
             ("Palakkad", "/digital-marketing-agency-in-palakkad/", "Palakkad, Ottapalam"),
             ("Thrissur", "/digital-marketing-agency-in-thrissur/", "Thrissur, Guruvayur, Chalakudy"),
             ("Ernakulam", "/digital-marketing-agency-in-kochi/", "Kochi, Kakkanad, Aluva"),
             ("Idukki", None, "Thodupuzha, Munnar"), ("Kottayam", None, "Kottayam, Pala, Changanassery"),
             ("Alappuzha", None, "Alappuzha, Cherthala"), ("Pathanamthitta", None, "Pathanamthitta, Thiruvalla"),
             ("Kollam", None, "Kollam, Karunagappally"),
             ("Thiruvananthapuram", "/digital-marketing-agency-in-trivandrum/", "Trivandrum, Kazhakkoottam, Neyyattinkara")]
def district_block():
    lis = []
    for d, u, towns in DISTRICTS:
        name = f'<a href="{u}" class="{CLS["a"]}">{d}</a>' if u and u in have else f'<strong class="{CLS["strong"]}">{d}</strong>'
        lis.append(f'<li class="{CLS["li"]}">{name}: {esc(towns)}</li>')
    return (f'<h2 id="areas-we-serve-in-kerala" class="{CLS["h2"]}">Areas we serve in Kerala</h2>'
            f'<p class="{CLS["p"]}">We work with businesses in all 14 districts of Kerala, from our base in Payyanur. Districts with their own page are linked.</p>'
            f'<ul class="{CLS["ul"]}">' + "".join(lis) + "</ul>")
S6 = re.compile(r"<!--s6-->.*?<!--/s6-->", re.S)
for page, title, items in [
    ("digital-marketing-agency-in-kerala", "Industries, services and guides", inds + svcs + arts),
    ("digital-marketing-agency-in-kannur", "Nearby towns and guides", [x for x in locs if any(w in x[1] for w in ("thalassery", "taliparamba", "kasaragod", "kanhangad", "vadakara", "wayanad"))] + arts[:2]),
    ("digital-marketing-agency-in-payyanur", "Nearby towns and more services", [x for x in locs if any(w in x[1] for w in ("taliparamba", "kanhangad", "kasaragod"))] + svcs),
]:
    p = site / page / "index.html"
    t = p.read_text()
    t = S6.sub("", t)
    # drop the unmarked block an earlier run of this script added
    t = re.sub(r'<h2 id="(towns-we-serve-and-guides|nearby-towns-and-guides|nearby-towns-and-more-services)".*?</ul>', "", t, flags=re.S)
    block = (district_block() if page.endswith("kerala") else "") + link_block(title, items)
    assert t.count("</div></article>") == 1
    p.write_text(t.replace("</div></article>", "<!--s6-->" + block + "<!--/s6--></div></article>"))
    print("linked from", page)

# ------------------------------------------------ sitemap + llms.txt
sm = (site / "sitemap.xml").read_text()
add = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for k, t, u, d, p in new if f"{SITE}{u}<" not in sm)
for page in ("digital-marketing-agency-in-kerala", "digital-marketing-agency-in-kannur", "digital-marketing-agency-in-payyanur"):
    sm = re.sub(rf"(<loc>{SITE}/{page}/</loc><lastmod>)[^<]+", rf"\g<1>{TODAY}", sm)
(site / "sitemap.xml").write_text(sm.replace("</urlset>", add + "</urlset>"))

llms = (site / "llms.txt").read_text()
llms = re.sub(r"\n## More locations, services and guides\n.*?(?=\n## Contact)", "", llms, flags=re.S)
llms = llms.replace("\n## Contact", "\n## More locations, services and guides\n\n" +
                    "".join(f"- [{t}]({SITE}{u}): {d}\n" for k, t, u, d, p in new) + "\n## Contact")
if True:
    llms = llms.replace("Serves Payyanur, Kannur, Kasaragod, Kozhikode, Kochi",
                        "Serves Payyanur, Kannur, Thalassery, Taliparamba, Kasaragod, Kanhangad, Vadakara, Kozhikode, Kochi")
    llms = llms.replace("Vadakara, Kozhikode, Kochi and the rest of Kerala", "Vadakara, Kozhikode, Wayanad, Malappuram, Palakkad, Thrissur, Kochi, Thiruvananthapuram and the rest of Kerala")
    (site / "llms.txt").write_text(llms)

manifest = {}
for f in sorted(site.rglob("*")):
    if f.is_file():
        manifest["/" + f.relative_to(site).as_posix()] = hashlib.sha1(f.read_bytes()).hexdigest()
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("new pages:", len(new), "manifest files:", len(manifest))
