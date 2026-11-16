#!/usr/bin/env python3
"""Step 3 of the Nov 2026 SEO build.

Usage: python3 tools/build_step3.py site-build prerender.json content/pages

- Injects pre-rendered #root HTML into the homepage, blog and policy pages
  (so crawlers that don't run JavaScript see the content).
- Rewrites the homepage head (title, description, Open Graph, JSON-LD).
- Builds the new static location, service and industry pages from Markdown.
  These pages load only the CSS, never the JS bundle, because the bundle's
  router would replace any unknown path with the homepage.
- Adds a styled 404.html and rewrites sitemap.xml.
"""
import html
import json
import re
import sys
from pathlib import Path

import markdown

SITE = "https://brandvodigital.com"
TODAY = "2026-11-16"
PHONE = "+91 62820 70376"
EMAIL = "info@brandvodigital.com"

out = Path(sys.argv[1])
pre = json.loads(Path(sys.argv[2]).read_text())
pages_dir = Path(sys.argv[3])

BODY_FORM = """    <!-- Static copy of the contact form so Netlify Forms can detect it at deploy time -->
    <form name="contact" data-netlify="true" netlify-honeypot="bot-field" hidden>
      <input type="hidden" name="form-name" value="contact" />
      <input name="bot-field" />
      <input name="name" /><input name="email" /><input name="phone" />
      <input name="company" /><input name="service" /><textarea name="message"></textarea>
    </form>"""

ORG = {
    "@type": "ProfessionalService",
    "@id": SITE + "/#organization",
    "name": "Brandvo Digital Co.",
    "alternateName": "Brandvo Digital",
    "description": "Performance-driven digital marketing and creative agency based in Payyanur, Kerala.",
    "url": SITE + "/",
    "logo": SITE + "/favicon-512.png",
    "image": SITE + "/og-image.png",
    "email": EMAIL,
    "telephone": PHONE,
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Payyanur",
        "addressRegion": "Kerala",
        "addressCountry": "IN",
    },
    "areaServed": [
        {"@type": "City", "name": "Payyanur"},
        {"@type": "AdministrativeArea", "name": "Kannur district"},
        {"@type": "State", "name": "Kerala"},
    ],
    "founder": [
        {"@type": "Person", "name": "Abhishek"},
        {"@type": "Person", "name": "Sajeer Angillath"},
    ],
    "sameAs": [
        "https://www.instagram.com/brandvo_digital_co/",
        "https://www.facebook.com/p/Brandvo-Digital-Co-61590207584449/",
        "https://www.linkedin.com/company/144779128/",
    ],
    "knowsAbout": [
        "Social media marketing", "Meta Ads", "Performance marketing",
        "Branding", "Creative design", "Web design and development",
    ],
}


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def esc(s):
    return html.escape(s, quote=True)


def inject_root(path, root_html):
    t = path.read_text()
    new, n = re.subn(r'<div id="root">.*?</div>\n  </body>', lambda m: '<div id="root">' + root_html + "</div>\n  </body>", t, flags=re.S)
    assert n == 1, path
    path.write_text(new)


# ---------------------------------------------------------------- homepage head
home = out / "index.html"
t = home.read_text()
home_title = "Digital Marketing Agency in Kerala | Brandvo"
home_desc = ("Payyanur-based digital marketing agency helping Kerala businesses get more leads "
             "with social media marketing, Meta Ads, branding and web design.")
t = re.sub(r"<title>.*?</title>", "<title>" + esc(home_title) + "</title>", t)
t = re.sub(r'<meta name="description" content="[^"]*" />', '<meta name="description" content="' + esc(home_desc) + '" />', t)
t = re.sub(r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="' + esc(home_title) + '" />', t)
t = re.sub(r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="' + esc(home_desc) + '" />', t)
t = t.replace('<meta property="og:site_name" content="Brandvo Digital Co." />',
              '<meta property="og:site_name" content="Brandvo Digital Co." />\n    <meta property="og:locale" content="en_IN" />')
graph = {"@context": "https://schema.org", "@graph": [
    dict(ORG, serviceType=["Social Media Marketing", "Meta Ads", "Performance Marketing", "Branding", "Creative Design", "Web Design & Development"]),
    {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Brandvo Digital Co.",
     "publisher": {"@id": SITE + "/#organization"}, "inLanguage": "en-IN"},
]}
new_t, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: ld(graph), t, flags=re.S)
assert n == 1
home.write_text(new_t)

# ------------------------------------------------- prerendered SPA routes
inject_root(home, pre["/"]["root"])
inject_root(out / "blog" / "index.html", pre["/blog/"]["root"])
for route, v in pre.items():
    if route.startswith("/blog/") and route != "/blog/":
        inject_root(out / route.strip("/") / "index.html", v["root"])

# privacy/terms: new files built from the homepage shell, own title + canonical
shell = (out / "index.html").read_text()
for slug, desc in [("privacy", "How Brandvo Digital Co. collects, uses and protects information submitted through brandvodigital.com."),
                   ("terms", "Terms of use for brandvodigital.com, the website of Brandvo Digital Co.")]:
    v = pre["/" + slug]
    p = shell
    p = re.sub(r"<title>.*?</title>", "<title>" + esc(v["title"]) + "</title>", p)
    p = re.sub(r'<meta name="description" content="[^"]*" />', '<meta name="description" content="' + esc(desc) + '" />', p)
    p = re.sub(r'\s*<meta name="keywords" content="[^"]*" />', "", p)
    p = p.replace('<link rel="canonical" href="https://brandvodigital.com/" />', f'<link rel="canonical" href="{SITE}/{slug}" />')
    p = re.sub(r'<meta property="og:title" content="[^"]*" />', '<meta property="og:title" content="' + esc(v["title"]) + '" />', p)
    p = re.sub(r'<meta property="og:description" content="[^"]*" />', '<meta property="og:description" content="' + esc(desc) + '" />', p)
    p = p.replace('<meta property="og:url" content="https://brandvodigital.com/" />', f'<meta property="og:url" content="{SITE}/{slug}" />')
    p = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: ld({"@context": "https://schema.org", "@type": "WebPage", "name": v["title"], "url": f"{SITE}/{slug}", "isPartOf": {"@id": SITE + "/#website"}}), p, flags=re.S)
    p = re.sub(r'<div id="root">.*?</div>\n  </body>', lambda m: '<div id="root">' + v["root"] + "</div>\n  </body>", p, flags=re.S)
    (out / f"{slug}.html").write_text(p)

# ---------------------------------------------- static page chrome (no bundle)
ref = pre["/blog/best-digital-marketing-agency-in-kannur/"]["root"]
chrome_top = ref[: ref.index('<main id="main">')]
chrome_footer = ref[ref.index("<footer"):]
aside_html = ref[ref.index("<aside"): ref.index("</aside>") + len("</aside>")]
aside_html = aside_html.replace("Ready to put this into practice?", "Talk to a Payyanur team about your growth")
assert "Talk to a Payyanur team" in aside_html

MENU_JS = """<script>
(function(){
  var b=document.querySelector('button[aria-controls="mobile-menu"]'),m=document.getElementById('mobile-menu'),h=document.querySelector('body>div#root>header');
  function sc(){var s=window.scrollY>24;['bg-ink-950/80','backdrop-blur-xl','border-white/[0.06]'].forEach(function(c){h.classList.toggle(c,s)});h.classList.toggle('border-transparent',!s);}
  if(h){window.addEventListener('scroll',sc,{passive:true});sc();}
  if(!b||!m)return;var sp=b.querySelectorAll('span.absolute'),li=m.querySelectorAll('li');
  function set(o){b.setAttribute('aria-expanded',o?'true':'false');b.setAttribute('aria-label',o?'Close menu':'Open menu');
    ['visible','opacity-100'].forEach(function(c){m.classList.toggle(c,o)});['invisible','pointer-events-none','opacity-0'].forEach(function(c){m.classList.toggle(c,!o)});
    li.forEach(function(l,i){l.style.transitionDelay=o?(80+i*50)+'ms':'0ms';['translate-y-0','opacity-100'].forEach(function(c){l.classList.toggle(c,o)});['translate-y-4','opacity-0'].forEach(function(c){l.classList.toggle(c,!o)});});
    if(sp.length===3){sp[0].classList.toggle('rotate-45',o);sp[0].classList.toggle('-translate-y-1.5',!o);sp[1].classList.toggle('opacity-0',o);sp[2].classList.toggle('-rotate-45',o);sp[2].classList.toggle('translate-y-1.5',!o);}
    document.body.style.overflow=o?'hidden':'';}
  b.addEventListener('click',function(){set(b.getAttribute('aria-expanded')!=='true')});
  m.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')set(false)});
})();
</script>"""

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
    out_ = []
    for q, a in re.findall(r"^### (.+?)\s*\n(.*?)(?=^### |\Z)", m.group(1), flags=re.M | re.S):
        ans = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a.strip())
        ans = re.sub(r"\*\*(.+?)\*\*", r"\1", ans)
        out_.append((q.strip(), " ".join(ans.split())))
    return out_


def page_head(title, desc, url, extra_ld, robots=None):
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}" />
{'    <meta name="robots" content="' + robots + '" />' + chr(10) if robots else ''}    <meta name="theme-color" content="#06050b" />
{'    <link rel="canonical" href="' + url + '" />' + chr(10) if url else ''}    <link rel="icon" type="image/png" href="/favicon.png" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Brandvo Digital Co." />
    <meta property="og:locale" content="en_IN" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(desc)}" />
{'    <meta property="og:url" content="' + url + '" />' + chr(10) if url else ''}    <meta property="og:image" content="{SITE}/og-image.png" />
    <meta name="twitter:card" content="summary_large_image" />

{extra_ld}
    <link rel="stylesheet" crossorigin href="/assets/index-MyKFRt77.css">
  </head>
  <body>
{BODY_FORM}
    <div id="root">"""


PAGE_END = "</div>\n" + MENU_JS + "\n  </body>\n</html>\n"


def hero(crumbs, eyebrow, h1, lead=None):
    items = []
    for i, (name, href) in enumerate(crumbs):
        if i:
            items.append('<li aria-hidden="true">/</li>')
        if href:
            items.append(f'<li><a href="{href}" class="focus-ring rounded hover:text-white">{esc(name)}</a></li>')
        else:
            items.append(f'<li aria-current="page" class="text-white/70">{esc(name)}</li>')
    lead_html = f'<p class="mt-6 text-lg leading-relaxed text-white/65">{lead}</p>' if lead else ""
    return ('<header class="relative isolate overflow-x-clip pt-[72px]"><div aria-hidden="true" class="pointer-events-none absolute inset-0 -z-10">'
            '<div class="absolute -right-32 -top-40 h-[560px] w-[560px] rounded-full bg-brand-magenta/20 blur-[140px]"></div>'
            '<div class="absolute left-[4%] top-[30%] h-[380px] w-[380px] rounded-full bg-brand-indigo/25 blur-[130px]"></div></div>'
            '<div class="container-x max-w-3xl pb-10 pt-14 sm:pt-20"><nav aria-label="Breadcrumb" class="text-xs text-white/45">'
            f'<ol class="flex flex-wrap items-center gap-x-2 gap-y-1">{"".join(items)}</ol></nav>'
            f'<p class="eyebrow mt-8">{esc(eyebrow)}</p>'
            f'<h1 class="h-display mt-4 text-[clamp(2rem,4.6vw,3.4rem)] leading-[1.08]">{esc(h1)}</h1>{lead_html}</div></header>')


SECTION_CRUMB = {"Services": "/#services", "Industries": None}
new_urls = []
for f in sorted(pages_dir.glob("*.md")):
    raw = f.read_text()
    fm_txt, body_md = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, flags=re.S).groups()
    fm = dict(line.split(": ", 1) for line in fm_txt.splitlines() if ": " in line)
    body_md = re.sub(r"^# .+\n", "", body_md.lstrip(), count=1)  # H1 lives in the hero
    url = fm["url"]
    full = SITE + url
    new_urls.append(url)
    crumb = fm.get("breadcrumb", "")
    parts = [p.strip() for p in crumb.split(">")] if ">" in crumb else []
    if parts and parts[0] == "Services":
        eyebrow, crumbs = "Services", [("Home", "/"), ("Services", "/#services"), (parts[-1], None)]
    elif parts and parts[0] == "Industries":
        eyebrow, crumbs = "Industries", [("Home", "/"), (parts[-1], None)]
    else:
        place = re.search(r"in-(\w+)/$", url).group(1).title()
        eyebrow, crumbs = f"Digital marketing · {place}", [("Home", "/"), (f"Digital marketing in {place}", None)]
    body = style(markdown.markdown(body_md, extensions=["tables", "sane_lists"]))
    bc = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": crumbs[-1][0], "item": full}]}
    webpage = {"@type": "WebPage", "@id": full + "#webpage", "url": full, "name": fm["title"], "description": fm["metaDescription"],
               "isPartOf": {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Brandvo Digital Co."},
               "about": {"@id": SITE + "/#organization"}, "inLanguage": "en-IN", "dateModified": TODAY}
    service = {"@type": "Service", "name": fm["h1"], "serviceType": fm.get("primaryKeyword", fm["h1"]).title(),
               "provider": ORG, "url": full,
               "areaServed": ({"@type": "City", "name": "Payyanur"} if "payyanur" in url else
                              {"@type": "AdministrativeArea", "name": "Kannur district"} if "kannur" in url else
                              {"@type": "State", "name": "Kerala"})}
    graph = [webpage, service, bc]
    fq = faqs(body_md)
    if fq:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]})
    head = page_head(fm["title"], fm["metaDescription"], full, "    " + ld({"@context": "https://schema.org", "@graph": graph}))
    main = ('<main id="main">' + hero(crumbs, eyebrow, fm["h1"]) +
            '<div class="container-x max-w-3xl pb-24"><article class="mt-4"><div class="text-[17px] leading-8 text-white/70">'
            + body + "</div></article>" + aside_html + "</div></main>")
    dest = out / url.strip("/") / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(head + chrome_top + main + chrome_footer + PAGE_END)

# -------------------------------------------------------------------- 404 page
nf_main = ('<main id="main">' + hero([("Home", "/"), ("Page not found", None)], "Error 404", "This page doesn't exist")
           + '<div class="container-x max-w-3xl pb-24 text-[17px] leading-8 text-white/70"><p>The link may be old or mistyped. '
           'Here are the pages most people are looking for:</p><ul class="' + CLS["ul"] + '">'
           + "".join(f'<li class="pl-1"><a class="{CLS["a"]}" href="{h}">{n}</a></li>' for n, h in [
               ("Home", "/"), ("Digital marketing in Kerala", "/digital-marketing-agency-in-kerala/"),
               ("Social media marketing", "/services/social-media-marketing/"), ("Meta Ads", "/services/meta-ads/"),
               ("Blog", "/blog/"), ("Contact us", "/#contact")])
           + "</ul></div></main>")
(out / "404.html").write_text(page_head("Page not found | Brandvo Digital Co.", "This page could not be found on brandvodigital.com.", None, "", robots="noindex")
                              + chrome_top + nf_main + chrome_footer + PAGE_END)

# -------------------------------------------------------------------- sitemap
urls = [("/", TODAY)] + [(u, TODAY) for u in new_urls] + [
    ("/blog/", "2026-10-30")] + [(r, "2026-10-30") for r in pre if r.startswith("/blog/") and r != "/blog/"] + [
    ("/privacy", None), ("/terms", None)]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, d in urls:
    sm.append(f"  <url><loc>{SITE}{u}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "") + "</url>")
sm.append("</urlset>")
(out / "sitemap.xml").write_text("\n".join(sm) + "\n")
print("new pages:", new_urls)
