#!/usr/bin/env python3
"""Build brandvo-kerala-keyword-database-v3.csv (20 Nov 2026) from v2.

What v3 adds (Kerala-wide master prompt, 20 Nov 2026):
- Four patterns v2 did not have, for every town: "best digital marketing agency in {c}",
  "seo agency in {c}", "social media management company in {c}", "performance marketing agency in {c}".
- Mattannur (Kannur district), which v2 did not list.
- Page statuses refreshed for pages built on 19-20 Nov (local SEO, lead generation, about,
  expanded SMM/performance/real estate, deepened Kannur/Payyanur/Kasaragod/Kozhikode pages).
- A CompetitorEvidence column for Kannur-district rows (Takees, Moris Media, Sinaura).
No metrics are invented: search volume and KD stay "Unavailable" (Ahrefs free plan).
"""
import csv, re

SRC = '/mnt/project-files/seo-2026-11/brandvo-kerala-keyword-database-v2.csv'
OUT = '/mnt/project-files/seo-2026-11/2026-11-20-kerala-wide/brandvo-kerala-keyword-database-v3.csv'
UNAV3 = 'Unavailable (Ahrefs free plan, rechecked 20 Nov 2026)'

rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
fields = list(rows[0].keys()) + ['CompetitorEvidence', 'V3Change']
for r in rows:
    r['CompetitorEvidence'] = ''
    r['V3Change'] = ''

BUILT = {  # page -> new status (built on branch, not yet deployed unless noted)
    '/services/local-seo/': 'Built 19 Nov (branch, awaiting deploy)',
    '/services/lead-generation/': 'Built 19 Nov (branch, awaiting deploy)',
    '/about/': 'Built 19 Nov (branch, awaiting deploy)',
}
EXPANDED = {
    '/services/social-media-marketing/': 'Live; expanded to ~1,050 words 19 Nov (branch, awaiting deploy)',
    '/services/performance-marketing/': 'Live; expanded to ~930 words 19 Nov (branch, awaiting deploy)',
    '/industries/real-estate/': 'Live; expanded to ~840 words 19 Nov (branch, awaiting deploy)',
    '/digital-marketing-agency-in-kannur/': 'Live; deepened to ~1,400 words 20 Nov (branch, awaiting deploy)',
    '/digital-marketing-agency-in-payyanur/': 'Live; deepened 20 Nov (branch, awaiting deploy)',
    '/digital-marketing-agency-in-kasaragod/': 'Live; deepened 20 Nov (branch, awaiting deploy)',
    '/digital-marketing-agency-in-kozhikode/': 'Live; deepened 20 Nov (branch, awaiting deploy)',
}
for r in rows:
    page = r['RecommendedPage']
    for p, st in BUILT.items():
        if p in page and ('MISSING' in page or r['PageStatus'].startswith('Missing')):
            r['RecommendedPage'] = page.replace(' (MISSING: team and founders page)', '').replace(' (MISSING)', '')
            r['PageStatus'] = st
            r['V3Change'] = 'Status refreshed'
    for p, st in EXPANDED.items():
        if r['RecommendedPage'].split(' ')[0] == p and r['PageStatus'].startswith('Live'):
            r['PageStatus'] = st
            r['V3Change'] = 'Status refreshed'
    r['SearchVolume'] = r['KeywordDifficulty'] = UNAV3

KANNUR_EVIDENCE = ('Google SERP 17 Nov 2026 (person\'s browser, personalised): takees.in #1 (homepage, title "Digital Marketing Agency in Kannur"), '
                   'morismedia.in #7 (programmatic page, 13 H1s); map pack Bisaura, Sinaura, Stellent. Brandvo not in top 20. Not re-checked 20 Nov (no browser).')

def town_of(r):
    m = re.match(r'(.+?) \(', r['LocationRelevance'])
    return m.group(1) if m else ''

base = {}
for r in rows:
    if r['Cluster'].startswith('Location x'):
        t = town_of(r)
        k = r['Keyword']
        if k == f'digital marketing agency in {t.lower()}': base.setdefault(t, {})['dm'] = r
        if k == f'seo company in {t.lower()}': base.setdefault(t, {})['seo'] = r
        if k == f'social media marketing agency in {t.lower()}': base.setdefault(t, {})['smm'] = r
        if t in ('Kannur', 'Payyanur', 'Thalassery', 'Taliparamba') and r['Cluster'] == 'Location x Digital marketing':
            r['CompetitorEvidence'] = KANNUR_EVIDENCE if t == 'Kannur' else ''

# Mattannur: section on the Kannur page (added 20 Nov), cloned from Taliparamba's shape
if 'Mattannur' not in base:
    for kind, tmpl in base['Taliparamba'].items():
        n = dict(tmpl)
        n['Keyword'] = tmpl['Keyword'].replace('taliparamba', 'mattannur')
        n['LocationRelevance'] = 'Mattannur (Kannur district)'
        n['EstimatedCompetition'] = 'Low (estimate: small town near Kannur International Airport)'
        n['Priority'] = 'P3'
        n['RecommendedPage'] = '/digital-marketing-agency-in-kannur/ (section: Mattannur)' if kind == 'dm' else '/digital-marketing-agency-in-kannur/ (section: Mattannur) + ' + tmpl['RecommendedPage'].split('+ ')[-1]
        n['PageStatus'] = 'Section on Kannur page (built 20 Nov, branch)'
        n['ContentType'] = 'Section of district page'
        n['Notes'] = 'Airport-area hotels, travel, real estate and new retail. No standalone page without a local client.'
        n['DemandSignal'] = ''
        n['CompetitorEvidence'] = ''
        n['V3Change'] = 'New town'
        rows.append(n)
        base.setdefault('Mattannur', {})[kind] = n

NEW = [  # (pattern, base kind, cluster, intent, value, page override for service rows)
    ('best digital marketing agency in {c}', 'dm', 'Location x Digital marketing', 'Commercial (comparison)', 'High', None),
    ('seo agency in {c}', 'seo', 'Location x SEO', 'Commercial / local (hire)', 'High', None),
    ('social media management company in {c}', 'smm', 'Location x SMM', 'Commercial / local (hire)', 'High', None),
    ('performance marketing agency in {c}', 'smm', 'Location x PERF', 'Commercial / local (hire)', 'Medium',
     ('/services/social-media-marketing/', '/services/performance-marketing/')),
]
existing = {r['Keyword'] for r in rows}
added = 0
for t, kinds in base.items():
    for pat, kind, cluster, intent, value, swap in NEW:
        kw = pat.format(c=t.lower())
        if kw in existing or kind not in kinds:
            continue
        n = dict(kinds[kind])
        n.update(Keyword=kw, Cluster=cluster, SearchIntent=intent, CommercialValue=value, DemandSignal='',
                 DataStatus='Pattern-generated: demand not verified', V3Change='New pattern (20 Nov)')
        if swap:
            n['RecommendedPage'] = n['RecommendedPage'].replace(*swap)
            n['Notes'] = 'Usually lower demand than "digital marketing agency"; target with the performance marketing page, not a new city page.'
            if n['Priority'] == 'P1': n['Priority'] = 'P2'
        if kind == 'smm' and 'management' in kw:
            n['Notes'] = 'Same intent as "social media marketing agency": serve with the SMM page; do not build a separate management page (cannibalisation).'
        if kind == 'seo':
            n['Notes'] = (n['Notes'] + ' Same intent as "seo company": one page.').strip()
        if t == 'Kannur' and kind == 'dm':
            n['CompetitorEvidence'] = KANNUR_EVIDENCE
        rows.append(n)
        existing.add(kw)
        added += 1

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print('rows', len(rows), 'added', added, 'towns', len(base))
