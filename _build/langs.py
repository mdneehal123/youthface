# Hindi and Urdu landing pages. Read by build.py with exec(), so it uses the helpers defined there.
L = {
 'hi': dict(
  path='/hi/', lang='hi', dir='ltr', font='Noto+Sans+Devanagari:wght@400;600;700', ff='"Noto Sans Devanagari"',
  title='यूथ फेस ब्यूटी क्रीम | कोजिक एसिड और अल्फा आर्बुटिन | ऑफिशियल स्टोर',
  desc='यूथ फेस ब्यूटी क्रीम: कोजिक एसिड और अल्फा आर्बुटिन वाली डेली फेस क्रीम, डार्क स्पॉट्स की देखभाल के लिए। ₹549 से, फ्री शिपिंग, कैश ऑन डिलीवरी।',
  eyebrow='यूथ फेस ब्यूटी क्रीम · कोजिक एसिड और अल्फा आर्बुटिन',
  h1='साफ़, निखरी त्वचा। <em>रोज़ की आसान आदत।</em>',
  lead='डार्क स्पॉट्स की देखभाल और एक-सी दिखने वाली रंगत के लिए डेली फेस क्रीम, सुबह-शाम की छोटी-सी रूटीन में।',
  ticks=['100% ओरिजिनल, सीधे ब्रांड से', 'कैश ऑन डिलीवरी उपलब्ध (₹99 एडवांस)', 'पूरे भारत में फ्री शिपिंग'],
  cta='पैक चुनें', ask='WhatsApp पर पूछें', watext='नमस्ते Youth Face, मुझे क्रीम के बारे में जानकारी चाहिए।',
  packs_h='अपना पैक चुनें', packs_p='एक जार से शुरू करें, या 2 और 3 के पैक में ज़्यादा बचत करें। हर ऑर्डर पर फ्री शिपिंग।',
  names={'p1': 'ब्यूटी क्रीम · 1 जार', 'p2': 'ब्यूटी क्रीम · 2 का पैक', 'p3': 'ब्यूटी क्रीम · 3 का पैक', 'lotion': 'बॉडी लोशन · 40 ml', 'combo': 'कॉम्बो: क्रीम + लोशन'},
  sizes={'p1': '1 × 25 ग्राम', 'p2': '2 × 25 ग्राम', 'p3': '3 × 25 ग्राम', 'lotion': '40 ml', 'combo': '25 ग्राम क्रीम + 40 ml लोशन'},
  badges={'p2': 'सबसे लोकप्रिय', 'p3': 'सबसे फ़ायदेमंद'},
  add='कार्ट में डालें', buy='अभी खरीदें', off='% छूट',
  combo_h='चेहरा + शरीर, एक दाम में', combo_p='यूथ फेस ब्यूटी क्रीम 25 ग्राम चेहरे के लिए और बॉडी लोशन 40 ml शरीर के लिए, साथ में सिर्फ़ %s में। अलग-अलग खरीदने से %s कम।',
  how_h='इस्तेमाल का तरीका', how=['हल्के क्लींज़र से चेहरा धोकर सुखा लें।', 'मटर के दाने जितनी क्रीम चेहरे और गर्दन पर हल्के हाथ से लगाएँ। आँखों से बचाएँ।', 'दिन में एक या दो बार लगाएँ। सुबह सनस्क्रीन ज़रूर लगाएँ।'],
  patch='पहली बार इस्तेमाल से पहले हाथ पर पैच टेस्ट करें। जलन हो तो इस्तेमाल बंद करें। नतीजे हर व्यक्ति में अलग हो सकते हैं।',
  cod_h='कैश ऑन डिलीवरी कैसे काम करता है', cod_p='अभी सिर्फ़ ₹99 ऑनलाइन दें, बाकी रकम पार्सल मिलने पर नकद दें। चाहें तो पूरा पेमेंट UPI, कार्ड या नेटबैंकिंग से भी कर सकते हैं।',
  faq_h='आपके सवाल',
  faq=[('क्या यह ओरिजिनल यूथ फेस क्रीम है?', 'जी हाँ। यह ब्रांड का अपना स्टोर है, जिसे भटकल, कर्नाटक का Beauty Mart चलाता है। हर ऑर्डर सीधे हमारे यहाँ से भेजा जाता है।'),
       ('डिलीवरी में कितने दिन लगते हैं?', 'ऑर्डर 1 से 3 कामकाजी दिनों में पैक होता है और भेजे जाने के बाद आम तौर पर 3 से 7 दिन में पहुँच जाता है।'),
       ('नतीजे कब दिखेंगे?', 'हर त्वचा अलग होती है। कई हफ़्तों तक रोज़ इस्तेमाल करें और रोज़ सनस्क्रीन लगाएँ।'),
       ('ऑर्डर कैसे करूँ?', 'पैक चुनकर “अभी खरीदें” दबाएँ। ऑर्डर फ़ॉर्म अंग्रेज़ी में है; कोई दिक्कत हो तो WhatsApp पर मैसेज करें, हम ऑर्डर कर देंगे।')],
  english='Read in English'),
 'ur': dict(
  path='/ur/', lang='ur', dir='rtl', font='Noto+Nastaliq+Urdu:wght@400;600;700', ff='"Noto Nastaliq Urdu"',
  title='یوتھ فیس بیوٹی کریم | کوجک ایسڈ اور الفا آربیوٹن | آفیشل اسٹور',
  desc='یوتھ فیس بیوٹی کریم: کوجک ایسڈ اور الفا آربیوٹن والی روزانہ کی فیس کریم، ڈارک اسپاٹس کی دیکھ بھال کے لیے۔ ₹549 سے، مفت شپنگ، کیش آن ڈیلیوری۔',
  eyebrow='یوتھ فیس بیوٹی کریم · کوجک ایسڈ اور الفا آربیوٹن',
  h1='صاف، نکھری جلد۔ <em>روز کی آسان عادت۔</em>',
  lead='ڈارک اسپاٹس کی دیکھ بھال اور یکساں نظر آنے والی رنگت کے لیے روزانہ کی فیس کریم، صبح و شام کی مختصر روٹین میں۔',
  ticks=['100% اصل، براہِ راست برانڈ سے', 'کیش آن ڈیلیوری دستیاب (₹99 ایڈوانس)', 'پورے ہندوستان میں مفت شپنگ'],
  cta='پیک منتخب کریں', ask='واٹس ایپ پر پوچھیں', watext='السلام علیکم Youth Face، مجھے کریم کے بارے میں معلومات چاہیے۔',
  packs_h='اپنا پیک منتخب کریں', packs_p='ایک جار سے شروع کریں، یا 2 اور 3 کے پیک میں زیادہ بچت کریں۔ ہر آرڈر پر مفت شپنگ۔',
  names={'p1': 'بیوٹی کریم · 1 جار', 'p2': 'بیوٹی کریم · 2 کا پیک', 'p3': 'بیوٹی کریم · 3 کا پیک', 'lotion': 'باڈی لوشن · 40 ml', 'combo': 'کومبو: کریم + لوشن'},
  sizes={'p1': '1 × 25 گرام', 'p2': '2 × 25 گرام', 'p3': '3 × 25 گرام', 'lotion': '40 ml', 'combo': '25 گرام کریم + 40 ml لوشن'},
  badges={'p2': 'سب سے مقبول', 'p3': 'سب سے فائدہ مند'},
  add='کارٹ میں ڈالیں', buy='ابھی خریدیں', off='% رعایت',
  combo_h='چہرہ + جسم، ایک قیمت میں', combo_p='یوتھ فیس بیوٹی کریم 25 گرام چہرے کے لیے اور باڈی لوشن 40 ml جسم کے لیے، دونوں صرف %s میں۔ الگ الگ خریدنے سے %s کم۔',
  how_h='استعمال کا طریقہ', how=['ہلکے کلینزر سے چہرہ دھو کر خشک کر لیں۔', 'مٹر کے دانے جتنی کریم چہرے اور گردن پر ہلکے ہاتھ سے لگائیں۔ آنکھوں سے بچائیں۔', 'دن میں ایک یا دو بار لگائیں۔ صبح سن اسکرین ضرور لگائیں۔'],
  patch='پہلی بار استعمال سے پہلے ہاتھ پر پیچ ٹیسٹ کریں۔ جلن ہو تو استعمال بند کر دیں۔ نتائج ہر شخص میں مختلف ہو سکتے ہیں۔',
  cod_h='کیش آن ڈیلیوری کیسے کام کرتی ہے', cod_p='ابھی صرف ₹99 آن لائن ادا کریں، باقی رقم پارسل ملنے پر نقد دیں۔ چاہیں تو پوری رقم UPI، کارڈ یا نیٹ بینکنگ سے بھی ادا کر سکتے ہیں۔',
  faq_h='آپ کے سوالات',
  faq=[('کیا یہ اصل یوتھ فیس کریم ہے؟', 'جی ہاں۔ یہ برانڈ کا اپنا اسٹور ہے، جسے بھٹکل، کرناٹک کا Beauty Mart چلاتا ہے۔ ہر آرڈر سیدھا ہمارے یہاں سے بھیجا جاتا ہے۔'),
       ('ڈیلیوری میں کتنے دن لگتے ہیں؟', 'آرڈر 1 سے 3 کاروباری دنوں میں پیک ہوتا ہے اور روانگی کے بعد عام طور پر 3 سے 7 دن میں پہنچ جاتا ہے۔'),
       ('نتائج کب نظر آئیں گے؟', 'ہر جلد مختلف ہوتی ہے۔ کئی ہفتوں تک روزانہ استعمال کریں اور روز سن اسکرین لگائیں۔'),
       ('آرڈر کیسے کروں؟', 'پیک منتخب کر کے «ابھی خریدیں» دبائیں۔ آرڈر فارم انگریزی میں ہے؛ کوئی مشکل ہو تو واٹس ایپ پر میسج کریں، ہم آرڈر کر دیں گے۔')],
  english='Read in English'),
}


def lcard(p, t):
    off = pct(p)
    b = t['badges'].get(p['id'], '')
    return '''<article class="card"><a class="ph" href="%s"><img src="%s" alt="%s" width="600" height="600" loading="lazy"></a>
  <div class="bd">%s<h3><a href="%s">%s</a></h3><span class="size">%s</span>
  <div class="price"><b>%s</b>%s%s</div>
  <div class="acts"><button class="btn ghost" type="button" data-add="%s">%s</button><button class="btn" type="button" data-buy="%s">%s</button></div></div></article>''' % (
        url(p), img(p['thumb']), html.escape(p['name']), '<span class="badge%s">%s</span>' % (' gold' if p['id'] == 'p3' else '', b) if b else '',
        url(p), t['names'][p['id']], t['sizes'][p['id']], rs(p['price']), '<s>%s</s>' % rs(p['mrp']) if off else '',
        '<span class="off">%d%s</span>' % (off, t['off']) if off else '', p['id'], t['add'], p['id'], t['buy'])


for code, t in L.items():
    c = BYID['combo']
    sep = BYID['p1']['price'] + BYID['lotion']['price']
    body = '''<div class="lpage" lang="%(lang)s" dir="%(dir)s" style="--lf:%(ff)s">
<div class="wrap hero">
  <div>
    <span class="eyebrow">%(eyebrow)s</span>
    <h1>%(h1)s</h1>
    <p class="lead">%(lead)s</p>
    <ul class="ticks">%(ticks)s</ul>
    <div class="cta"><a class="btn" href="#packs">%(cta)s</a><a class="btn ghost" href="https://wa.me/%(wa)s?text=%(watext)s" target="_blank" rel="noopener">%(ask)s</a></div>
    <p class="lang-en"><a href="/" lang="en" dir="ltr">%(english)s</a></p>
  </div>
  <div class="hero-media"><div class="frame"><img src="/assets/img/yf-combo.webp" alt="Youth Face Beauty Cream and Body Lotion" width="1200" height="1200" fetchpriority="high"></div></div>
</div>
<section id="packs"><div class="wrap">
  <div class="sec-h"><h2>%(packs_h)s</h2><p>%(packs_p)s</p></div>
  <div class="grid">%(cards)s</div>
  <div class="combo"><a class="ph" href="%(curl)s"><img src="%(cimg)s" alt="Youth Face Combo" width="600" height="600" loading="lazy"></a>
    <div class="combo-tx"><h2><a href="%(curl)s">%(cname)s</a></h2><p>%(combo_p)s</p>
    <div class="price"><b>%(cprice)s</b><s>%(cmrp)s</s><span class="off">%(coff)d%(off)s</span></div>
    <div class="acts"><button class="btn ghost" type="button" data-add="combo">%(add)s</button><button class="btn" type="button" data-buy="combo">%(buy)s</button></div></div></div>
</div></section>
<section><div class="wrap band">
  <div><h2>%(how_h)s</h2><p>%(patch)s</p></div>
  <ol>%(how)s</ol>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="note lnote"><b>%(cod_h)s</b><p>%(cod_p)s</p></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="sec-h"><h2>%(faq_h)s</h2></div>%(faq)s</div></section>
</div>''' % dict(t, ff=t['ff'], ticks=''.join('<li>%s</li>' % x for x in t['ticks']), wa=WA, watext=urllib.parse.quote(t['watext']),
                 cards=''.join(lcard(p, t) for p in MAIN), curl=url(c), cimg=img(c['thumb']), cname=t['combo_h'],
                 combo_p=t['combo_p'] % (rs(c['price']), rs(sep - c['price'])), cprice=rs(c['price']), cmrp=rs(c['mrp']), coff=pct(c),
                 how=''.join('<li>%s</li>' % x for x in t['how']), faq=faq_html(t['faq']))
    head = ALT + '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=%s&display=swap">\n' % t['font']
    page(t['path'], t['title'], t['desc'], body, og='website', ogimg=c['og'], extra_head=head, lang=t['lang'],
         schema=[faq_ld(t['faq'])])
