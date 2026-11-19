# Brandvo Digital Co.: Kerala SEO, Phase 1 findings and plan

Prepared 19 Nov 2026. This builds on the work already live on brandvodigital.com (38 URLs, deploy of 18 Nov 2026) and the earlier teardowns of Haris&Co, Rayans Creative, Progbiz, Netstager and Klyqin. Nothing on the site was changed for this report.

Companion files in this folder:
- `brandvo-kerala-keyword-database-v2.csv`: 594 keywords, all 14 districts and the 43 towns in the brief, with the recommended page and whether it exists.
- `brandvo-monthly-seo-report-template.csv`: the monthly reporting sheet.
- `brandvo-kerala-keyword-master-list.csv`: the 16 Nov list (kept for history; v2 replaces it).

---

## 1. Summary

**Where things stand.** Brandvo Digital Co. already has more SEO structure than any of the three named competitors. It has 15 location pages, 6 service pages, 3 industry pages, a case study with real numbers, 9 guides, and schema on every page. None of Pappayas, Klyqin or Bisaura has a single location page or any JSON-LD. The gap is **authority, not pages**. Brandvo's domain rating is 0 against Pappayas 6, Klyqin 2.5, Bisaura 0.3, Rayans 15, Progbiz 43 and Haris&Co 47 (Ahrefs, 19 Nov 2026). Brandvo also has no Google Business Profile and no reviews. Bisaura shows up in the Kannur map pack with weaker pages than Brandvo, because it has a verified GBP at a Kannur address.

**Top findings**
1. **Map pack and reviews decide the Kannur and Payyanur results more than page content.** Bisaura, Sinaura and Stellent hold the Kannur map pack (17 Nov). A verified GBP plus 15–25 genuine reviews is the single biggest lever. Only Hola can do it.
2. **Competitors win on exact-match homepages, not depth.** Pappayas, Klyqin and Bisaura each put "Best Digital Marketing Agency in Kannur" in the title and H1, and that is mostly all they do. Brandvo now does the same for Kerala and Kannur, with far more supporting content.
3. **Brandvo's internal linking is uneven.** The homepage links to only 6 of the 15 location pages. It does not link to the SEO, website or branding service pages, the case study, or the healthcare and beauty industry pages. The Trivandrum and Wayanad pages have 2 internal links each, and the beauty page has 1. Fixing this is cheap and fast.
4. **No analytics or conversion tracking anywhere.** No GA4 or GTM tag is in the build, so WhatsApp, call and form enquiries can't be measured by page. Every later decision depends on this.
5. **Three service pages are thin**: Performance Marketing (~335 words), Social Media Marketing (~400) and Real Estate (~305). These are Brandvo's core money pages.
6. **The missing pages that matter**: Google Ads (only if it is sold), Lead Generation, Local SEO, an About/Team page with real founder credentials, a Food & Restaurants industry page built on the Unicorn Bakes proof, and a services hub. District pages for Kollam, Kottayam, Alappuzha, Pathanamthitta and Idukki are worth building only with a genuine local angle.
7. **Keyword metrics could not be verified.** The Ahrefs connector is on the free plan, and keyword and site endpoints return "Insufficient plan". Every volume and KD cell says "Unavailable". Priorities are based on commercial intent, observed SERPs and Brandvo's proof, not on volume.

**What I propose to build next (needs your OK).** Details are in section 7.
- A. Tracking: GA4 + GTM with WhatsApp, call and form events (needs a GA4 property from you).
- B. Internal linking fix: homepage and footer links to every service, location, industry and case-study page; breadcrumbs everywhere; a /services/ hub.
- C. Expand the three thin money pages (Social Media Marketing, Performance Marketing, Real Estate) to 900–1,300 words each, with real proof.
- D. New pages: /services/lead-generation/, /services/local-seo/, /about/ (founders Ansar, Akshay and Abhishek, with real credentials), and /industries/food-and-restaurants/.
- E. Service x city pages, only where Brandvo has proof: SEO and social media for Kannur, Kochi and Kozhikode, plus website design for Kannur (7 pages).
- F. Two to four guides a month from the content plan (section 6.3).

Blocked on you: GBP creation and reviews, whether Google Ads and video production are sold, whether to publish starting prices, and GA4 access.

---

## 2. Data sources and limits

| Data | Source | Status |
|---|---|---|
| Domain rating | Ahrefs public DR endpoint, 19 Nov 2026 | Verified |
| Search volume, KD, competitor organic keywords and backlinks | Ahrefs Keywords/Site Explorer | **Unavailable**: API returned "Insufficient plan" (free subscription) |
| Competitor page structure, titles, headings, schema, CTAs | Live pages fetched 19 Nov 2026 (homepages, sitemaps, sample inner pages) | Verified for the pages listed |
| Google SERPs | Hola's browser on 16–17 Nov 2026 (from earlier threads) | Observed, personalised, Kannur location |
| Brandvo audit | Repo build (branch claude/project-thread-2peiwo, 205ba48) = live deploy | Verified from source |
| Search Console data | Property verified 16 Nov; only 3 days of data, and no browser was connected this session | Not pulled |

To turn "Unavailable" into real numbers, any one of these works: (a) upgrade Ahrefs to a plan with API access; (b) Google Ads Keyword Planner (free with a Google Ads account) export for the keyword list; (c) after 4–6 weeks, Search Console impressions per query. Option (b) is the cheapest and I can merge the export into the CSV.

Note: an external fetch of the homepage returned the old title ("Brandvo Digital Co. | Digital Marketing & Creative Agency"), while the deployed build has "Best Digital Marketing Agency in Kerala & Kannur | Brandvo Digital Co.". This is probably a cached copy, but the live HTML should be checked once from a browser.

---

## 3. Competitor teardowns

### 3.1 Pappayas Digital (pappayas.com), Thalassery

- **Stack and size:** WordPress with a Yoast sitemap. 20 pages and 1 blog post (Oct 2024). DR 6.
- **Homepage:** title "Best Digital Marketing Agency in Kannur - PAPPAYAS DIGITAL"; H1 "Best Digital Marketing Agency in Kannur"; about 750 words. H2s are generic ("Meet the Pappayas Crew!", "We offers for you") and services are H3s. 4 FAQs with no FAQ schema. 4 named testimonials (Wheels, We Five Developers, Pioneer Yamaha, Nettur Opticals). Client logos include Honda, Yamaha and Samsung.
- **Architecture:** service pages /smm/, /branding-logo-design/, /web-designing/, /best-seo-agency-in-kerala/ (plus a conflicting /seo/ link). Industry pages: healthcare, education, real estate, vehicle dealers, fashion. Package pages for SMM, web design and branding. A Kerala page /best-digital-marketing-agency-in-kerala/. No location pages beyond that.
- **Quality:** thin and templated. The Kerala page has about 85 words of body copy. The healthcare page has about 150 words and no healthcare specifics. The SEO page (~700 words) repeats FAQs and answers "how long does SEO take" with text about social media. Alt text repeats "Best Digital Marketing Agency in Kannur" on about 13 logos (keyword stuffing). No JSON-LD found. Two different WhatsApp numbers appear on the healthcare page.
- **Conversion:** WhatsApp-first. "Get a Free Audit" and "Get a Free Consult" are wa.me links. No form.
- **Why it ranks (#2 for "digital marketing agency kannur", 17 Nov):** exact-match title and H1, a Thalassery address with a GBP map embed, recognisable client logos, and an older domain (content from 2024).
- **What to learn:** visible **packages** pages capture "packages" and price-intent searches; industry pages; a "free audit" offer. Brandvo can do each of these with real substance.

### 3.2 Bisaura Technologies (bisauratechnologies.com), Kochi and Kannur

- **Stack and size:** static HTML (.html URLs). 12 sitemap URLs: 8 core pages and 4 blog posts (Aug–Sep 2026). DR 0.3.
- **Homepage:** title "Best Digital Marketing & SEO Agency in Kannur | Bisaura Technologies". The meta description names Kannur and Kochi. **Two H1s** ("Creative Business Solutions", "Efficient Solutions for Companies"), with no keyword in either. Canonical, OG and Twitter tags are present. About 700 words.
- **Architecture:** a single /service.html hub. Every individual service, footer and support link is "#". No service, location or industry pages.
- **Blog:** article bodies are loaded by JavaScript (blog-detail.html?slug=…), so the static HTML has no H1, no meta description and no article text. Google may index these only partly. A public "Admin Login" link is in the navigation.
- **Trust:** DPIIT-recognised startup (DIPP153089) and Kerala Startup Mission (KSUM3363) badges. Two real offices: Infopark Kakkanad and KK Trade Centre, Thavakkara, Kannur. No testimonials or client logos on the homepage.
- **Why it shows up (Kannur map pack, 17 Nov):** a verified **Google Business Profile at a Kannur address** (Thavakkara, near the bus terminal), plus a title tag that names Kannur. The website itself is weak.
- **What to learn:** the map pack can be won with a weak site and a good GBP. Startup India and KSUM recognition are real, cheap trust signals (and KSUM has a startup directory that links out). Brandvo could check whether it qualifies.

### 3.3 Klyqin (klyqin.com), Kannur: refresh of the 18 Nov notes

- **Stack and size:** WordPress with Site Kit (so GA is likely). 3 pages (/, /blogs/, and a duplicate /home/) plus 33 posts published Jul–Sep 2026. DR 2.5.
- **Homepage:** title "Best Digital Marketing Agency in Kannur,Kerala| Klyqin Creative Agency"; H1 "Digital Marketing Agency in Kannur". The nav is on-page anchors only. 8 FAQs, 6 named testimonials (AK Interio, Stainaway Bahrain and others) and 7 client logos. A founder section (Muhammed Thashreef). Office at Royal Oak Mall, Thana, Kannur. Two tel: numbers that differ by one digit (likely a typo).
- **Blog strategy (new since the last check):** 33 long-form posts of about 2,000 words each, almost all generic SEO topics (what is SEO, AEO, GEO, robots.txt, canonical tags, Core Web Vitals, E-E-A-T, AI Overviews). Posts have FAQs but no schema and no named author, and link only to the homepage. They barely mention Kerala.
- **What it means:** Klyqin is building topical authority on "SEO" in general. That attracts learners more than Kerala buyers. Its posts don't link to service or location pages, because it has none.
- **What to learn:** consistent publishing, and a named founder on the homepage.

### 3.4 Side-by-side

| | Brandvo Digital Co. | Pappayas | Klyqin | Bisaura | Progbiz (ref.) | Rayans (ref.) |
|---|---|---|---|---|---|---|
| Domain rating (Ahrefs, 19 Nov) | 0 | 6 | 2.5 | 0.3 | 43 | 15 |
| Indexable URLs (sitemap) | 38 | 21 | 36 | 12 | n/a | 52 |
| Location pages | 15 | 1 (Kerala) | 0 | 0 | 5 | 0 |
| Service pages | 6 | 4 + 3 packages | 0 | 0 (hub only) | yes | 0 (placeholder links) |
| Industry pages | 3 | 5 | 0 | 0 | 3 | 0 |
| Case study with numbers | 1 (Unicorn Bakes) | 0 | 0 | 0 | yes (GEPS ₹4Cr→₹40Cr) | 0 |
| Blog posts | 9 (Kerala-focused) | 1 | 33 (generic SEO) | 4 (JS-rendered) | yes | 39 |
| JSON-LD | Every page (ProfessionalService, Service, FAQPage, Breadcrumb, BlogPosting) | none | none | none | none | none |
| Google Business Profile | **none** | yes (Thalassery) | yes (Kannur) | **yes, in Kannur map pack** | 4.8★ | yes |
| Testimonials on site | 3 on homepage (Unicorn Bakes, Playbox Club, SAJ Realty) | 4 | 6 | 0 | yes | 0 |
| Pricing or packages shown | no | packages | no | no | yes | pricing page |
| Analytics tag | **none** | GTM | Site Kit | not seen | n/a | n/a |
| Conversion path | WhatsApp, call, form | WhatsApp only | WhatsApp, call | Phone (href "#") | form, calculator | quote form |

---

## 4. Competitor advantage strategy (brief section 13)

**4.1 Keywords they rank for that Brandvo does not.** This can't be pulled without an Ahrefs plan, so it is observed only. On 17 Nov, for "digital marketing agency kannur", Pappayas was #2, Klyqin #5 and Rayans #8, and Bisaura was in the map pack. Brandvo was outside the top 20, with its Kannur page indexed. Likely variants they also hold: "best digital marketing agency in kannur", "digital marketing company kannur", "seo agency kannur" (Bisaura title), "best seo agency in kerala" (Pappayas page), "digital marketing agency thalassery" (Pappayas address). Brandvo has pages for all of these. The gap is authority and the map pack.

**4.2 Dedicated pages they have and Brandvo does not.**
- Packages and pricing pages (Pappayas: SMM, web, branding packages). Brandvo option: a pricing section on service pages, or a /pricing/ page, if Hola approves starting prices.
- Education, vehicle dealer and fashion industry pages (Pappayas). Brandvo: build only where there is proof. Auto Jota covers automobile; education has no proof yet, so it gets a guide, not a page.
- A Food & Restaurants industry page. No competitor has one, but Brandvo has the strongest proof here (Unicorn Bakes, ₹8L → ₹95L).
- Google Ads, Lead Generation and Local SEO service pages. Progbiz and Haris have Google Ads or PPC coverage.

**4.3 Locations they target.** Pappayas: Kannur, Thalassery, Kerala. Klyqin: Kannur. Bisaura: Kannur and Kochi. Brandvo already covers all of these with dedicated pages, plus 11 more.

**4.4 Content gaps.**
- Pricing and cost content: Brandvo has digital marketing cost and website cost guides. Add SEO cost and Meta Ads cost.
- Google Maps ranking, getting reviews, local SEO checklist: Klyqin has a generic local SEO checklist. Brandvo should write the Kerala-specific version, linking to /services/local-seo/.
- Industry playbooks (clinics, restaurants, real estate, tourism and homestays, education). No competitor has depth here.
- Seasonal Kerala marketing (Onam, Vishu, wedding season, Gulf return season). No competitor covers it, and it suits Brandvo's voice.

**4.5 Backlink opportunities (verifiable without Ahrefs).** Startup India / DPIIT and the Kerala Startup Mission directory (Bisaura uses both); Clutch and GoodFirms (Progbiz); DesignRush (Haris&Co); Justdial and Sulekha (dominate Kannur results); client websites with a "Marketing by Brandvo Digital Co." credit (Unicorn Bakes, SAJ Realty, Land4Sale, Ruyah, Playbox Club, K1 Kitchen Gallery, Auto Jota), only with each client's permission. Competitor backlink lists need Ahrefs Site Explorer (paid).

**4.6 Their strongest pages.** Pappayas homepage and /best-seo-agency-in-kerala/; Klyqin homepage (testimonials + FAQ); Bisaura's GBP rather than any page; Progbiz /service/digital-marketing-agency-in-kerala (~2,000 words, case study, calculator, 12 FAQs). Progbiz is the benchmark for the Kerala pillar.

**4.7 Architecture weaknesses to exploit.** None of the three has location pages or schema. Bisaura's links are "#" and its blog is JS-only. Pappayas is templated and thin with keyword-stuffed alt text. Klyqin has no service pages and its posts don't link to money pages. All three are WhatsApp-only, or close to it, with no case studies with numbers.

**4.8 How Brandvo outperforms them.** Brandvo already wins on structure, so the work now is: (1) a GBP and reviews to enter the map pack; (2) proof everywhere (case studies, named testimonials, founders); (3) internal links that pass the homepage's authority to every money page; (4) 10–20 genuine, relevant backlinks in 90 days to move DR above the Kannur competitors (6–15); (5) measured conversions, so effort goes to pages that produce enquiries.

**Keyword gap priorities (business value × realistic chance):**
1. Kannur and Payyanur head terms (DM, SEO, social media, website). Highest chance, because Brandvo is based there. Needs a GBP.
2. "near me" terms: map pack only, needs a GBP.
3. Kerala service terms (social media marketing kerala, meta ads agency kerala, performance marketing kerala). Medium chance, lower competition than "digital marketing agency kerala".
4. North Malabar towns (Thalassery, Taliparamba, Kasaragod, Kanhangad, Vadakara). Pages are live; they need links and time.
5. Metro head terms (Kochi, Kozhikode, Trivandrum). Long game of 6–12+ months, against high-DR agencies with many reviews.

---

## 5. Brandvo audit update (19 Nov 2026)

Checked against the deployed build (38 URLs). Items from the 16 Nov audit that are already fixed (prerendering, 404s, schema, WebP, sitemap, robots, llms.txt, IndexNow) are not repeated.

| # | Issue | Evidence | Priority |
|---|---|---|---|
| 1 | No GA4, GTM or conversion tracking | No gtag or googletagmanager in any page | P1 |
| 2 | Homepage links to only 6 of 15 location pages and none of SEO, Website, Branding, Healthcare, Beauty or the case study. Service cards go to #contact | Link count on index.html | P1 |
| 3 | Weakly linked pages: Trivandrum (2 inlinks), Wayanad (2), Beauty (1), Malappuram, Palakkad, Kanhangad, Taliparamba, Vadakara (3 each), Unicorn Bakes (4) | Internal link count across 38 pages | P1 |
| 4 | Footer lists social media marketing twice and sends Content Strategy and Reels to /#services; Thrissur and the newer towns are missing from the footer | Kochi page footer | P2 |
| 5 | Thin money pages: Performance Marketing ~335 words, Real Estate ~305, Social Media Marketing ~397 | Word count of main content | P1 |
| 6 | Several titles too long for SERPs: Trivandrum (81 chars), Unicorn Bakes (87) | Title lengths | P3 |
| 7 | No About/Team page. Founders appear only in schema; the AI Overview had confused entity details (16 Nov) | No /about/ URL | P2 |
| 8 | No /services/ hub or /industries/ hub; breadcrumbs point to /#services | Sitemap | P2 |
| 9 | `meta name="keywords"` on the homepage (ignored by Google, harmless, can go) | index.html | P3 |
| 10 | No Google Business Profile, no citations; Justdial and Sulekha profiles not set up | 16–17 Nov SERP checks | P1 (Hola) |
| 11 | Search Console: indexing requests not made for the 22 pages from 17–18 Nov (only IndexNow) | Memory note | P2 |
| 12 | Core Web Vitals not measured this session (PageSpeed API quota was exhausted on 16 Nov) | — | P3: check with PageSpeed Insights in a browser |

---

## 6. Architecture and keyword-to-page map

### 6.1 URL decision
The brief suggests `/digital-marketing-agency/kochi/`. **Keep the existing `/digital-marketing-agency-in-<city>/` URLs.** They are already indexed and sent to IndexNow, and moving them buys nothing. Services stay under `/services/`, industries under `/industries/`, case studies under `/work/`. New service x city pages use `/seo-company-in-<city>/` and `/social-media-marketing-agency-in-<city>/`, matching how people search.

### 6.2 Page map (existing vs missing)

**Hubs**
| Page | Status | Primary keyword |
|---|---|---|
| / | Live | best digital marketing agency in kerala (and kannur) |
| /digital-marketing-agency-in-kerala/ | Live (880 words; should grow toward Progbiz depth, ~1,500) | digital marketing agency in kerala |
| /services/ | **Missing** | digital marketing services kerala |
| /industries/ | **Missing** | (hub, internal linking) |
| /work/ | **Missing** (only /work/unicorn-bakes/) | case studies |
| /about/ | **Missing** | brandvo digital co founders, digital marketing consultant kerala |

**Services**
| Page | Status | Primary keyword(s) |
|---|---|---|
| /services/social-media-marketing/ | Live, thin | social media marketing agency in kerala, instagram marketing agency kerala |
| /services/meta-ads/ | Live | meta ads agency kerala, facebook ads agency kerala |
| /services/performance-marketing/ | Live, thin | performance marketing agency kerala |
| /services/seo/ | Live | seo company in kerala / kannur |
| /services/website-design/ | Live | website design company in kerala, website development kerala |
| /services/branding/ | Live | branding agency kerala, logo design, creative agency |
| /services/lead-generation/ | **Missing, P2** | lead generation agency kerala |
| /services/local-seo/ | **Missing, P2** | local seo kerala, google maps ranking |
| /services/google-ads/ | **Missing, blocked** (confirm it is sold) | google ads agency kerala, ppc agency kerala |
| /services/content-marketing/ | Later (P3) | content marketing kerala |
| Video production | Not planned unless confirmed as a service | — |

**Locations** (15 live, 5 possible)
- Live: Kerala, Kannur, Payyanur, Thalassery, Taliparamba, Kasaragod, Kanhangad, Kozhikode, Vadakara, Kochi, Thrissur, Trivandrum, Malappuram, Palakkad, Wayanad.
- Possible district pages (P2–P3), each with a real local angle, never a template swap: Kottayam (education, hospitals, NRI families), Kollam (cashew and seafood exporters), Alappuzha (houseboats and backwater resorts), Idukki (Munnar and Thekkady resorts, homestays), Pathanamthitta (NRI households, Thiruvalla hospitals, Sabarimala season).
- **Towns get sections, not pages.** Kakkanad, Aluva, Thrippunithura, Perumbavoor, Muvattupuzha and Angamaly go in a "Areas we cover" section on the Kochi page. Guruvayur and Irinjalakuda go on Thrissur; Tirur, Manjeri, Perinthalmanna, Kottakkal, Kondotty and Nilambur on Malappuram; Koyilandy on Kozhikode; Kalpetta, Sulthan Bathery and Mananthavady on Wayanad; Ottapalam on Palakkad; Punalur, Changanassery, Cherthala, Adoor, Thiruvalla and Munnar on their district pages. Standalone pages for these would be doorway pages, since Brandvo has no clients or office there.

**Service x city** (P2; built only where Brandvo has proof)
| Page | Proof |
|---|---|
| /seo-company-in-kannur/ | based in Kannur district; Unicorn Bakes, Land4Sale |
| /social-media-marketing-agency-in-kannur/ | Unicorn Bakes case study |
| /website-design-company-in-kannur/ | Payyanur clients |
| /seo-company-in-kochi/, /social-media-marketing-agency-in-kochi/ | Playbox Club |
| /seo-company-in-kozhikode/, /social-media-marketing-agency-in-kozhikode/ | Ruyah by Naas |

Any further combination should wait until Search Console shows impressions for it.

**Industries**
| Page | Status | Proof |
|---|---|---|
| /industries/real-estate/ | Live, thin, expand | SAJ Realty, Land4Sale Payyanur |
| /industries/healthcare/ | Live | (no named client) |
| /industries/beauty-and-salons/ | Live | Ruyah by Naas |
| /industries/food-and-restaurants/ | **Missing, P2** | Unicorn Bakes |
| Hospitality and tourism, education, ecommerce | Guides first, pages when there is a client | — |

**Case studies (/work/)**: Unicorn Bakes is live. Next, if Hola can share real numbers: Ruyah by Naas, SAJ Realty or Land4Sale, Playbox Club.

### 6.3 Content plan (pillars and supporting posts)

| Pillar (commercial page) | Supporting guides (✓ = live) |
|---|---|
| Kerala page + homepage | ✓ How to choose an agency in Kerala; ✓ Digital marketing cost in Kerala; ✓ SEO vs Meta Ads vs Google Ads; How to grow a business in Kerala with digital marketing; Seasonal: Onam / Vishu / wedding-season marketing calendar |
| /services/seo/ + /services/local-seo/ | ✓ GBP optimisation; ✓ AI Overviews for local business; How to rank on Google Maps in Kerala; How to get more Google reviews (without breaking rules); SEO cost in Kerala |
| /services/meta-ads/ + /services/lead-generation/ | Meta Ads cost in India / Kerala; Lead generation with Meta Ads and WhatsApp; Click-to-WhatsApp ads guide |
| /services/social-media-marketing/ | Instagram marketing for small businesses in Kerala; Reels ideas for local businesses; Malayalam vs English content |
| /services/website-design/ | ✓ Website cost in Kerala; Why every Kerala business needs a website (and when it doesn't) |
| Industry pages | Digital marketing for clinics and hospitals; for restaurants and bakeries (Unicorn Bakes); for real estate; for resorts and homestays; for schools and coaching centres |

Cadence: 2–4 posts a month, each 1,200–2,000 words, written from Brandvo's own experience and linking to one service page and one or two location pages with natural anchors.

The full keyword-level mapping (594 rows) is in the CSV, under the `RecommendedPage` and `PageStatus` columns.

---

## 7. Prioritised implementation list

| # | Task | Impact | Effort | Who |
|---|---|---|---|---|
| 1 | Create and verify Google Business Profile (Payyanur address), categories "Marketing agency" + "Internet marketing service", service area of North Kerala districts | Very high | Low | **Hola** (I can draft every field) |
| 2 | Ask 7 existing clients for genuine Google reviews | Very high | Low | **Hola** (I can draft the WhatsApp message) |
| 3 | GA4 + GTM with events: whatsapp_click, phone_click, form_submit, email_click; mark them as key events; link GA4 to Search Console | High | Low | Claude after Hola creates GA4 (or shares access) |
| 4 | Internal linking: homepage services link to service pages; footer lists all services, locations, industries and the case study; breadcrumbs; /services/ and /industries/ hubs | High | Low | Claude |
| 5 | Expand Social Media Marketing, Performance Marketing and Real Estate pages | High | Medium | Claude |
| 6 | /about/ page with founders and real credentials (fixes the entity confusion) | Medium-High | Low | Claude, with facts from Hola |
| 7 | /services/lead-generation/, /services/local-seo/, /industries/food-and-restaurants/ | Medium-High | Medium | Claude |
| 8 | Citations: Justdial, Sulekha, IndiaMART, Bing Places, Apple Business Connect, Clutch, GoodFirms, DesignRush, with identical name, address and phone (NAP) | High | Medium | Hola (accounts), Claude (copy) |
| 9 | 7 service x city pages (section 6.2) | Medium | Medium | Claude |
| 10 | Search Console: request indexing for the 22 newer URLs; check coverage | Medium | Low | Hola's browser |
| 11 | 2–4 guides a month | Medium (compounding) | Ongoing | Claude |
| 12 | District pages for Kottayam, Kollam, Alappuzha, Idukki, Pathanamthitta (with local angles) | Low-Medium | Medium | Claude, month 3+ |
| 13 | Google Ads page (if sold); pricing section (if approved) | Medium | Low | Needs Hola's decision |
| 14 | More case studies with numbers | High | Depends on client data | Hola supplies numbers |

---

## 8. Roadmap

Rankings are not guaranteed. The timelines below are what is realistic for a new domain (DR 0) in a local market.

**Days 1–30 (to 19 Dec 2026): foundation**
- GBP live and verified; first 10 reviews.
- GA4 + GTM + conversion events live; GA4 linked to Search Console.
- Internal linking fix, hubs, breadcrumbs; About page.
- Expand the three thin money pages.
- Justdial, Sulekha, Bing Places, Apple Business Connect listings with consistent NAP.
- 2 guides (How to rank on Google Maps in Kerala; Meta Ads cost in Kerala).
- Baseline report: Search Console impressions and positions per page, and indexed pages.
- *Expected by day 30:* all 38+ pages indexed; Brandvo in the Payyanur map pack if the GBP is verified; first impressions for Kannur and Payyanur terms.

**Days 31–60 (to 18 Jan 2027): service depth**
- Lead Generation, Local SEO and Food & Restaurants pages; Google Ads page if confirmed.
- First 4 service x city pages (Kannur SEO, Kannur social media, Kochi social media, Kozhikode social media).
- Clutch, GoodFirms, DesignRush, KSUM and Startup India (if eligible) profiles; client-site credits.
- 3 guides; a second case study if numbers are available.
- First monthly report; adjust titles on pages with impressions but low CTR.
- *Expected:* Kannur and Payyanur long-tail terms in the top 20–30; first organic enquiries tracked.

**Days 61–90 (to 17 Feb 2027): Kerala reach**
- Remaining 3 service x city pages; 2 district pages with real angles (Kottayam, Alappuzha or Idukki).
- Grow the Kerala pillar toward ~1,500 words, with a second case study and pricing (if approved).
- Local PR: a Unicorn Bakes growth story pitched to Kerala business media; a guest article on a Kerala startup or SME blog.
- 3–4 guides. Review GBP insights and reviews (target 20+).
- *Expected:* top 10 for some Payyanur and Kannur terms; DR above 5 with 10–20 genuine referring domains.

**Months 4–6 (to May 2027): authority and optimisation**
- Refresh pages using Search Console query data: build what has impressions, merge or prune what has none.
- Remaining district pages only where demand shows.
- Industry guides cluster (clinics, real estate, tourism, education); a seasonal Vishu campaign post by March.
- Quarterly competitor check (Pappayas, Klyqin, Bisaura, Progbiz, Rayans): new pages, titles, map pack.
- *Realistic 6-month target:* consistent top-10 rankings and map pack for Payyanur and Kannur-area terms; page 1–2 for North Malabar town terms; first Kerala-wide service terms on pages 2–3; organic enquiries measured monthly. Metro head terms (Kochi, Kozhikode, Kerala) usually take longer than 6 months against DR 40+ agencies.

---

## 9. Local SEO plan

- **GBP:** business name exactly "Brandvo Digital Co." (no keywords added: keyword-stuffed names risk suspension). Payyanur address only, the real one; never Kochi or Kannur addresses Brandvo doesn't have. Primary category "Marketing agency"; secondary "Internet marketing service", "Advertising agency", "Website designer", "Graphic designer" (only if offered). Service areas: Kannur, Kasaragod, Kozhikode, Wayanad, Malappuram districts (GBP allows up to 20). Services list mirroring /services/. Real photos (team, office, shoots), weekly posts, Q&A seeded with real FAQs. Website link to the homepage, or UTM-tagged so GA4 separates GBP traffic.
- **Reviews:** ask every current client personally, with a direct review link; never incentivise; reply to every review within 48 hours, naming the service. Target 10 in 30 days and 25 in 90 days (Payyanur pack competitors had 13–24 on 16 Nov).
- **NAP consistency:** one phone format across all listings: call number +91 62354 34787, WhatsApp +91 62820 70376, email info@brandvodigital.com. Clean up the stray details the AI Overview showed on 16 Nov (+91 94955 36480, brandvodigitalco.info@gmail.com, about.me/brandvod, second Facebook page) once Hola confirms which are old.
- **Citations (priority order):** Justdial, Sulekha, IndiaMART, Bing Places, Apple Business Connect, Facebook page address, LinkedIn page address, Clutch, GoodFirms, DesignRush, Kerala Startup Mission / Startup India (if eligible), local chamber or trade association listings in Kannur.
- **Location pages:** keep each one unique. Never say Brandvo has an office outside Payyanur. Add real local proof as it comes in.

## 10. Backlink plan

Legitimate sources only: no paid link packages, PBNs or automated links.
1. **Client credits** (7 possible): a "Website / marketing by Brandvo Digital Co." footer credit or a case-study link on client sites, with each client's permission.
2. **Profiles with real review value:** Clutch, GoodFirms, DesignRush, Sortlist, Google Partners (if certified), Meta Business Partners (if eligible).
3. **Kerala startup ecosystem:** Kerala Startup Mission, Startup India, TiE Kerala events, Kannur and Malabar chamber of commerce.
4. **PR with real numbers:** the Unicorn Bakes ₹8L→₹95L story pitched to Kerala business and startup media and local news portals; founder interviews.
5. **Guest expertise:** articles for Kerala SME, real estate or hospitality association blogs and newsletters (for example, a guide to Meta lead ads for real-estate developers).
6. **Linkable assets:** a free "Kerala business digital marketing cost calculator" or a "Kerala festival marketing calendar" that others cite.
7. **Competitor link research:** needs Ahrefs Site Explorer (paid). Once available, filter Progbiz and Haris&Co referring domains for Kerala directories, media and associations.

Target: 10–20 relevant referring domains in 90 days, quality over count.

## 11. Analytics and tracking plan

1. **GA4 property** "brandvodigital.com" (Hola creates it in their Google account, or adds Claude's working account).
2. **GTM container** on every page (static pages and the SPA). Triggers and events:
   - `whatsapp_click`: clicks on links containing wa.me
   - `phone_click`: clicks on tel: links
   - `email_click`: clicks on mailto: links
   - `form_submit`: Netlify form success (thank-you state or submit event)
   - `cta_click`: "Book a Strategy Call" buttons, with page path and button text as parameters
   Mark the first four as key events (conversions).
3. **Link GA4 to Search Console**, and send GBP's website link with UTMs (utm_source=google&utm_medium=organic&utm_campaign=gbp).
4. **Ask on the form "How did you hear about us?"** so WhatsApp leads can be attributed, since WhatsApp chats can't be tracked past the click.
5. **Lead log** (simple sheet): date, source, landing page, service, city, qualified (Y/N), won (Y/N), value.
6. **Consent:** a light cookie notice, with GA4 consent mode set to analytics only.

## 12. Monthly reporting template

See `brandvo-monthly-seo-report-template.csv`. Sections: Search Console totals (clicks, impressions, CTR, average position), indexed pages, tracked keyword positions (top 30 from the CSV), organic key events by type, organic conversion rate, top landing pages by enquiries, city-level and service-level performance, GBP (calls, website clicks, direction requests, reviews), new referring domains, work completed, next month's plan.

## 13. Open questions for Hola

1. Will you create the Google Business Profile at the Payyanur address? I can prepare every field.
2. Does Brandvo sell **Google Ads** management? And **video production**? (Decides two pages.)
3. OK to publish **starting prices** or packages? (Pappayas and Progbiz show them.)
4. Can you create a **GA4 property**, or give access, so I can add tracking?
5. Are +91 94955 36480, brandvodigitalco.info@gmail.com, about.me/brandvod and Facebook page 61589250814076 old Brandvo details we should clean up?
6. Real numbers for a second case study (Ruyah by Naas, SAJ Realty, Land4Sale or Playbox Club)?
7. Founders' real credentials for the About page (years of experience, certifications, previous work)?
8. Keyword volumes: is an Ahrefs upgrade or a Google Ads Keyword Planner export possible?
