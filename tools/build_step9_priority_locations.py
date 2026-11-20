#!/usr/bin/env python3
"""Step 9: deepen the four priority location pages (20 Nov 2026). Run after build_step8_linking.py.

Usage: python3 tools/build_step9_priority_locations.py site-build content/pages-2026-11-20

From the Kerala-wide SEO plan (Takees / Moris Media / Sinaura teardown, 20 Nov 2026):
- Rewrites the article body of the Kannur, Payyanur, Kasaragod and Kozhikode pages from
  content/pages-2026-11-20/*.md (more local detail, all service and industry pages linked,
  the Unicorn Bakes result, an honest "no office here" FAQ, links to the guides).
- Updates title, meta description, og tags, WebPage name/description/dateModified and
  rebuilds the FAQPage node from the visible FAQ section, so schema matches the page.
- Shortens the Trivandrum title (was 81 characters).
- Bumps sitemap lastmod for changed pages and regenerates tools/deploy-manifest.json.
Idempotent: re-running gives the same output. Header, hero, aside and footer are untouched.
"""
import hashlib, html, json, re, sys
from pathlib import Path

import markdown

SITE = "https://brandvodigital.com"
TODAY = "2026-11-20"
site, src = Path(sys.argv[1]), Path(sys.argv[2])

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


def style(body):  # same classes as build_step8 so the pages look identical
    body = re.sub(r"<h2>(.*?)</h2>", lambda m: f'<h2 id="{slugify(m.group(1))}" class="{CLS["h2"]}">{m.group(1)}</h2>', body)
    body = re.sub(r"<h3>(.*?)</h3>", lambda m: f'<h3 class="{CLS["h3"]}">{m.group(1)}</h3>', body)
    for tag in ["p", "ul", "ol", "li", "strong"]:
        body = body.replace(f"<{tag}>", f'<{tag} class="{CLS[tag]}">')
    body = re.sub(r'<a href="((?:/|mailto:)[^"]*)">', lambda m: f'<a href="{m.group(1)}" class="{CLS["a"]}">', body)
    body = body.replace("<table>", '<div class="mt-7 overflow-x-auto rounded-2xl border border-white/10"><table class="w-full min-w-[560px] border-collapse text-left text-[15px] leading-6">').replace("</table>", "</table></div>")
    body = body.replace("<thead>\n<tr>", '<thead>\n<tr class="bg-white/[0.04]">').replace("<th>", '<th class="px-4 py-3 font-display text-sm font-semibold text-white">')
    body = re.sub(r"<tbody>(.*?)</tbody>", lambda m: "<tbody>" + m.group(1).replace("<tr>", '<tr class="border-t border-white/[0.07]">').replace("<td>", '<td class="px-4 py-3.5 align-top">') + "</tbody>", body, flags=re.S)
    assert "<a href" not in re.sub(r'<a href="[^"]+" class', "", body), "unstyled link"
    return body


def faqs(md_body):
    m = re.search(r"^## Frequently asked questions\s*$(.*?)(?=^## |\Z)", md_body, flags=re.M | re.S)
    out = []
    for q, a in re.findall(r"^### (.+?)\s*\n(.*?)(?=^### |\Z)", m.group(1), flags=re.M | re.S):
        a = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a.strip())
        a = re.sub(r"\*\*(.+?)\*\*", r"\1", a)
        out.append((q.strip(), " ".join(a.split())))
    return out


def set_head(t, title, desc):
    t = re.sub(r"<title>.*?</title>", "<title>" + esc(title) + "</title>", t, count=1)
    for attr, val in [('name="description"', desc), ('property="og:title"', title), ('property="og:description"', desc),
                      ('name="twitter:title"', title), ('name="twitter:description"', desc)]:
        t = re.sub(r'<meta ' + attr + r' content="[^"]*" />', f'<meta {attr} content="{esc(val)}" />', t, count=1)
    return t


def update_graph(t, url, title, desc, fq):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, flags=re.S)
    data = json.loads(m.group(1))
    nodes = data["@graph"]
    full = SITE + url
    for n in nodes:
        if n.get("@type") in ("WebPage", "CollectionPage", "AboutPage") and n.get("url") == full:
            n.update(name=title, description=desc, dateModified=TODAY)
    nodes[:] = [n for n in nodes if n.get("@type") != "FAQPage"]
    if fq:
        nodes.append({"@type": "FAQPage", "@id": full + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]})
    return t.replace(m.group(0), ld(data), 1)


ART = re.compile(r'(<article class="mt-4"><div class="text-\[17px\] leading-8 text-white/70">).*?(</div></article>)', re.S)
changed = []
for f in sorted(src.glob("*.md")):
    fm_txt, body_md = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(), flags=re.S).groups()
    fm = dict(line.split(": ", 1) for line in fm_txt.splitlines() if ": " in line)
    url = fm["url"]
    page = site / url.strip("/") / "index.html"
    t = page.read_text()
    body = style(markdown.markdown(body_md.strip(), extensions=["tables", "sane_lists"]))
    t, k = ART.subn(lambda m: m.group(1) + body + m.group(2), t, count=1)
    assert k == 1, url
    h1 = re.search(r"<h1 [^>]*>(.*?)</h1>", t).group(1)
    assert html.unescape(h1) == fm["h1"], (url, h1)
    fq = faqs(body_md)
    assert len(fq) >= 4, url
    t = set_head(t, fm["title"], fm["metaDescription"])
    t = update_graph(t, url, fm["title"], fm["metaDescription"], fq)
    page.write_text(t)
    changed.append(url)
    print("page", url, len(re.sub(r"<[^>]+>", " ", body).split()), "words", len(fq), "faqs")

# Trivandrum title: 81 -> 60 characters (Thiruvananthapuram stays in the meta description and body)
p = site / "digital-marketing-agency-in-trivandrum" / "index.html"
t = p.read_text()
new_title = "Digital Marketing Agency in Trivandrum | Brandvo Digital Co."
desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', t).group(1))
t = set_head(t, new_title, desc)
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, flags=re.S)
data = json.loads(m.group(1))
for n in data.get("@graph", []):
    if n.get("@type") == "WebPage":
        n["name"] = new_title
t = t.replace(m.group(0), ld(data), 1)
p.write_text(t)
changed.append("/digital-marketing-agency-in-trivandrum/")

# sitemap lastmod
sm = (site / "sitemap.xml").read_text()
for u in changed:
    loc = f"<loc>{SITE}{u}</loc>"
    assert loc in sm, u
    sm = re.sub(re.escape(loc) + r"<lastmod>[^<]+", loc + f"<lastmod>{TODAY}", sm)
(site / "sitemap.xml").write_text(sm)

# every internal link must resolve
missing = set()
for p in site.rglob("*.html"):
    for href in re.findall(r'href="(/[^"#?]*)"', p.read_text()):
        if href.startswith("/assets/") or "." in href.rsplit("/", 1)[-1] or href in ("/", "/privacy", "/terms"):
            continue
        if not (site / href.strip("/") / "index.html").exists():
            missing.add((href, p.relative_to(site).as_posix()))
assert not missing, sorted(missing)[:20]

manifest = {"/" + f.relative_to(site).as_posix(): hashlib.sha1(f.read_bytes()).hexdigest()
            for f in sorted(site.rglob("*")) if f.is_file()}
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("changed:", len(changed), "manifest files:", len(manifest))
