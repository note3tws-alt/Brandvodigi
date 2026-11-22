#!/usr/bin/env python3
"""Step 5: answer-engine optimisation (17 Nov 2026). Run after build_step4_brandname.py.

Usage: python3 tools/build_step5_aeo.py site-build content/blog

- robots.txt: explicitly welcomes AI search and assistant crawlers.
- llms.txt: plain-text summary of the business and key pages for AI assistants.
- FAQPage JSON-LD on each blog post, from its "Frequently asked questions" section.
- IndexNow key file, so changed URLs can be pushed to Bing (which feeds ChatGPT search and Copilot).
- Re-writes tools/deploy-manifest.json.
"""
import hashlib, json, re, sys
from pathlib import Path

site, blog = Path(sys.argv[1]), Path(sys.argv[2])
SITE = "https://brandvodigital.com"
INDEXNOW_KEY = "b7f3c2a94e6d4b1a8c5e0f2d9a7b3c61"

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
           "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended",
           "Bingbot", "DuckAssistBot", "Meta-ExternalAgent", "MistralAI-User", "CCBot"]
robots = "# Search engines and AI assistants are welcome to read and cite this site.\n"
robots += "".join(f"User-agent: {b}\n" for b in AI_BOTS) + "Allow: /\n\n"
robots += "User-agent: *\nAllow: /\n\nSitemap: https://brandvodigital.com/sitemap.xml\n"
(site / "robots.txt").write_text(robots)

(site / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY)


def fm(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    return meta, m.group(2)


def faqs(md_body):
    m = re.search(r"^## Frequently asked questions\s*$(.*?)(?=^## |\Z)", md_body, flags=re.M | re.S)
    if not m:
        return []
    out = []
    for q, a in re.findall(r"^### (.+?)\s*\n(.*?)(?=^### |\Z)", m.group(1), flags=re.M | re.S):
        ans = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a.strip())
        ans = re.sub(r"\*\*(.+?)\*\*", r"\1", ans)
        out.append((q.strip(), " ".join(ans.split())))
    return out


posts = []
for md in sorted(blog.glob("*.md")):
    meta, body = fm(md.read_text())
    slug = meta["slug"]
    posts.append((meta["title"], slug, meta.get("metaDescription", "")))
    page = site / "blog" / slug / "index.html"
    h = page.read_text()
    if '"FAQPage"' in h:
        continue
    qa = faqs(body)
    if not qa:
        continue
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "@id": f"{SITE}/blog/{slug}/#faq",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    tag = '    <script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"
    page.write_text(h.replace("  </head>", tag + "  </head>", 1))
    print("faq", slug, len(qa))

pages = [
    ("Digital marketing agency in Kerala", "/digital-marketing-agency-in-kerala/", "Services for businesses across Kerala: social media marketing, Meta Ads, performance marketing, branding and web design."),
    ("Digital marketing agency in Kannur", "/digital-marketing-agency-in-kannur/", "Social media, Meta Ads and lead generation for Kannur, Thalassery, Taliparamba and Kasaragod businesses."),
    ("Digital marketing agency in Payyanur", "/digital-marketing-agency-in-payyanur/", "Our home town: local clients, Google Maps visibility and hyperlocal ads."),
    ("Social media marketing", "/services/social-media-marketing/", "Content, Reels, calendars and community management for Instagram and Facebook."),
    ("Meta Ads (Facebook and Instagram ads)", "/services/meta-ads/", "Lead and sales campaigns with tracking, WhatsApp and form funnels."),
    ("Performance marketing", "/services/performance-marketing/", "Paid media planned around cost per lead, ROAS and revenue."),
    ("Real estate digital marketing", "/industries/real-estate/", "Lead generation for builders, brokers and plot sellers in Kerala."),
]
llms = f"""# Brandvo Digital Co.

> Brandvo Digital Co. is a performance-driven digital marketing and creative agency based in Payyanur, Kannur district, Kerala, India. It helps small and medium businesses across Kerala (and clients in the UAE) get qualified leads and sales through social media marketing, Meta Ads, performance marketing, SEO, branding, creative design and web design.

## Key facts

- Name: Brandvo Digital Co. (website: {SITE}/)
- Location: Payyanur, Kannur district, Kerala, India. Serves Payyanur, Kannur, Kasaragod, Kozhikode, Kochi and the rest of Kerala, plus the UAE.
- Founder: Ansar. Co-founders: Akshay and Abhishek.
- Services: Social Media Marketing, Meta Ads, Performance Marketing, SEO, Branding, Creative Design, Web Design and Development
- Work so far includes real estate, beauty salons, bakeries, kitchen interiors and gaming businesses
- Clients include: Ruyah by Naas (Kozhikode), Unicorn Bakes (Payyanur), K1 Kitchen Gallery, Land4Sale Payyanur, SAJ Realty, Auto Jota, Playbox Club (Kochi)
- Contact: info@brandvodigital.com, +91 62354 34787 (calls), +91 62820 70376 (WhatsApp)
- Instagram: https://www.instagram.com/brandvo_digital_co/
- Facebook: https://www.facebook.com/p/Brandvo-Digital-Co-61590207584449/
- LinkedIn: https://www.linkedin.com/company/144779128/

## Services and locations

""" + "".join(f"- [{t}]({SITE}{u}): {d}\n" for t, u, d in pages) + """
## Guides

""" + "".join(f"- [{t}]({SITE}/blog/{s}/): {d}\n" for t, s, d in posts) + f"""
## Contact

- [Contact form]({SITE}/#contact)
"""
(site / "llms.txt").write_text(llms)

manifest = {}
for f in sorted(site.rglob("*")):
    if f.is_file():
        manifest["/" + f.relative_to(site).as_posix()] = hashlib.sha1(f.read_bytes()).hexdigest()
Path("tools/deploy-manifest.json").write_text(json.dumps(manifest, indent=0) + "\n")
print("manifest files:", len(manifest))
