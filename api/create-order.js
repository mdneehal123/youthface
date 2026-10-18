const { BRAND, keys, cartFrom, customer, orderRef } = require('./_shared');
const guard = require('./_guard');

// Creates a Razorpay order for the FULL amount of the cart. The amount is worked out here from the fixed price table.
// (Cash on Delivery has nothing to pay online: it goes to api/cod-order instead.)
module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });
  const k = keys();
  if (!k) return res.status(503).json({ error: 'not_configured' });
  let body = req.body || {};
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const cart = cartFrom(body.items);
  const c = customer(body);
  if (!cart || !c) return res.status(400).json({ error: 'invalid_details' });
  if (!(await guard.limit('order:' + c.phone, 15, 3600)) || !(await guard.limit('order', 1000, 3600))) return res.status(429).json({ error: 'busy' });
  const ref = orderRef(body.ref);
  try {
    const r = await fetch('https://api.razorpay.com/v1/orders', {
      method: 'POST',
      headers: { Authorization: 'Basic ' + Buffer.from(k.id + ':' + k.secret).toString('base64'), 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: cart.total * 100, currency: 'INR', receipt: ref,
        notes: {
          brand: BRAND, ref, product: BRAND + ': ' + cart.label.slice(0, 200), items: cart.code, total: String(cart.total),
          name: c.name, phone: c.phone, address: c.address, city: c.city, pincode: c.pin, mode: 'full',
          remind: body.remind === true ? 'yes' : 'no',
          payment: 'Paid in full online'
        }
      })
    });
    const data = await r.json();
    if (!r.ok || !data.id) return res.status(502).json({ error: 'gateway_error' });
    return res.status(200).json({ order_id: data.id, amount: data.amount, currency: data.currency, key_id: k.id, total: cart.total, ref });
  } catch (e) {
    return res.status(502).json({ error: 'gateway_unreachable' });
  }
};
