# More guide articles (25 Oct 2026), aimed at questions people search. Read by build.py with exec() after guides_extra.py.
_p1c = BYID['p1']
_P1 = '<a href="%s">Youth Face Beauty Cream</a>' % url(_p1c)
GUIDES += [
    dict(slug='how-long-does-dark-spot-cream-take-to-work', old='how-long', title='How long does a dark spot cream take to work?',
         blurb='A realistic week-by-week timeline, and how to track your skin so you can judge fairly.',
         seo='How Long Does a Dark Spot Cream Take to Work? A Realistic Timeline',
         desc='How long a dark spot cream takes to work: a realistic week-by-week timeline, why sunscreen matters, how to track progress with photos and when to see a doctor.',
         body='''<p>Dark spot creams work slowly. Most people need <b>6 to 12 weeks of daily use</b> before they can judge a product fairly, and older spots can take longer. Anyone promising results in three days is not being honest.</p>
<h2>Why it takes so long</h2><p>Your skin renews itself roughly every four to six weeks, and slower as you get older. A cream works on the colour in the new skin cells as they rise to the surface. So the earliest you can expect a visible change is after at least one full renewal cycle, and spots that sit deeper take several cycles.</p>
<h2>A realistic timeline</h2>
<div class="tbl"><table><thead><tr><th>When</th><th>What you may notice</th></tr></thead><tbody>
<tr><td>Week 1</td><td>Your skin gets used to the cream. A little tingling or dryness is possible. No change in spots yet.</td></tr>
<tr><td>Weeks 2 to 4</td><td>Skin may feel smoother. Spots usually look the same. This is where most people give up too early.</td></tr>
<tr><td>Weeks 4 to 8</td><td>Newer marks (for example from pimples) may start to look lighter. Compare photos, not memory.</td></tr>
<tr><td>Weeks 8 to 12</td><td>A clearer picture. Fresh marks are often much less visible. Older spots may be lighter but not gone.</td></tr>
<tr><td>After 12 weeks</td><td>If there is no change at all with daily use and sunscreen, speak to a dermatologist.</td></tr>
</tbody></table></div>
<p>This is a general guide, not a promise. Results vary from person to person.</p>
<h2>What speeds things up, and what ruins it</h2><ul><li><b>Sunscreen every morning.</b> Sun darkens spots faster than any cream can lighten them. See <a href="/skincare-guides/sunscreen-with-dark-spot-cream/">how to use sunscreen with a dark spot cream</a>.</li><li><b>Daily use.</b> Using it two days a week and stopping gives skin no time to respond.</li><li><b>Not picking at pimples.</b> Each picked pimple can leave a new mark.</li><li><b>One product at a time.</b> Changing creams every two weeks resets the clock and makes it impossible to tell what helps.</li></ul>
<h2>Track it properly</h2><ol><li>Take a photo on day one, in daylight near a window, with no filter.</li><li>Take another every two weeks from the same spot, same light, same distance.</li><li>Compare only the photos. Your mirror in different lighting will fool you.</li></ol>
<h2>Where %(p)s fits</h2><p>%(p)s is built around Kojic Acid and Alpha Arbutin, two ingredients widely used in dark spot care. Use a pea-sized amount on the face and neck, once or twice a day, and follow with sunscreen in the morning. Patch test first. See <a href="/skincare-guides/kojic-acid-vs-alpha-arbutin/">Kojic Acid vs Alpha Arbutin</a> for how the two work together.</p>
<h2>When to see a doctor</h2><p>Patchy brown areas on both cheeks (possible melasma), spots that change shape or colour, or no change after three months all need a dermatologist. A cream is a cosmetic, not a treatment for a skin condition.</p>''' % dict(p=_P1)),

    dict(slug='sunscreen-with-dark-spot-cream', old='sunscreen', title='How to use sunscreen with a dark spot cream',
         blurb='The order to apply them, how much to use and when to reapply, so the sun does not undo your routine.',
         seo='Sunscreen With a Dark Spot Cream: Order, Amount & Reapplying',
         desc='How to use sunscreen with a dark spot cream: the order to apply, how much to use, when to reapply and common mistakes that let sun darken spots again.',
         body='''<p>If you use a dark spot cream and skip sunscreen, you are working against yourself. Sunlight tells your skin to make more pigment, so unprotected skin keeps darkening the very spots you are trying to fade. Sunscreen is not an extra step. It is the step that makes the others count.</p>
<h2>The order, morning and night</h2>
<div class="tbl"><table><thead><tr><th>Time</th><th>Step 1</th><th>Step 2</th><th>Step 3</th></tr></thead><tbody>
<tr><td>Morning</td><td>Gentle cleanser, pat dry</td><td>Dark spot cream (pea-sized)</td><td>Sunscreen, last</td></tr>
<tr><td>Night</td><td>Cleanse off sunscreen and dust</td><td>Dark spot cream</td><td>Plain moisturiser if skin feels dry</td></tr>
</tbody></table></div>
<p>Rule of thumb: thinnest to thickest. Sunscreen always goes last in the morning, because it has to sit on top as a protective layer.</p>
<h2>How much sunscreen is enough?</h2><p>Most people use far too little. For the face and neck, a line of sunscreen along two fingers is a good guide. A thin smear gives you much less protection than the number on the bottle.</p>
<h2>Which sunscreen?</h2><ul><li>Broad-spectrum, SPF 30 or higher.</li><li>A texture you enjoy wearing, because you will only use it daily if you like it.</li><li>Gel or lightweight lotion types suit oily and humid weather. Creamier types suit dry skin.</li></ul>
<h2>Reapplying</h2><p>If you are outdoors for long, reapply about every two to three hours, and after heavy sweating or wiping your face. Indoors away from windows, once in the morning is usually fine.</p>
<h2>Common mistakes</h2><ul><li><b>Skipping it on cloudy days.</b> UV still reaches you.</li><li><b>Skipping it indoors near windows or in vehicles.</b> UVA passes through glass.</li><li><b>Applying sunscreen first, then the cream.</b> The cream then cannot reach your skin properly.</li><li><b>Forgetting the neck, ears and hands.</b> These show uneven colour first.</li></ul>
<h2>With Kojic Acid and Alpha Arbutin creams</h2><p>Kojic Acid is used in many dark spot creams, and creams with active ingredients can leave skin a little more sensitive to the sun. That is one more reason to apply sunscreen daily when you use %(p)s. Patch test first, and stop if redness or burning continues.</p>
<p>Related: <a href="/skincare-guides/daytime-skincare-routine/">Daytime skincare routine</a> · <a href="/skincare-guides/how-to-remove-dark-spots-on-face/">How to remove dark spots</a></p>''' % dict(p=_P1)),

    dict(slug='pimple-marks-vs-dark-spots', old='pimple-marks', title='Pimple marks vs dark spots: what is the difference?',
         blurb='Why pimples leave marks on Indian skin, how they differ from sun spots, and how to treat each calmly.',
         seo='Pimple Marks vs Dark Spots: Causes, Differences & What Helps',
         desc='Pimple marks vs dark spots: why acne leaves dark marks on Indian skin, how they differ from sun spots and melasma, and a calm routine that helps them fade.',
         body='''<p>Not every dark mark on the face is the same. Knowing which kind you have helps you choose a sensible routine, and helps you know when to see a doctor. The three you will meet most often are pimple marks, sun spots and melasma.</p>
<h2>Why pimples leave marks</h2><p>When a pimple inflames, the skin responds by making extra pigment where the damage was. This is called post-inflammatory hyperpigmentation. It is common on medium to deep skin tones, including most Indian skin, and it can stay for weeks or months after the pimple itself has healed.</p>
<h2>How to tell them apart</h2>
<div class="tbl"><table><thead><tr><th></th><th>Pimple marks</th><th>Sun spots</th><th>Melasma</th></tr></thead><tbody>
<tr><td>Where</td><td>Where pimples were</td><td>Cheeks, forehead, nose, backs of hands</td><td>Both cheeks, upper lip, forehead</td></tr>
<tr><td>Shape</td><td>Small round marks</td><td>Small, clearly edged spots</td><td>Larger, patchy areas</td></tr>
<tr><td>Cause</td><td>Inflamed or picked pimples</td><td>Years of sun</td><td>Hormones plus sun</td></tr>
<tr><td>Self-care?</td><td>Usually yes</td><td>Usually yes</td><td>See a dermatologist</td></tr>
</tbody></table></div>
<h2>What helps pimple marks fade</h2><ol><li><b>Stop picking.</b> It is the single biggest cause of new marks.</li><li><b>Sunscreen every morning.</b> Sun makes marks darker and keeps them longer.</li><li><b>A gentle routine.</b> Mild cleanser, no hard scrubs, no lemon or toothpaste.</li><li><b>A cream made for dark spots,</b> used daily for many weeks, such as %(p)s with Kojic Acid and Alpha Arbutin. Patch test first.</li><li><b>Patience.</b> Marks often fade over 6 to 12 weeks, and some take longer.</li></ol>
<h2>If you still get pimples</h2><p>Treating active acne is a separate job from fading the marks. Frequent, painful or cystic acne needs a dermatologist, because letting it scar makes marks harder to fix. Do not mix several strong products at once, which can irritate skin and cause more marks.</p>
<h2>Do not do this</h2><ul><li>Scrubbing marks harder to make them go away.</li><li>Using lemon juice, baking soda or toothpaste.</li><li>Switching products every week.</li></ul>
<p>More: <a href="/skincare-guides/how-long-does-dark-spot-cream-take-to-work/">how long a dark spot cream takes to work</a> · <a href="/skincare-guides/how-to-remove-dark-spots-on-face/">how to remove dark spots</a></p>''' % dict(p=_P1)),

    dict(slug='dark-spots-on-cheeks-and-around-mouth', old='cheeks-mouth', title='Dark spots on cheeks and around the mouth',
         blurb='What commonly causes patches on the cheeks and above the lip, and a gentle routine to try.',
         seo='Dark Spots on Cheeks & Around the Mouth: Causes and a Gentle Routine',
         desc='Dark spots on the cheeks and around the mouth: common causes, which kinds need a dermatologist, and a gentle daily routine with sunscreen to keep them from getting darker.',
         body='''<p>Darkening on the cheeks, above the upper lip and around the mouth is very common. It has several possible causes, and some of them need a doctor rather than a cream. Here is a calm way to think about it.</p>
<h2>Common causes</h2><ul><li><b>Sun exposure.</b> Cheeks and the upper lip get the most sun on the face, and the colour builds up over years.</li><li><b>Melasma.</b> Patchy brown areas, often on both cheeks and above the lip, linked to hormones, pregnancy, some medicines and sun.</li><li><b>Old pimple marks</b> on the lower cheeks and jawline.</li><li><b>Friction or irritation,</b> for example from rough towels, harsh scrubs, or hair removal creams and threading on the upper lip.</li><li><b>Dryness and irritation</b> around the mouth that leaves the skin darker afterwards.</li></ul>
<h2>When this needs a dermatologist</h2><p>See a doctor if the dark area is patchy and symmetrical on both cheeks or the upper lip (possible melasma), if it appeared during pregnancy or after starting new medicine, if it is raised, itchy or changing, or if it does not improve after about three months of daily care. A cosmetic cream does not treat a skin condition.</p>
<h2>A gentle daily routine</h2><ol><li><b>Cleanse</b> with lukewarm water and a mild cleanser. Avoid hot water and scrubs.</li><li><b>Apply a pea-sized amount of a dark spot cream</b> to the face, avoiding the lips and eyes. %(p)s is made with Kojic Acid and Alpha Arbutin. Patch test first.</li><li><b>Sunscreen every morning,</b> SPF 30 or higher, and reapply if you are outside for hours. Pay attention to the upper lip area, which most people skip.</li><li><b>Night:</b> cleanse, repeat the cream, and moisturise if skin feels dry.</li></ol>
<h2>Habits that make patches worse</h2><ul><li>Skipping sunscreen on cloudy days.</li><li>Waxing, threading or hair removal creams on the upper lip, with no care afterwards.</li><li>Scrubbing or picking.</li><li>Trying several new products in the same week.</li></ul>
<h2>Be patient, and measure</h2><p>This area is slow to change. Take a photo in daylight now and every two weeks. If you are not sure it is only sun or pimple marks, a dermatologist can tell you quickly.</p>
<p>See also: <a href="/skincare-guides/sunscreen-with-dark-spot-cream/">sunscreen with a dark spot cream</a> · <a href="/skincare-guides/pimple-marks-vs-dark-spots/">pimple marks vs dark spots</a></p>''' % dict(p=_P1)),

    dict(slug='morning-vs-night-dark-spot-cream', old='morning-night', title='Morning or night: when to use a dark spot cream',
         blurb='Should you apply it once or twice a day, in the morning, at night, or both?',
         seo='Dark Spot Cream: Morning or Night? How Often to Apply',
         desc='Should you use a dark spot cream in the morning, at night or both? How often to apply it, how to start slowly, the right order with sunscreen and what to avoid.',
         body='''<p>Many people ask whether a dark spot cream should be used in the morning or at night. For most creams, the answer is: <b>both can work, if your skin is comfortable, and sunscreen is non-negotiable in the morning.</b></p>
<h2>The short answer</h2>
<div class="tbl"><table><thead><tr><th>Your skin</th><th>A sensible start</th></tr></thead><tbody>
<tr><td>Sensitive or new to active creams</td><td>Night only, for the first week. Add the morning once skin is comfortable.</td></tr>
<tr><td>Normal, used to active products</td><td>Morning and night from the start, with sunscreen in the morning.</td></tr>
<tr><td>Dry or easily tight</td><td>Night, with a plain moisturiser after the cream.</td></tr>
</tbody></table></div>
<h2>Why many people like night</h2><p>At night you are not exposed to sun, skin sits undisturbed for hours, and you can follow with a moisturiser without worrying about sunscreen or make-up. It is the gentlest way to start.</p>
<h2>Why the morning also works</h2><p>Using the cream in the morning, under sunscreen, gives more regular contact. The key is sunscreen on top, every day. A dark spot cream without sunscreen is a waste, because the sun re-darkens the spots.</p>
<h2>How to start slowly</h2><ol><li><b>Day 1:</b> patch test behind the ear or on the inner arm for 24 hours.</li><li><b>Week 1:</b> a pea-sized amount at night only.</li><li><b>Week 2:</b> add the morning if there is no redness, stinging or dryness.</li><li><b>Always:</b> sunscreen last in the morning.</li></ol>
<h2>How much and how often</h2><p>A pea-sized amount is enough for the face and neck. More cream does not work faster and can irritate. For %(p)s, once or twice a day is the usual directions. Keep it away from the eyes and lips.</p>
<h2>What not to mix it with</h2><ul><li>Several strong products at once, such as scrubs, peels and retinol on the same evening.</li><li>Waxing, threading or a facial on the same day.</li></ul>
<h2>If skin feels irritated</h2><p>Cut back to every other night, add a plain moisturiser, and avoid new products. If redness, burning or itching continues, stop and see a dermatologist.</p>
<p>Related: <a href="/skincare-guides/evening-skincare-routine/">Evening routine</a> · <a href="/skincare-guides/daytime-skincare-routine/">Daytime routine</a></p>''' % dict(p=_P1)),

    dict(slug='order-youth-face-cream-cash-on-delivery', old='order-cod', title='How to order Youth Face Cream: COD, online payment and tracking',
         blurb='Step by step: choosing a pack, paying online or on delivery, delivery times and tracking your parcel.',
         seo='How to Order Youth Face Cream: Cash on Delivery, Online Payment & Tracking',
         desc='How to order Youth Face Beauty Cream online in India: choose a pack, pay by UPI or Cash on Delivery with no extra fee, delivery times, tracking and returns.',
         body='''<p>Ordering from youthfacebeautycream.com takes about a minute. You can pay online or choose Cash on Delivery, and shipping is free on every order.</p>
<h2>Step by step</h2><ol><li><b>Choose your pack</b> on the <a href="/shop/">shop page</a>: Pack of 1, 2 or 3, or the Cream + Body Lotion combo. See the <a href="/skincare-guides/youth-face-cream-price/">price list</a>.</li><li><b>Add to cart</b> and go to checkout.</li><li><b>Enter your name, mobile number, address and pincode.</b> The pincode shows your city and an estimated delivery date.</li><li><b>Choose how to pay:</b> online by UPI, card or netbanking, or Cash on Delivery.</li><li><b>Confirm.</b> You see your order details on screen. Cash on Delivery orders also get a Delhivery tracking number straight away.</li></ol>
<h2>Cash on Delivery</h2><ul><li>Nothing to pay in advance.</li><li>You pay the full amount in cash to the courier when the parcel arrives.</li><li>No extra Cash on Delivery fee.</li><li>Available on most pincodes. If your pincode is not eligible, the checkout tells you, and you can pay online instead.</li></ul>
<p>Please keep your phone on and the exact amount ready, so the delivery goes smoothly. Please order Cash on Delivery only when you are sure you want the product, so the parcel is accepted at the door.</p>
<h2>Pay online</h2><p>Pay by UPI, card or netbanking through Razorpay, on a secure payment page. You get a payment ID, which you can also use on the Track Order page.</p>
<h2>How long does delivery take?</h2><p>Orders are packed and handed to the courier in 1 to 3 business days. After dispatch, delivery usually takes 3 to 7 business days, depending on your pincode. These are estimates, and weather, festivals or courier delays can add time.</p>
<h2>Track your order</h2><p>Open <a href="/track-order/">Track Order</a> and use your mobile number with your pincode, or your order number, payment ID or tracking number.</p>
<h2>Returns</h2><p>If an item arrives damaged, leaking or wrong, we replace it or refund you in full. Sealed, unused items can be returned within 7 days of delivery. Opened or used cosmetics cannot be returned. Read the full <a href="/refund-returns-policy/">returns policy</a>.</p>
<h2>Prefer WhatsApp?</h2><p>You can also message us on WhatsApp at +91 99808 81230 and we will help you place the order. Every order is packed in sealed packaging by our team in Bhatkal, Karnataka.</p>
<p>Not sure which pack? Read <a href="/skincare-guides/how-to-use-youth-face/">how to use Youth Face</a> and our <a href="/skincare-guides/youth-face-cream-side-effects/">safe use guide</a> first.</p>'''),
]
