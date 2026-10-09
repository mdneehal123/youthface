const { BRAND, keys, cartFrom } = require('./_shared');
const shiprocket = require('./_shiprocket');

// Order tracking. Accepts mobile number + delivery pincode, a Payment ID (pay_...), an Order ID (order_...)
// or a courier AWB. Returns status only: never a name, phone number or address.
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
  if (!k || !shiprocket.settings()) return res.status(503).json({ error: 'not_configured' });
  const auth = { Authorization: 'Basic ' + Buffer.from(k.id + ':' + k.secret).toString('base64') };
  try {
    let orderId = '', others = 0;
    if (byPhone) {
      const since = Math.floor(Date.now() / 1000) - 90 * 86400;
      let hit = null;
      for (let skip = 0; skip < 1000; skip += 100) {
        const r = await fetch('https://api.razorpay.com/v1/orders?count=100&skip=' + skip + '&from=' + since, { headers: auth });
        const d = await r.json();
        if (!r.ok) return res.status(502).json({ error: 'lookup_failed' });
        const items = d.items || [];
        items.forEach((o) => {
          const n = o.notes || {};
          if (o.status !== 'paid' || n.brand !== BRAND) return;
          if (String(n.phone || '').replace(/\D/g, '').slice(-10) !== phone || String(n.pincode || '').trim() !== pin) return;
          if (!hit || o.created_at > hit.created_at) { if (hit) others++; hit = o; } else { others++; }
        });
        if (items.length < 100) break;
      }
      if (!hit) return res.status(404).json({ error: 'not_found' });
      orderId = hit.id;
    } else if (/^pay_[A-Za-z0-9]{6,40}$/.test(id)) {
      const r = await fetch('https://api.razorpay.com/v1/payments/' + id, { headers: auth });
      const p = await r.json();
      if (!r.ok || !p.order_id) return res.status(404).json({ error: 'not_found' });
      orderId = p.order_id;
    } else if (/^order_[A-Za-z0-9]{6,40}$/.test(id)) {
      orderId = id;
    } else if (/^[A-Za-z0-9]{8,30}$/.test(id)) {
      const t = await shiprocket.track('awb', id);
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
    const due = n.mode === 'advance' && cart ? cart.total - 99 : 0;
    const placed = o.created_at ? new Date(o.created_at * 1000).toISOString() : '';
    if (o.status !== 'paid') return res.status(200).json({ found: true, paid: false, items, placed, due });
    const t = await shiprocket.track('order', orderId);
    return res.status(200).json(Object.assign({ paid: true, items, placed, due, others }, t.found ? t : { found: true, shipped: false }));
  } catch (e) {
    return res.status(502).json({ error: 'lookup_failed' });
  }
};
