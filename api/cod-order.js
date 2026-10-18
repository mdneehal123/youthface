// POST /api/cod-order — Cash on Delivery with nothing paid upfront.
// The price is worked out here on the server from the fixed price table (combo rule included), Delhivery is checked
// for the pincode, the shipment is booked with Delhivery, and the order is ALWAYS saved in the Order Desk
// (with the Delhivery tracking number when booked, or flagged for manual booking when not).
const { cartFrom, customer, orderRef } = require('./_shared');
const guard = require('./_guard');
const kv = require('./_kv');
const { delhiveryOn, serviceable, createShipment } = require('./_delhivery');
const { pushToDesk, deskOn } = require('./_orderdesk');

const KEEP = 120 * 86400; // how long the order record is kept for tracking and retries (seconds)
const HOLD = 180; // an order still being placed blocks a second copy for this long (seconds), in case the first one crashed

// Retry memory. With the Redis database connected it is shared by every server instance; without it, each
// instance remembers its own recent orders (and the Order Desk still keeps one entry per order number).
const local = new Map(); // ref -> { pending, phone, result, until }
const store = {
  async claim(ref, phone) {
    if (kv.cfg()) {
      try { return Boolean(await kv.cmd('SET', 'codord:' + ref, JSON.stringify({ pending: true, phone }), 'NX', 'EX', HOLD)); } catch (e) { /* fall back to memory */ }
    }
    const now = Date.now();
    const e = local.get(ref);
    if (e && e.until > now) return false;
    local.set(ref, { pending: true, phone, until: now + HOLD * 1000 });
    if (local.size > 2000) { for (const [k, v] of local) { if (v.until < now) local.delete(k); } }
    return true;
  },
  async get(ref) {
    if (kv.cfg()) { try { const v = JSON.parse((await kv.cmd('GET', 'codord:' + ref)) || 'null'); if (v) return v; } catch (e) { /* memory */ } }
    const e = local.get(ref);
    return e && e.until > Date.now() ? e : null;
  },
  async release(ref) {
    local.delete(ref);
    if (kv.cfg()) { try { await kv.cmd('DEL', 'codord:' + ref); } catch (e) { /* ignore */ } }
  },
  async done(ref, rec, phone, pin) {
    local.set(ref, Object.assign({}, rec, { until: Date.now() + KEEP * 1000 }));
    if (kv.cfg()) {
      // Kept for the tracking page (order number, or mobile number + pincode) and for retries of the same checkout.
      try { await kv.pipe([['SET', 'codord:' + ref, JSON.stringify(rec), 'EX', KEEP], ['SET', 'codp:' + phone + ':' + pin, JSON.stringify({ ref, at: rec.at }), 'EX', KEEP]]); } catch (e) { /* tracking falls back to the AWB */ }
    }
  }
};

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });
  let body = req.body || {};
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  if (body.website) return res.status(200).json({ ok: true }); // form trap for bots
  const cart = cartFrom(body.items);
  const c = customer(body);
  if (!cart || !c) return res.status(400).json({ error: 'invalid_details' });
  // Without Delhivery and without the Order Desk the order could not be saved anywhere: the page offers WhatsApp instead.
  if (!delhiveryOn() && !deskOn()) return res.status(503).json({ error: 'not_configured' });

  const ref = orderRef(body.ref);
  // The same checkout sent twice (double tap, slow network) gets the first answer back instead of a second parcel.
  // Checked before the rate limit, so a retry is never refused as "too many tries".
  if (!(await store.claim(ref, c.phone))) {
    const prev = await store.get(ref);
    if (prev && prev.result && prev.phone === c.phone) return res.status(200).json(prev.result);
    return res.status(409).json({ error: 'in_progress' });
  }
  // Public endpoint that books real shipments: limited per mobile number and for the whole shop.
  if (!(await guard.limit('cod:' + c.phone, 6, 3600)) || !(await guard.limit('cod', 300, 3600))) {
    await store.release(ref);
    return res.status(429).json({ error: 'busy' });
  }

  const total = cart.total;
  let d = { ok: false, error: 'Delhivery is not set up on the website (DELHIVERY_TOKEN / DELHIVERY_PICKUP missing)' };
  if (delhiveryOn()) {
    try {
      const s = await serviceable(c.pin);
      if (!s.cod) {
        await store.release(ref);
        return res.status(409).json({ error: 'cod_unavailable', codUnavailable: true, message: 'Cash on Delivery is not available for pincode ' + c.pin + '. Please pay online instead.' });
      }
    } catch (e) { /* if the check itself fails, still try to book */ }
    try { d = await createShipment({ ref, c, cart, total, pay: 'cod' }); } catch (e) { d = { ok: false, error: String((e && e.message) || e) }; }
  }

  const order = { ref, c, lines: cart.lines, sub: cart.total, disc: 0, coupon: '', total, pay: 'cod', paid: false };
  const desk = await pushToDesk(d.ok
    ? Object.assign(order, { courier: 'Delhivery', awb: d.awb, note: 'COD booked with Delhivery · AWB ' + d.awb + ' · print the label from the Delhivery panel' })
    : Object.assign(order, { note: '⚠ COD website order — Delhivery booking failed: ' + d.error + '. Please book it in Delhivery.' }));
  if (!desk.ok) console.error('order desk push failed', ref, desk.error);

  if (!d.ok && !desk.ok) {
    // Not booked and not saved: never tell the customer it worked. Log it so it can be recovered, and let the page offer WhatsApp.
    console.error('COD order NOT saved', JSON.stringify({ ref, name: c.name, phone: c.phone, pin: c.pin, items: cart.code, total, delhivery: d.error, desk: desk.error }));
    await store.release(ref);
    return res.status(502).json({ error: 'not_saved' });
  }

  const result = { ok: true, ref, total, awb: d.ok ? d.awb : '', courier: d.ok ? 'Delhivery' : '', pending: !d.ok, savedToDesk: desk.ok,
    trackUrl: d.ok ? 'https://www.delhivery.com/track/package/' + d.awb : '' };
  await store.done(ref, { result, phone: c.phone, pin: c.pin, awb: result.awb, items: cart.code, total, at: Date.now() }, c.phone, c.pin);
  return res.status(200).json(result);
};
