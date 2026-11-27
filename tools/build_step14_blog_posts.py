#!/usr/bin/env python3
"""Step 14 (27 Nov 2026): three new guides from the content calendar. Run after step 13.

Usage: python3 tools/build_step14_blog_posts.py site-build content/pages-2026-11-27

Builds static /blog/<slug>/ pages from Markdown (same front matter as step 6 articles), using an
existing static guide as the template so header, footer, aside and styles match. Adds BlogPosting,
WebPage, BreadcrumbList and FAQPage JSON-LD; links each new guide from the related service and
industry pages; adds them to sitemap.xml and llms.txt; rewrites the deploy manifest. Idempotent.
The /blog/ index is rendered by the React bundle and only lists the five original posts, so it is
not changed here.
"""
import hashlib, html, json, re, sys
from pathlib import Path

import markdown

SITE = "https://brandvodigital.com"
site, src = Path(sys.argv[1]), Path(sys.argv[2])
ORG_REF = {"@id": SITE + "/#organization", "@type": "ProfessionalService", "name": "Brandvo Digital Co.", "url": SITE + "/"}
CLS = {
    "h2": "mb-1 mt-14 font-display text-[1.65rem] font-semibold leading-tight tracking-tight text-white sm:text-[2rem]",
    "h3": "mb-1 mt-9 font-display text-xl font-semibold leading-snug text-white",
    "p": "mt-5", "ul": "mt-5 list-disc space-y-2.5 pl-6 marker:text-brand-magenta",
    "ol": "mt-5 list-decimal space-y-2.5 pl-6 marker:font-semibold marker:text-brand-orange",
    "li": "pl-1", "strong": "font-semibold text-white",
    "a": "focus-ring rounded text-white underline decoration-brand-magenta decoration-2 underline-offset-4 transition-colors hover:text-brand-orange",
    # these two are not in the compiled Tailwind CSS, so they carry inline styles
    "blockquote": 'mt-5 pl-5 text-white/80" style="border-left:2px solid rgba(236,31,189,.6);font-style:italic',
    "code": 'rounded" style="background:rgba(255,255,255,.06);padding:2px 6px;font-size:14px;word-break:break-all',
}
esc = lambda s: html.escape(s, quote=True)
ld = lambda o: '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"
slugify = lambda s: re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", s)).lower()).strip("-")


def style(body):
    body = re.sub(r"<h2>(.*?)</h2>", lambda m: f'<h2 id="{slugify(m.group(1))}" class="{CLS["h2"]}">{m.group(1)}</h2>', body)
    body = re.sub(r"<h3>(.*?)</h3>", lambda m: f'<h3 class="{CLS["h3"]}">{m.group(1)}</h3>', body)
    for tag in ["p", "ul", "ol", "li", "strong", "blockquote", "code"]:
        body = body.replace(f"<{tag}>", f'<{tag} class="{CLS[tag]}">')
    body = body.replace(f'<blockquote class="{CLS["blockquote"]}">\n<p class="mt-5">', f'<blockquote class="{CLS["blockquote"]}">\n<p>')
    body = re.sub(r'<a href="(/[^"]*)">', lambda m: f'<a href="{m.group(1)}" class="{CLS["a"]}">', body)
    body = body.replace("<table>", '<div class="mt-7 overflow-x-auto rounded-2xl border border-white/10"><table class="w-full min-w-[560px] border-collapse text-left text-[15px] leading-6">').replace("</table>", "</table></div>")
    body = body.replace("<thead>\n<tr>", '<thead>\n<tr class="bg-white/[0.04]">').replace("<th>", '<th class="px-4 py-3 font-display text-sm font-semibold text-white">')
    body = re.sub(r"<tbody>(.*?)</tbody>", lambda m: "<tbody>" + m.group(1).replace("<tr>", '<tr class="border-t border-white/[0.07]">').replace("<td>", '<td class="px-4 py-3.5 align-top">') + "</tbody>", body, flags=re.S)
    assert "<a href" not in re.sub(r'<a href="[^"]+" (target|class)', "", body), "unstyled link"
    return body


def faqs(md):
    m = re.search(r"^## Frequently asked questions\s*$(.*?)(?=^## |\Z)", md, flags=re.M | re.S)
    out = []
    for q, a in re.findall(r"^### (.+?)\s*\n(.*?)(?=^### |\Z)", m.group(1), flags=re.M | re.S):
        a = re.sub(r"\*\*(.+?)\*\*", r"\1", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a.strip()))
        out.append((q.strip(), " ".join(a.split())))
    return out


tpl = (site / "blog" / "google-business-profile-optimization-kerala" / "index.html").read_text()
head_tpl = tpl[: tpl.index('<div id="root">') + len('<div id="root">')]
rest = tpl[len(head_tpl):]
chrome_top = rest[: rest.index('<main id="main">')]
hero_tpl = rest[rest.index('<main id="main">'): rest.index('<div class="container-x max-w-3xl pb-24">')]
aside_html = rest[rest.index("<aside"): rest.index("</aside>") + len("</aside>")]
footer_and_end = rest[rest.index("<footer"):].replace("<!-- build_step6 -->", "<!-- build_step14 -->")

new = []
for f in sorted(src.glob("*.md")):
    fm_txt, body_md = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(), flags=re.S).groups()
    fm = dict(l.split(": ", 1) for l in fm_txt.splitlines() if ": " in l)
    url, full = fm["url"], SITE + fm["url"]
    crumb = fm["breadcrumb"].split(">")[-1].strip()
    fq = faqs(body_md)
    assert len(fq) >= 3, f
    graph = [
        {"@type": "WebPage", "@id": full + "#webpage", "url": full, "name": fm["title"], "description": fm["metaDescription"],
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#organization"}, "inLanguage": "en-IN", "dateModified": fm["date"]},
        {"@type": "BlogPosting", "@id": full + "#article", "headline": fm["h1"], "description": fm["metaDescription"],
         "datePublished": fm["date"], "dateModified": fm["date"], "inLanguage": "en-IN", "mainEntityOfPage": full,
         "image": SITE + "/og-image.png", "author": ORG_REF, "publisher": ORG_REF, "keywords": fm["primaryKeyword"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": crumb, "item": full}]},
        {"@type": "FAQPage", "@id": full + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]},
    ]
    h = head_tpl
    h = re.sub(r"<title>.*?</title>", "<title>" + esc(fm["title"]) + "</title>", h)
    for attr, val in [('name="description"', fm["metaDescription"]), ('property="og:title"', fm["title"]),
                      ('property="og:description"', fm["metaDescription"]), ('property="og:url"', full)]:
        h, n = re.subn(r"<meta " + attr + r' content="[^"]*" />', f'<meta {attr} content="{esc(val)}" />', h)
        assert n == 1, attr
    for attr, val in [('name="twitter:title"', fm["title"]), ('name="twitter:description"', fm["metaDescription"])]:
        h = re.sub(r"<meta " + attr + r' content="[^"]*" />', f'<meta {attr} content="{esc(val)}" />', h)
    h, n = re.subn(r'<link rel="canonical" href="[^"]*" />', f'<link rel="canonical" href="{full}" />', h)
    assert n == 1
    h, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: ld({"@context": "https://schema.org", "@graph": graph}), h, flags=re.S)
    assert n == 1
    hero = hero_tpl
    hero = re.sub(r'(<li aria-current="page" class="text-white/70">)[^<]*(</li>)', lambda m: m.group(1) + esc(crumb) + m.group(2), hero)
    hero = re.sub(r"(<h1 [^>]*>)[^<]*(</h1>)", lambda m: m.group(1) + esc(fm["h1"]) + m.group(2), hero)
    d = fm["date"].split("-")
    nice = f'{int(d[2])} {["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(d[1])-1]} {d[0]}'
    hero = re.sub(r'(<p class="mt-6 text-sm text-white/50">)[^<]*(</p>)', lambda m: m.group(1) + f'Brandvo Digital Co. · {fm["readMinutes"]} min read · Updated {nice}' + m.group(2), hero)
    body_md = re.sub(r"^# .+\n", "", body_md.lstrip(), count=1)
    body = style(markdown.markdown(body_md, extensions=["tables", "sane_lists"]))
    main = (hero + '<div class="container-x max-w-3xl pb-24"><article class="mt-4"><div class="text-[17px] leading-8 text-white/70">'
            + body + "</div></article>" + aside_html + "</div></main>")
    dest = site / url.strip("/") / "index.html"
    assert not dest.exists() or "build_step14" in dest.read_text(), dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    out = h + chrome_top + main + footer_and_end
    assert out.count("<h1") == 1
    dest.write_text(out)
    new.append((fm["h1"], url, fm["metaDescription"], fm["date"]))
    print("page", url, len(fq), "faqs", len(re.sub("<[^>]+>", " ", body).split()), "words")

# ---------------------------------------------------- links from related static pages
by = {u: t for t, u, _, _ in new}
LINKS = {
    "services/local-seo": ["/blog/how-to-get-more-google-reviews/", "/blog/dental-clinic-marketing-kerala/"],
    "industries/healthcare": ["/blog/dental-clinic-marketing-kerala/", "/blog/how-to-get-more-google-reviews/"],
    "services/lead-generation": ["/blog/whatsapp-lead-tracking/"],
    "services/meta-ads": ["/blog/whatsapp-lead-tracking/"],
    "services/performance-marketing": ["/blog/whatsapp-lead-tracking/"],
    "blog/google-business-profile-optimization-kerala": ["/blog/how-to-get-more-google-reviews/"],
}
S14 = re.compile(r"<!--s14-->.*?<!--/s14-->", re.S)
for page, urls in LINKS.items():
    p = site / page / "index.html"
    t = S14.sub("", p.read_text())
    lis = "".join(f'<li class="{CLS["li"]}"><a href="{u}" class="{CLS["a"]}">{esc(by[u])}</a></li>' for u in urls)
    block = f'<!--s14--><h2 id="guides" class="{CLS["h2"]}">Guides</h2><ul class="{CLS["ul"]}">{lis}</ul><!--/s14-->'
    assert t.count("</div></article>") == 1, page
    p.write_text(t.replace("</div></article>", block + "</div></article>"))
    print("linked from", page)

# ---------------------------------------------------- sitemap + llms.txt
sm = (site / "sitemap.xml").read_text()
add = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{d}</lastmod></url>\n" for _, u, _, d in new if f"{SITE}{u}<" not in sm)
(site / "sitemap.xml").write_text(sm.replace("</urlset>", add + "</urlset>"))
llms = (site / "llms.txt").read_text()
llms = re.sub(r"\n## Guides added November 2026\n.*?(?=\n## )", "", llms, flags=re.S)
block = "\n## Guides added November 2026\n\n" + "".join(f"- [{t}]({SITE}{u}): {d}\n" for t, u, d, _ in new)
assert "\n## Contact" in llms
(site / "llms.txt").write_text(llms.replace("\n## Contact", block + "\n## Contact", 1))

manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
