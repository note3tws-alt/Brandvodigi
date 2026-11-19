#!/usr/bin/env python3
"""Build brandvo-kerala-keyword-database-v2.csv (19 Nov 2026).

No keyword metrics are invented. Ahrefs keyword endpoints returned
"Insufficient plan" on 19 Nov 2026, so volume and KD are marked unavailable.
Competition is an estimate unless the row says it was observed.
"""
import csv, sys

OLD = '/mnt/project-files/seo-2026-11/brandvo-kerala-keyword-master-list.csv'
OUT = '/mnt/project-files/seo-2026-11/brandvo-kerala-keyword-database-v2.csv'

UNAV = 'Unavailable (Ahrefs free plan, 19 Nov 2026)'

LIVE = {
 'kerala': '/digital-marketing-agency-in-kerala/', 'kannur': '/digital-marketing-agency-in-kannur/',
 'payyanur': '/digital-marketing-agency-in-payyanur/', 'thalassery': '/digital-marketing-agency-in-thalassery/',
 'taliparamba': '/digital-marketing-agency-in-taliparamba/', 'kasaragod': '/digital-marketing-agency-in-kasaragod/',
 'kanhangad': '/digital-marketing-agency-in-kanhangad/', 'kozhikode': '/digital-marketing-agency-in-kozhikode/',
 'vadakara': '/digital-marketing-agency-in-vadakara/', 'kochi': '/digital-marketing-agency-in-kochi/',
 'thrissur': '/digital-marketing-agency-in-thrissur/', 'thiruvananthapuram': '/digital-marketing-agency-in-trivandrum/',
 'malappuram': '/digital-marketing-agency-in-malappuram/', 'palakkad': '/digital-marketing-agency-in-palakkad/',
 'wayanad': '/digital-marketing-agency-in-wayanad/',
}
MISSING_DISTRICT = {
 'kollam': 'cashew and seafood exporters, coastal retail, Gulf-family households',
 'kottayam': 'education hubs, hospitals, rubber and plantation trade, NRI families',
 'alappuzha': 'houseboats, backwater resorts and homestays, coir',
 'pathanamthitta': 'NRI households, Sabarimala season retail and stays, Thiruvalla hospitals',
 'idukki': 'Munnar and Thekkady resorts, homestays, spices and tea',
}

# (town, district, kind) kind: live / district-missing / section
TOWNS = [
 ('Thiruvananthapuram','Thiruvananthapuram','live'),('Trivandrum','Thiruvananthapuram','alias'),
 ('Kollam','Kollam','missing'),('Punalur','Kollam','section'),
 ('Pathanamthitta','Pathanamthitta','missing'),('Adoor','Pathanamthitta','section'),('Thiruvalla','Pathanamthitta','section'),
 ('Alappuzha','Alappuzha','missing'),('Cherthala','Alappuzha','section'),
 ('Kottayam','Kottayam','missing'),('Changanassery','Kottayam','section'),
 ('Idukki','Idukki','missing'),('Munnar','Idukki','section'),
 ('Ernakulam','Ernakulam','alias'),('Kochi','Ernakulam','live'),('Cochin','Ernakulam','alias'),
 ('Kakkanad','Ernakulam','section'),('Thrippunithura','Ernakulam','section'),('Aluva','Ernakulam','section'),
 ('Perumbavoor','Ernakulam','section'),('Muvattupuzha','Ernakulam','section'),('Angamaly','Ernakulam','section'),
 ('Thrissur','Thrissur','live'),('Guruvayur','Thrissur','section'),('Irinjalakuda','Thrissur','section'),
 ('Palakkad','Palakkad','live'),('Ottapalam','Palakkad','section'),
 ('Malappuram','Malappuram','live'),('Kottakkal','Malappuram','section'),('Manjeri','Malappuram','section'),
 ('Perinthalmanna','Malappuram','section'),('Tirur','Malappuram','section'),('Kondotty','Malappuram','section'),
 ('Nilambur','Malappuram','section'),
 ('Kozhikode','Kozhikode','live'),('Calicut','Kozhikode','alias'),('Vadakara','Kozhikode','live'),('Koyilandy','Kozhikode','section'),
 ('Wayanad','Wayanad','live'),('Kalpetta','Wayanad','section'),('Sulthan Bathery','Wayanad','section'),('Mananthavady','Wayanad','section'),
 ('Kannur','Kannur','live'),('Thalassery','Kannur','live'),('Payyanur','Kannur','live'),('Taliparamba','Kannur','live'),
 ('Kasaragod','Kasaragod','live'),('Kanhangad','Kasaragod','live'),
]
DISTRICT_PAGE = {
 'Thiruvananthapuram': LIVE['thiruvananthapuram'], 'Ernakulam': LIVE['kochi'], 'Thrissur': LIVE['thrissur'],
 'Palakkad': LIVE['palakkad'], 'Malappuram': LIVE['malappuram'], 'Kozhikode': LIVE['kozhikode'],
 'Wayanad': LIVE['wayanad'], 'Kannur': LIVE['kannur'], 'Kasaragod': LIVE['kasaragod'],
}
for d in MISSING_DISTRICT:
    DISTRICT_PAGE[d.title()] = f'/digital-marketing-agency-in-{d}/'

HOME = {'Kannur','Payyanur','Thalassery','Taliparamba','Kasaragod','Kanhangad','Vadakara'}
METRO = {'Kochi','Ernakulam','Cochin','Kozhikode','Calicut','Thiruvananthapuram','Trivandrum','Thrissur','Malappuram'}
# Cities where Brandvo has a real client or is based (proof for service x city pages)
PROOF = {'Kannur':'Unicorn Bakes, Land4Sale (Payyanur)','Payyanur':'Unicorn Bakes, Land4Sale Payyanur',
         'Kozhikode':'Ruyah by Naas','Calicut':'Ruyah by Naas','Kochi':'Playbox Club','Ernakulam':'Playbox Club','Cochin':'Playbox Club'}
# Planned service x city pages (only where proof exists)
SVC_CITY_PAGES = {
 ('seo','Kannur'):'/seo-company-in-kannur/', ('smm','Kannur'):'/social-media-marketing-agency-in-kannur/',
 ('web','Kannur'):'/website-design-company-in-kannur/',
 ('seo','Kochi'):'/seo-company-in-kochi/', ('smm','Kochi'):'/social-media-marketing-agency-in-kochi/',
 ('seo','Kozhikode'):'/seo-company-in-kozhikode/', ('smm','Kozhikode'):'/social-media-marketing-agency-in-kozhikode/',
}
ALIAS_OF = {'Trivandrum':'Thiruvananthapuram','Ernakulam':'Kochi','Cochin':'Kochi','Calicut':'Kozhikode'}

SVC_PAGE = {'seo':'/services/seo/','smm':'/services/social-media-marketing/','gads':'/services/google-ads/ (MISSING; only if Google Ads is sold)',
            'web':'/services/website-design/','brand':'/services/branding/','dm':None,'adv':None,'meta':'/services/meta-ads/'}

PATTERNS = [  # (pattern, svc, intent, value)
 ('digital marketing agency in {c}','dm','Commercial / local (hire)','High'),
 ('best digital marketing company in {c}','dm','Commercial (comparison)','High'),
 ('digital marketing company in {c}','dm','Commercial / local (hire)','High'),
 ('seo company in {c}','seo','Commercial / local (hire)','High'),
 ('seo services in {c}','seo','Commercial / transactional','High'),
 ('social media marketing agency in {c}','smm','Commercial / local (hire)','High'),
 ('google ads agency in {c}','gads','Commercial / local (hire)','Medium-High'),
 ('website development company in {c}','web','Commercial / local (hire)','High'),
 ('branding agency in {c}','brand','Commercial / local (hire)','Medium'),
 ('advertising agency in {c}','adv','Mixed (offline and online advertising)','Medium'),
]

rows = []
def add(**k):
    base = dict(Keyword='',Cluster='',SearchIntent='',SearchVolume=UNAV,KeywordDifficulty=UNAV,
                EstimatedCompetition='',LocationRelevance='',District='',CommercialValue='',Priority='',
                RecommendedPage='',PageStatus='',ContentType='',DataStatus='',DemandSignal='',Notes='')
    base.update(k); rows.append(base)

# old demand signals
old = {}
try:
    for r in csv.DictReader(open(OLD, encoding='utf8')):
        old[r['Keyword'].strip().lower()] = r
except FileNotFoundError:
    pass

def comp(town, kind):
    if town in ('Kannur',):
        return 'Medium-High (observed SERP 17 Nov 2026: takees, Pappayas, Klyqin, Progbiz, Rayans, Justdial; map pack Bisaura, Sinaura, Stellent)'
    if town in METRO: return 'High (estimate: metro, many agencies with GBP reviews)'
    if kind in ('live','alias') or town in HOME: return 'Medium (estimate)'
    if kind == 'missing': return 'Medium-Low (estimate)'
    return 'Low (estimate: small town, directories dominate)'

for town, district, kind in TOWNS:
    canon = ALIAS_OF.get(town, town)
    key = canon.lower()
    live_page = LIVE.get(key)
    for pat, svc, intent, value in PATTERNS:
        kw = pat.format(c=town.lower())
        page, status, ctype, notes = '', '', '', ''
        city_page = SVC_CITY_PAGES.get((svc, canon))
        if city_page:
            page, status = city_page, 'Missing: proposed service x city page (P2)'
            ctype = 'Service x city landing page (unique, with local proof)'
            notes = f'Proof available: {PROOF.get(canon, "")}. Until built, the city page section and {SVC_PAGE[svc]} cover it.'
        elif svc in ('dm','adv') or svc == 'dm':
            if live_page:
                page, status, ctype = live_page, 'Live', 'Location landing page'
            elif kind == 'missing':
                page, status, ctype = DISTRICT_PAGE[district], 'Missing: proposed district page (P2-P3)', 'Location landing page'
                notes = f'Build only with a genuine local angle: {MISSING_DISTRICT[district.lower()]}.'
            else:
                dp = DISTRICT_PAGE.get(district)
                page = f'{dp} (section: towns we cover)'
                status = 'Section on district page (no standalone page)' + (' - district page missing' if district.lower() in MISSING_DISTRICT else '')
                ctype = 'Section of district page'
                notes = 'No standalone page: it would be a doorway page without local clients or proof.'
            if svc == 'adv':
                notes = (notes + ' "Advertising agency" also pulls outdoor/print intent; cover it as a secondary phrase, not a separate page.').strip()
        else:
            sp = SVC_PAGE[svc]
            if live_page:
                page = f'{live_page} (service section) + {sp}'
                status = 'Partly covered: city page section links to service page' if 'MISSING' not in sp else 'Missing: Google Ads service page'
            elif kind == 'missing':
                page = f'{DISTRICT_PAGE[district]} (service section) + {sp}'
                status = 'Missing (district page not built)'
            else:
                page = f'{sp}'
                status = 'Service page only (town too small for its own page)'
            ctype = ('Service section within location page; service page is the main target' if (live_page or kind=='missing')
                     else 'Service page; town listed in its areas-served section')
        # priority
        if canon in HOME or canon == 'Kannur':
            pr = 'P1' if svc in ('dm','seo','smm','web') else 'P2'
        elif canon in METRO or town in METRO:
            pr = 'P1' if svc == 'dm' else 'P2'
        elif kind in ('live',):
            pr = 'P2' if svc == 'dm' else 'P3'
        elif kind == 'missing':
            pr = 'P2' if svc == 'dm' else 'P3'
        else:
            pr = 'P3'
        if svc == 'gads': pr = 'P3 (blocked: confirm Google Ads is sold)' if pr != 'P1' else 'P2 (blocked: confirm Google Ads is sold)'
        o = old.get(kw)
        add(Keyword=kw, Cluster=f'Location x {svc.upper() if svc!="dm" else "Digital marketing"}',
            SearchIntent=intent, EstimatedCompetition=comp(canon, kind), LocationRelevance=f'{town} ({district} district)',
            District=district, CommercialValue=value, Priority=pr, RecommendedPage=page, PageStatus=status,
            ContentType=ctype, DataStatus='Pattern-generated: demand not verified',
            DemandSignal=(o['Demand signal'] if o else ''), Notes=notes.strip())

# Kerala service clusters (brief section 3)
K = [
 # keyword, cluster, intent, value, page, status, priority, ctype
 ('digital marketing agency kerala','Primary','Commercial (hire)','High',LIVE['kerala'],'Live','P1','Pillar location page'),
 ('best digital marketing agency in kerala','Primary','Commercial (comparison)','High',LIVE['kerala'],'Live','P1','Pillar location page + /blog/best-digital-marketing-agency-in-kerala/'),
 ('top digital marketing agency in kerala','Primary','Commercial (comparison)','High',LIVE['kerala'],'Live','P2','Pillar location page'),
 ('digital marketing company kerala','Primary','Commercial (hire)','High',LIVE['kerala'],'Live','P1','Pillar location page'),
 ('digital marketing services kerala','Primary','Commercial / transactional','High',LIVE['kerala'],'Live','P1','Pillar location page'),
 ('online marketing agency kerala','Primary','Commercial (hire)','Medium',LIVE['kerala'],'Live','P2','Secondary phrase on pillar'),
 ('advertising agency kerala','Primary','Mixed','Medium',LIVE['kerala'],'Live','P3','Secondary phrase on pillar'),
 ('creative agency kerala','Primary','Commercial (hire)','Medium','/services/branding/','Live','P2','Service page'),
 ('digital marketing experts kerala','Primary','Commercial','Medium',LIVE['kerala'],'Live','P3','Secondary phrase on pillar'),
 ('digital marketing consultant kerala','Primary','Commercial','Medium','/about/ (MISSING: team and founders page)','Missing','P2','About / team page with real credentials'),
 ('seo agency kerala','SEO','Commercial (hire)','High','/services/seo/','Live','P1','Service page'),
 ('seo company kerala','SEO','Commercial (hire)','High','/services/seo/','Live','P1','Service page'),
 ('best seo company in kerala','SEO','Commercial (comparison)','High','/services/seo/','Live','P1','Service page'),
 ('seo services kerala','SEO','Commercial / transactional','High','/services/seo/','Live','P1','Service page'),
 ('seo packages kerala','SEO','Transactional','High','/services/seo/ (pricing section) or /blog/digital-marketing-cost-in-kerala/','Partly covered','P2','Pricing section'),
 ('local seo kerala','SEO','Commercial','High','/services/local-seo/ (MISSING)','Missing','P2','Service sub-page'),
 ('local seo services','SEO','Commercial','High','/services/local-seo/ (MISSING)','Missing','P2','Service sub-page'),
 ('google business profile optimization kerala','SEO','Commercial / informational','High','/blog/google-business-profile-optimization-kerala/','Live','P2','Guide'),
 ('technical seo services kerala','SEO','Commercial','Medium','/services/seo/ (section)','Partly covered','P3','Section'),
 ('ecommerce seo kerala','SEO','Commercial','Medium','/services/seo/ (section)','Partly covered','P3','Section'),
 ('seo freelancer kerala','SEO','Commercial (alternative)','Low','/services/seo/ (FAQ: agency vs freelancer)','Partly covered','P3','FAQ'),
 ('social media marketing kerala','Social','Commercial','High','/services/social-media-marketing/','Live (thin, ~400 words)','P1','Service page: expand'),
 ('social media marketing agency in kerala','Social','Commercial (hire)','High','/services/social-media-marketing/','Live (thin)','P1','Service page: expand'),
 ('social media management kerala','Social','Commercial','High','/services/social-media-marketing/','Live (thin)','P1','Service page: expand'),
 ('instagram marketing agency kerala','Social','Commercial (hire)','High','/services/social-media-marketing/ (Instagram section)','Partly covered','P2','Section'),
 ('instagram marketing services','Social','Commercial','High','/services/social-media-marketing/','Partly covered','P2','Section'),
 ('social media marketing packages kerala','Social','Transactional','High','/services/social-media-marketing/ (pricing section)','Missing','P2','Pricing section (needs Hola to approve starting prices)'),
 ('influencer marketing kerala','Social','Commercial','Medium','/services/social-media-marketing/ (influencer section) + /work/unicorn-bakes/','Partly covered','P2','Section + case study'),
 ('facebook advertising kerala','Paid','Commercial','High','/services/meta-ads/','Live','P1','Service page'),
 ('facebook ads agency kerala','Paid','Commercial (hire)','High','/services/meta-ads/','Live','P1','Service page'),
 ('meta ads agency kerala','Paid','Commercial (hire)','High','/services/meta-ads/','Live','P1','Service page'),
 ('instagram ads agency kerala','Paid','Commercial (hire)','High','/services/meta-ads/','Live','P2','Service page'),
 ('google ads agency kerala','Paid','Commercial (hire)','High','/services/google-ads/ (MISSING)','Missing (blocked: confirm Google Ads is sold)','P2','Service page'),
 ('ppc agency kerala','Paid','Commercial (hire)','High','/services/google-ads/ (MISSING)','Missing (blocked)','P2','Service page'),
 ('ppc company in kerala','Paid','Commercial (hire)','High','/services/google-ads/ (MISSING)','Missing (blocked)','P3','Service page'),
 ('performance marketing agency kerala','Paid','Commercial (hire)','High','/services/performance-marketing/','Live (thin, ~335 words)','P1','Service page: expand'),
 ('performance marketing kerala','Paid','Commercial','High','/services/performance-marketing/','Live (thin)','P1','Service page: expand'),
 ('lead generation agency kerala','Paid','Commercial (hire)','High','/services/lead-generation/ (MISSING)','Missing','P2','Service page'),
 ('lead generation services kerala','Paid','Commercial','High','/services/lead-generation/ (MISSING)','Missing','P2','Service page'),
 ('real estate lead generation kerala','Paid','Commercial','High','/industries/real-estate/','Live (thin, ~305 words)','P1','Industry page: expand'),
 ('digital advertising kerala','Paid','Commercial','Medium','/services/performance-marketing/','Live','P3','Secondary phrase'),
 ('website development kerala','Web','Commercial','High','/services/website-design/','Live','P1','Service page'),
 ('website design kerala','Web','Commercial','High','/services/website-design/','Live','P1','Service page'),
 ('web design company in kerala','Web','Commercial (hire)','High','/services/website-design/','Live','P1','Service page'),
 ('website development company in kerala','Web','Commercial (hire)','High','/services/website-design/','Live','P1','Service page'),
 ('ecommerce website development kerala','Web','Commercial (hire)','High','/services/website-design/ (ecommerce section)','Partly covered','P2','Section; separate page only once there is an ecommerce case study'),
 ('website cost in kerala','Web','Informational / commercial','High','/blog/website-cost-in-kerala/','Live','P2','Guide'),
 ('landing page design kerala','Web','Commercial','Medium','/services/website-design/ (section)','Partly covered','P3','Section'),
 ('branding agency kerala','Brand','Commercial (hire)','Medium','/services/branding/','Live','P2','Service page'),
 ('branding company in kerala','Brand','Commercial (hire)','Medium','/services/branding/','Live','P2','Service page'),
 ('logo design kerala','Brand','Transactional','Medium','/services/branding/ (logo section)','Partly covered','P3','Section'),
 ('graphic design agency kerala','Brand','Commercial (hire)','Medium','/services/branding/ (creative design section)','Partly covered','P3','Section'),
 ('content marketing kerala','Content','Commercial','Medium','/services/content-marketing/ (MISSING)','Missing','P3','Service page (later)'),
 ('content writing services kerala','Content','Commercial','Medium','/services/content-marketing/ (MISSING)','Missing','P3','Service page (later)'),
 ('video production kerala','Video','Commercial (hire)','Medium','None: confirm whether video production is a Brandvo service','Not a listed service','P3','Do not build unless confirmed'),
 ('reels production kerala','Video','Commercial','Medium','/services/social-media-marketing/ (Reels section)','Partly covered','P3','Section'),
 ('marketing consultancy kerala','Consulting','Commercial','Medium',LIVE['kerala'],'Live','P3','Secondary phrase'),
 ('whatsapp marketing kerala','Paid','Commercial','Medium','/services/performance-marketing/ (WhatsApp funnels section)','Partly covered','P3','Section'),
 ('digital marketing agency near me','Near me','Local (map pack)','High','Google Business Profile (not a page)','Missing (no GBP)','P1','GBP listing'),
 ('seo company near me','Near me','Local (map pack)','High','Google Business Profile','Missing (no GBP)','P1','GBP listing'),
 ('social media marketing agency near me','Near me','Local (map pack)','High','Google Business Profile','Missing (no GBP)','P1','GBP listing'),
 ('brandvo digital co','Brand','Navigational','High','/','Live','P1','Homepage + GBP + consistent citations'),
 ('brandvo digital payyanur','Brand','Navigational','High','/','Live','P1','Homepage; fixes AI Overview entity confusion'),
]
for kw, cl, it, val, pg, st, pr, ct in K:
    o = old.get(kw)
    add(Keyword=kw, Cluster=f'Kerala service: {cl}', SearchIntent=it,
        EstimatedCompetition=('High (observed SERP 16 Nov 2026: Haris&Co #1, Progbiz, listicles, AI Overview)' if kw in ('best digital marketing agency in kerala','digital marketing agency kerala') else 'High (estimate: statewide)' if 'kerala' in kw else 'Varies by searcher location'),
        LocationRelevance='Kerala (statewide)' if 'kerala' in kw else 'Searcher location', District='All',
        CommercialValue=val, Priority=pr, RecommendedPage=pg, PageStatus=st, ContentType=ct,
        DataStatus='Curated from brief and earlier research: demand not verified',
        DemandSignal=(o['Demand signal'] if o else ''), Notes='')

# Industries
IND = [
 ('digital marketing for real estate kerala','/industries/real-estate/','Live (thin)','P1','SAJ Realty, Land4Sale Payyanur'),
 ('real estate marketing agency kerala','/industries/real-estate/','Live (thin)','P1','SAJ Realty, Land4Sale Payyanur'),
 ('digital marketing for hospitals kerala','/industries/healthcare/','Live','P2',''),
 ('digital marketing for clinics kerala','/industries/healthcare/','Live','P2',''),
 ('dental clinic marketing kerala','/industries/healthcare/ (dental section)','Partly covered','P2',''),
 ('salon marketing kerala','/industries/beauty-and-salons/','Live','P2','Ruyah by Naas'),
 ('beauty parlour marketing ideas','/industries/beauty-and-salons/','Live','P3','Ruyah by Naas'),
 ('restaurant marketing kerala','/industries/food-and-restaurants/ (MISSING)','Missing','P2','Unicorn Bakes case study'),
 ('bakery marketing ideas','/industries/food-and-restaurants/ (MISSING) + /work/unicorn-bakes/','Missing','P2','Unicorn Bakes'),
 ('hotel digital marketing kerala','/industries/hospitality-and-tourism/ (MISSING)','Missing','P3','No client yet: guide first'),
 ('resort marketing kerala','/industries/hospitality-and-tourism/ (MISSING)','Missing','P3','No client yet: guide first'),
 ('homestay marketing kerala','/blog/ guide (MISSING)','Missing','P3','No client yet'),
 ('tourism digital marketing kerala','/blog/ guide (MISSING)','Missing','P3','No client yet'),
 ('digital marketing for schools kerala','/blog/ guide (MISSING)','Missing','P3','No client yet'),
 ('education marketing agency kerala','/blog/ guide (MISSING)','Missing','P3','No client yet'),
 ('interior design marketing kerala','/industries/ (later)','Missing','P3','K1 Kitchen Gallery'),
 ('automobile dealer marketing kerala','/industries/ (later)','Missing','P3','Auto Jota'),
 ('gaming cafe marketing','/work/ case study (later)','Missing','P3','Playbox Club'),
 ('ecommerce marketing agency kerala','/industries/ecommerce/ (later)','Missing','P3','No client case yet'),
]
for kw, pg, st, pr, proof in IND:
    add(Keyword=kw, Cluster='Industry', SearchIntent='Commercial (hire)' if 'ideas' not in kw else 'Informational',
        EstimatedCompetition='Medium-Low (estimate: few Kerala agencies have industry pages; Progbiz and Pappayas do)',
        LocationRelevance='Kerala', District='All', CommercialValue='High' if pr!='P3' else 'Medium', Priority=pr,
        RecommendedPage=pg, PageStatus=st, ContentType='Industry page or guide', DataStatus='Curated: demand not verified',
        Notes=f'Proof: {proof}' if proof else '')

# Informational / topical authority
INFO = [
 ('how to choose a digital marketing agency in kerala','/blog/best-digital-marketing-agency-in-kerala/','Live'),
 ('digital marketing cost in kerala','/blog/digital-marketing-cost-in-kerala/','Live'),
 ('how much does seo cost in india','/blog/seo-cost-in-kerala/ (MISSING)','Missing'),
 ('seo vs google ads','/blog/seo-vs-meta-ads-vs-google-ads/','Live'),
 ('how to grow a business in kerala with digital marketing','/blog/ (MISSING)','Missing'),
 ('social media marketing strategy for small business','/blog/ (MISSING)','Missing'),
 ('why every business needs a website','/blog/website-cost-in-kerala/ (section) or new post','Partly covered'),
 ('how local seo helps small businesses','/blog/ (MISSING) -> /services/local-seo/','Missing'),
 ('instagram marketing tips for small business','/blog/ (MISSING)','Missing'),
 ('google business profile optimization','/blog/google-business-profile-optimization-kerala/','Live'),
 ('how to rank on google maps','/blog/ (MISSING) -> GBP guide cluster','Missing'),
 ('how to get more google reviews','/blog/ (MISSING)','Missing'),
 ('meta ads lead generation','/blog/ (MISSING) -> /services/meta-ads/','Missing'),
 ('meta ads cost in india','/blog/ (MISSING) -> /services/meta-ads/','Missing'),
 ('whatsapp business marketing tips','/blog/ (MISSING)','Missing'),
 ('digital marketing trends 2027','/blog/ (later; low lead value)','Missing'),
 ('seo for tourism business kerala','/blog/ (MISSING)','Missing'),
 ('digital marketing for hospitals and clinics','/industries/healthcare/','Live'),
 ('digital marketing for restaurants','/blog/ (MISSING) -> food industry page','Missing'),
 ('digital marketing for real estate','/industries/real-estate/','Live (thin)'),
 ('digital marketing for educational institutions','/blog/ (MISSING)','Missing'),
 ('how to appear in google ai overviews','/blog/google-ai-overviews-for-local-business-kerala/','Live'),
 ('onam marketing ideas','/blog/ (MISSING, seasonal: publish by July)','Missing'),
 ('vishu offers marketing ideas','/blog/ (seasonal: publish by March)','Missing'),
]
for kw, pg, st in INFO:
    add(Keyword=kw, Cluster='Informational / topical authority', SearchIntent='Informational',
        EstimatedCompetition='Medium (estimate: national publishers compete; Kerala angle narrows it)',
        LocationRelevance='Kerala / India', District='All', CommercialValue='Medium',
        Priority='P2' if st=='Missing' else 'P3', RecommendedPage=pg, PageStatus=st, ContentType='Blog guide',
        DataStatus='Curated: demand not verified')

# Malayalam / Manglish watchlist
ML = [
 ('ഡിജിറ്റൽ മാർക്കറ്റിംഗ്','Malayalam script'),('ഡിജിറ്റൽ മാർക്കറ്റിംഗ് കോഴ്സ്','Malayalam script (course intent: not a lead)'),
 ('digital marketing malayalam','Manglish (mostly learners/courses)'),('seo malayalam','Manglish (mostly learners)'),
 ('instagram marketing malayalam','Manglish'),('business engane valarthaam','Transliterated Malayalam'),
 ('online business ideas malayalam','Manglish (informational)'),('meta ads malayalam','Manglish (mostly tutorials)'),
]
for kw, note in ML:
    add(Keyword=kw, Cluster='Malayalam / Manglish watchlist', SearchIntent='Mostly informational / learning',
        EstimatedCompetition='Unknown', LocationRelevance='Kerala', District='All', CommercialValue='Low',
        Priority='Watchlist (do not target yet)', RecommendedPage='None until Search Console or Keyword Planner shows demand',
        PageStatus='Not planned', ContentType='Possibly Malayalam Reels/YouTube rather than web pages',
        DataStatus='Unverified: listed only to test; brief says include only with proven demand', Notes=note)

# de-dup
seen=set(); out=[]
for r in rows:
    k=r['Keyword'].lower()
    if k in seen: continue
    seen.add(k); out.append(r)
cols=['Keyword','Cluster','SearchIntent','SearchVolume','KeywordDifficulty','EstimatedCompetition','LocationRelevance','District',
      'CommercialValue','Priority','RecommendedPage','PageStatus','ContentType','DataStatus','DemandSignal','Notes']
with open(OUT,'w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(out)
from collections import Counter
print(len(out)); print(Counter(r['Priority'] for r in out)); print(Counter(r['PageStatus'].split(':')[0].split(' (')[0] for r in out).most_common())
