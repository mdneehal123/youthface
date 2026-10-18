// Sends a website order into the Order Desk inbox (server to server, protected by WEB_ORDER_KEY).
// Order Desk keeps one entry per order number, so sending the same order twice never makes a duplicate.
const { DESK_BRAND, DESK_ID } = require('./_shared');
const deskUrl = () => (process.env.ORDERDESK_URL || 'https://www.skinday.shop').replace(/\/+$/, '');
const deskOn = () => Boolean((process.env.WEB_ORDER_KEY || '').trim());

// lines: [{id, name, qty, price}]; total: amount actually charged (paid online, or collected at the door for COD).
async function pushToDesk({ ref, c, lines, sub, disc, coupon, total, pay, paid, payId, courier, awb, note }) {
  if (!deskOn()) return { ok: false, error: 'WEB_ORDER_KEY not set' };
  const body = {
    ref, src: 'web', site: 'youthfacebeautycream.com', brand: DESK_BRAND, pay: pay === 'cod' ? 'cod' : 'upi', paid: Boolean(paid), payId: payId || '',
    total, sub: sub == null ? total : sub, disc: disc || 0, coupon: coupon || '', courier: courier || '', awb: awb || '', note: note || '',
    name: c.name, phone: c.phone, email: c.email || '', house: c.address, area: c.city, landmark: c.landmark || '', pin: c.pin, city: c.city, state: c.state || '',
    items: lines.map((l) => [DESK_ID[l.id] || '', l.name, l.qty, l.price])
  };
  try {
    const r = await fetch(deskUrl() + '/api/web-order', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'x-web-order-key': process.env.WEB_ORDER_KEY.trim() }, body: JSON.stringify(body)
    });
    const j = await r.json().catch(() => ({}));
    return r.ok && j.ok ? { ok: true, id: j.id } : { ok: false, error: j.error || 'Order Desk HTTP ' + r.status };
  } catch (e) { return { ok: false, error: String((e && e.message) || e) }; }
}

module.exports = { pushToDesk, deskOn };
