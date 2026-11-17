"""Step 1: copy live snapshot, patch the JS bundle, optimise images, write homepage head."""
import shutil, os, re, json, sys
from PIL import Image
SRC = sys.argv[1]; OUT = sys.argv[2]
if os.path.exists(OUT): shutil.rmtree(OUT)
shutil.copytree(SRC, OUT)
os.chmod(OUT, 0o755)
for root, ds, fs in os.walk(OUT):
    for d in ds: os.chmod(os.path.join(root, d), 0o755)
    for f in fs: os.chmod(os.path.join(root, f), 0o644)

js_old = 'assets/index-rwkBGRtk.js'
s = open(os.path.join(OUT, js_old)).read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (old[:80], n)
    s = s.replace(old, new)

# 1. service pages on the four services that have one
for title, page in [("Social Media Management", "/services/social-media-marketing/"),
                    ("Social Media Marketing", "/services/social-media-marketing/"),
                    ("Meta Ads", "/services/meta-ads/"),
                    ("Performance Marketing", "/services/performance-marketing/")]:
    rep(f'title:"{title}",chips:', f'title:"{title}",page:"{page}",chips:')
# 2. service cards link to their page
rep('i.jsxs("a",{href:"#contact",onPointerMove:Pp,', 'i.jsxs("a",{href:l.page||"#contact",onPointerMove:Pp,')
rep('children:["Discuss this",', 'children:[l.page?"Learn more":"Discuss this",')
# 3. footer: service links + locations list
rep('Wn.slice(0,6).map(e=>i.jsx("li",{children:i.jsx("a",{href:"/#services",className:Ot,children:e.title})},e.title))})]})',
    'Wn.slice(0,6).map(e=>i.jsx("li",{children:i.jsx("a",{href:e.page||"/#services",className:Ot,children:e.title})},e.title))}),'
    'i.jsx("h3",{className:cl+" mt-8",children:"Locations & industries"}),'
    'i.jsx("ul",{className:"mt-4 space-y-2.5",children:Lx.map(e=>i.jsx("li",{children:i.jsx("a",{href:e[1],className:Ot,children:e[0]})},e[1]))})]})')
rep('const cl="font-display text-sm font-semibold text-white"',
    'const Lx=[["Digital marketing in Kerala","/digital-marketing-agency-in-kerala/"],["Digital marketing in Kannur","/digital-marketing-agency-in-kannur/"],["Digital marketing in Payyanur","/digital-marketing-agency-in-payyanur/"],["Real estate marketing","/industries/real-estate/"]],cl="font-display text-sm font-semibold text-white"')
# 4. copy with location context
rep('"Brandvo Digital combines creative strategy, content, social media and paid advertising to help businesses grow, with every post and every ad built to earn a result."',
    '"Brandvo Digital is a Payyanur-based digital marketing agency helping businesses across Kerala grow with creative strategy, content, social media and paid advertising, with every post and every ad built to earn a result."')
rep('"Brandvo Digital Co. is a performance-driven digital marketing and creative agency. We help businesses build a strong online presence, generate qualified leads and turn attention into revenue."',
    '"Brandvo Digital Co. is a performance-driven digital marketing and creative agency based in Payyanur, Kerala. We help businesses across Kerala build a strong online presence, generate qualified leads and turn attention into revenue."')
rep('"A performance-driven digital marketing and creative agency helping businesses get seen, chosen and remembered."',
    '"A performance-driven digital marketing and creative agency in Payyanur, Kerala, helping businesses get seen, chosen and remembered."')
rep('"Brandvo Digital Co. | Digital Marketing & Creative Agency"', '"Digital Marketing Agency in Kerala | Brandvo"')

# Internal links from blog posts to the location and service pages (17 Nov 2026)
rep("Brandvo Digital Co. is based in Payyanur in Kannur district. We work with local businesses on social media marketing, Meta Ads, SEO, branding and web design, and we build strategy, creative and campaigns together. If you are shortlisting",
    "Brandvo Digital Co. is based in [Payyanur](/digital-marketing-agency-in-payyanur/) in Kannur district. We work with local businesses on social media marketing, Meta Ads, SEO, branding and web design, and we build strategy, creative and campaigns together. See what we do as a [digital marketing agency in Kannur](/digital-marketing-agency-in-kannur/). If you are shortlisting")
rep("Brandvo Digital Co. is a performance-driven agency based in Payyanur, Kannur, working across social media marketing, Meta Ads, SEO,",
    "Brandvo Digital Co. is a performance-driven [digital marketing agency in Kerala](/digital-marketing-agency-in-kerala/), based in Payyanur, Kannur, working across [social media marketing](/services/social-media-marketing/), [Meta Ads](/services/meta-ads/), SEO,")
rep("Brandvo Digital Co. plans SEO, Meta Ads, Google campaigns", "Brandvo Digital Co. plans SEO, [Meta Ads](/services/meta-ads/), Google campaigns")
rep("strategy, creativity and performance should work as a single system", "strategy, creativity and [performance marketing](/services/performance-marketing/) should work as a single system")

# Seobility fixes (16 Nov 2026): alt text on every image, spaces in split headings
rep('alt:r<e.length?n.name:"",loading:"lazy"', 'alt:n.name+" logo",loading:"lazy"')
rep('alt:h?`${c.name}, ${ho(c)}`:"",width:"720"', 'alt:`${c.name}, ${ho(c)}`,width:"720"')
rep('{src:e.image,alt:"",width:"44"', '{src:e.image,alt:e.name,width:"44"')
rep('{src:"/logo-mark.png",alt:"",width:"306",height:"516",fetchpriority', '{src:"/logo-mark.png",alt:"Brandvo Digital Co. logo",width:"306",height:"516",fetchpriority')
rep('{src:"/logo-mark.png",alt:"",width:"306",height:"516",loading', '{src:"/logo-mark.png",alt:"Brandvo Digital Co.",width:"306",height:"516",loading')
for a in ["Everything You Need", "A Clear Path", "Brands Love"]:
    rep(f'"{a}",i.jsx("br",{{}})', f'"{a} ",i.jsx("br",{{}})')
# 5. optimised images
imgs = {}
for p, maxw in [("clients/gallery.png", 640), ("clients/land4sale-payyanur.png", 640), ("clients/saj-realty.png", 640),
                ("clients/auto-jota.png", 640), ("work/ruyah-by-naas.png", 640), ("work/unicorn-bakes.png", 640),
                ("testimonials/saj-realty.jpg", 320), ("testimonials/jishnu-playbox-club.jpg", 320),
                ("testimonials/abhishek-unicorn-bakes.jpg", 320)]:
    im = Image.open(os.path.join(OUT, p))
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    newp = re.sub(r'\.(png|jpg)$', '.webp', p)
    im.save(os.path.join(OUT, newp), 'WEBP', quality=82, method=6)
    imgs[p] = (os.path.getsize(os.path.join(OUT, p)), os.path.getsize(os.path.join(OUT, newp)))
    rep(f'"/{p}"', f'"/{newp}"')
print(json.dumps(imgs, indent=0))

# The pre-rendered HTML is for crawlers; on load React replaces it with a fresh
# client render instead of hydrating (hydrating would mismatch on animations).
rep('dl.hasChildNodes()?Ac(dl,vo):Mc(dl).render(vo);', 'Mc(dl).render(vo);')

import hashlib
js_new = 'assets/index-bv' + hashlib.sha1(s.encode()).hexdigest()[:8] + '.js'  # content-hashed so caches never serve an old bundle
open(os.path.join(OUT, js_new), 'w').write(s)
os.remove(os.path.join(OUT, js_old))
# point every html at the new bundle
for root, ds, fs in os.walk(OUT):
    for f in fs:
        if f.endswith('.html'):
            p = os.path.join(root, f); h = open(p).read()
            if js_old in h:
                open(p, 'w').write(h.replace('/' + js_old, '/' + js_new))
print('bundle ok', len(s))
