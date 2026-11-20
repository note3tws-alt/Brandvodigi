# Brandvo Digital Co.: Kerala-wide SEO strategy (Takees, Moris Media, Sinaura)

Prepared 20 Nov 2026. Builds on the Phase 1 plan of 19 Nov (`seo-2026-11/kerala-seo-phase1-findings-and-plan.md`), which is not repeated here. Read this as the next layer: three new competitors, an updated audit, the Kerala-wide architecture, and what was implemented today.

Files in this folder:

- `kerala-wide-seo-strategy-takees-moris-sinaura.md` (this document: items 1 and 3 to 10)
- `brandvo-kerala-keyword-database-v3.csv` (item 2: 793 keywords, 49 towns, 14 districts)
- `content-calendar-dec-2026-feb-2027.csv` (item 7 as a sheet)
- Monthly report template: `seo-2026-11/brandvo-monthly-seo-report-template.csv` (unchanged; additions in section 11)

---

## 0. Summary

**What the three competitors teach us.**

- **Takees** ranks #1 for "digital marketing agency kannur" with a homepage whose title and H1 say exactly that, a DR of 25, a physical Kannur address (Mele Chovva), a named founder, 32 client logos and listings on Clutch, DesignRush, GoodFirms and TechBehemoths. It does not win on content: it has only two city pages (Bangalore and a generic Kochi page), no Kozhikode page, and no case studies with numbers.
- **Moris Media** ranks #7 for the same term with a programmatic page that has about 13 H1s, no Kannur address, no local clients, and US phone numbers. It ranks on domain strength (DR 37) and sheer volume, with what looks like tens of thousands of city × service × country pages, some with the wrong country in the URL. This is the model *not* to copy. Google's scaled-content and doorway policies target exactly this, and it gives Brandvo nothing that would survive a core update.
- **Sinaura** wins in the Kannur **map pack**, not the organic results. It has a real office (3rd floor, Amenity Center, University Complex, Thavakkara, Kannur), a Google Maps embed, 14 client logos and a claimed 18–19 years of founder experience. Its site is technically weak: wrong canonicals, blog posts titled just "sinaura", a typo slug in the sitemap, and no location pages at all.

**The honest read.** Brandvo Digital Co. already has better on-page SEO than all three: 15 unique location pages, service and industry pages, schema that matches visible content, a real case study with numbers. What Brandvo lacks is **off-page trust**: Domain Rating 0 against 25–37, no Google Business Profile in the map pack, and no directory profiles. Publishing more pages will not close that gap. Reviews, a verified GBP, citations and genuine links will.

**What was implemented today** (branch `claude/project-thread-39x7zu`, not deployed):

- The four priority location pages (Kannur, Payyanur, Kasaragod, Kozhikode) were deepened with local market detail, every relevant service and industry page linked, the Unicorn Bakes result, and an honest "do you have an office here?" FAQ. Kannur went from ~560 to ~1,420 words, and now has sections for Mattannur, Iritty and Kuthuparamba.
- FAQ schema was rebuilt from the visible FAQs, titles and meta descriptions were tightened, and the Trivandrum title was cut from 81 to 60 characters.
- This sits on top of the 19 Nov work (hubs, About, Local SEO and Lead Generation pages, footer, breadcrumbs), which **is still not live**. As of today the live site's footer is the old short one, and `/services/`, `/about/` and `/services/local-seo/` do not load.

**Decisions needed from you** (also at the end):

1. Deploy the 19 Nov and 20 Nov batches together (one Netlify deploy).
2. Confirm or correct the homepage stats ("40+ clients", "1200+ campaigns", "18K+ leads", "₹1Cr+ revenue"). They are on the site today, but no record of them is in project notes.
3. Set up the Google Business Profile (a service-area profile if there is no office customers visit).
4. Say whether Google Ads, content marketing and video are sold, before those service pages are built.

---

## 1. Competitor SEO comparison

### 1.1 Data sources and what could not be checked

| Source | Used for | Limit |
| --- | --- | --- |
| Direct page fetches, 20 Nov 2026 | Titles, H1–H3, copy, sitemaps, NAP, claims | Raw HTML not visible, so JSON-LD presence on competitor pages is **unverified** |
| Ahrefs `public-domain-rating-free` (20 Nov) | Domain Rating | The free plan gives no backlinks, referring domains, keywords or volumes |
| Google SERP from your browser, 17 Nov 2026 (in project notes) | Rankings for "digital marketing agency kannur" | Personalised to your location. **Not re-checked today**, because no Chrome or built-in browser was connected to this session |
| Web search (US index), 20 Nov | Directory and citation footprint | Not Google India; used only as evidence that profiles exist |
| Search Console / GA4 | — | **Not accessed.** No numbers in this report come from them |

### 1.2 Side-by-side

| | Takees (takees.in) | Moris Media (Kannur page) | Sinaura (sinaura.in) | Brandvo Digital Co. |
| --- | --- | --- | --- | --- |
| DR (Ahrefs, 20 Nov) | 25 | 37 | 27 | 0 |
| Observed Google rank, "digital marketing agency kannur" (17 Nov) | #1 organic | #7 organic | Map pack (top 3) | Not in top 20 |
| Physical address | Mele Chovva, Kannur + UB City, Bangalore | None on page; homepage targets San Francisco | Thavakkara, Kannur | Payyanur (no street address published) |
| Platform | Mixed: custom build + WordPress (Bangalore) | Custom app, programmatic pages | Custom PHP-style, server-rendered | Static HTML on Netlify (prerendered) |
| Sitemap URLs | 24 | ~111 child sitemaps; likely tens of thousands of URLs (not counted) | 15 | 44 (38 live) |
| Location pages | 2 (Bangalore, Kochi) | Programmatic city pages across countries | 0 | 15 live (Kerala + 14) |
| Service pages | 1 hub with #anchors; a few Bangalore service pages | Many, programmatic | 6 thin pages, 3 missing from sitemap | 10 built (8 live) |
| Homepage title | "Digital Marketing Agency in Kannur \| Takees Marketing" | "…PR and Strategic Marketing Agency in San Francisco" | "Best Digital Marketing Agency in Kerala" | "Best Digital Marketing Agency in Kerala & Kannur \| Brandvo Digital Co." (in the build; see audit C3) |
| H1 hygiene | 1 per page (Bangalore repeats H1 as H2) | ~13 H1s on the Kannur page | 1 per page, 2 on blog posts | 1 per page |
| FAQs | 5 on homepage, 8 on Bangalore | None seen | None | 4–6 on every money page |
| Case studies with numbers | None | Unsourced ("1000% more ROI") | None ("+145% growth", unsourced) | Unicorn Bakes: ₹8L ad spend → ₹95L sales |
| Testimonials | None seen | None seen | None | 2 named client quotes |
| Founder / E-E-A-T | Named founder (Akhinil Thabraiz), LinkedIn, founded 2023 | Conflicting (8 vs 10+ years) | Unnamed founder, "18+ / 19 years" | Founders named in schema and About (About not live yet) |
| Blog | 13 posts, news-style (Instagram/Google updates), mostly not local | ~38 topic sitemaps, many unrelated to marketing | 4 posts, last Jan 2026, generic | 9 guides, Kerala-specific |
| Directory footprint | Clutch, DesignRush, GoodFirms, TechBehemoths, syncgtm | Not checked | Not checked | None found |
| Notable technical faults | Two URL families, inconsistent footer links, alt-text typos, bulk-set lastmod | Wrong country tags in URLs, og:url points to homepage, Bingbot blocked in robots.txt | Wrong canonical on posts, http canonicals, generic post titles, typo slug | No major faults in the build; live site is behind the build |

### 1.3 Takees: how it targets Kerala cities

**What is genuinely working**

- **Exact-match homepage.** The title, H1 ("Digital Marketing Agency in Kannur and Bangalore") and an H2 with "Best Digital Marketing Agency in Kannur" all sit on the domain's strongest page, which collects the internal links.
- **Real local entity.** A Kannur street address, a named founder with LinkedIn, and 32 client logos make the business easy for Google to trust and connect to Kannur.
- **Directory citations.** Profiles on Clutch, DesignRush, GoodFirms and TechBehemoths show up for Kannur agency searches. They give Takees links, brand mentions and a presence in those directory listings.
- **Fresh blog activity.** It posts about Google and Instagram updates (latest: November 2026 core update). The posts are not local, but they keep the site crawled.

**What is weak**

- Only two location pages. The "Kerala cities" strategy is mostly the homepage plus Kochi. Kozhikode is a footer anchor to the contact page, not a page.
- The Kochi page is generic. It names no Kochi areas, clients or landmarks, and says the head office is in Kannur.
- No case studies with numbers. Claims such as "Page #1 Google Rankings Achieved" name no keyword or client.
- Messy URL structure: WordPress and non-WordPress slugs, and footer links to `/kochi` and `/bangalore` that are not in the sitemap.

**What Brandvo Digital Co. can do better**

- Outrank its thin Kochi page with Brandvo's existing Kochi page plus Playbox Club proof.
- Match the homepage signal (done in the build: title and H1 now lead with Kerala and Kannur) and push internal links from every page to the Kannur page with "digital marketing agency in Kannur" anchors (done through the footer in the 19 Nov batch).
- Get the same directory profiles, with the case study attached. Takees has none to show there.

### 1.4 Moris Media: how it builds location ranking pages

**What is working**

- Domain strength (DR 37) and crawl volume mean even weak pages get indexed and rank in thin local SERPs like Kannur's.
- The URL and title contain the exact phrase ("best digital marketing agency… kannur").

**What is weak, and risky**

- The Kannur page has no Kannur address, client, landmark or industry. "Kannur" is pasted into stacked H1s such as "Moris Media's No. 1 PR Agency in Kannur in 2026".
- The sitemap shows city × service × country combinations with wrong countries (Delhi tagged as Iraq, Ismailia as Iran). This is scaled, low-value content of the kind Google's spam policies name.
- The homepage targets San Francisco. The Kannur page shows a US phone number. There is no coherent local entity.
- Unsourced "No. 1" and "award-winning" claims with no awarding body.
- robots.txt blocks Bingbot entirely, which also hides it from Bing-powered AI answers.

**What Brandvo Digital Co. should take from it:** only that exact-match phrases in titles still matter in thin local SERPs. Everything else is a warning. Brandvo should not build city pages it cannot back with real local content, and it should not use "No. 1" or "award-winning" without a source.

### 1.5 Sinaura: how it builds local authority

**What is working**

- **Map pack presence.** A real Kannur office at Thavakkara, a Maps embed on the contact page, and (by inference from the 17 Nov map pack) a verified GBP with reviews. For "near me" and "in Kannur" searches, this is worth more than any page.
- Consistent NAP in the footer of every page.
- Kerala in the homepage title and the services H1.

**What is weak**

- No location pages and almost no content (services page ~200 words, about ~250).
- Broken technical basics: blog canonicals point to a non-existent `/blog_read`, mixed http/https canonicals, blog posts titled "sinaura", a keyword-stuffed meta keywords tag, and service pages missing from the sitemap.
- No testimonials, case studies or named team; experience claims conflict (18+ vs 19 years).
- The blog is stale (last post Jan 2026).

**What Brandvo Digital Co. can do better**

- Its organic content already beats Sinaura's. The gap is the map pack: a verified GBP plus reviews from Brandvo's existing clients is the single highest-leverage local action.
- Sinaura is 40–45 km from Payyanur. In the Payyanur map pack (13–24 reviews per competitor on 16 Nov) Brandvo can realistically win; in Kannur town it will take a stronger review base.

### 1.6 Rankings and indexing: what is validated and what is not

- **Validated (17 Nov, your browser):** Takees #1 and Moris Media #7 organic, Sinaura in the map pack, Brandvo not in the top 20, for "digital marketing agency kannur".
- **Validated (20 Nov):** the competitor pages exist and are served with self-referencing canonicals (except Sinaura's blog). Brandvo's Kannur, Kasaragod and case study pages return 200 with full content.
- **Not validated today:** current positions, competitor indexed page counts (needs Google `site:` checks in a browser), backlink lists (needs a paid Ahrefs plan), Core Web Vitals (the PageSpeed API quota was exhausted on 16 Nov, and there is likely too little traffic for field data).

---

## 2. Keyword research spreadsheet

File: `brandvo-kerala-keyword-database-v3.csv` (793 rows). It extends v2 (594 rows); nothing is invented.

**What changed from v2**

- Four new patterns for all 49 towns: "best digital marketing agency in {city}", "seo agency in {city}", "social media management company in {city}", "performance marketing agency in {city}" (196 rows).
- Mattannur added (a section on the Kannur page, not its own page).
- Statuses refreshed for pages built on 19–20 Nov (36 rows).
- A `CompetitorEvidence` column for Kannur rows, carrying the 17 Nov SERP observation.
- `V3Change` marks every new or changed row.

**Search volume and difficulty are "Unavailable".** The Ahrefs connector is on the free plan (rechecked today), and Search Console data was not accessed. Priorities are therefore based on commercial intent, competition seen in the SERP, Brandvo's proof in each place, and how close it is to Payyanur. Not on volume.

**How to fill the gap (cheap and honest):**

1. After the deploy, export Search Console queries per page every month. That is real demand for Brandvo specifically.
2. Google Keyword Planner via a Google Ads account (free) gives volume ranges for Kerala and district targeting.
3. Google autocomplete order for Kerala agency terms (16 Nov) already ranked demand as Kochi > Kerala > Calicut > Thrissur > Kannur > Trivandrum.

**Priority tiers**

| Tier | Keywords | Page |
| --- | --- | --- |
| P1 (134 rows) | Kerala head terms; Kannur, Payyanur, Kasaragod, Kozhikode × digital marketing / SEO / social media / website; Meta Ads Kerala; SEO and SMM Kerala | Existing location and service pages |
| P2 (173) | Metro service terms (Kochi, Trivandrum, Thrissur), "best … in {town}" for home towns, lead generation, local SEO, real estate leads | Existing pages; service × city pages only where there is proof |
| P3 (430) | Small-town service combinations, branding/advertising in towns | Sections on district pages and service pages; no new pages |
| Blocked (48) | Google Ads × city | Waits for confirmation that Google Ads is sold |
| Watchlist (8) | Malayalam / Manglish queries | Do not target until Search Console shows impressions |

**Cannibalisation rules built into the sheet**

- "seo agency" = "seo company"; "social media management company" = "social media marketing agency". One page each.
- "performance marketing agency in {town}" goes to `/services/performance-marketing/`, never a new city page.
- The Kannur blog guide (`/blog/best-digital-marketing-agency-in-kannur/`) is the informational "how to choose" piece. The Kannur location page is the commercial target. Check in Search Console after the deploy that Google keeps them apart. If both get impressions for the same query, retitle the blog post to "How to Choose a Digital Marketing Agency in Kannur".

---

## 3. Brandvo website SEO audit (20 Nov 2026)

Method: a crawl of every HTML file in the build (`site-build/`, 44 pages), checked for titles, descriptions, canonicals, H1s, word counts, alt text, schema types, internal links and broken links; a headless Chromium render at phone and desktop widths; and fetches of the live site. GA4 and Search Console were **not** checked: there is no GA4 on the site, and this session had no Search Console access.

### Critical

| # | Issue | Evidence | Fix |
| --- | --- | --- | --- |
| C1 | **The live site is two batches behind the build.** | Live footer still lists 3 services and 7 locations; `/services/`, `/about/` and `/services/local-seo/` failed to load on 20 Nov; live sitemap has 38 URLs vs 44 in the build | Deploy the 19 Nov + 20 Nov build (needs your go-ahead and the Brandvo Chrome window) |
| C2 | **No Google Business Profile in the map pack** | Map pack for Kannur shows Bisaura, Sinaura, Stellent; no Brandvo listing found on 16–17 Nov | Create and verify a GBP (section 9) |
| C3 | **Live homepage title may still be the old one** | A fetch on 20 Nov returned "Brandvo Digital Co. \| Digital Marketing & Creative Agency"; the build has "Best Digital Marketing Agency in Kerala & Kannur…" (deployed 18 Nov according to notes). Possibly a cached fetch | Re-check right after the next deploy, in a browser and with Search Console URL Inspection |
| C4 | **No analytics or conversion tracking** | No GA4/GTM tag in any page | Needs a GA4 property (your Google account). Events: whatsapp_click, phone_click, form_submit |

### High

| # | Issue | Evidence | Fix |
| --- | --- | --- | --- |
| H1 | **Off-page authority is zero** | DR 0 vs 25–37 for the three competitors; no directory profiles found | Citations and links (section 9) |
| H2 | **Homepage stats are unverified** | "40+ Clients Served", "1200+ Campaigns Launched", "18K+ Leads Generated", "₹1Cr+ Revenue Generated for Clients" are on the homepage; there is no record of them in project notes | Confirm from your records or remove. Not repeated on any new page |
| H3 | Priority location pages were thin | Kannur ~560 words, Kasaragod ~600, Kozhikode ~625 | **Fixed today** (section 12) |
| H4 | Blog guides get few internal links | 3–11 inlinks per post vs 45 for footer pages | Partly fixed: the deepened pages link to 5 guides. Next: a "Guides" column in the footer |
| H5 | No street address in schema or on the site | `PostalAddress` has only Payyanur, Kerala, IN | Add the real address once the GBP is verified, and only if customers can visit it |

### Medium

| # | Issue | Fix |
| --- | --- | --- |
| M1 | Four services in the brief have no page: Google Ads, Content Marketing, Video Marketing, Social Media Management | Social Media Management merges into the SMM page (same intent). The other three wait for confirmation that they are sold |
| M2 | Five districts have no page (Kollam, Alappuzha, Kottayam, Pathanamthitta, Idukki) | Build only with a real angle or client (section 5) |
| M3 | Tier 3 location pages are 500–630 words (Thrissur, Trivandrum, Malappuram, Palakkad, Wayanad) | Deepen as local proof arrives; do not pad |
| M4 | FAQ rich results are not shown for agency sites (Google has limited FAQ results to government and health sites since 2023) | Keep the FAQPage markup, since it matches visible content and helps AI answers, but expect no rich result |
| M5 | Case study title is 87 characters | Leave for now (the numbers are the hook); revisit if Search Console shows low CTR |
| M6 | Core Web Vitals not measured | Run PageSpeed Insights after deploy; the pages are static HTML with WebP images, so no major issue is expected |

### Low

| # | Issue | Fix |
| --- | --- | --- |
| L1 | `/404.html` has no canonical | Correct as is (404s should not be canonicalised) |
| L2 | `privacy.html` and `terms.html` have no inbound links from static pages | Fine for SEO; footer links exist in the SPA |
| L3 | Old contact details in third-party sources (the 16 Nov AI Overview showed another phone, Gmail and Facebook page) | Confirm which are old and get them corrected or removed |

### Already in good shape (verified in the build)

One H1 per page; no duplicate titles; every page has a canonical and Open Graph tags; no broken internal links; no images without alt attributes; robots.txt allows search and AI crawlers and points to the sitemap; real 404s (no soft 404s); breadcrumbs with matching BreadcrumbList schema; BlogPosting schema on guides; Service schema on service and location pages; no LocalBusiness schema claiming addresses Brandvo does not have; no ratings or reviews in schema.

---

## 4. Recommended website architecture

Keep the existing URL pattern. Changing to `/digital-marketing-agency-kannur/` (as in the brief's examples) would throw away the indexing the current URLs already have, for no ranking gain.

```
/                                         Kerala & Kannur homepage (exact-match title and H1)
/digital-marketing-agency-in-kerala/      Kerala pillar: all 14 districts, links to every location page
  /digital-marketing-agency-in-kannur/    Tier 1  (sections: Kannur town, Thalassery, Taliparamba, Payyanur, Mattannur, Iritty)
  /digital-marketing-agency-in-payyanur/  Tier 1  (home base; Pilathara, Cheruvathur, Trikaripur)
  /digital-marketing-agency-in-kasaragod/ Tier 1  (Kasaragod town, Kanhangad, Nileshwar, Uppala, Bekal)
  /digital-marketing-agency-in-kozhikode/ Tier 1  (Feroke, Ramanattukara, Koyilandy, Perambra, Thamarassery)
  /digital-marketing-agency-in-thalassery|taliparamba|kanhangad|vadakara/   Tier 2 towns
  /digital-marketing-agency-in-kochi|thrissur|trivandrum|malappuram|palakkad|wayanad/  district pages
/services/                                hub
  /services/seo/  /services/local-seo/  /services/social-media-marketing/  /services/meta-ads/
  /services/performance-marketing/  /services/lead-generation/  /services/website-design/  /services/branding/
  /services/google-ads/  /services/content-marketing/  /services/video-marketing/   (only if sold)
/industries/                              hub
  /industries/real-estate/  /industries/healthcare/  /industries/beauty-and-salons/  /industries/food-and-restaurants/
/work/                                    (add a hub once there is a second case study)
  /work/unicorn-bakes/
/about/                                   founders, how we work, the Payyanur base
/blog/                                    guides (informational intent only)
```

**Internal linking rules**

- Every location page links to: the Kerala pillar, 2–3 neighbouring towns, every relevant service page, the matching industry pages, the case study, and 1–3 guides.
- Every service page links to the location pages where Brandvo has proof, using the city name in the anchor.
- Guides link to one service page and one location page, with descriptive anchors (not "click here").
- The footer (built 19 Nov) carries all services, locations and industries. Add a "Guides" column next.

**Service × city pages:** only where there is proof, as decided in Phase 1. The next four are `/seo-company-in-kannur/`, `/social-media-marketing-agency-in-kannur/`, `/social-media-marketing-agency-in-kozhikode/` (Ruyah by Naas) and `/social-media-marketing-agency-in-kochi/` (Playbox Club). Build them after the current batch is indexed and Search Console shows which terms get impressions.

---

## 5. Location landing page strategy

### 5.1 Rules

1. No page without something local and true: a client, a market feature Brandvo actually plans around, a language or seasonal difference, or distance from Payyanur that makes in-person work possible.
2. Never claim an office outside Payyanur. Every location page now has an FAQ that answers "do you have an office here?" honestly.
3. No city-swap templates. Each page has its own H1, intro, town list, industries and FAQs.
4. Schema: `Service` with `areaServed` set to the city, `provider` set to the Payyanur organisation. Never a LocalBusiness with a city address Brandvo does not have.
5. The CTA on every page is WhatsApp (+91 62820 70376) and call (+91 62354 34787), already in the shared aside.

### 5.2 All locations in the brief

| Location | District | Status | Decision and reason |
| --- | --- | --- | --- |
| Kannur | Kannur | Live, **deepened today** | Tier 1. Second keyword priority; Takees and Moris rank with weaker pages |
| Payyanur | Kannur | Live, **deepened today** | Tier 1. Home base, Unicorn Bakes and Land4Sale |
| Thalassery | Kannur | Live (~770 words) | Tier 2. Good already; add local proof when available |
| Taliparamba | Kannur | Live | Tier 2 |
| Mattannur | Kannur | **New section on Kannur page** | No standalone page; airport-area angle covered |
| Kasaragod | Kasaragod | Live, **deepened today** | Tier 1. Next door to Payyanur; language angle |
| Kanhangad | Kasaragod | Live | Tier 2 |
| Kozhikode | Kozhikode | Live, **deepened today** | Tier 1. Ruyah by Naas; biggest North Kerala market |
| Vadakara | Kozhikode | Live | Tier 2 |
| Koyilandy | Kozhikode | Section on Kozhikode page | No standalone page |
| Wayanad / Kalpetta | Wayanad | Live district page; Kalpetta is a section | Tier 3 |
| Kochi / Ernakulam | Ernakulam | Live ("Kochi (Ernakulam)" in title) | Tier 2. Playbox Club; next for a service × city page |
| Thrissur | Thrissur | Live | Tier 3 |
| Palakkad | Palakkad | Live | Tier 3 |
| Malappuram, Manjeri, Perinthalmanna, Tirur | Malappuram | Live district page; towns are sections | Tier 3 |
| Thiruvananthapuram | Thiruvananthapuram | Live (title shortened today) | Tier 3 |
| Kollam | Kollam | No page | Tier 4. Build with a cashew, seafood or coastal-retail client |
| Alappuzha | Alappuzha | No page | Tier 4. Build with a houseboat or resort client |
| Kottayam | Kottayam | No page | Tier 4. Education and hospitals angle |
| Pathanamthitta | Pathanamthitta | No page | Tier 4. NRI households, Sabarimala season |
| Idukki | Idukki | No page | Tier 4. Munnar and Thekkady resorts |

All 14 districts are named, with towns, in the "Areas we serve" section of the Kerala pillar page.

### 5.3 What each Tier 1 page now has (the 13 required elements)

Unique title and meta description; one H1; a location-specific introduction; services with links; local industries; client proof (Unicorn Bakes result, named testimonials, Ruyah by Naas for Kozhikode); a "why choose a Kannur-district agency" section; 4–6 location-specific FAQs including the office question; links to services, neighbouring towns and guides; WhatsApp and call CTAs; and Service + BreadcrumbList + FAQPage schema that matches the visible content.

**Local testimonials:** only two exist (Unicorn Bakes, SAJ Realty). A short quote from Ruyah by Naas (Kozhikode) and Playbox Club (Kochi) would strengthen those pages more than any copy change. Ask them.

---

## 6. Service page strategy

| Service in the brief | Page | Status | Decision |
| --- | --- | --- | --- |
| SEO | /services/seo/ | Live (~700 words) | Add a "how long SEO takes" section and Kerala SEO pricing drivers |
| Local SEO | /services/local-seo/ | Built 19 Nov, not live | Deploy |
| Social Media Marketing | /services/social-media-marketing/ | Expanded 19 Nov, not live | Deploy |
| Social Media Management | (same page) | — | **Do not build separately.** Same search intent; a second page would compete with the first. "Management" is covered in the SMM page copy and title |
| Google Ads Management | /services/google-ads/ | Not built | **Blocked**: confirm Google Ads is sold. The site and case study only show Meta Ads |
| Meta Ads Management | /services/meta-ads/ | Live (~510 words) | Next to deepen: add the Unicorn Bakes Meta Ads detail and lead-form vs WhatsApp guidance |
| Website Design and Development | /services/website-design/ | Live | Add portfolio links when you have client sites to show |
| Branding and Brand Identity | /services/branding/ | Live | Add before/after work |
| Performance Marketing | /services/performance-marketing/ | Expanded 19 Nov, not live | Deploy |
| Content Marketing | /services/content-marketing/ | Not built | Blocked: confirm it is sold as its own service. Otherwise keep it inside SMM |
| Video Marketing | /services/video-marketing/ | Not built | Blocked: confirm Reels/video production is sold. The homepage lists "Reels & Short-Form", so this is likely a yes |
| Lead Generation | /services/lead-generation/ | Built 19 Nov, not live | Deploy |

Each service page targets one commercial intent ("seo company in kerala", "meta ads agency kerala" and so on), links to the Tier 1 location pages and the matching industries, and carries `Service` schema with `areaServed` Kerala (and UAE where relevant).

---

## 7. Three-month content calendar (Dec 2026 to Feb 2027)

Also in `content-calendar-dec-2026-feb-2027.csv`. Each article avoids overlap with the nine existing guides and has one search intent, one service page and one location page to link to. Wherever an article needs first-hand material, the input needed from you is listed.

| Week of | Title (working) | Intent / primary keyword | Links to | Input needed |
| --- | --- | --- | --- | --- |
| 1 Dec | How Much Does SEO Cost in Kerala? What You Pay For, and What to Avoid | seo cost in kerala | /services/seo/, Kannur | Your SEO starting price, or approval to publish only cost drivers |
| 8 Dec | How to Get More Google Reviews in Kerala Without Breaking Google's Rules | how to get google reviews | /services/local-seo/, Payyanur | — |
| 15 Dec | What a Payyanur Bakery Taught Us About Instagram Marketing (Unicorn Bakes) | bakery instagram marketing kerala | /industries/food-and-restaurants/, /work/unicorn-bakes/ | Two or three campaign examples or screenshots |
| 22 Dec | Real Estate Lead Generation in Kerala: Reaching Gulf-Based Buyers | real estate leads kerala | /industries/real-estate/, Kasaragod | SAJ Realty or Land4Sale campaign detail (no client numbers without permission) |
| 5 Jan | Digital Marketing for Dental Clinics in Kerala: Reviews, Maps and Ads That Follow the Rules | dental clinic marketing kerala | /industries/healthcare/, Kozhikode | — |
| 12 Jan | WhatsApp Leads: How to Know Which Enquiries Came From Your Ads | whatsapp lead tracking | /services/lead-generation/, Kannur | — |
| 19 Jan | Salon and Bridal Marketing in Kozhikode: Reels That Fill the Booking Diary | salon marketing kozhikode | /industries/beauty-and-salons/, Kozhikode | Ruyah by Naas permission and examples |
| 26 Jan | Local SEO Checklist for Kerala Small Businesses (Printable) | local seo checklist | /services/local-seo/, Kerala | — |
| 2 Feb | Ramadan and Eid Marketing for Kerala and UAE Businesses (2027) | ramadan marketing kerala | /services/meta-ads/, UAE guide | — (Ramadan 2027 is expected to begin around 8 Feb, so publish by early Feb) |
| 9 Feb | Does a Small Business in Kerala Need a Website, or Is Instagram Enough? | website vs instagram | /services/website-design/, Payyanur | — |
| 16 Feb | Google Ads vs Meta Ads for Kerala Service Businesses | google ads vs meta ads kerala | /services/meta-ads/ (+ /services/google-ads/ if sold) | Whether Google Ads is sold |
| 23 Feb | Vishu and Wedding-Season Marketing Plan for North Malabar Businesses | vishu marketing ideas | /services/social-media-marketing/, Kannur | — |

**Refreshes in the same period:** update `/blog/best-digital-marketing-agency-in-kannur/` and `/blog/best-digital-marketing-agency-in-kerala/` in January with links to the new pages and a "last updated" date; add the Unicorn Bakes result to `/blog/digital-marketing-cost-in-kerala/`.

**Rules for every article:** a real example or Brandvo's own experience in the first third; no invented statistics (cite Google or Meta documentation where facts are needed); the keyword in bold in the first paragraph; H2/H3 structure; a "Where Brandvo Digital Co. fits" section; an FAQ at the end; BlogPosting schema; and the full brand name.

---

## 8. Technical SEO implementation plan

| Item | Status | Action |
| --- | --- | --- |
| XML sitemap | Done; 44 URLs with lastmod in the build | Deploy; resubmit in Search Console |
| robots.txt | Done; allows search and AI crawlers | None |
| Canonicals | Done on every indexable page | None |
| Open Graph | Done on every page | None |
| SEO-friendly URLs | Done | Keep the current pattern; no redirects needed |
| Breadcrumbs | Done (19 Nov build) with BreadcrumbList | Deploy |
| Images: WebP, lazy loading | WebP done 16 Nov; static pages carry only the logo | Check lazy-loading on homepage client logos after deploy |
| Mobile | Verified today at 390px: no horizontal scroll, one H1 | None |
| Page speed / CWV | Not measured | PageSpeed Insights after deploy; target LCP < 2.5s on mobile |
| Schema: Organization (ProfessionalService) | Done; founders, sameAs, phone, email | Add streetAddress and geo only when the real address is public and on the GBP |
| LocalBusiness | ProfessionalService is a LocalBusiness subtype, used only for the Payyanur entity | Never add city-specific LocalBusiness nodes |
| Service | Done on service, industry and location pages | None |
| BreadcrumbList | Done | None |
| Article | BlogPosting on guides; Article on the case study | None |
| FAQPage | On money pages, matching visible FAQs | Keep; no rich result expected (see M4) |
| 404 and redirects | Real 404 page; no SPA catch-all | None |
| Indexability | All pages indexable; no noindex | After deploy: URL Inspection for the 6 new and 4 deepened pages; IndexNow ping |
| Pagination | Not applicable (blog has 9 posts on one page) | Revisit at ~30 posts |
| Analytics | Missing | GA4 + key events once you share access |

**Deploy checklist (when you say go):** build order is step 6 → 7 → 8 → 9; regenerate the manifest (step 9 does this); deploy through the Netlify digest API from the Brandvo Chrome window; then check 10 URLs return 200, `/services/` loads, the footer shows all locations, and the sitemap has 44 URLs; then IndexNow and Search Console requests.

---

## 9. Local SEO and backlink strategy

### 9.1 Google Business Profile

- **Eligibility.** Google allows a profile for a business that meets customers in person. If customers can visit your Payyanur base during staffed hours, list the address. If they can't, create a **service-area business** with the address hidden. Either way, **one profile**. No profiles for Kannur, Kozhikode or Kochi, because there are no offices there.
- **Name:** "Brandvo Digital Co." exactly. Adding keywords to the name risks suspension.
- **Categories:** primary "Internet marketing service" or "Marketing agency" (pick the one whose wording the competitors in your map pack use; check in the GBP category picker). Secondary: "Social media agency", "Website designer", "Advertising agency", "Graphic designer", "Marketing consultant". Only list what you sell.
- **Service areas** (up to 20): Payyanur, Kannur, Thalassery, Taliparamba, Kasaragod, Kanhangad, Kozhikode, Vadakara, then wider districts.
- **Services:** mirror `/services/`, each with a 2–3 sentence description taken from the service page.
- **Description draft (750-character limit):** "Brandvo Digital Co. is a digital marketing agency based in Payyanur, Kannur district. We help businesses across Kerala and the UAE get more enquiries through social media marketing, Meta Ads, SEO and Google Maps, websites and branding. We create content in Malayalam and English, track calls and WhatsApp enquiries, and report results in plain language. Clients include Unicorn Bakes (Payyanur), Ruyah by Naas (Kozhikode) and Playbox Club (Kochi). Book a free strategy call to see what we would change first."
- **Photos:** team, workspace, shoots in progress, finished client work (with permission).
- **Posts:** weekly; reuse the guide or case-study angle of the week.
- **Website link:** `https://brandvodigital.com/?utm_source=google&utm_medium=organic&utm_campaign=gbp`.

### 9.2 Reviews

- Ask each of the seven current clients personally, with a direct review link. Never offer anything in return, and never write reviews for them.
- Reply to every review within 48 hours, naming the service delivered.
- Benchmarks: the Payyanur map pack had 13–24 reviews per business on 16 Nov; Kannur town 68–96. Aim for 10 in the first month, then steady growth from new clients.

### 9.3 Citations (same name, phone and URL everywhere)

Priority order: Justdial, Sulekha, IndiaMART, Bing Places, Apple Business Connect, Clutch, GoodFirms, DesignRush, TechBehemoths, Sortlist, the LinkedIn company page, the Facebook page. Takees appears on Clutch, DesignRush, GoodFirms and TechBehemoths, and those profiles show up in Kannur agency searches. Clutch and GoodFirms rank better with verified client reviews, so ask one or two clients to review there too.

Use the calling number (+91 62354 34787) as the primary phone on listings and mention WhatsApp (+91 62820 70376) where a second field exists.

### 9.4 Genuine local links and PR

| Opportunity | Why it is realistic | Effort |
| --- | --- | --- |
| "Website / marketing by Brandvo Digital Co." credit on client sites Brandvo built or manages | Genuine, relevant, Kerala-local | Low |
| Client case-study cross-posts (Unicorn Bakes Instagram/website mentioning the partnership) | Real relationship | Low |
| North Malabar Chamber of Commerce (Kannur) and Malabar Chamber of Commerce (Kozhikode) member listings | Business associations with local authority | Medium (membership) |
| Kerala Startup Mission / Startup India listing | Only if Brandvo is registered; Bisaura shows KSUM and DPIIT badges | Medium |
| A free "Get found on Google Maps" workshop for Payyanur traders, with a press note to Mathrubhumi and Malayala Manorama local editions | Real local news, real community value | Medium |
| A guest article for a Kerala SME or startup publication, using the Unicorn Bakes numbers (with permission) | Brandvo has a concrete story; competitors have none | Medium |
| A founder profile on the About page, plus LinkedIn articles | E-E-A-T and brand mentions | Low |

**Will not do:** buy links, join link exchanges or PBNs, mass-submit to directories, post fake reviews, or create location listings without an office.

### 9.5 Competitor backlinks

The free Ahrefs plan returns only DR (Takees 25, Moris Media 37, Sinaura 27). The referring domains behind those numbers can't be listed without a paid plan. What is visible: Takees's directory profiles (above). Moris Media's DR likely comes from its size and long-running content operation, which is not a model to follow. A one-month paid Ahrefs or Semrush plan would give the full link lists. That is worth it once the GBP and citations are done, not before.

---

## 10. Prioritised implementation roadmap

Rankings are not guaranteed, and nothing below promises positions. Timelines assume the 19–20 Nov build is deployed this week.

### Phase 1: Foundation (now to 19 Dec 2026)

| Task | Priority | Owner | Status |
| --- | --- | --- | --- |
| Deploy the 19 Nov + 20 Nov build | Critical | Claude, after your go-ahead | Ready |
| Create and verify the GBP; first reviews | Critical | You (Claude can draft everything) | Waiting |
| GA4 + key events; link GA4 to Search Console | Critical | You grant access, Claude installs | Waiting |
| Confirm or remove the homepage stats | High | You | Waiting |
| Citations: Justdial, Sulekha, IndiaMART, Bing, Apple | High | You or Claude via your browser | Not started |
| Search Console baseline: indexed pages, queries per page | High | Claude via your browser | After deploy |
| Competitor teardowns, keyword DB v3, audit, architecture | High | Claude | **Done** (this document) |
| Deepen the Tier 1 location pages | High | Claude | **Done** (branch) |

*Expected by mid-December:* all 44 URLs indexed; first impressions for Kannur and Payyanur terms in Search Console; a GBP in the Payyanur map results if it is verified.

### Phase 2: Local SEO expansion (Dec 2026 to Jan 2027)

| Task | Priority |
| --- | --- |
| Service × city pages: SEO Kannur, SMM Kannur, SMM Kozhikode, SMM Kochi | High |
| Google Ads, Video and Content Marketing pages, if confirmed | High |
| Deepen Meta Ads, SEO and Kochi pages | Medium |
| A "Guides" column in the footer; refresh the two location-named blog posts | Medium |
| Clutch, GoodFirms, DesignRush, TechBehemoths profiles with client reviews | High |
| Testimonials from Ruyah by Naas and Playbox Club | High |

*Expected:* Payyanur and Kannur long-tail terms in the top 20–30; first tracked organic WhatsApp and call enquiries.

### Phase 3: Authority building (Jan to Mar 2027)

| Task | Priority |
| --- | --- |
| Publish the content calendar (4 articles a month) | High |
| A second case study with real numbers | High |
| Local PR: Payyanur workshop, guest article, chamber listings | Medium |
| Client-site credits | Medium |
| One month of paid Ahrefs/Semrush for competitor link gap and volumes | Medium |

*Expected:* DR above 5 with 10–20 genuine referring domains; top-10 positions for some Payyanur and Kannur terms.

### Phase 4: Growth and optimisation (Apr 2027 onward)

| Task | Priority |
| --- | --- |
| Monthly report (section 11); rewrite titles where impressions are high and CTR is low | High |
| Build pages only where Search Console shows impressions without a matching page | High |
| Tier 4 district pages once there is a client in that district | Medium |
| Conversion tests on location pages (CTA wording, WhatsApp prefill text) | Medium |
| Quarterly competitor re-check (Takees, Moris, Sinaura, plus the Phase 1 set) | Medium |

*Realistic 6-month picture:* consistent top-10 rankings and map presence for Payyanur and nearby towns; page 1–2 for Kannur district terms; Kerala head terms on pages 2–3. Kochi, Kozhikode and "best digital marketing agency in Kerala" are held by DR 40+ agencies and usually take longer than six months.

---

## 11. SEO performance tracking

Use `seo-2026-11/brandvo-monthly-seo-report-template.csv`. It already covers organic clicks, impressions, CTR, position, indexed pages, keyword positions, organic WhatsApp/phone/form enquiries, landing pages, city and service page performance, GBP, referring domains and DR. Add these rows from this plan:

- Map pack position for "digital marketing agency payyanur" and "… kannur" (manual check from Payyanur and Kannur town).
- Competitor watch: Takees, Moris Media and Sinaura titles, new location pages, GBP review counts.
- Positions for the four Tier 1 pages' primary keywords.
- Citations built this month (list) and reviews gained.

**Sources:** Search Console (needs your login in the browser session), GA4 (needs setup), GBP Performance, Ahrefs free DR. Rank checks without a paid tracker are manual and personalised, so note the location and date with every check.

---

## 12. What was implemented today

Branch `claude/project-thread-39x7zu` (built on the 19 Nov branch `claude/project-thread-zbww0p`).

- `tools/build_step9_priority_locations.py` (run after step 8; idempotent, verified by running it twice and diffing the output).
- `content/pages-2026-11-20/`: new sources for the Kannur, Payyanur, Kasaragod and Kozhikode pages.
- **Kannur** (~560 → ~1,420 words): town-by-town section (Kannur town, Thalassery/Kuthuparamba, Taliparamba, Payyanur/Pilathara, Mattannur, Iritty); "what holds Kannur businesses back" section; all 8 service pages and 4 industry pages linked; the Unicorn Bakes result; an engagement process; 6 FAQs, including "Do you have an office in Kannur town? No…".
- **Payyanur:** a Google Maps section, nearby towns, links to the Local SEO, Lead Generation, Branding and Website pages, the Unicorn Bakes numbers, and a new FAQ.
- **Kasaragod:** town-by-town section, a "what we would check first" list, honest proof ("we do not yet have a published Kasaragod case study"), and an office FAQ.
- **Kozhikode:** areas around Calicut, links to the industry pages, and the bakery result.
- **Trivandrum:** title shortened to 60 characters.
- Schema: FAQPage rebuilt from the visible FAQs; WebPage name, description and dateModified updated; sitemap lastmod bumped.
- Keyword database v3 generator: `tools/build_keyword_database_v3.py`.
- **Tests:** crawl of all 44 pages (no broken internal links, no duplicate titles, one H1 each, all canonicals present); Chromium render of the four pages at 390px and 1366px (no horizontal overflow, no console errors).

**Not deployed.** It goes live with the 19 Nov batch when you say so.

---

## 13. Decisions and inputs needed

1. **Deploy go-ahead** for the 19 Nov + 20 Nov batch (one deploy, which saves Netlify credits).
2. **Homepage stats:** keep (if your records support them), edit, or remove.
3. **GBP:** is there an address in Payyanur where customers can visit during staffed hours? If not, a service-area profile.
4. **Services sold:** Google Ads? Video/Reels production? Content marketing as its own service?
5. **Testimonials:** can we ask Ruyah by Naas and Playbox Club for a short quote?
6. **Pricing:** may the SEO cost article and service pages show starting prices?
7. **GA4 / Search Console:** access, or a browser session where Claude can read Search Console.
