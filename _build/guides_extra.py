# Extra guide articles aimed at what people search. Read by build.py with exec() right after GUIDES.
_c = BYID['combo']; _p1, _p2, _p3, _lo = BYID['p1'], BYID['p2'], BYID['p3'], BYID['lotion']
GUIDES += [
    dict(slug='youth-face-cream-price', old='price', title='Youth Face Cream price in India',
         blurb='Every pack, the price per jar, and how much a jar lasts.',
         seo='Youth Face Cream Price in India: Pack of 1, 2, 3 & Combo (2026)',
         desc='Youth Face Beauty Cream price in India: ₹549 for 25 g, ₹999 for 2 jars, ₹1,444 for 3, and the Cream + Body Lotion combo at ₹999. Free shipping, COD.',
         body='''<p>Youth Face Beauty Cream costs <b>%(p1)s for one 25 g jar</b> on youthfacebeautycream.com. Packs of two and three cost less per jar, and every order ships free across India with Cash on Delivery available.</p>
<h2>Price list</h2>
<div class="tbl"><table><thead><tr><th>Pack</th><th>What you get</th><th>MRP</th><th>Price</th><th>Per jar</th></tr></thead><tbody>
<tr><td><a href="%(u1)s">Pack of 1</a></td><td>1 × 25 g jar</td><td>%(m1)s</td><td>%(p1)s</td><td>%(p1)s</td></tr>
<tr><td><a href="%(u2)s">Pack of 2</a></td><td>2 × 25 g jars</td><td>%(m2)s</td><td>%(p2)s</td><td>%(e2)s</td></tr>
<tr><td><a href="%(u3)s">Pack of 3</a></td><td>3 × 25 g jars</td><td>%(m3)s</td><td>%(p3)s</td><td>%(e3)s</td></tr>
<tr><td><a href="%(uc)s">Combo</a></td><td>25 g cream + 40 ml Body Lotion</td><td>%(mc)s</td><td>%(pc)s</td><td>n/a</td></tr>
</tbody></table></div>
<p>Prices include all taxes. Shipping is free on every order, with no extra Cash on Delivery fee.</p>
<h2>How long does one jar last?</h2><p>With a pea-sized amount on the face and neck once or twice a day, a 25 g jar usually lasts around a month, depending on how much you apply. Because results take several weeks of regular use, many people choose the Pack of 2 or Pack of 3 so the routine doesn't stop halfway.</p>
<h2>Which pack should I buy?</h2><ul><li><b>Trying it for the first time:</b> Pack of 1. Patch test it and see how your skin feels.</li><li><b>Planning a two-month routine:</b> Pack of 2, at %(e2)s a jar.</li><li><b>Best value:</b> Pack of 3, at %(e3)s a jar.</li><li><b>Face and body together:</b> the <a href="%(uc)s">Combo</a>, which adds the 40 ml Body Lotion for %(save)s less than buying both separately.</li></ul>
<h2>How to pay</h2><p>Pay online by UPI, card or netbanking through Razorpay, or choose Cash on Delivery: nothing to pay in advance, you pay the full amount in cash when the parcel arrives. You can also order on WhatsApp.</p>
<h2>Where to buy</h2><p>This store is run by Beauty Mart in Bhatkal, Karnataka, and every order is packed in sealed packaging and shipped from Bhatkal. Prices on other websites or shops may differ. Before buying elsewhere, check that the seller shows a real business name, address and return policy.</p>
<p><a class="btn" href="/shop/">See all packs</a></p>''' % dict(p1=rs(_p1['price']), p2=rs(_p2['price']), p3=rs(_p3['price']), pc=rs(_c['price']),
            m1=rs(_p1['mrp']), m2=rs(_p2['mrp']), m3=rs(_p3['mrp']), mc=rs(_c['mrp']),
            e2=rs(round(_p2['price'] / 2)), e3=rs(round(_p3['price'] / 3)), save=rs(_p1['price'] + _lo['price'] - _c['price']),
            u1=url(_p1), u2=url(_p2), u3=url(_p3), uc=url(_c))),
    dict(slug='youth-face-cream-side-effects', old='side-effects', title='Youth Face Cream: side effects and safe use',
         blurb='What is normal, what is not, and who should check with a doctor first.',
         seo='Youth Face Cream Side Effects and Safe Use',
         desc='Youth Face Beauty Cream side effects: mild tingling vs a real reaction, how to patch test, and who should ask a doctor first.',
         body='''<p>Most people use Youth Face Beauty Cream without problems, but any cream with active ingredients like Kojic Acid and Alpha Arbutin can irritate some skin. Here is how to use it safely and what to watch for.</p>
<h2>What can happen</h2><ul><li><b>Mild tingling or warmth</b> for a minute after applying, in the first few days. This is common with active creams and usually settles.</li><li><b>Dryness or light peeling</b>, especially if you also use scrubs, retinol or other strong products.</li><li><b>Redness, itching or burning that lasts</b>: this is a reaction. Stop using the cream.</li><li><b>Rash, swelling or bumps</b>: stop at once, wash it off, and see a doctor if it doesn't settle.</li></ul>
<h2>How to patch test (do this first)</h2><ol><li>Apply a small amount behind the ear or on the inner arm.</li><li>Leave it for 24 hours without washing the spot.</li><li>No redness, itching or swelling? Start on the face, once a day for the first week.</li></ol>
<h2>Using it safely every day</h2><ul><li>A pea-sized amount is enough for the face and neck. More cream does not work faster.</li><li>Avoid the eyes, lips, broken skin, sunburn and freshly waxed or threaded skin.</li><li>Don't layer several strong active products (retinol, acids, other brightening creams) at the same time.</li><li><b>Use sunscreen every morning.</b> Dark-spot creams work against sun damage you keep adding.</li></ul>
<h2>Who should ask a doctor first</h2><ul><li>Anyone pregnant or breastfeeding.</li><li>People with eczema, rosacea, very sensitive skin or an active skin infection.</li><li>Anyone using prescription skin treatments.</li><li>Teenagers with acne: a dermatologist can suggest the right routine.</li></ul>
<h2>Check the label</h2><p>The full ingredient list is printed on every Youth Face pack. Read it before use, especially if you know you react to particular ingredients. Avoid any cream, from any brand, that has no ingredient list or promises dramatic results in a few days.</p>
<p>See also: <a href="/skincare-guides/kojic-acid/">Understanding Kojic Acid</a> · <a href="/how-to-use/">How to use Youth Face</a></p>'''),
    dict(slug='kojic-acid-vs-alpha-arbutin', old='kojic-vs-arbutin', title='Kojic Acid vs Alpha Arbutin',
         blurb='How the two ingredients differ, and why they are often used together.',
         seo='Kojic Acid vs Alpha Arbutin: Differences & Using Both',
         desc='Kojic Acid vs Alpha Arbutin: what each does for dark spots, which is gentler, and why many creams combine both. With a comparison table.',
         body='''<p>Kojic Acid and Alpha Arbutin are two of the most common ingredients in creams for dark spots and uneven-looking tone. They are not rivals: many formulas use both, because they suit different skin and work well together.</p>
<h2>Side by side</h2>
<div class="tbl"><table><thead><tr><th></th><th>Kojic Acid</th><th>Alpha Arbutin</th></tr></thead><tbody>
<tr><td>Where it comes from</td><td>Fermentation (first found in rice fermentation for sake)</td><td>A stable form of arbutin, found in plants like bearberry</td></tr>
<tr><td>Used for</td><td>Dark spots, uneven-looking tone</td><td>Dark spots, a brighter-looking complexion</td></tr>
<tr><td>Feel on skin</td><td>Can tingle for some people at first</td><td>Generally gentle</td></tr>
<tr><td>Results</td><td>Gradual, over weeks</td><td>Gradual, over weeks</td></tr>
<tr><td>Needs sunscreen</td><td>Yes</td><td>Yes</td></tr>
</tbody></table></div>
<h2>Which one should you choose?</h2><p>If your skin is sensitive, a gentle Alpha Arbutin product is an easy start. If your skin tolerates actives well, Kojic Acid adds a well-known ingredient to the routine. A cream that combines the two, at levels made for daily use, gives you both without layering several products.</p>
<h2>Using them together</h2><ol><li>Choose one product that contains both, rather than stacking separate serums.</li><li>Apply to clean, dry skin once a day for the first week, then twice if comfortable.</li><li>Use sunscreen every morning.</li><li>Judge the results after 6 to 8 weeks of regular use, in the same light.</li></ol>
<p><a href="/product/youth-face-beauty-cream-25g-pack-of-1-kojic-acid-alpha-arbutin/">Youth Face Beauty Cream</a> is built around exactly this pair. Read more in <a href="/skincare-guides/kojic-acid/">Understanding Kojic Acid</a> and <a href="/skincare-guides/alpha-arbutin/">Understanding Alpha Arbutin</a>.</p>'''),
    dict(slug='how-to-remove-dark-spots-on-face', old='dark-spots', title='How to remove dark spots on the face',
         blurb='What causes dark spots, what actually fades them, and how long it takes.',
         seo='How to Remove Dark Spots on Face: Causes, Routine & Timeline',
         desc='How to remove dark spots on the face: common causes, a simple daily routine with sunscreen, home remedies to avoid, and when to see a doctor.',
         body='''<p>Dark spots fade with a steady routine: daily sunscreen, a cream with proven ingredients, and patience of 6 to 12 weeks. There is no overnight fix, and harsh shortcuts usually make spots darker.</p>
<h2>What causes dark spots</h2><ul><li><b>Marks after pimples</b> (post-inflammatory hyperpigmentation): the most common cause on Indian skin.</li><li><b>Sun spots</b>: from years of sun exposure, often on cheeks and forehead.</li><li><b>Melasma</b>: patchy brown areas, often on both cheeks, linked to hormones and sun. This needs a dermatologist.</li><li><b>Irritation</b>: from scrubbing, threading, waxing or harsh products.</li></ul>
<h2>A routine that works</h2><ol><li><b>Morning:</b> gentle cleanser, a pea-sized amount of a dark-spot cream, then broad-spectrum sunscreen SPF 30 or higher.</li><li><b>Night:</b> cleanse off sunscreen and dust, then apply your cream again.</li><li><b>Every day:</b> don't squeeze pimples, and reapply sunscreen if you are outdoors for long.</li></ol>
<p>Look for creams with ingredients such as Kojic Acid, Alpha Arbutin, niacinamide or vitamin C, and stick with one product rather than switching every week.</p>
<h2>Home remedies to avoid</h2><ul><li><b>Lemon juice:</b> acidic and can make skin sensitive to the sun.</li><li><b>Baking soda or toothpaste:</b> irritate skin and can darken marks.</li><li><b>Hard scrubs:</b> cause tiny injuries that leave new marks.</li></ul>
<h2>How long it takes</h2><p>Fresh marks often fade in 6 to 8 weeks with daily care. Older spots can take 3 months or more, and some may only lighten partly. Take a photo on day one in the same light and compare every few weeks.</p>
<h2>When to see a dermatologist</h2><p>See a doctor for patchy brown areas on both cheeks, spots that change shape or colour, or no improvement after 3 months of daily care. Prescription treatments and procedures work better for melasma and deep pigmentation.</p>
<p>Related: <a href="/skincare-guides/kojic-acid-vs-alpha-arbutin/">Kojic Acid vs Alpha Arbutin</a> · <a href="/skincare-guides/daytime-skincare-routine/">Daytime skincare routine</a> · <a href="/shop/">Shop Youth Face</a></p>'''),
]
