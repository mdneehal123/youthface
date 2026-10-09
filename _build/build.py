#!/usr/bin/env python3
"""Builds the Youth Face static store into the repository root.
Every public address of the old WordPress site is kept, so search engines see no broken links."""
import json, os, html, shutil

B = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(B)
SITE = 'https://youthfacebeautycream.com'
OLD = 'https://youthfacebeautycream.com'   # images are read from here until the files are added to this repo
WA = '919980881230'
WA_SHOW = '+91 99808 81230'
OWNER = 'Beauty Mart'
ADDR = 'Azad Nagar, 4th Cross, Bhatkal, Uttara Kannada, Karnataka 581320, India'
TODAY = '2026-10-09'
GOOGLE_ADS = ''        # e.g. AW-XXXXXXXXXX when Youth Face gets its own Google Ads account
META_PIXEL = ''        # Meta Pixel ID for Youth Face, when there is one
GSC_FILE = ''          # Search Console verification file name, if one is used

UP = '/wp-content/uploads/2026/10/'


def img(name):
    """Same path as the old site. Served from this repo when the file is present, otherwise from the old site."""
    local = os.path.join(ROOT, UP.strip('/'), name)
    return (UP if os.path.exists(local) else OLD + UP) + name


PRODUCTS = [
    dict(id='p1', wc=16, slug='youth-face-beauty-cream-25g-pack-of-1-kojic-acid-alpha-arbutin', short='youth-face-beauty-cream-25g',
         name='Youth Face Beauty Cream 25g – Pack of 1', card='Beauty Cream · Pack of 1', size='1 × 25 g jar', price=549, mrp=899, badge='',
         sku='YFB-CREAM-25',
         title='Buy Youth Face Beauty Cream 25g – Pack of 1 (Original) | Kojic Acid & Alpha Arbutin',
         desc='Buy the original Youth Face Beauty Cream 25g with Kojic Acid & Alpha Arbutin, direct from the brand. ₹549, Cash on Delivery available, ships from Bhatkal.',
         imgs=['Youth-Face-Beauty-Cream-25g.png', 'ChatGPT-Image-Sep-15-2026-05_56_58-PM-1.png', '6be0a814-b1de-412c-98cd-06647184de2d.jpg'],
         thumb='Youth-Face-Beauty-Cream-25g-600x600.png'),
    dict(id='p2', wc=17, slug='youth-face-beauty-cream-pack-of-2-kojic-acid-alpha-arbutin', short='youth-face-beauty-cream-pack-of-2',
         name='Youth Face Beauty Cream Pack of 2 – Kojic Acid & Alpha Arbutin', card='Beauty Cream · Pack of 2', size='2 × 25 g jars (50 g)', price=999, mrp=1599, badge='Most popular',
         sku='YFB-CREAM-25x2',
         title='Youth Face Beauty Cream Pack of 2 | Kojic Acid & Alpha Arbutin',
         desc='Buy Youth Face Beauty Cream Pack of 2 with Kojic Acid & Alpha Arbutin online in India. 2 × 25g jars for your daily skincare routine. ₹999, COD available.',
         imgs=['ChatGPT-Image-Sep-17-2026-08_27_12-PM.png', '9c791416-0b6d-4985-8465-48bb4a913b23.jpg', '55e4f26b-d70e-42f0-bc88-0ea37c533cb6.jpg', '319c2295-d196-4a76-9f95-1a0316f45f67.jpg'],
         thumb='ChatGPT-Image-Sep-17-2026-08_27_12-PM-600x600.png'),
    dict(id='p3', wc=18, slug='youth-face-beauty-cream-pack-of-3-kojic-acid-alpha-arbutin', short='youth-face-beauty-cream-pack-of-3',
         name='Youth Face Beauty Cream Pack of 3 – Kojic Acid & Alpha Arbutin', card='Beauty Cream · Pack of 3', size='3 × 25 g jars (75 g)', price=1444, mrp=1899, badge='Best value',
         sku='YFB-CREAM-25x3',
         title='Youth Face Beauty Cream Pack of 3 | Kojic Acid & Alpha Arbutin',
         desc='Youth Face Beauty Cream Pack of 3: three 25g jars with Kojic Acid & Alpha Arbutin. ₹1,444, best value per jar, free shipping and Cash on Delivery.',
         imgs=['Youth-Face-Beauty-Cream-skincare-product-for-dark-spot-care.png', '6be0a814-b1de-412c-98cd-06647184de2d.jpg', 'ba3e3a86-0e0f-41bb-93da-3e0e1d486bee.jpg', 'ChatGPT-Image-Sep-15-2026-05_56_58-PM-1.png', 'ChatGPT-Image-Sep-15-2026-05_51_41-PM.png'],
         thumb='Youth-Face-Beauty-Cream-skincare-product-for-dark-spot-care-600x600.png'),
    dict(id='lotion', wc=19, slug='youth-face-body-lotion', short='',
         name='Youth Face Body Lotion', card='Body Lotion · 40 ml', size='40 ml bottle', price=599, mrp=599, badge='',
         sku='YFB-LOTION-40',
         title='Youth Face Body Lotion 40ml | Youth Face',
         desc='Youth Face Body Lotion, 40ml: a lightweight, quick-absorbing daily moisturiser for soft, comfortable skin. Order direct from Youth Face, India.',
         imgs=['ChatGPT-Image-Sep-19-2026-01_47_45-AM.png'],
         thumb='ChatGPT-Image-Sep-19-2026-01_47_45-AM-600x600.png'),
]
BYID = {p['id']: p for p in PRODUCTS}


def url(p):
    return '/product/%s/' % p['slug']


def rs(n):
    return '₹{:,}'.format(n)


def pct(p):
    return round((p['mrp'] - p['price']) * 100 / p['mrp']) if p['mrp'] > p['price'] else 0


NAV = [('/', 'Home'), ('/shop/', 'Shop'), ('/about-us/', 'About Us'), ('/contact/', 'Contact'), ('/faq/', 'FAQ'),
       ('/skincare-guides/', 'Skincare Guides'), ('/track-order/', 'Track Order'), ('/how-to-use/', 'How To Use')]
POLICIES = [('/privacy-policy/', 'Privacy Policy'), ('/terms-conditions/', 'Terms & Conditions'),
            ('/refund-returns-policy/', 'Refund & Returns'), ('/shipping-delivery/', 'Shipping & Delivery')]

CART_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 7h14l-1.2 11.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8L5 7Z"/><path d="M9 7V6a3 3 0 0 1 6 0v1"/></svg>'
MENU_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
WA_GLYPH = '<img class="wa-glyph" src="/assets/whatsapp-glyph-green.svg" alt="" width="%d" height="%d">'
BRAND = '<b>Youth</b><i>Face</i>'

pages = []


def org_graph():
    return [{
        '@type': 'Organization', '@id': SITE + '/#org', 'name': 'Youth Face', 'url': SITE + '/', 'legalName': OWNER,
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Azad Nagar, 4th Cross', 'addressLocality': 'Bhatkal',
                    'addressRegion': 'Karnataka', 'postalCode': '581320', 'addressCountry': 'IN'},
        'contactPoint': {'@type': 'ContactPoint', 'telephone': '+' + WA, 'contactType': 'customer service', 'areaServed': 'IN'}
    }, {'@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': 'Youth Face', 'publisher': {'@id': SITE + '/#org'}}]


def product_ld(p):
    return {'@type': 'Product', '@id': SITE + url(p) + '#product', 'name': p['name'], 'sku': p['sku'],
            'image': [img(i) if img(i).startswith('http') else SITE + img(i) for i in p['imgs']],
            'description': p['desc'], 'brand': {'@type': 'Brand', 'name': 'Youth Face'},
            'offers': {'@type': 'Offer', 'url': SITE + url(p), 'price': str(p['price']), 'priceCurrency': 'INR',
                       'availability': 'https://schema.org/InStock', 'itemCondition': 'https://schema.org/NewCondition',
                       'seller': {'@id': SITE + '/#org'}}}


def page(path, title, desc, body, schema=None, crumbs=None, index=True, og='website', ogimg=None, extra_head=''):
    full = SITE + path
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == path else '', t) for h, t in NAV)
    graph = org_graph()
    if crumbs:
        items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'}]
        for i, (n, u) in enumerate(crumbs):
            items.append({'@type': 'ListItem', 'position': i + 2, 'name': n, 'item': SITE + u})
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': items})
        trail = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / ' + ' / '.join(
            ('<a href="%s">%s</a>' % (u, html.escape(n)) if i < len(crumbs) - 1 else html.escape(n)) for i, (n, u) in enumerate(crumbs)) + '</nav>'
        body = '<div class="wrap">' + trail + '</div>' + body
    if schema:
        graph += schema
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    ogi = ogimg or img(PRODUCTS[0]['imgs'][0])
    if not ogi.startswith('http'):
        ogi = SITE + ogi
    tags = ''
    if GOOGLE_ADS:
        tags += '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","%s");</script>\n' % (GOOGLE_ADS, GOOGLE_ADS)
    if META_PIXEL and index:
        tags += "<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','%s');fbq('track','PageView');</script>\n" % META_PIXEL
    doc = '''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="%(robots)s">
<link rel="canonical" href="%(url)s">
<meta name="theme-color" content="#F7F4EE">
<meta property="og:locale" content="en_IN">
<meta property="og:type" content="%(og)s">
<meta property="og:site_name" content="Youth Face">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(ogi)s">
<meta name="twitter:card" content="summary_large_image">
%(extra)s<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/site.css">
%(tags)s<script type="application/ld+json">%(ld)s</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip">Free shipping<span>•</span>COD &amp; online payment<span>•</span>100%% original Youth Face</div>
<header class="head"><div class="wrap head-in">
  <a class="brand" href="/" aria-label="Youth Face home">%(brand)s</a>
  <nav class="nav" id="nav" aria-label="Main">%(nav)s</nav>
  <button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false" aria-label="Menu">%(menu)s</button>
  <a class="cart-link" href="/cart/" aria-label="Cart">%(cart)s<span class="cart-count" hidden>0</span></a>
</div></header>
<main id="main">
%(body)s
</main>
<footer><div class="wrap">
  <div class="fgrid">
    <div><a class="brand" href="/">%(brand)s</a><p class="about">Premium skincare for a simple everyday routine. %(owner)s, Bhatkal, Karnataka.</p>
      <div class="accept" aria-label="We accept"><span>UPI</span><span>Cards</span><span>Netbanking</span><span>Cash on Delivery</span></div></div>
    <div><h4>Shop</h4>%(shop)s</div>
    <div><h4>Customer care</h4><a href="/about-us/">About Us</a><a href="/contact/">Contact</a><a href="/faq/">FAQ</a><a href="/track-order/">Track Order</a><a href="/how-to-use/">How To Use</a><a href="/skincare-guides/">Skincare Guides</a></div>
    <div><h4>Policies</h4>%(pol)s<a href="https://wa.me/%(wa)s">WhatsApp %(wash)s</a></div>
  </div>
  <div class="legal"><span>© 2026 Youth Face · %(owner)s · %(addr)s</span><span>Online payments by Razorpay. Cosmetic product; results vary from person to person.</span></div>
</div></footer>
<a class="wa-float" href="https://wa.me/%(wa)s?text=%(watext)s" target="_blank" rel="noopener" aria-label="Chat with Youth Face on WhatsApp">%(glyph)s</a>
<script src="/assets/store.js" defer></script>
</body>
</html>
''' % dict(title=html.escape(title), desc=html.escape(desc), robots='index, follow, max-image-preview:large' if index else 'noindex, follow',
           url=full, og=og, ogi=ogi, extra=extra_head, tags=tags, ld=ld, brand=BRAND, nav=nav, menu=MENU_SVG, cart=CART_SVG, body=body,
           owner=OWNER, addr=ADDR, wa=WA, wash=WA_SHOW, watext='Hi%20Youth%20Face%2C%20I%20need%20help%20with%20my%20order.',
           glyph=WA_GLYPH % (56, 56),
           shop=''.join('<a href="%s">%s</a>' % (url(p), p['card']) for p in PRODUCTS),
           pol=''.join('<a href="%s">%s</a>' % (h, t) for h, t in POLICIES))
    out = os.path.join(ROOT, path.strip('/'), 'index.html') if path not in ('/404',) else os.path.join(ROOT, '404.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(doc)
    if index:
        pages.append(path)


def top(eyebrow, h1, lead=''):
    return '<div class="wrap page-top"><span class="eyebrow">%s</span><h1>%s</h1>%s</div>' % (eyebrow, h1, '<p>%s</p>' % lead if lead else '')


def card(p, h='h3'):
    off = pct(p)
    return '''<article class="card">%s<a class="ph" href="%s"><img src="%s" alt="%s" width="600" height="600" loading="lazy"></a>
  <div class="bd"><%s><a href="%s">%s</a></%s><span class="size">%s</span>
  <div class="price"><b>%s</b>%s%s</div>
  <div class="acts"><button class="btn ghost" type="button" data-add="%s">Add to cart</button><button class="btn" type="button" data-buy="%s">Buy now</button></div></div></article>''' % (
        '<span class="badge%s">%s</span>' % (' gold' if p['badge'] == 'Best value' else '', p['badge']) if p['badge'] else '',
        url(p), img(p['thumb']), html.escape(p['name']), h, url(p), p['card'], h, p['size'], rs(p['price']),
        '<s>%s</s>' % rs(p['mrp']) if off else '', '<span class="off">%d%% off</span>' % off if off else '', p['id'], p['id'])


def faq_html(items):
    return '<div class="faq">' + ''.join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in items) + '</div>'


def faq_ld(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


ICON = {
    'orig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3l7 3v6c0 4.4-3 7.8-7 9-4-1.2-7-4.6-7-9V6l7-3Z"/><path d="M8.5 12l2.4 2.4L15.5 10"/></svg>',
    'cod': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9v.01M18 15v.01"/></svg>',
    'wa': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 18.8L4 20Z"/></svg>',
    'routine': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/></svg>',
}

HOME_FAQ = [
    ('Is Youth Face Beauty Cream original when bought here?', 'Yes. This is the brand\'s own store, run by Beauty Mart in Bhatkal, Karnataka. Every jar ships directly from us, so you get the original product.'),
    ('What does the cream contain?', 'Youth Face Beauty Cream is built around Kojic Acid and Alpha Arbutin, two ingredients widely used in creams for dark-spot care and a more even-looking tone. The full ingredient list is printed on every pack.'),
    ('How do I use it?', 'Wash your face, pat it dry, and apply a small amount to the face and neck, once or twice a day. Always follow with sunscreen in the morning. Patch test first if you have sensitive skin.'),
    ('Is Cash on Delivery available?', 'Yes. Choose Cash on Delivery at checkout: you pay ₹99 online to confirm the order and the rest in cash when it arrives. You can also pay the full amount online by UPI, card or netbanking.'),
    ('How long does delivery take?', 'Orders are packed in 1 to 3 business days and usually reach you 3 to 7 business days after dispatch, depending on your pincode.'),
]

# ---------------- Home ----------------
home = '''<div class="wrap hero">
  <div>
    <span class="eyebrow">Youth Face Beauty Cream · Kojic Acid &amp; Alpha Arbutin</span>
    <h1>Clearer skin. <em>Brighter you.</em></h1>
    <p class="lead">A focused daily cream for dark-spot care and a more even-looking tone, made for a routine you'll actually keep.</p>
    <ul class="ticks"><li>Made for dark-spot care</li><li>For a more even-looking tone</li><li>One small step, morning and night</li></ul>
    <div class="cta"><a class="btn" href="#packs">Shop now</a><a class="btn ghost" href="/how-to-use/">How to use</a></div>
  </div>
  <div class="hero-media"><div class="frame"><img src="%s" alt="Youth Face Beauty Cream 25g jar with Kojic Acid and Alpha Arbutin" width="1000" height="1000" fetchpriority="high"></div>
    <span class="chip a">From <b>₹549</b> · COD available</span><span class="chip b">100%% original</span></div>
</div>
<div class="wrap trust">
  <div>%s<p><b>100%% original</b><span>Direct from the brand</span></p></div>
  <div>%s<p><b>COD + online</b><span>UPI, cards, netbanking</span></p></div>
  <div>%s<p><b>WhatsApp support</b><span>Real people, quick replies</span></p></div>
  <div>%s<p><b>Simple routine</b><span>Morning and night</span></p></div>
</div>
<section id="packs"><div class="wrap">
  <div class="sec-h"><span class="eyebrow">Find your ritual</span><h2>Choose your Youth Face pack</h2><p>Start with one jar, or save more with a pack of two or three. Free shipping on every order.</p></div>
  <div class="grid">%s</div>
</div></section>
<section><div class="wrap">
  <div class="sec-h"><span class="eyebrow">The formula</span><h2>Two proven ingredients. One easy habit.</h2></div>
  <div class="formula">
    <div><span class="n">01</span><h3>Kojic Acid</h3><p>A well-known skincare ingredient used in creams made for dark-spot care and an even-looking complexion.</p></div>
    <div><span class="n">02</span><h3>Alpha Arbutin</h3><p>A gentle partner to Kojic Acid, used for a brighter-looking, more even skin tone over time.</p></div>
    <div><span class="n">03</span><h3>Daily routine</h3><p>Results come from regular use. A small amount after washing your face, with sunscreen every morning.</p></div>
  </div>
</div></section>
<section><div class="wrap band">
  <div><span class="eyebrow" style="color:#E7C98C">How to use</span><h2>Your routine in three steps</h2><p>Consistency matters more than quantity. Use it daily for several weeks and judge in the same light.</p><p style="margin-top:22px"><a class="btn gold" href="/how-to-use/">Read the full guide</a></p></div>
  <ol><li>Wash your face with a gentle cleanser and pat dry.</li><li>Apply a small amount to the face and neck and massage in.</li><li>In the morning, finish with a broad-spectrum sunscreen.</li></ol>
</div></section>
<section><div class="wrap">
  <div class="sec-h"><span class="eyebrow">Questions</span><h2>Before you order</h2></div>
  %s
  <p style="margin-top:22px"><a class="btn ghost" href="/faq/">All questions</a></p>
</div></section>''' % (img(PRODUCTS[0]['imgs'][0]), ICON['orig'], ICON['cod'], ICON['wa'], ICON['routine'],
                         ''.join(card(p) for p in PRODUCTS), faq_html(HOME_FAQ))
page('/', 'Youth Face Beauty Cream | Kojic Acid & Alpha Arbutin | Official Store',
     'Youth Face is a modern Indian skincare brand: Beauty Cream with Kojic Acid & Alpha Arbutin for dark-spot care and an even-looking tone. From ₹549, free shipping, COD.',
     home, og='website', schema=[{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + url(p)} for i, p in enumerate(PRODUCTS)]}, faq_ld(HOME_FAQ)])

# ---------------- Shop ----------------
shop = top('Shop', 'Shop Youth Face', 'Beauty Cream in packs of one, two and three, and the Youth Face Body Lotion. Free shipping and Cash on Delivery on every order.') + \
    '<section style="padding-top:28px"><div class="wrap"><div class="grid">%s</div></div></section>' % ''.join(card(p, 'h2') for p in PRODUCTS)
page('/shop/', 'Shop Youth Face Skincare | Beauty Cream & Body Lotion', 'Shop Youth Face Beauty Cream (Pack of 1, 2 and 3) with Kojic Acid & Alpha Arbutin, and Youth Face Body Lotion. Free shipping, COD available.',
     shop, crumbs=[('Shop', '/shop/')], schema=[{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + url(p)} for i, p in enumerate(PRODUCTS)]}])

# ---------------- Product pages ----------------
CREAM_TABS = [
    ('Description', '<p>Youth Face Beauty Cream is a daily face cream built around Kojic Acid and Alpha Arbutin, two ingredients widely used in skincare for dark-spot care and a more even-looking tone. It has a light texture that spreads easily and fits into a simple morning and night routine.</p><p>Buying here means you get the original Youth Face product, shipped directly by the brand from Bhatkal, Karnataka.</p>'),
    ('Key ingredients', '<p><b>Kojic Acid:</b> used in creams made for dark spots and uneven-looking tone.</p><p><b>Alpha Arbutin:</b> a gentle partner ingredient used for a brighter-looking, more even complexion.</p><p>The complete ingredient list is printed on the pack.</p>'),
    ('How to use', '<p>1. Wash your face and pat dry. 2. Apply a small amount to face and neck and massage gently. 3. Use once or twice daily; in the morning, always follow with sunscreen.</p><p>Patch test on a small area first. Avoid the eyes. Stop use if irritation occurs.</p>'),
    ('Shipping & payment', '<p>Free shipping across India. Pay online by UPI, card or netbanking, or choose Cash on Delivery with a ₹99 advance. Orders are packed in 1 to 3 business days and usually delivered 3 to 7 business days after dispatch.</p>'),
]
LOTION_TABS = [
    ('Description', '<p>Youth Face Body Lotion is a lightweight daily body moisturiser with a quick-absorbing, non-greasy texture that leaves skin feeling soft and comfortable. It is a separate product from Youth Face Beauty Cream and is made for the body.</p>'),
    ('How to use', '<p>Apply a generous amount to clean, dry body skin and massage gently until absorbed. Use daily, or whenever your skin feels dry.</p>'),
    ('Shipping & payment', CREAM_TABS[3][1]),
]
PDP_FAQ = [
    ('Is this the original Youth Face product?', 'Yes. This is the official Youth Face store and every order ships directly from the brand.'),
    ('Can I pay Cash on Delivery?', 'Yes. Pay ₹99 online to confirm and the rest in cash at delivery, or pay the full amount online.'),
    ('When will I see a difference?', 'Skin responds slowly and differently for everyone. Use it regularly for several weeks with daily sunscreen before judging.'),
]
for p in PRODUCTS:
    off = pct(p)
    thumbs = ''.join('<button type="button" data-src="%s"%s aria-label="Picture %d"><img src="%s" alt="" width="76" height="76" loading="lazy"></button>' % (
        img(i), ' class="on"' if n == 0 else '', n + 1, img(i)) for n, i in enumerate(p['imgs'])) if len(p['imgs']) > 1 else ''
    tabs = CREAM_TABS if p['id'] != 'lotion' else LOTION_TABS
    others = [q for q in PRODUCTS if q['id'] != p['id']][:3]
    summary = ('One %s with Kojic Acid &amp; Alpha Arbutin for dark-spot care and a more even-looking tone.' % p['size']) if p['id'] == 'p1' else \
        ('%s of Youth Face Beauty Cream with Kojic Acid &amp; Alpha Arbutin. Better value per jar for regular use.' % p['size'].capitalize()) if p['id'] in ('p2', 'p3') else \
        'A lightweight, quick-absorbing daily moisturiser for soft, comfortable skin.'
    body = '''<div class="wrap pdp" data-product="%(id)s">
  <div class="gallery"><div class="main"><img id="pdp-img" src="%(main)s" alt="%(alt)s" width="1000" height="1000" fetchpriority="high"></div><div class="thumbs">%(thumbs)s</div></div>
  <div>
    <span class="eyebrow">Youth Face%(badge)s</span>
    <h1>%(name)s</h1>
    <div class="price"><b>%(price)s</b>%(mrp)s%(off)s</div>
    <p class="tax">Inclusive of all taxes · Free shipping · %(size)s</p>
    <p class="summary">%(summary)s</p>
    <div class="qty-row"><div class="qty" data-qty><button type="button" data-dec aria-label="Less">−</button><output>1</output><button type="button" data-inc aria-label="More">+</button></div><span class="muted" style="font-size:.9rem">In stock · ships from Bhatkal</span></div>
    <div class="acts"><button class="btn ghost" type="button" data-add="%(id)s" data-useqty>Add to cart</button><button class="btn" type="button" data-buy="%(id)s" data-useqty>Buy now</button></div>
    <ul class="perks"><li>Cash on Delivery available (₹99 advance)</li><li>Free shipping across India</li><li>100%% original, shipped by the brand</li></ul>
    <div class="tabs">%(tabs)s</div>
  </div>
</div>
<section style="padding-top:20px"><div class="wrap"><div class="sec-h"><h2>Questions</h2></div>%(faq)s</div></section>
<section style="padding-top:20px"><div class="wrap"><div class="sec-h"><span class="eyebrow">You may also like</span><h2>More from Youth Face</h2></div><div class="grid three">%(rel)s</div></div></section>''' % dict(
        id=p['id'], main=img(p['imgs'][0]), alt=html.escape(p['name']), thumbs=thumbs,
        badge=' · ' + p['badge'] if p['badge'] else '', name=html.escape(p['name']), price=rs(p['price']),
        mrp='<s>MRP %s</s>' % rs(p['mrp']) if off else '', off='<span class="off">%d%% off</span>' % off if off else '', size=p['size'], summary=summary,
        tabs=''.join('<details%s><summary>%s</summary><div class="in">%s</div></details>' % (' open' if n == 0 else '', t, c) for n, (t, c) in enumerate(tabs)),
        faq=faq_html(PDP_FAQ), rel=''.join(card(q) for q in others))
    ogt = '<meta property="product:brand" content="Youth Face">\n<meta property="product:availability" content="in stock">\n<meta property="product:condition" content="new">\n<meta property="product:price:amount" content="%d">\n<meta property="product:price:currency" content="INR">\n<meta property="product:retailer_item_id" content="%s">\n' % (p['price'], p['sku'])
    page(url(p), p['title'], p['desc'], body, og='product', ogimg=img(p['imgs'][0]), extra_head=ogt,
         crumbs=[('Shop', '/shop/'), (p['card'], url(p))], schema=[product_ld(p), faq_ld(PDP_FAQ)])

# ---------------- Cart & checkout ----------------
cart_body = top('Your cart', 'Cart') + '''<div class="wrap cart-wrap"><div class="panel" id="cart-lines"><div class="empty">Loading your cart…</div></div>
<aside class="panel"><h2 style="font-size:1.4rem;margin-bottom:14px">Order summary</h2><div class="sum" id="cart-sum"></div>
<a class="btn block" id="to-checkout" href="/checkout/" style="margin-top:16px">Proceed to checkout</a>
<p class="muted" style="font-size:.82rem;margin-top:10px">Free shipping · Cash on Delivery available · Secure payment by Razorpay</p></aside></div>'''
page('/cart/', 'Cart | Youth Face', 'Your Youth Face cart.', cart_body, index=False)

checkout_body = top('Checkout', 'Checkout', 'Enter your delivery details and choose how you would like to pay.') + '''<div class="wrap cart-wrap" id="checkout">
<div class="panel"><form class="form" id="co-form" novalidate>
  <div class="f"><label for="co-name">Full name</label><input id="co-name" autocomplete="name"></div>
  <div class="f"><label for="co-phone">Mobile number</label><input id="co-phone" type="tel" inputmode="numeric" maxlength="16" autocomplete="tel"></div>
  <div class="f"><label for="co-address">Full address (house no., street, area)</label><textarea id="co-address" rows="2" autocomplete="street-address"></textarea></div>
  <div class="two"><div class="f"><label for="co-pin">Pincode</label><input id="co-pin" inputmode="numeric" maxlength="6" autocomplete="postal-code"></div><div class="f"><label for="co-city">City</label><input id="co-city" autocomplete="address-level2"></div></div>
  <p class="pinnote" id="pin-note" hidden></p>
  <fieldset class="pay"><legend>How would you like to pay?</legend>
    <label><em class="rec-tag">Recommended</em><input type="radio" name="pay" value="online" checked><span>Pay online<small>UPI, cards, netbanking · nothing to pay at the door</small></span><b id="amt-online"></b></label>
    <label><input type="radio" name="pay" value="cod"><span>Cash on Delivery<small id="cod-note">Pay ₹99 now, the rest at delivery</small></span><b id="amt-cod"></b></label>
    <label><input type="radio" name="pay" value="wa"><span>Order on WhatsApp<small>Send your order, we confirm on chat</small></span><b id="amt-wa"></b></label>
  </fieldset>
  <p class="muted" id="cod-terms" style="font-size:.84rem" hidden>Cash on Delivery orders are confirmed with a ₹99 advance paid online now. It is part of the price, not an extra charge. If the parcel is refused at delivery, the ₹99 is not refunded.</p>
  <div class="notyet" id="not-yet" hidden><p><b>Your order isn't placed yet.</b> The payment wasn't completed. Your details are saved, so you can finish in one tap.</p><button type="button" class="btn" id="ny-retry">Try payment again</button><button type="button" class="btn ghost" id="ny-switch">Switch to Cash on Delivery</button></div>
  <p class="oerr" id="co-err" role="alert" hidden></p>
  <button class="btn block" type="submit" id="co-pay">Pay securely</button>
  <p class="muted" style="font-size:.8rem">Your details are used only to deliver this order, and we may message you on this number about it. See our <a href="/privacy-policy/">privacy policy</a>.</p>
</form></div>
<aside class="panel"><h2 style="font-size:1.4rem;margin-bottom:14px">Your order</h2><div id="co-lines"></div><div class="sum" id="co-sum" style="margin-top:12px"></div></aside>
</div>'''
page('/checkout/', 'Checkout | Youth Face', 'Secure checkout for Youth Face orders.', checkout_body, index=False)

# ---------------- Information pages ----------------
about = top('About us', 'About Youth Face', 'A modern Indian skincare brand focused on simple, practical skincare for everyday routines.') + '''<section style="padding-top:24px"><div class="wrap prose">
<p>Youth Face started with one idea: good skincare should be simple enough to keep doing. Instead of a shelf of products, we focus on a few well-chosen ingredients in products that fit into a busy day.</p>
<h2>What we make</h2>
<p>Our first product is <a href="%s">Youth Face Beauty Cream</a>, built around Kojic Acid and Alpha Arbutin for dark-spot care and a more even-looking tone. It is available as a single 25 g jar and in packs of two and three. We also make <a href="%s">Youth Face Body Lotion</a>, a light daily moisturiser for the body. More products are on the way.</p>
<h2>Our promise</h2>
<ul><li><b>Genuine products</b>, shipped directly by us. Buy from this site to avoid third-party copies.</li><li><b>Clear information</b> on ingredients, usage and pricing, with no hidden costs.</li><li><b>Secure payment</b> online, or Cash on Delivery with a small advance.</li><li><b>Real support</b> on WhatsApp, before and after you buy.</li></ul>
<h2>Who we are</h2>
<p>Youth Face is run by %s from Bhatkal, Karnataka. Every order is packed by our team and handed to a trusted courier.</p>
<p style="margin-top:26px"><a class="btn" href="/shop/">Shop Youth Face</a></p></div></section>''' % (url(PRODUCTS[0]), url(PRODUCTS[3]), OWNER)
page('/about-us/', 'About Youth Face | Simple, Ingredient-Focused Skincare from India', 'Youth Face is a modern Indian skincare brand from Bhatkal, Karnataka, focused on simple, practical skincare for everyday routines.', about, crumbs=[('About Us', '/about-us/')])

contact = top('Contact', 'Contact Youth Face', 'The fastest way to reach us is WhatsApp. We help with orders, delivery, products and returns.') + '''<section style="padding-top:24px"><div class="wrap prose">
<p><a class="btn" href="https://wa.me/%s?text=Hi%%20Youth%%20Face%%2C%%20I%%20need%%20help%%20with%%20my%%20order." target="_blank" rel="noopener">%s Chat on WhatsApp</a></p>
<h2>Details</h2>
<ul><li><b>WhatsApp and phone:</b> %s</li><li><b>Business:</b> %s (Youth Face)</li><li><b>Address:</b> %s</li><li><b>Hours:</b> Monday to Saturday, 10 am to 7 pm</li></ul>
<p>Please include your order number or the mobile number used on the order, so we can help you faster. You can also check your parcel any time on the <a href="/track-order/">Track Order</a> page.</p></div></section>''' % (WA, WA_GLYPH % (22, 22), WA_SHOW, OWNER, ADDR)
page('/contact/', 'Contact Youth Face | WhatsApp Support', 'Contact Youth Face on WhatsApp at +91 99808 81230 for help with orders, delivery and products. Beauty Mart, Bhatkal, Karnataka.', contact, crumbs=[('Contact', '/contact/')])

FAQ_ALL = HOME_FAQ + [
    ('How do I track my order?', 'Open the Track Order page and enter the mobile number and pincode used on your order, or your payment ID. Tracking appears once the courier collects the parcel.'),
    ('Can I cancel my order?', 'Yes, if it has not been packed or dispatched yet. Message us on WhatsApp with your order details as soon as possible.'),
    ('What if my product arrives damaged or wrong?', 'Contact us within 7 days of delivery with your order details and photos of the product, packaging and label. After checking, we will offer a replacement or refund.'),
    ('Can I return an opened jar?', 'For hygiene reasons, opened or used products cannot be returned unless they arrived damaged, defective or incorrect. See the Refund & Returns policy.'),
    ('Should I use sunscreen?', 'Yes. Daily broad-spectrum sunscreen is important with any dark-spot care routine.'),
    ('Is the Body Lotion the same as the Beauty Cream?', 'No. The Body Lotion is a separate, lightweight moisturiser for the body. The Beauty Cream is made for the face.'),
]
page('/faq/', 'Youth Face FAQ | Orders, COD, Delivery & Usage', 'Answers about Youth Face Beauty Cream and Body Lotion: original products, Cash on Delivery, delivery times, tracking, returns and how to use.',
     top('FAQ', 'Frequently asked questions') + '<section style="padding-top:24px"><div class="wrap">%s</div></section>' % faq_html(FAQ_ALL),
     crumbs=[('FAQ', '/faq/')], schema=[faq_ld(FAQ_ALL)])

GUIDES = [
    ('routine', 'Skincare routine basics', 'Build a simple routine and learn the usual order to apply products.',
     '<p>A good routine has three parts: cleanse, treat, protect. Wash your face with a gentle cleanser, apply your treatment cream to dry skin, and in the morning finish with sunscreen. Keep it short enough to do every day; consistency matters more than the number of products.</p>'),
    ('kojic-acid', 'Understanding Kojic Acid', 'Why it is used in skincare and what to keep in mind.',
     '<p>Kojic Acid is an ingredient used in creams made for dark spots and uneven-looking tone. Introduce it slowly, patch test first, and use sunscreen daily, because sun exposure is a major cause of dark spots in the first place.</p>'),
    ('alpha-arbutin', 'Understanding Alpha Arbutin', 'Its role in products for a more even-looking complexion.',
     '<p>Alpha Arbutin is a gentle ingredient often paired with Kojic Acid in products for a brighter-looking, more even complexion. It works gradually, so judge results over weeks rather than days.</p>'),
    ('using-youth-face', 'How to use Youth Face products', 'Simple directions for the Beauty Cream and Body Lotion.',
     '<p>Beauty Cream: apply a small amount to clean face and neck, once or twice daily, with sunscreen in the morning. Body Lotion: apply generously to clean, dry body skin and massage until absorbed. See the full <a href="/how-to-use/">How To Use</a> guide.</p>'),
    ('daytime', 'Daytime skincare routine', 'Cleanse, apply and protect before you step out.',
     '<p>Morning: rinse or cleanse, apply your cream, wait a minute, then apply a broad-spectrum sunscreen. Reapply sunscreen if you are outdoors for long.</p>'),
    ('evening', 'Evening skincare routine', 'A calm, simple routine before bed.',
     '<p>Evening: remove sunscreen and the day\'s dirt with a gentle cleanser, pat dry, apply your cream and let it absorb. Avoid layering too many active products at night.</p>'),
]
guides = top('Skincare Guides', 'Youth Face skincare guides', 'Plain, practical guides to building a routine and understanding the ingredients you use.') + \
    '<section style="padding-top:24px"><div class="wrap"><div class="guides">%s</div><div class="prose" style="margin-top:40px">%s<p class="note">This information is general and does not replace advice from a qualified dermatologist or healthcare professional.</p></div></div></section>' % (
        ''.join('<a href="#%s"><span class="eyebrow">Guide</span><h3>%s</h3><p>%s</p></a>' % (g[0], g[1], g[2]) for g in GUIDES),
        ''.join('<h2 id="%s">%s</h2>%s' % (g[0], g[1], g[3]) for g in GUIDES))
page('/skincare-guides/', 'Skincare Guides | Kojic Acid, Alpha Arbutin & Daily Routines | Youth Face', 'Youth Face skincare guides: routine basics, Kojic Acid, Alpha Arbutin, how to use Youth Face, and simple day and night routines.', guides, crumbs=[('Skincare Guides', '/skincare-guides/')])

howto = top('How to use', 'How to use Youth Face', 'Simple steps for the Beauty Cream and the Body Lotion.') + '''<section style="padding-top:24px"><div class="wrap prose">
<h2>Youth Face Beauty Cream</h2>
<ol><li>Wash your face with a gentle cleanser and pat it dry.</li><li>Take a small amount, about the size of a pea, for the face and neck.</li><li>Massage gently until absorbed. Avoid the eye area.</li><li>Use once or twice a day. In the morning, always finish with sunscreen.</li></ol>
<h3>Tips</h3><ul><li>Patch test on a small area for 24 hours before first use.</li><li>Use it regularly for several weeks before judging.</li><li>Stop use if redness, burning or irritation continues, and consult a dermatologist.</li></ul>
<h2>Youth Face Body Lotion</h2>
<ol><li>Apply a generous amount to clean, dry body skin.</li><li>Massage gently until absorbed.</li><li>Use daily, or whenever your skin feels dry.</li></ol>
<p style="margin-top:26px"><a class="btn" href="/shop/">Shop Youth Face</a></p></div></section>'''
page('/how-to-use/', 'How To Use Youth Face Beauty Cream & Body Lotion', 'How to use Youth Face Beauty Cream with Kojic Acid & Alpha Arbutin, step by step, plus Body Lotion directions and patch-test tips.', howto, crumbs=[('How To Use', '/how-to-use/')])

track = top('Track order', 'Track your Youth Face order', 'Use the mobile number and pincode from your order, or your payment ID.') + '''<section style="padding-top:20px"><div class="wrap track">
<form class="form" id="track-form" novalidate>
  <div class="track-by" role="tablist"><button type="button" id="by-phone" class="on" aria-selected="true">Mobile number</button><button type="button" id="by-id" aria-selected="false">Payment ID / tracking no.</button></div>
  <div id="by-phone-box" class="form"><div class="f"><label for="t-phone">Mobile number used on the order</label><input id="t-phone" type="tel" inputmode="numeric" maxlength="16"></div><div class="f"><label for="t-pin">Delivery pincode</label><input id="t-pin" inputmode="numeric" maxlength="6"></div></div>
  <div id="by-id-box" class="form" hidden><div class="f"><label for="t-id">Payment ID or tracking number</label><input id="t-id" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="pay_XXXXXXXXXXXX"></div></div>
  <button class="btn block" type="submit" id="t-go">Track order</button>
</form>
<div class="track-out" id="t-out" role="status" aria-live="polite" hidden></div></div></section>'''
page('/track-order/', 'Track Your Order | Youth Face', 'Track your Youth Face order with your mobile number and pincode, payment ID or courier tracking number.', track, crumbs=[('Track Order', '/track-order/')])

POL = {
'/privacy-policy/': ('Privacy Policy', 'Privacy Policy | Youth Face', 'How Youth Face collects, uses and protects your information when you shop on youthfacebeautycream.com.', '''
<p>This policy explains what information Youth Face (%s) collects when you use this website and place an order, and how it is used.</p>
<h2>What we collect</h2><p>When you order, we collect your name, mobile number, delivery address, city and pincode, and the items you buy. Payments are processed by Razorpay; we never see or store your card or UPI details.</p>
<h2>How we use it</h2><p>Only to process, deliver and support your order: sharing your delivery details with our courier partner (through Shiprocket), sending order updates, and helping you on WhatsApp. If you start a payment and do not finish, we may message you once on that number to ask whether you need help.</p>
<h2>Details saved on your device</h2><p>Your cart and, after you start an order, your delivery details are saved in your own browser so you do not need to type them again. You can clear them from your browser settings at any time.</p>
<h2>Cookies and measurement</h2><p>The site may use advertising and analytics tags (such as Google or Meta) to measure visits and orders from our ads. We do not send them your name, phone number or address.</p>
<h2>Your choices</h2><p>To ask about, correct or delete your information, contact us on WhatsApp at %s.</p>''' % (OWNER, WA_SHOW)),
'/terms-conditions/': ('Terms & Conditions', 'Terms & Conditions | Youth Face', 'Terms and conditions for buying Youth Face products on youthfacebeautycream.com.', '''
<p>By using this website and placing an order you agree to these terms. The site is operated by %s, Bhatkal, Karnataka, India.</p>
<h2>Products and prices</h2><p>Prices are in Indian rupees and include applicable taxes. We may change prices or availability at any time; the price shown at checkout is the price you pay.</p>
<h2>Orders</h2><p>An order is confirmed when payment (or the Cash on Delivery advance) is received. We may cancel an order if a product is unavailable or details appear incorrect or fraudulent, and will refund any amount paid.</p>
<h2>Cash on Delivery</h2><p>Cash on Delivery orders require a ₹99 advance paid online, which is part of the price. If a Cash on Delivery parcel is refused or cannot be delivered because of incorrect details, the advance is not refunded, as it covers shipping costs.</p>
<h2>Product use</h2><p>Youth Face products are cosmetics. Follow the directions on the pack, patch test before use and stop if irritation occurs. Results vary from person to person and are not guaranteed.</p>
<h2>Liability</h2><p>To the extent permitted by law, our liability for any order is limited to the amount paid for it. Nothing here limits your rights under Indian consumer law.</p>
<h2>Contact</h2><p>WhatsApp %s · %s</p>''' % (OWNER, WA_SHOW, ADDR)),
'/refund-returns-policy/': ('Refund & Returns', 'Refund and Returns Policy | Youth Face', 'Youth Face refund and returns policy: 7-day window for damaged, defective or wrong items, how to request a return, and refund timing.', '''
<h2>Return window</h2><p>Return requests are accepted within <b>7 days of delivery</b>.</p>
<h2>What can be returned</h2><ul><li>Wrong, damaged, defective or materially different items.</li><li>Unused, unopened items in original condition with original packaging and seals.</li></ul>
<h2>Hygiene products</h2><p>Opened, used, tested or tampered products cannot be returned, unless they arrived damaged, defective or incorrect. Your legal rights for such products are not affected.</p>
<h2>How to request a return</h2><ol><li>Message us on WhatsApp at %s within 7 days of delivery.</li><li>Share your order details and photos of the product, packaging and shipping label (a short video if needed).</li><li>Wait for approval and instructions before sending anything back.</li></ol>
<h2>Refunds</h2><p>Approved refunds are made to the original payment method after the returned item is received and checked. Banks usually take 5 to 7 business days to show the amount. Shipping costs are refunded when the error was ours.</p>
<h2>Cancellations</h2><p>Orders can be cancelled before they are packed or dispatched. Once dispatched, the return process applies.</p>
<h2>Refused or undelivered orders</h2><p>For Cash on Delivery orders refused at delivery or undeliverable because of incorrect details, the ₹99 advance is not refunded.</p>
<h2>Purchases elsewhere</h2><p>This policy applies to orders placed on this website. Purchases from other sellers follow that seller's policy.</p>''' % WA_SHOW),
'/shipping-delivery/': ('Shipping & Delivery', 'Shipping & Delivery Policy | Youth Face', 'Youth Face shipping: free shipping across India, packed in 1 to 3 business days, delivered in 3 to 7 business days after dispatch, Cash on Delivery available.', '''
<h2>Shipping charges</h2><p>Shipping is <b>free</b> on all orders across India.</p>
<h2>Processing time</h2><p>Orders are packed within <b>1 to 3 business days</b> of payment or confirmation. Orders placed on Sundays or public holidays are processed the next business day.</p>
<h2>Delivery time</h2><p>After dispatch, delivery usually takes <b>3 to 7 business days</b> depending on your pincode. Remote areas can take longer. Timelines are estimates.</p>
<h2>Cash on Delivery</h2><p>Available on most pincodes. Pay ₹99 online to confirm and the rest in cash at delivery.</p>
<h2>Tracking</h2><p>Track your parcel on the <a href="/track-order/">Track Order</a> page with your mobile number and pincode. Tracking appears once the courier collects the parcel.</p>
<h2>Address and delivery attempts</h2><p>Please give a complete address and a reachable mobile number. If the courier cannot deliver after its attempts, the parcel returns to us.</p>
<h2>Damaged or wrong parcels</h2><p>Photograph the package, product and label before discarding anything, and contact us within 7 days. See our <a href="/refund-returns-policy/">Refund & Returns</a> policy.</p>
<h2>Shipping area</h2><p>We ship within India only.</p>'''),
}
for path, (h, t, d, body) in POL.items():
    page(path, t, d, top('Policy', h, 'Last updated: 9 October 2026') + '<section style="padding-top:20px"><div class="wrap prose">%s</div></section>' % body, crumbs=[(h, path)])

page('/404', 'Page not found | Youth Face', 'This page could not be found.', top('404', 'This page could not be found', 'The link may be old or mistyped.') + '<section style="padding-top:20px"><div class="wrap"><a class="btn" href="/shop/">Go to the shop</a></div></section>', index=False)

# ---------------- Assets, sitemap, redirects ----------------
os.makedirs(os.path.join(ROOT, 'assets'), exist_ok=True)
shutil.copy(os.path.join(B, 'site.css'), os.path.join(ROOT, 'assets', 'site.css'))
shutil.copy(os.path.join(B, 'store.js'), os.path.join(ROOT, 'assets', 'store.js'))
open(os.path.join(ROOT, 'assets', 'products.json'), 'w').write(json.dumps({p['id']: {'name': p['name'], 'card': p['card'], 'price': p['price'], 'mrp': p['mrp'], 'img': img(p['thumb']), 'url': url(p), 'wc': p['wc']} for p in PRODUCTS}, ensure_ascii=False))
open(os.path.join(ROOT, 'assets', 'icon.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#24493F"/><text x="32" y="43" text-anchor="middle" font-family="Georgia,serif" font-size="30" fill="#F7F4EE">Y<tspan font-style="italic" fill="#E7C98C">F</tspan></text></svg>')

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for pth in pages:
    pri = '1.0' if pth == '/' else '0.9' if pth.startswith('/product/') or pth == '/shop/' else '0.6'
    sm.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % (SITE, pth, TODAY, pri))
sm.append('</urlset>')
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
open(os.path.join(ROOT, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /cart/\nDisallow: /checkout/\nDisallow: /api/\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)

redirects = []
for p in PRODUCTS:
    if p['short']:
        redirects.append({'source': '/product/%s' % p['short'], 'destination': url(p), 'permanent': True})
        redirects.append({'source': '/product/%s/' % p['short'], 'destination': url(p), 'permanent': True})
for src, dst in [('/my-account', '/track-order/'), ('/my-account/:path*', '/track-order/'), ('/product-category/:path*', '/shop/'),
                 ('/product-tag/:path*', '/shop/'), ('/feed', '/'), ('/feed/', '/'), ('/comments/feed/', '/'), ('/home', '/'), ('/home/', '/'),
                 ('/wp-sitemap.xml', '/sitemap.xml'), ('/sitemap_index.xml', '/sitemap.xml'), ('/product-sitemap.xml', '/sitemap.xml'),
                 ('/page-sitemap.xml', '/sitemap.xml'), ('/post-sitemap.xml', '/sitemap.xml'), ('/wp-sitemap-:rest*', '/sitemap.xml'),
                 ('/about', '/about-us/'), ('/shipping-policy/', '/shipping-delivery/'), ('/refund_returns/', '/refund-returns-policy/')]:
    redirects.append({'source': src, 'destination': dst, 'permanent': True})
for src in ['/wp-admin', '/wp-admin/:path*', '/wp-login.php', '/xmlrpc.php']:
    redirects.append({'source': src, 'destination': '/', 'permanent': False})
vercel = {'cleanUrls': False, 'redirects': redirects,
          'headers': [{'source': '/(assets|wp-content)/(.*)\\.(webp|jpg|jpeg|png|svg|mp4)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=86400, stale-while-revalidate=604800'}]},
                      {'source': '/(cart|checkout)/(.*)', 'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex'}]}]}
open(os.path.join(ROOT, 'vercel.json'), 'w').write(json.dumps(vercel, indent=2) + '\n')
open(os.path.join(ROOT, '.vercelignore'), 'w').write('_build\nREADME.md\n')
missing = [i for p in PRODUCTS for i in set(p['imgs'] + [p['thumb']]) if not os.path.exists(os.path.join(ROOT, UP.strip('/'), i))]
print('built', len(pages), 'indexed pages;', len(redirects), 'redirects;', len(set(missing)), 'images still served from the old site')
