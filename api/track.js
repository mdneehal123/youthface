const { BRAND, REF_PREFIX, keys, cartFrom, shipArgs } = require('./_shared');
const delhivery = require('./_delhivery');
const shiprocket = require('./_shiprocket'); // legacy: orders shipped through Shiprocket before the switch
const kv = require('./_kv');

// Order tracking. Accepts mobile number + delivery pincode, a Payment ID (pay_...), an Order ID (order_...),
// a website order number (YC........) or a courier AWB. Returns status only: never a name, phone number or address.
// Paid orders are found in Razorpay; Cash on Delivery orders (no online payment) in the database, saved by api/cod-order.
async function kvJson(key) { if (!kv.cfg()) return null; try { return JSON.parse((await kv.cmd('GET', key)) || 'null'); } catch (e) { return null; } }

async function codTrack(ref, others) {
  const rec = await kvJson('codord:' + ref);
  if (!rec || !rec.result) return null;
  const cart = cartFrom(String(rec.items || ''));
  const items = cart ? cart.lines.map((l) => l.name + (l.qty > 1 ? ' × ' + l.qty : '')).join(', ') : '';
  let t = { found: false };
  if (rec.awb && delhivery.delhiveryOn()) { try { t = await delhivery.track(rec.awb); } catch (e) { t = { found: false }; } }
  const base = { found: true, cod: true, items, placed: rec.at ? new Date(rec.at).toISOString() : '', due: rec.total, others: others || 0, order: ref };
  return Object.assign(base, t.found ? t : { shipped: false, courier: rec.awb ? 'Delhivery' : '', awb: rec.awb || '' }, { found: true });
}
module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  const q = req.query || {};
  const id = String(q.id || '').trim();
  const phone = String(q.phone || '').replace(/\D/g, '').slice(-10);
  const pin = String(q.pin || '').trim();
  const byPhone = !id && (q.phone || q.pin);
  if (byPhone && (!/^[6-9]\d{9}$/.test(phone) || !/^[1-9]\d{5}$/.test(pin))) return res.status(400).json({ error: 'bad_phone' });
  if (!byPhone && (!id || id.length > 60)) return res.status(400).json({ error: 'missing_id' });
  const k = keys();
  const sOn = !!shiprocket.settings();
  if (!k && !kv.cfg() && !delhivery.delhiveryOn() && !sOn) return res.status(503).json({ error: 'not_configured' });
  const auth = k ? { Authorization: 'Basic ' + Buffer.from(k.id + ':' + k.secret).toString('base64') } : null;
  const needRzp = () => { if (!k) { const e = new Error('not_configured'); e.code = 503; throw e; } };
  try {
    let orderId = '', others = 0;
    if (byPhone) {
      const cod = await kvJson('codp:' + phone + ':' + pin);
      const since = Math.floor(Date.now() / 1000) - 90 * 86400;
      let hit = null;
      for (let skip = 0; k && skip < 1000; skip += 100) {
        const r = await fetch('https://api.razorpay.com/v1/orders?count=100&skip=' + skip + '&from=' + since, { headers: auth });
        const d = await r.json();
        if (!r.ok) { if (cod) break; return res.status(502).json({ error: 'lookup_failed' }); }
        const items = d.items || [];
        items.forEach((o) => {
          const n = o.notes || {};
          if (o.status !== 'paid' || n.brand !== BRAND) return;
          if (String(n.phone || '').replace(/\D/g, '').slice(-10) !== phone || String(n.pincode || '').trim() !== pin) return;
          if (!hit || o.created_at > hit.created_at) { if (hit) others++; hit = o; } else { others++; }
        });
        if (items.length < 100) break;
      }
      // the most recent order wins: a Cash on Delivery order or a paid one
      if (cod && cod.ref && (!hit || cod.at > hit.created_at * 1000)) {
        const out = await codTrack(cod.ref, others + (hit ? 1 : 0));
        if (out) return res.status(200).json(out);
      }
      if (!hit) return res.status(404).json({ error: 'not_found' });
      if (cod) others++;
      orderId = hit.id;
    } else if (new RegExp('^' + REF_PREFIX + '\\d{8}$', 'i').test(id)) {
      const out = await codTrack(id.toUpperCase());
      if (!out) return res.status(404).json({ error: 'not_found' });
      return res.status(200).json(out);
    } else if (/^pay_[A-Za-z0-9]{6,40}$/.test(id)) {
      needRzp();
      const r = await fetch('https://api.razorpay.com/v1/payments/' + id, { headers: auth });
      const p = await r.json();
      if (!r.ok || !p.order_id) return res.status(404).json({ error: 'not_found' });
      orderId = p.order_id;
    } else if (/^order_[A-Za-z0-9]{6,40}$/.test(id)) {
      needRzp();
      orderId = id;
    } else if (/^[A-Za-z0-9]{8,30}$/.test(id)) {
      let t = { found: false };
      if (delhivery.delhiveryOn()) t = await delhivery.track(id);
      if (!t.found && sOn) t = await shiprocket.track('awb', id);
      if (!t.found) return res.status(404).json({ error: 'not_found' });
      return res.status(200).json(t);
    } else {
      return res.status(400).json({ error: 'bad_id' });
    }
    const r = await fetch('https://api.razorpay.com/v1/orders/' + orderId, { headers: auth });
    const o = await r.json();
    if (!r.ok || (o.notes || {}).brand !== BRAND) return res.status(404).json({ error: 'not_found' });
    const n = o.notes || {};
    const cart = cartFrom(String(n.items || ''));
    const items = cart ? cart.lines.map((l) => l.name + (l.qty > 1 ? ' × ' + l.qty : '')).join(', ') : '';
    const sa = shipArgs(o);
    const due = sa && sa.cod ? sa.collect : 0;
    const placed = o.created_at ? new Date(o.created_at * 1000).toISOString() : '';
    if (o.status !== 'paid') return res.status(200).json({ found: true, paid: false, items, placed, due });
    // Paid orders are shipped from the Order Desk; tracking through Shiprocket only for orders from before the switch.
    let t = { found: false };
    if (sOn) { try { t = await shiprocket.track('order', orderId); } catch (e) { t = { found: false }; } }
    return res.status(200).json(Object.assign({ paid: true, items, placed, due, others }, t.found ? t : { found: true, shipped: false }));
  } catch (e) {
    if (e && e.code === 503) return res.status(503).json({ error: 'not_configured' });
    return res.status(502).json({ error: 'lookup_failed' });
  }
};
