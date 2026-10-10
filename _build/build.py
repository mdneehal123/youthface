#!/usr/bin/env python3
"""Builds the Youth Face static store into the repository root.
Every public address of the old WordPress site is kept, so search engines see no broken links."""
import json, os, html, shutil, urllib.parse

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
GSC_FILE = ''
GRIEVANCE_NAME = 'Nihal'   # put the owner's full name here (required by the E-Commerce Rules)          # Search Console verification file name, if one is used

UP = '/wp-content/uploads/2026/10/'


def img(name):
    """Images in this repo are given as /assets/... paths. Old-site names fall back to the old site if missing."""
    if name.startswith('/'):
        return name
    local = os.path.join(ROOT, UP.strip('/'), name)
    return (UP if os.path.exists(local) else OLD + UP) + name


PRODUCTS = [
    dict(id='p1', wc=16, slug='youth-face-beauty-cream-25g-pack-of-1-kojic-acid-alpha-arbutin', short='youth-face-beauty-cream-25g',
         name='Youth Face Beauty Cream 25g – Pack of 1', card='Beauty Cream · Pack of 1', size='1 × 25 g jar', price=549, mrp=899, badge='',
         sku='YFB-CREAM-25',
         title='Buy Youth Face Beauty Cream 25g – Pack of 1 (Original) | Kojic Acid & Alpha Arbutin',
         desc='Buy the original Youth Face Beauty Cream 25g with Kojic Acid & Alpha Arbutin, direct from the brand. ₹549, Cash on Delivery available, ships from Bhatkal.',
         imgs=['/assets/img/yf-pack-1.webp'], og='/assets/img/yf-pack-1.jpg',
         thumb='/assets/img/yf-pack-1-600.webp'),
    dict(id='p2', wc=17, slug='youth-face-beauty-cream-pack-of-2-kojic-acid-alpha-arbutin', short='youth-face-beauty-cream-pack-of-2',
         name='Youth Face Beauty Cream Pack of 2 – Kojic Acid & Alpha Arbutin', card='Beauty Cream · Pack of 2', size='2 × 25 g jars (50 g)', price=999, mrp=1599, badge='Most popular',
         sku='YFB-CREAM-25x2',
         title='Youth Face Beauty Cream Pack of 2 | Kojic Acid & Alpha Arbutin',
         desc='Buy Youth Face Beauty Cream Pack of 2 with Kojic Acid & Alpha Arbutin online in India. 2 × 25g jars for your daily skincare routine. ₹999, COD available.',
         imgs=['/assets/img/yf-pack-2.webp', '/assets/img/yf-pack-1.webp'], og='/assets/img/yf-pack-2.jpg',
         thumb='/assets/img/yf-pack-2-600.webp'),
    dict(id='p3', wc=18, slug='youth-face-beauty-cream-pack-of-3-kojic-acid-alpha-arbutin', short='youth-face-beauty-cream-pack-of-3',
         name='Youth Face Beauty Cream Pack of 3 – Kojic Acid & Alpha Arbutin', card='Beauty Cream · Pack of 3', size='3 × 25 g jars (75 g)', price=1444, mrp=1899, badge='Best value',
         sku='YFB-CREAM-25x3',
         title='Youth Face Beauty Cream Pack of 3 | Kojic Acid & Alpha Arbutin',
         desc='Youth Face Beauty Cream Pack of 3: three 25g jars with Kojic Acid & Alpha Arbutin. ₹1,444, best value per jar, free shipping and Cash on Delivery.',
         imgs=['/assets/img/yf-pack-3.webp', '/assets/img/yf-pack-1.webp'], og='/assets/img/yf-pack-3.jpg',
         thumb='/assets/img/yf-pack-3-600.webp'),
    dict(id='lotion', wc=19, slug='youth-face-body-lotion', short='',
         name='Youth Face Body Lotion', card='Body Lotion · 40 ml', size='40 ml bottle', price=599, mrp=599, badge='',
         sku='YFB-LOTION-40',
         title='Youth Face Body Lotion 40ml | Youth Face',
         desc='Youth Face Body Lotion, 40ml: a lightweight, quick-absorbing daily moisturiser for soft, comfortable skin. Order direct from Youth Face, India.',
         imgs=['/assets/img/yf-body-lotion.webp'], og='/assets/img/yf-body-lotion.jpg',
         thumb='/assets/img/yf-body-lotion-600.webp'),
    dict(id='combo', wc=0, slug='youth-face-beauty-cream-body-lotion-combo', short='',
         name='Youth Face Combo – Beauty Cream 25g + Body Lotion 40ml', card='Combo · Cream + Lotion', size='25 g cream + 40 ml lotion', price=999, mrp=1498, badge='Face + body',
         sku='YFB-COMBO-CL',
         title='Youth Face Combo: Beauty Cream + Body Lotion | ₹999 | Kojic Acid & Alpha Arbutin',
         desc='Youth Face Combo: Beauty Cream 25g with Kojic Acid & Alpha Arbutin for the face plus Body Lotion 40ml for the body, together for ₹999. Free shipping, COD available.',
         imgs=['/assets/img/yf-combo.webp', '/assets/img/yf-pack-1.webp', '/assets/img/yf-body-lotion.webp'], og='/assets/img/yf-combo.jpg',
         thumb='/assets/img/yf-combo-600.webp'),
]
MAIN = [p for p in PRODUCTS if p['id'] != 'combo']
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
BRAND = '<img src="/assets/img/youth-face-logo-88.png" alt="Youth Face Beauty Cream" width="297" height="88">'
BRAND_W = '<img src="/assets/img/youth-face-logo-88-white.png" alt="Youth Face Beauty Cream" width="297" height="88">'

pages = []


def org_graph():
    return [{
        '@type': 'Organization', '@id': SITE + '/#org', 'name': 'Youth Face', 'url': SITE + '/', 'legalName': OWNER, 'logo': SITE + '/assets/img/youth-face-logo.png', 'image': SITE + '/icon-512.png',
        'address': {'@type': 'PostalAddress', 'streetAddress': 'Azad Nagar, 4th Cross', 'addressLocality': 'Bhatkal',
                    'addressRegion': 'Karnataka', 'postalCode': '581320', 'addressCountry': 'IN'},
        'contactPoint': {'@type': 'ContactPoint', 'telephone': '+' + WA, 'contactType': 'customer service', 'areaServed': 'IN'}
    }, {'@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': 'Youth Face', 'publisher': {'@id': SITE + '/#org'}}]


def product_ld(p):
    return {'@type': 'Product', '@id': SITE + url(p) + '#product', 'name': p['name'], 'sku': p['sku'],
            'image': [SITE + p['og']] + [SITE + i for i in p['imgs']],
            'description': p['desc'], 'brand': {'@type': 'Brand', 'name': 'Youth Face'},
            'offers': {'@type': 'Offer', 'url': SITE + url(p), 'price': str(p['price']), 'priceCurrency': 'INR',
                       'availability': 'https://schema.org/InStock', 'itemCondition': 'https://schema.org/NewCondition',
                       'seller': {'@id': SITE + '/#org'}}}


def page(path, title, desc, body, schema=None, crumbs=None, index=True, og='website', ogimg=None, extra_head='', js='store.js', lang='en-IN'):
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
    ogi = ogimg or PRODUCTS[0]['og']
    if not ogi.startswith('http'):
        ogi = SITE + ogi
    tags = ''
    if GOOGLE_ADS:
        tags += '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","%s");</script>\n' % (GOOGLE_ADS, GOOGLE_ADS)
    if META_PIXEL and index:
        tags += "<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','%s');fbq('track','PageView');</script>\n" % META_PIXEL
    doc = '''<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="%(robots)s">
<link rel="canonical" href="%(url)s">
<meta name="theme-color" content="#FBF3EA">
<meta property="og:locale" content="%(ogl)s">
<meta property="og:type" content="%(og)s">
<meta property="og:site_name" content="Youth Face">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(ogi)s">
<meta name="twitter:card" content="summary_large_image">
%(extra)s<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;1,500&family=Montserrat:wght@400;500;600;700&display=swap">
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
    <div><a class="brand" href="/">%(brandw)s</a><p class="about">Premium skincare for a simple everyday routine. %(owner)s, Bhatkal, Karnataka.</p>
      <div class="accept" aria-label="We accept"><span>UPI</span><span>Cards</span><span>Netbanking</span><span>Cash on Delivery</span></div></div>
    <div><h4>Shop</h4>%(shop)s</div>
    <div><h4>Customer care</h4><a href="/about-us/">About Us</a><a href="/contact/">Contact</a><a href="/faq/">FAQ</a><a href="/track-order/">Track Order</a><a href="/how-to-use/">How To Use</a><a href="/skincare-guides/">Skincare Guides</a></div>
    <div><h4>Policies</h4>%(pol)s<a href="https://wa.me/%(wa)s">WhatsApp %(wash)s</a></div>
  </div>
  <div class="legal"><span>© 2026 Youth Face · %(owner)s · %(addr)s</span><span>Online payments by Razorpay. Cosmetic product; results vary from person to person.</span><span class="langs"><a href="/" lang="en">English</a> · <a href="/hi/" lang="hi">हिंदी</a> · <a href="/ur/" lang="ur">اردو</a></span></div>
</div></footer>
<a class="wa-float" href="https://wa.me/%(wa)s?text=%(watext)s" target="_blank" rel="noopener" aria-label="Chat with Youth Face on WhatsApp">%(glyph)s</a>
%(js)s
</body>
</html>
''' % dict(title=html.escape(title), desc=html.escape(desc), robots='index, follow, max-image-preview:large' if index else 'noindex, follow',
           url=full, og=og, ogi=ogi, extra=extra_head, tags=tags, ld=ld, brand=BRAND, brandw=BRAND_W, nav=nav, menu=MENU_SVG, cart=CART_SVG, body=body,
           owner=OWNER, addr=ADDR, wa=WA, wash=WA_SHOW, watext='Hi%20Youth%20Face%2C%20I%20need%20help%20with%20my%20order.',
           glyph=WA_GLYPH % (56, 56),
           lang=lang, ogl={'hi': 'hi_IN', 'ur': 'ur_IN'}.get(lang, 'en_IN'),
           js=''.join('<script src="/assets/%s" defer></script>' % j for j in js.split(',')),
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
    return '''<article class="card"><a class="ph" href="%s"><img src="%s" alt="%s" width="600" height="600" loading="lazy"></a>
  <div class="bd">%s<%s><a href="%s">%s</a></%s><span class="size">%s</span>
  <div class="price"><b>%s</b>%s%s</div>
  <div class="acts"><button class="btn ghost" type="button" data-add="%s">Add to cart</button><button class="btn" type="button" data-buy="%s">Buy now</button></div></div></article>''' % (
        url(p), img(p['thumb']), html.escape(p['name']),
        '<span class="badge%s">%s</span>' % (' gold' if p['badge'] == 'Best value' else '', p['badge']) if p['badge'] else '', h, url(p), p['card'], h, p['size'], rs(p['price']),
        '<s>%s</s>' % rs(p['mrp']) if off else '', '<span class="off">%d%% off</span>' % off if off else '', p['id'], p['id'])


def combo_band(h='h2'):
    c = BYID['combo']
    sep = BYID['p1']['price'] + BYID['lotion']['price']
    return '''<div class="combo"><a class="ph" href="%s"><img src="%s" alt="Youth Face Combo: Beauty Cream and Body Lotion" width="600" height="600" loading="lazy"></a>
  <div class="combo-tx"><span class="eyebrow">Combo offer · Face + body</span><%s><a href="%s">Beauty Cream + Body Lotion</a></%s>
  <p>Youth Face Beauty Cream 25 g for your face and Body Lotion 40 ml for your body, together for %s. That is %s less than buying them separately.</p>
  <div class="price"><b>%s</b><s>MRP %s</s><span class="off">%d%% off</span></div>
  <div class="acts"><button class="btn ghost" type="button" data-add="combo">Add to cart</button><button class="btn" type="button" data-buy="combo">Buy the combo</button></div></div></div>''' % (
        url(c), img(c['thumb']), h, url(c), h, rs(c['price']), rs(sep - c['price']), rs(c['price']), rs(c['mrp']), pct(c))


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

ALT = ''.join('<link rel="alternate" hreflang="%s" href="%s%s">\n' % (h, SITE, u) for h, u in [('en-IN', '/'), ('hi-IN', '/hi/'), ('ur-IN', '/ur/'), ('x-default', '/')])

# ---------------- Home ----------------
home = '''<div class="wrap hero">
  <div>
    <span class="eyebrow">Youth Face Beauty Cream · Kojic Acid &amp; Alpha Arbutin</span>
    <h1>Clearer skin. <em>Brighter you.</em></h1>
    <p class="lead">A focused daily cream for dark-spot care and a more even-looking tone, made for a routine you'll actually keep.</p>
    <ul class="ticks"><li>Made for dark-spot care</li><li>For a more even-looking tone</li><li>One small step, morning and night</li></ul>
    <div class="cta"><a class="btn" href="#packs">Shop now</a><a class="btn ghost" href="/how-to-use/">How to use</a></div>
  </div>
  <div class="hero-media"><div class="frame"><a href="/product/youth-face-beauty-cream-body-lotion-combo/"><img src="%s" alt="Youth Face Combo: Beauty Cream 25g with Kojic Acid and Alpha Arbutin, and Body Lotion 40ml" width="1200" height="1200" fetchpriority="high"></a></div>
    <div class="chips"><span class="chip a">Combo <b>₹999</b> · COD available</span><span class="chip b">100%% original</span></div></div>
</div>
<div class="wrap trust">
  <div>%s<p><b>100%% original</b><span>Direct from the brand</span></p></div>
  <div>%s<p><b>COD + online</b><span>UPI, cards, netbanking</span></p></div>
  <div>%s<p><b>WhatsApp support</b><span>Real people, quick replies</span></p></div>
  <div>%s<p><b>Simple routine</b><span>Morning and night</span></p></div>
</div>
<section id="packs"><div class="wrap">
  <div class="sec-h"><span class="eyebrow">Find your ritual</span><h2>Choose your Youth Face pack</h2><p>Start with one jar, or save more with a pack of two or three. Free shipping on every order.</p></div>
  <div class="grid">%s</div>%s
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
  <div><span class="eyebrow" style="color:#E9C98B">How to use</span><h2>Your routine in three steps</h2><p>Consistency matters more than quantity. Use it daily for several weeks and judge in the same light.</p><p style="margin-top:22px"><a class="btn gold" href="/how-to-use/">Read the full guide</a></p></div>
  <ol><li>Wash your face with a gentle cleanser and pat dry.</li><li>Apply a small amount to the face and neck and massage in.</li><li>In the morning, finish with a broad-spectrum sunscreen.</li></ol>
</div></section>
<section><div class="wrap">
  <div class="sec-h"><span class="eyebrow">Questions</span><h2>Before you order</h2></div>
  %s
  <p style="margin-top:22px"><a class="btn ghost" href="/faq/">All questions</a></p>
</div></section>''' % ('/assets/img/yf-combo.webp', ICON['orig'], ICON['cod'], ICON['wa'], ICON['routine'],
                         ''.join(card(p) for p in MAIN), combo_band(), faq_html(HOME_FAQ))
page('/', 'Youth Face Beauty Cream | Kojic Acid & Alpha Arbutin | Official Store',
     'Youth Face is a modern Indian skincare brand: Beauty Cream with Kojic Acid & Alpha Arbutin for dark-spot care and an even-looking tone. From ₹549, free shipping, COD.',
     home, og='website', extra_head=ALT, schema=[{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + url(p)} for i, p in enumerate(PRODUCTS)]}, faq_ld(HOME_FAQ)])

# ---------------- Shop ----------------
shop = top('Shop', 'Shop Youth Face', 'Beauty Cream in packs of one, two and three, and the Youth Face Body Lotion. Free shipping and Cash on Delivery on every order.') + \
    '<section style="padding-top:28px"><div class="wrap"><div class="grid">%s</div>%s</div></section>' % (''.join(card(p, 'h2') for p in MAIN), combo_band('h2'))
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
COMBO_TABS = [
    ('What you get', '<p><b>1 × Youth Face Beauty Cream, 25 g jar</b>: a daily face cream with Kojic Acid and Alpha Arbutin for dark-spot care and a more even-looking tone.</p><p><b>1 × Youth Face Body Lotion, 40 ml</b>: a lightweight, quick-absorbing daily moisturiser for soft, comfortable body skin.</p>'),
    ('How to use', '<p><b>Face:</b> apply a pea-sized amount of the Beauty Cream to clean, dry face and neck, once or twice a day, with sunscreen every morning.</p><p><b>Body:</b> apply the Body Lotion generously to clean, dry skin after a bath and massage until absorbed.</p><p>Patch test both products first. Avoid the eyes. Stop use if irritation occurs.</p>'),
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
    tabs = COMBO_TABS if p['id'] == 'combo' else CREAM_TABS if p['id'] != 'lotion' else LOTION_TABS
    others = [q for q in PRODUCTS if q['id'] != p['id']][:3]
    summary = ('One %s with Kojic Acid &amp; Alpha Arbutin for dark-spot care and a more even-looking tone.' % p['size']) if p['id'] == 'p1' else \
        ('%s of Youth Face Beauty Cream with Kojic Acid &amp; Alpha Arbutin. Better value per jar for regular use.' % p['size'].capitalize()) if p['id'] in ('p2', 'p3') else \
        ('One jar of Youth Face Beauty Cream (25 g) for the face and one Youth Face Body Lotion (40 ml) for the body, together for %s instead of %s when bought separately.' % (rs(p['price']), rs(BYID['p1']['price'] + BYID['lotion']['price']))) if p['id'] == 'combo' else \
        'A lightweight, quick-absorbing daily moisturiser for soft, comfortable skin.'
    if p['id'] == 'lotion':
        opts = [BYID['lotion'], BYID['combo']]
    else:
        opts = [BYID['p1'], BYID['p2'], BYID['p3'], BYID['combo']]
    def opt_sub(q):
        if q['id'] in ('p2', 'p3'):
            return '%s / jar' % rs(round(q['price'] / int(q['id'][1])))
        return {'p1': '1 jar', 'combo': '+ Body Lotion', 'lotion': '40 ml'}[q['id']]
    def opt_name(q):
        return {'p1': 'Pack of 1', 'p2': 'Pack of 2', 'p3': 'Pack of 3', 'combo': 'Combo', 'lotion': 'Body Lotion'}[q['id']]
    switch = '<div class="switch" role="group" aria-label="Choose a pack">%s</div>' % ''.join(
        '<a href="%s"%s><b>%s</b><span>%s</span><small>%s</small>%s</a>' % (
            url(q), ' class="on" aria-current="page"' if q['id'] == p['id'] else '', opt_name(q), rs(q['price']), opt_sub(q),
            '<em>Popular</em>' if q['id'] == 'p2' else '<em>Save</em>' if q['id'] == 'combo' else '') for q in opts)
    body = '''<div class="wrap pdp" data-product="%(id)s">
  <div class="gallery"><div class="main"><img id="pdp-img" src="%(main)s" alt="%(alt)s" width="1000" height="1000" fetchpriority="high"></div><div class="thumbs">%(thumbs)s</div></div>
  <div>
    <span class="eyebrow">Youth Face%(badge)s</span>
    <h1>%(name)s</h1>
    <div class="price"><b>%(price)s</b>%(mrp)s%(off)s</div>
    <p class="tax">Inclusive of all taxes · Free shipping · %(size)s</p>
    <p class="summary">%(summary)s</p>
    %(switch)s
    <div class="qty-row"><div class="qty" data-qty><button type="button" data-dec aria-label="Less">−</button><output>1</output><button type="button" data-inc aria-label="More">+</button></div><span class="muted" style="font-size:.9rem">In stock · ships from Bhatkal</span></div>
    <div class="acts"><button class="btn ghost" type="button" data-add="%(id)s" data-useqty>Add to cart</button><button class="btn" type="button" data-buy="%(id)s" data-useqty>Buy now</button></div>
    <div class="dcheck"><label for="dc-pin">Check delivery to your pincode</label><div class="dc-row"><input id="dc-pin" inputmode="numeric" maxlength="6" autocomplete="postal-code" placeholder="6-digit pincode"><button type="button" class="btn sm ghost" id="dc-go">Check</button></div><p class="dc-out" id="dc-out" role="status" aria-live="polite" hidden></p></div>
    <ul class="perks"><li>Cash on Delivery available (₹99 advance)</li><li>Free shipping across India</li><li>100%% original, shipped by the brand</li></ul>
    <div class="tabs">%(tabs)s</div>
  </div>
</div>
<section style="padding-top:20px"><div class="wrap"><div class="sec-h"><h2>Questions</h2></div>%(faq)s</div></section>
<section style="padding-top:20px"><div class="wrap"><div class="sec-h"><span class="eyebrow">You may also like</span><h2>More from Youth Face</h2></div><div class="grid three">%(rel)s</div></div></section>
<div class="buybar" id="buybar" hidden><div class="wrap buybar-in"><img src="%(thumb)s" alt="" width="48" height="48"><div class="bb-t"><b>%(card)s</b><span><b>%(price)s</b>%(bbmrp)s</span></div><button class="btn" type="button" data-buy="%(id)s" data-useqty>Buy now</button></div></div>''' % dict(
        thumb=img(p['thumb']), card='Body Lotion' if p['id'] == 'lotion' else p['card'].split(' · ')[-1], bbmrp=' <s>%s</s>' % rs(p['mrp']) if off else '',
        id=p['id'], switch=switch, main=img(p['imgs'][0]), alt=html.escape(p['name']), thumbs=thumbs,
        badge=' · ' + p['badge'] if p['badge'] else '', name=html.escape(p['name']), price=rs(p['price']),
        mrp='<s>MRP %s</s>' % rs(p['mrp']) if off else '', off='<span class="off">%d%% off</span>' % off if off else '', size=p['size'], summary=summary,
        tabs=''.join('<details%s><summary>%s</summary><div class="in">%s</div></details>' % (' open' if n == 0 else '', t, c) for n, (t, c) in enumerate(tabs)),
        faq=faq_html(PDP_FAQ), rel=''.join(card(q) for q in others))
    ogt = '<meta property="product:brand" content="Youth Face">\n<meta property="product:availability" content="in stock">\n<meta property="product:condition" content="new">\n<meta property="product:price:amount" content="%d">\n<meta property="product:price:currency" content="INR">\n<meta property="product:retailer_item_id" content="%s">\n' % (p['price'], p['sku'])
    page(url(p), p['title'], p['desc'], body, og='product', ogimg=p['og'], extra_head=ogt,
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
  <label class="remind"><input type="checkbox" id="co-remind"><span><b>Remind me on WhatsApp when my cream is about to run out</b><small>One friendly message, timed to your pack size. Reply STOP any time.</small></span></label>
  <p class="muted" id="cod-terms" style="font-size:.84rem" hidden>Cash on Delivery orders are confirmed with a ₹99 advance paid online now. It is part of the price, not an extra charge. If the parcel is refused at delivery, the ₹99 is not refunded.</p>
  <div class="notyet" id="not-yet" hidden><p><b>Plot twist: your order isn't placed yet.</b> The payment window closed before it finished. Nothing is lost. Your details are saved, so it's one tap from here.</p><button type="button" class="btn" id="ny-retry">Try payment again</button><button type="button" class="btn ghost" id="ny-switch">Switch to Cash on Delivery</button></div>
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
    dict(slug='skincare-routine-basics', old='routine', title='Skincare routine basics', blurb='Build a simple routine and learn the usual order to apply products.',
         seo='Skincare Routine Basics: The Simple Order to Apply Products | Youth Face',
         desc='A beginner-friendly skincare routine: cleanse, treat and protect. Learn the order to apply products, how much to use and how long to wait for results.',
         body='''<p>A skincare routine does not need ten steps. Most people do best with three: <b>cleanse, treat, protect</b>. The routine that works is the one you can repeat every day without thinking about it.</p>
<h2>Step 1: Cleanse</h2><p>Wash your face with a gentle cleanser and lukewarm water, then pat dry with a clean towel. Very hot water and harsh scrubbing can leave skin tight and irritated, which makes every product that follows feel worse.</p>
<h2>Step 2: Treat</h2><p>This is where a targeted cream such as <a href="/product/youth-face-beauty-cream-25g-pack-of-1-kojic-acid-alpha-arbutin/">Youth Face Beauty Cream</a> goes. Apply it to clean, dry skin. A pea-sized amount covers the face; a little more if you include the neck. Massage gently until it disappears.</p>
<h2>Step 3: Protect (mornings)</h2><p>In the morning, finish with a broad-spectrum sunscreen. Sun exposure is one of the main reasons dark spots appear and stay, so skipping sunscreen undoes much of the work of any dark-spot routine.</p>
<h2>The usual order</h2><p>A simple rule: <b>thinnest to thickest</b>. Watery products go first, creams next, sunscreen last in the morning. Give each layer about a minute before the next.</p>
<h2>How long before you see a change?</h2><p>Skin renews itself slowly. Use the same routine daily for several weeks before deciding whether it works for you, and compare photos taken in the same light. Changing products every few days makes it impossible to tell what is helping.</p>
<h2>Keep it gentle</h2><ul><li>Patch test any new product on a small area for 24 hours.</li><li>Introduce one new product at a time.</li><li>If redness, burning or itching continues, stop and speak to a dermatologist.</li></ul>'''),
    dict(slug='kojic-acid', old='kojic-acid', title='Understanding Kojic Acid', blurb='Why it is used in skincare and what to keep in mind.',
         seo='What Is Kojic Acid? Uses in Skincare, How to Use It & Tips | Youth Face',
         desc='Kojic Acid explained simply: where it comes from, why it is used in creams for dark spots and uneven-looking tone, and how to use it safely with sunscreen.',
         body='''<p>Kojic Acid is one of the most familiar names on the label of creams made for dark spots and uneven-looking skin tone. Here is what it is and how to use it sensibly.</p>
<h2>Where it comes from</h2><p>Kojic Acid was first identified as a by-product of fermenting rice for sake and soy sauce. Today it is produced for cosmetic use and added to creams, serums and soaps.</p>
<h2>Why it is used in skincare</h2><p>It is used in products for <b>dark-spot care</b> and a <b>more even-looking complexion</b>. It is often paired with other ingredients such as Alpha Arbutin, as in <a href="/product/youth-face-beauty-cream-25g-pack-of-1-kojic-acid-alpha-arbutin/">Youth Face Beauty Cream</a>, so the formula works as a team rather than relying on a single ingredient.</p>
<h2>How to use a Kojic Acid cream</h2><ol><li>Patch test first, on the side of the neck or inner arm, for 24 hours.</li><li>Apply a small amount to clean, dry skin once a day to start. Move to twice a day if your skin is comfortable.</li><li>Use sunscreen every morning. Without it, new spots keep forming.</li></ol>
<h2>What to keep in mind</h2><ul><li>Some people find it mildly tingly at first. Persistent redness or burning means stop.</li><li>Avoid the eye area and broken or freshly waxed skin.</li><li>Do not stack several strong active products at once. Keep the rest of the routine simple.</li><li>Results are gradual and vary from person to person.</li></ul>
<h2>The short version</h2><p>Kojic Acid is a well-known ingredient for dark-spot care. Use it consistently, gently and always with sunscreen, and judge it over weeks, not days.</p>'''),
    dict(slug='alpha-arbutin', old='alpha-arbutin', title='Understanding Alpha Arbutin', blurb='Its role in products for a more even-looking complexion.',
         seo='What Is Alpha Arbutin? Benefits in Skincare & How to Use It | Youth Face',
         desc='Alpha Arbutin explained: why this gentle ingredient is used for a brighter, more even-looking complexion, how it pairs with Kojic Acid, and how to use it.',
         body='''<p>Alpha Arbutin is a popular ingredient in products made for a brighter-looking, more even complexion. It has a reputation for being gentle, which is why it is often paired with stronger-feeling ingredients.</p>
<h2>What it is</h2><p>Arbutin occurs naturally in plants such as bearberry. Alpha Arbutin is a stable form made for cosmetics, so it keeps working in a cream over the product's shelf life.</p>
<h2>Why it is used</h2><p>It is used for <b>dark-spot care</b> and to help skin look more even in tone. Because it is generally well tolerated, it suits people who want a steady, low-drama routine.</p>
<h2>Alpha Arbutin and Kojic Acid together</h2><p>The two are a common pairing. <a href="/skincare-guides/kojic-acid/">Kojic Acid</a> and Alpha Arbutin are used side by side so one gentle formula can do more than either alone. <a href="/product/youth-face-beauty-cream-25g-pack-of-1-kojic-acid-alpha-arbutin/">Youth Face Beauty Cream</a> is built around exactly this pair.</p>
<h2>How to use it</h2><ol><li>Apply to clean, dry skin, once or twice a day.</li><li>Follow with sunscreen in the morning.</li><li>Be patient: expect gradual change over several weeks of regular use.</li></ol>
<h2>Good to know</h2><ul><li>Even gentle ingredients deserve a patch test.</li><li>Consistency beats quantity. A thick layer does not work faster.</li><li>If you are pregnant, nursing or under treatment for a skin condition, ask your doctor before starting any new active product.</li></ul>'''),
    dict(slug='how-to-use-youth-face', old='using-youth-face', title='How to use Youth Face products', blurb='Simple directions for the Beauty Cream and Body Lotion.',
         seo='How to Use Youth Face Beauty Cream and Body Lotion | Step-by-Step Guide',
         desc='Step-by-step directions for Youth Face Beauty Cream with Kojic Acid & Alpha Arbutin and Youth Face Body Lotion: how much to use, when, and what to avoid.',
         body='''<p>Both Youth Face products are made for a simple daily routine. Here is exactly how to use each one.</p>
<h2>Youth Face Beauty Cream (face)</h2><ol><li>Wash your face with a gentle cleanser and pat dry.</li><li>Take a pea-sized amount for the face, a little more if you include the neck.</li><li>Dot it on the forehead, cheeks and chin, then massage in gently until absorbed. Avoid the eye area.</li><li>Use once a day to start, then twice a day (morning and night) if your skin is comfortable.</li><li>Every morning, finish with a broad-spectrum sunscreen.</li></ol>
<p>One 25 g jar usually lasts around a month of daily use, depending on how much you apply, which is why many customers choose the <a href="/product/youth-face-beauty-cream-pack-of-2-kojic-acid-alpha-arbutin/">Pack of 2</a> or <a href="/product/youth-face-beauty-cream-pack-of-3-kojic-acid-alpha-arbutin/">Pack of 3</a> to keep the routine going without a gap.</p>
<h2>Youth Face Body Lotion (body)</h2><ol><li>Apply a generous amount to clean, dry body skin, ideally after a bath.</li><li>Massage in until absorbed.</li><li>Use daily, or whenever skin feels dry.</li></ol>
<p>The <a href="/product/youth-face-body-lotion/">Body Lotion</a> is a separate product for the body. Use the Beauty Cream on your face.</p>
<h2>Before first use</h2><ul><li>Patch test on a small area for 24 hours.</li><li>Do not apply on broken, sunburnt or freshly waxed skin.</li><li>Stop if irritation continues, and consult a dermatologist.</li></ul>
<p>See also the full <a href="/how-to-use/">How To Use</a> page.</p>'''),
    dict(slug='daytime-skincare-routine', old='daytime', title='Daytime skincare routine', blurb='Cleanse, apply and protect before you step out.',
         seo='Daytime Skincare Routine: 3 Steps Before You Step Out | Youth Face',
         desc='A quick morning skincare routine for Indian weather: cleanse, apply your cream and protect with sunscreen. Includes reapplying tips for long days outdoors.',
         body='''<p>The morning routine has one main job: get your skin ready for the day and protect it from the sun. It takes under five minutes.</p>
<h2>1. Rinse or cleanse</h2><p>If your skin feels oily or you sweated at night, use a gentle cleanser. If it feels comfortable, a splash of water is enough. Pat dry.</p>
<h2>2. Apply your cream</h2><p>Apply a pea-sized amount of <a href="/product/youth-face-beauty-cream-25g-pack-of-1-kojic-acid-alpha-arbutin/">Youth Face Beauty Cream</a> to the face and neck and let it absorb for a minute.</p>
<h2>3. Sunscreen, every day</h2><p>Use a broad-spectrum sunscreen, SPF 30 or higher, on the face, neck and ears. Use about two finger-lengths for the face and neck. Sunscreen matters even on cloudy days and indoors near windows.</p>
<h2>On long days outdoors</h2><ul><li>Reapply sunscreen every two to three hours, and after sweating heavily.</li><li>A cap, scarf or umbrella helps more than people expect.</li><li>Carry a small towel to blot sweat instead of rubbing.</li></ul>
<h2>Keep it light in humid weather</h2><p>In heat and humidity, fewer, thinner layers feel better and stay put. Skip heavy creams in the morning and save extra moisture for the night.</p>
<p>Next: the <a href="/skincare-guides/evening-skincare-routine/">evening routine</a>.</p>'''),
    dict(slug='evening-skincare-routine', old='evening', title='Evening skincare routine', blurb='A calm, simple routine before bed.',
         seo='Evening Skincare Routine: A Simple Night Routine | Youth Face',
         desc='A calm night skincare routine: remove sunscreen and the day\'s dirt, apply your treatment cream, and let skin rest. Simple steps and common mistakes to avoid.',
         body='''<p>The evening routine is about cleaning off the day and giving your treatment cream time to work while you sleep.</p>
<h2>1. Clean off the day</h2><p>Sunscreen, sweat, dust and makeup need to come off. Use a gentle cleanser; if you wear heavy makeup or water-resistant sunscreen, cleanse twice. Pat dry.</p>
<h2>2. Apply your cream</h2><p>Apply <a href="/product/youth-face-beauty-cream-25g-pack-of-1-kojic-acid-alpha-arbutin/">Youth Face Beauty Cream</a> to clean, dry skin. Night is a good time for your treatment step because there is no sun exposure afterwards.</p>
<h2>3. Let it rest</h2><p>Give the cream a few minutes to absorb before lying down, and change pillowcases often, since they collect oil and dirt.</p>
<h2>Common mistakes</h2><ul><li><b>Too many actives at once.</b> Layering several strong products at night is a common cause of irritation. Keep it to one treatment cream.</li><li><b>Skipping the cleanse.</b> Cream applied over the day's sunscreen and dust works less well.</li><li><b>Scrubbing hard.</b> Rough exfoliation makes skin sensitive. Gentle is enough.</li></ul>
<p>Pair this with the <a href="/skincare-guides/daytime-skincare-routine/">daytime routine</a> and you have the whole day covered.</p>'''),
]


def guide_url(g):
    return '/skincare-guides/%s/' % g['slug']


guides = top('Skincare Guides', 'Youth Face skincare guides', 'Plain, practical guides to building a routine and understanding the ingredients you use.') + \
    '<section style="padding-top:24px"><div class="wrap"><div class="guides">%s</div><div class="prose" style="margin-top:40px">%s<p class="note">This information is general and does not replace advice from a qualified dermatologist or healthcare professional.</p></div></div></section>' % (
        ''.join('<a href="%s"><span class="eyebrow">Guide</span><h3>%s</h3><p>%s</p></a>' % (guide_url(g), g['title'], g['blurb']) for g in GUIDES),
        ''.join('<h2 id="%s">%s</h2><p>%s <a href="%s">Read the full guide</a></p>' % (g['old'], g['title'], g['blurb'], guide_url(g)) for g in GUIDES))
page('/skincare-guides/', 'Skincare Guides | Kojic Acid, Alpha Arbutin & Daily Routines | Youth Face', 'Youth Face skincare guides: routine basics, Kojic Acid, Alpha Arbutin, how to use Youth Face, and simple day and night routines.', guides,
     crumbs=[('Skincare Guides', '/skincare-guides/')], schema=[{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': SITE + guide_url(g), 'name': g['title']} for i, g in enumerate(GUIDES)]}])

for i, g in enumerate(GUIDES):
    more = [GUIDES[(i + j) % len(GUIDES)] for j in (1, 2, 3)]
    body = top('Skincare guide', g['title'], g['blurb']) + \
        '<section style="padding-top:20px"><div class="wrap article"><div class="prose">%s<p class="note">This guide is general information about cosmetic skincare and does not replace advice from a qualified dermatologist. Results vary from person to person.</p></div>' \
        '<aside class="guide-cta"><img src="%s" alt="Youth Face Beauty Cream with Kojic Acid and Alpha Arbutin" width="600" height="600" loading="lazy"><b>Youth Face Beauty Cream</b><span>Kojic Acid &amp; Alpha Arbutin · from %s · COD available</span><a class="btn block" href="/shop/">Shop now</a></aside></div></section>' \
        '<section style="padding-top:8px"><div class="wrap"><div class="sec-h"><span class="eyebrow">Keep reading</span><h2>More guides</h2></div><div class="guides">%s</div></div></section>' % (
            g['body'], img(PRODUCTS[1]['thumb']), rs(PRODUCTS[0]['price']),
            ''.join('<a href="%s"><span class="eyebrow">Guide</span><h3>%s</h3><p>%s</p></a>' % (guide_url(m), m['title'], m['blurb']) for m in more))
    art = {'@type': 'Article', 'headline': g['title'], 'description': g['desc'], 'datePublished': TODAY, 'dateModified': TODAY,
           'mainEntityOfPage': SITE + guide_url(g), 'image': SITE + PRODUCTS[1]['og'], 'inLanguage': 'en-IN',
           'author': {'@id': SITE + '/#org'}, 'publisher': {'@id': SITE + '/#org'}}
    page(guide_url(g), g['seo'], g['desc'], body, og='article', crumbs=[('Skincare Guides', '/skincare-guides/'), (g['title'], guide_url(g))], schema=[art])

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

BIZ = '''<div class="bizcard"><b>Business details</b><span>Youth Face, a brand of %s</span><span>%s</span><span>WhatsApp and phone: %s</span><span>Hours: Monday to Saturday, 10 am to 7 pm IST</span></div>''' % (OWNER, ADDR, WA_SHOW)
GRIEV = '''<h2>Grievance officer</h2><p>In line with the Consumer Protection (E-Commerce) Rules, 2020, complaints can be sent to our Grievance Officer: <b>%s</b>, %s, %s. WhatsApp and phone: %s. We acknowledge every complaint within 48 hours and aim to resolve it within one month of receiving it.</p>''' % (GRIEVANCE_NAME, OWNER, ADDR, WA_SHOW)
POL = {
'/privacy-policy/': ('Privacy Policy', 'Privacy Policy | Youth Face', 'How Youth Face collects, uses, shares and protects your personal information, how we use cookies and Google and Meta advertising, and how to opt out or delete your data.', '''
<p>This Privacy Policy explains how Youth Face, a brand of %(o)s (&ldquo;we&rdquo;, &ldquo;us&rdquo;), collects, uses, shares and protects personal information when you visit youthfacebeautycream.com (the &ldquo;site&rdquo;) or place an order. By using the site you agree to this policy.</p>
%(biz)s
<h2>1. Information we collect</h2>
<p><b>Information you give us:</b> when you order or contact us, we collect your name, mobile number, delivery address, city and pincode, the products you choose, and any messages you send us on WhatsApp.</p>
<p><b>Payment information:</b> payments are processed by Razorpay Software Private Limited. Card, UPI and netbanking details are entered on Razorpay&rsquo;s secure page and are never seen or stored by us. We receive only a payment ID and the payment status.</p>
<p><b>Information collected automatically:</b> like most websites, our hosting provider and the tools described below record technical information such as your IP address, browser and device type, pages viewed, the website that referred you, and the time of your visit.</p>
<h2>2. How we use your information</h2>
<ul><li>To process, pack, ship and deliver your order, and to collect Cash on Delivery payments.</li><li>To send you order confirmations and delivery updates, and to answer your questions.</li><li>If you start a payment and do not complete it, we may contact you once on the number you entered to ask whether you need help finishing the order.</li><li>To prevent fraud and misuse of the site.</li><li>To measure how our website and ads perform and to show you relevant Youth Face ads (see section 4).</li><li>To meet legal, tax and accounting requirements.</li></ul>
<p>We do <b>not</b> sell or rent your personal information to anyone.</p>
<h2>3. Who we share it with</h2>
<p>We share only what each partner needs to do its job:</p>
<ul><li><b>Razorpay</b>, to process payments.</li><li><b>Shiprocket and its courier partners</b>, who receive your name, phone number and address to deliver your parcel.</li><li><b>Vercel</b>, which hosts this website.</li><li><b>Google and Meta</b>, for advertising measurement as described below.</li><li><b>WhatsApp</b> (Meta), when you choose to message us there.</li><li><b>Government or legal authorities</b>, when required by law.</li></ul>
<h2>4. Cookies, advertising and remarketing</h2>
<p>We use cookies and similar technologies to keep the site working (for example, your cart) and to measure and improve our advertising.</p>
<p><b>Google:</b> we use Google Ads, including remarketing. Third-party vendors, including Google, use cookies to show our ads to you on sites across the internet based on your previous visits to this site, and to measure ad conversions. You can opt out of Google&rsquo;s use of cookies for personalised ads at <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>, and learn how Google uses data at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">How Google uses information from sites that use its services</a>.</p>
<p><b>Meta (Facebook and Instagram):</b> we may use the Meta Pixel to measure the results of our ads and to show Youth Face ads to people who visited our site. You can control this in your <a href="https://www.facebook.com/adpreferences" rel="noopener">Facebook ad preferences</a>.</p>
<p>You can also opt out of many third-party vendors&rsquo; use of cookies for interest-based advertising at <a href="https://optout.aboutads.info" rel="noopener">aboutads.info</a>, or block and delete cookies in your browser settings. Blocking cookies may stop the cart from working.</p>
<p>We do not send your name, phone number or address to Google or Meta through these tools.</p>
<h2>5. Information saved on your device</h2>
<p>Your cart, and the delivery details you type at checkout, are saved in your own browser (local storage) so you do not need to type them again. This stays on your device and you can clear it at any time from your browser settings.</p>
<h2>6. How long we keep it</h2>
<p>We keep order records for as long as needed to fulfil and support your order and as required by Indian tax and accounting law. Information that is no longer needed is deleted.</p>
<h2>7. How we protect it</h2>
<p>The site uses HTTPS encryption. Payment details are handled only by Razorpay, which is PCI-DSS compliant. Access to order information is limited to the people who need it to serve you. No method of transmission over the internet is completely secure, but we take reasonable steps to protect your information.</p>
<h2>8. Your rights and choices</h2>
<p>You may ask us to access, correct or delete your personal information, or to stop contacting you, by messaging us on WhatsApp at %(wa)s. Reply STOP to any message from us and we will not contact you again about marketing. We will respond within 30 days.</p>
<h2>9. Children</h2>
<p>This site is intended for adults. We do not knowingly collect personal information from children under 18.</p>
<h2>10. Changes to this policy</h2>
<p>We may update this policy from time to time. The latest version is always on this page with the date it was last updated.</p>
%(griev)s''' % dict(o=OWNER, biz=BIZ, wa=WA_SHOW, griev=GRIEV)),

'/terms-conditions/': ('Terms & Conditions', 'Terms & Conditions | Youth Face', 'Terms and conditions for buying Youth Face products on youthfacebeautycream.com: orders, prices, payment, Cash on Delivery, product use, liability and governing law.', '''
<p>These Terms and Conditions apply to your use of youthfacebeautycream.com and to every order placed on it. The site is operated by %(o)s, which sells products under the Youth Face brand. By using the site or placing an order, you agree to these terms.</p>
%(biz)s
<h2>1. Eligibility</h2><p>You must be at least 18 years old, or use the site under the supervision of a parent or guardian, to place an order.</p>
<h2>2. Products and descriptions</h2><p>We try to show products, ingredients and prices accurately. Colours and packaging may look slightly different on screen. The full ingredient list is printed on every pack. Our products are cosmetics. They are not medicines and are not intended to diagnose, treat, cure or prevent any disease.</p>
<h2>3. Prices</h2><p>All prices are in Indian rupees (₹) and include applicable taxes. Shipping is free across India. There are no hidden charges: the amount shown at checkout is the full amount you pay. If a product is listed at a clearly wrong price because of an error, we may cancel the order and refund any amount paid in full.</p>
<h2>4. Orders</h2><p>An order is confirmed only when payment, or the Cash on Delivery advance, is received and you see the confirmation screen. We may refuse or cancel an order if a product is out of stock, the delivery pincode is not serviceable, or the order details appear incorrect or fraudulent. If we cancel, any amount paid is refunded in full to the original payment method.</p>
<h2>5. Payment</h2><p>You can pay online by UPI, debit or credit card, or netbanking through Razorpay. We do not store your card or UPI details.</p>
<h2>6. Cash on Delivery</h2><p>Cash on Delivery orders are confirmed with an advance of <b>₹99 paid online</b>. The advance is part of the product price, not an extra fee, and the remaining amount is paid in cash to the courier at delivery. If a Cash on Delivery parcel is refused at the door, or cannot be delivered because the address or phone number given was incorrect, the ₹99 advance is not refunded, as it covers the cost of shipping the parcel both ways. In every other case, including cancellations before dispatch, the advance is refunded in full.</p>
<h2>7. Shipping, returns and refunds</h2><p>Delivery is covered by our <a href="/shipping-delivery/">Shipping &amp; Delivery Policy</a>. Returns, replacements and refunds are covered by our <a href="/refund-returns-policy/">Refund &amp; Returns Policy</a>.</p>
<h2>8. Using our products safely</h2><p>Read the label and follow the directions. Patch test on a small area for 24 hours before first use. Avoid the eyes and broken skin. Stop use and consult a doctor if irritation occurs. If you are pregnant, breastfeeding or being treated for a skin condition, ask your doctor before use. Results vary from person to person and are not guaranteed.</p>
<h2>9. Reviews and content</h2><p>All text, photos, logos and designs on this site belong to %(o)s and may not be copied without permission.</p>
<h2>10. Limitation of liability</h2><p>To the extent permitted by law, our total liability for any claim relating to an order is limited to the amount you paid for that order. Nothing in these terms limits your rights under the Consumer Protection Act, 2019 or other Indian law.</p>
<h2>11. Governing law</h2><p>These terms are governed by the laws of India. Any dispute is subject to the jurisdiction of the courts in Uttara Kannada district, Karnataka.</p>
<h2>12. Changes</h2><p>We may update these terms. The version on this page on the day you place your order applies to that order.</p>
%(griev)s''' % dict(o=OWNER, biz=BIZ, griev=GRIEV)),

'/refund-returns-policy/': ('Refund & Returns', 'Refund and Returns Policy | Youth Face', 'Youth Face returns and refunds: 7-day return window, which items qualify, how to request a return, who pays return shipping, and refunds in 5 to 7 business days.', '''
<p>We want you to be happy with your Youth Face order. This policy explains when you can return a product, how to do it, and how and when you are refunded.</p>
<div class="policy-sum"><div><b>7 days</b><span>to request a return after delivery</span></div><div><b>Free</b><span>replacement or refund if the item is damaged, defective or wrong</span></div><div><b>5–7 days</b><span>for the refund to reach your account after approval</span></div></div>
<h2>1. Return window</h2><p>You can request a return within <b>7 days of delivery</b>. Requests made after 7 days cannot be accepted, except where required by law.</p>
<h2>2. Items that can be returned</h2><ul><li><b>Damaged, defective, leaking or wrong items:</b> we replace the item or refund you in full, including any shipping cost. You do not pay anything to return it.</li><li><b>Unopened items you no longer want:</b> accepted within 7 days if the item is unused, sealed and in its original packaging. You arrange and pay for the return shipping. After we receive and check it, we refund the product price.</li></ul>
<h2>3. Items that cannot be returned</h2><p>For hygiene and safety reasons, cosmetics that have been <b>opened, used, tested or tampered with</b>, or whose seal is broken, cannot be returned unless they arrived damaged, defective or wrong. Your statutory rights are not affected.</p>
<h2>4. How to request a return</h2><ol><li>Message us on WhatsApp at %(wa)s within 7 days of delivery with your order number or the mobile number used on the order.</li><li>Send clear photos of the product, its packaging and the shipping label. For damaged or leaking items, a short unboxing video helps us resolve it faster.</li><li>We reply within 2 business days. If approved, we tell you whether we will arrange a pickup or how to send the item back. Please do not send items back without approval.</li></ol>
<h2>5. Refunds</h2><ul><li><b>When:</b> we start the refund within 2 business days of receiving and checking the returned item, or of approving your claim when no return is needed (for example, a wrong item).</li><li><b>Prepaid orders:</b> refunded to the original payment method (UPI, card or bank account) through Razorpay. Banks usually take <b>5 to 7 business days</b> to show the amount.</li><li><b>Cash on Delivery orders:</b> the ₹99 advance is refunded to the original payment method; the cash part is refunded by UPI or bank transfer to the account details you share with us.</li><li>You will receive a confirmation on WhatsApp when the refund is made.</li></ul>
<h2>6. Replacements</h2><p>If you prefer a replacement for a damaged, defective or wrong item, we ship it free of charge as soon as the claim is approved, subject to stock.</p>
<h2>7. Cancellations</h2><p>You can cancel an order free of charge at any time <b>before it is dispatched</b> by messaging us on WhatsApp. Any amount paid, including the Cash on Delivery advance, is refunded in full within 5 to 7 business days. Once an order has been dispatched, it cannot be cancelled, but you may refuse delivery or follow the return process above.</p>
<h2>8. Refused or undeliverable Cash on Delivery orders</h2><p>If a Cash on Delivery parcel is refused at delivery, or returned because the address or phone number was incorrect, the ₹99 advance is not refunded, as it covers two-way shipping. This is shown at checkout before you pay.</p>
<h2>9. Orders from other sellers</h2><p>This policy covers orders placed on youthfacebeautycream.com. Products bought from other websites or shops follow that seller&rsquo;s policy.</p>
%(biz)s
%(griev)s''' % dict(wa=WA_SHOW, biz=BIZ, griev=GRIEV)),

'/shipping-delivery/': ('Shipping & Delivery', 'Shipping & Delivery Policy | Youth Face', 'Youth Face shipping: free shipping across India, dispatched in 1 to 3 business days, delivered in 3 to 7 business days after dispatch, Cash on Delivery and tracking.', '''
<p>This policy explains where we ship, what it costs and how long it takes.</p>
<div class="policy-sum"><div><b>₹0</b><span>shipping on every order, anywhere in India</span></div><div><b>1–3 days</b><span>to pack and dispatch (business days)</span></div><div><b>3–7 days</b><span>delivery after dispatch, depending on pincode</span></div></div>
<h2>1. Where we ship</h2><p>We ship to serviceable pincodes across <b>India only</b>. We do not ship outside India. At checkout, entering your pincode shows your city and an estimated delivery date. If your pincode turns out not to be serviceable after you order, we contact you and refund any amount paid in full.</p>
<h2>2. Shipping charges</h2><p>Shipping is <b>free</b> on all orders. There is no minimum order value and no extra handling or Cash on Delivery fee.</p>
<h2>3. Processing time</h2><p>Orders are packed and handed to the courier within <b>1 to 3 business days</b> (Monday to Saturday, excluding public holidays) after payment or Cash on Delivery confirmation. Orders placed on Sundays or holidays are processed on the next business day.</p>
<h2>4. Delivery time</h2><p>After dispatch, delivery usually takes <b>3 to 7 business days</b>: metro cities are often faster, and remote or hilly areas can take longer. Delivery dates are estimates. Delays can happen because of weather, strikes, festivals or courier issues outside our control; we will help you follow up if your parcel is late.</p>
<h2>5. Couriers and tracking</h2><p>Orders ship through Shiprocket with trusted courier partners. Once the parcel is collected, you can track it on our <a href="/track-order/">Track Order</a> page using your mobile number and pincode, or your payment ID.</p>
<h2>6. Cash on Delivery</h2><p>Cash on Delivery is available on most pincodes. You pay ₹99 online to confirm the order, and the remaining amount in cash to the courier at delivery. Please keep the exact amount ready.</p>
<h2>7. Delivery attempts and address</h2><p>Please enter a complete address with landmark and a mobile number that can be reached. The courier usually makes up to three delivery attempts. If the parcel cannot be delivered, it is returned to us; see our <a href="/refund-returns-policy/">Refund &amp; Returns Policy</a> for what happens next.</p>
<h2>8. Damaged or tampered parcels</h2><p>If the outer package looks damaged or tampered with, you may refuse it, or take photos before opening. Contact us on WhatsApp within 7 days of delivery and we will replace or refund damaged items at no cost.</p>
%(biz)s
%(griev)s''' % dict(biz=BIZ, griev=GRIEV)),
}

for path, (h, t, d, body) in POL.items():
    page(path, t, d, top('Policy', h, 'Last updated: 9 October 2026') + '<section style="padding-top:20px"><div class="wrap prose">%s</div></section>' % body, crumbs=[(h, path)])

page('/404', 'Page not found | Youth Face', 'This page could not be found.', top('404', 'This page could not be found', 'The link may be old or mistyped.') + '<section style="padding-top:20px"><div class="wrap"><a class="btn" href="/shop/">Go to the shop</a></div></section>', index=False)

exec(open(os.path.join(B, 'langs.py'), encoding='utf-8').read())

# ---------------- Owner page (private, needs ADMIN_KEY) ----------------
owner = top('Owner only', 'Orders and follow-ups', 'Paid orders, people who started an order and did not pay, and customers due a reorder. Youth Face orders only.') + \
    '''<section style="padding-top:20px"><div class="wrap track"><form class="form" id="ro-form" novalidate>
  <div class="f"><label for="ro-key">Owner code</label><input id="ro-key" type="text" class="masked" autocomplete="off" autocapitalize="off" spellcheck="false" inputmode="text"></div>
  <div class="f"><label for="ro-range">Show</label><select id="ro-range"><option value="today">Paid orders today</option><option value="week">Paid orders, last 7 days</option><option value="left">Started an order, did not pay (last 3 days)</option><option value="refill">Refill reminders due now (customer asked)</option><option value="25-40">Ordered 25 to 40 days ago (reorder due)</option><option value="41-70">Ordered 41 to 70 days ago (missed)</option><option value="0-24">Ordered 0 to 24 days ago (not due yet)</option></select></div>
  <button class="btn block" type="submit" id="ro-go">Show</button></form>
<div class="track-out" id="ro-out" hidden></div></div></section>'''
page('/reorder/', 'Orders and follow-ups | Youth Face', 'Owner page.', owner, index=False, js='store.js,owner.js')

# ---------------- Assets, sitemap, redirects ----------------
os.makedirs(os.path.join(ROOT, 'assets'), exist_ok=True)
shutil.copy(os.path.join(B, 'site.css'), os.path.join(ROOT, 'assets', 'site.css'))
shutil.copy(os.path.join(B, 'store.js'), os.path.join(ROOT, 'assets', 'store.js'))
shutil.copy(os.path.join(B, 'owner.js'), os.path.join(ROOT, 'assets', 'owner.js'))
open(os.path.join(ROOT, 'assets', 'products.json'), 'w').write(json.dumps({p['id']: {'name': p['name'], 'card': p['card'], 'price': p['price'], 'mrp': p['mrp'], 'img': img(p['thumb']), 'url': url(p), 'wc': p['wc']} for p in PRODUCTS}, ensure_ascii=False))
open(os.path.join(ROOT, 'assets', 'icon.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#740817"/><text x="32" y="44" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-weight="700" font-size="32" fill="#FBF3EA">YF</text></svg>')

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for pth in pages:
    pri = '1.0' if pth == '/' else '0.9' if pth.startswith('/product/') or pth == '/shop/' else '0.6'
    sm.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % (SITE, pth, TODAY, pri))
sm.append('</urlset>')
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
open(os.path.join(ROOT, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /cart/\nDisallow: /checkout/\nDisallow: /reorder/\nDisallow: /api/\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)

# Product feed for Google Merchant Center (free listings / Shopping) and the Meta or Instagram catalogue.
FEED_DESC = {
    'p1': 'Youth Face Beauty Cream, 25 g jar. A daily face cream with Kojic Acid and Alpha Arbutin for dark-spot care and a more even-looking skin tone. Apply a small amount to clean skin once or twice daily and use sunscreen in the morning. Cosmetic product. Free shipping across India, Cash on Delivery available.',
    'p2': 'Youth Face Beauty Cream, pack of 2 jars (2 x 25 g). A daily face cream with Kojic Acid and Alpha Arbutin for dark-spot care and a more even-looking skin tone. Better value per jar for regular use. Cosmetic product. Free shipping across India, Cash on Delivery available.',
    'p3': 'Youth Face Beauty Cream, pack of 3 jars (3 x 25 g). A daily face cream with Kojic Acid and Alpha Arbutin for dark-spot care and a more even-looking skin tone. Best value per jar. Cosmetic product. Free shipping across India, Cash on Delivery available.',
    'lotion': 'Youth Face Body Lotion, 40 ml. A lightweight, quick-absorbing daily body moisturiser for soft, comfortable skin. Apply to clean, dry skin after a bath. Free shipping across India, Cash on Delivery available.',
    'combo': 'Youth Face combo: one Beauty Cream 25 g jar with Kojic Acid and Alpha Arbutin for the face, and one Body Lotion 40 ml for the body, together at one price. Cosmetic products. Free shipping across India, Cash on Delivery available.',
}
FEED_GRAMS = {'p1': 60, 'p2': 120, 'p3': 180, 'lotion': 70, 'combo': 130}


def feed_xml():
    e = lambda v: html.escape(str(v), quote=False)
    items = []
    for p in PRODUCTS:
        cream = p['id'] != 'lotion'
        extra = ''.join('<g:additional_image_link>%s%s</g:additional_image_link>' % (SITE, i.replace('.webp', '.jpg')) for i in p['imgs'][1:])
        price = '<g:price>%d.00 INR</g:price>' % p['mrp'] + ('<g:sale_price>%d.00 INR</g:sale_price>' % p['price'] if p['mrp'] > p['price'] else '')
        multi = {'p2': '<g:multipack>2</g:multipack>', 'p3': '<g:multipack>3</g:multipack>', 'combo': '<g:is_bundle>yes</g:is_bundle>'}.get(p['id'], '')
        items.append('''<item>
  <g:id>%s</g:id><title>%s</title><description>%s</description>
  <link>%s%s</link><g:image_link>%s%s</g:image_link>%s
  <g:availability>in_stock</g:availability>%s
  <g:brand>Youth Face</g:brand><g:condition>new</g:condition><g:identifier_exists>no</g:identifier_exists>%s
  <g:google_product_category>%s</g:google_product_category><g:product_type>%s</g:product_type>
  <g:shipping><g:country>IN</g:country><g:service>Standard</g:service><g:price>0.00 INR</g:price></g:shipping>
  <g:shipping_weight>%d g</g:shipping_weight>
</item>''' % (p['sku'], e(p['name'].replace(' – ', ' - ')), e(FEED_DESC[p['id']]), SITE, url(p), SITE, p['og'], extra, price, multi,
                 'Health &amp; Beauty &gt; Personal Care &gt; Cosmetics &gt; Skin Care' + (' &gt; Lotion &amp; Moisturizer' if p['id'] == 'lotion' else ''),
                 'Skin Care &gt; ' + ('Body Lotion' if p['id'] == 'lotion' else 'Combo' if p['id'] == 'combo' else 'Face Cream'),
                 FEED_GRAMS[p['id']]))
    return '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
<channel>
<title>Youth Face</title><link>%s/</link><description>Youth Face product feed</description>
%s
</channel>
</rss>
''' % (SITE, '\n'.join(items))


os.makedirs(os.path.join(ROOT, 'feeds'), exist_ok=True)
open(os.path.join(ROOT, 'feeds', 'products.xml'), 'w').write(feed_xml())

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
# Old WordPress image addresses (indexed by Google Images) point to the matching new photo.
OLD_IMG = {'Youth-Face-Beauty-Cream-25g': 'yf-pack-1', 'ChatGPT-Image-Sep-17-2026-08_27_12-PM': 'yf-pack-2',
           'Youth-Face-Beauty-Cream-skincare-product-for-dark-spot-care': 'yf-pack-3', 'ChatGPT-Image-Sep-19-2026-01_47_45-AM': 'yf-body-lotion'}
for old, new in OLD_IMG.items():
    redirects.append({'source': '/wp-content/uploads/2026/10/%s(-600x600)?.png' % old, 'destination': '/assets/img/%s.jpg' % new, 'permanent': True})
for src in ['/wp-admin', '/wp-admin/:path*', '/wp-login.php', '/xmlrpc.php']:
    redirects.append({'source': src, 'destination': '/', 'permanent': False})
vercel = {'cleanUrls': False, 'redirects': redirects,
          'headers': [{'source': '/(assets|wp-content)/(.*)\\.(webp|jpg|jpeg|png|svg|mp4)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=86400, stale-while-revalidate=604800'}]},
                      {'source': '/(cart|checkout|reorder)/(.*)', 'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex'}]}]}
open(os.path.join(ROOT, 'vercel.json'), 'w').write(json.dumps(vercel, indent=2) + '\n')
open(os.path.join(ROOT, '.vercelignore'), 'w').write('_build\nREADME.md\n')
missing = [i for p in PRODUCTS for i in set(p['imgs'] + [p['thumb']]) if not os.path.exists(os.path.join(ROOT, i.strip('/')))]
print('built', len(pages), 'indexed pages;', len(redirects), 'redirects;', len(set(missing)), 'images still served from the old site')
