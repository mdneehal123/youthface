// Delhivery B2C API: pincode serviceability, shipment (waybill) booking for Cash on Delivery orders, and tracking.
// Vercel env: DELHIVERY_TOKEN, DELHIVERY_PICKUP (pickup/warehouse name exactly as registered in Delhivery; several names
// may be listed separated by "|", e.g. "mohammed nihal|Beauty Mart"), optional DELHIVERY_ENV=staging,
// DELHIVERY_MODE (Surface|Express, default Surface).
const { parcel } = require('./_shared');

const base = () => (process.env.DELHIVERY_ENV === 'staging' ? 'https://staging-express.delhivery.com' : 'https://track.delhivery.com');
const token = () => (process.env.DELHIVERY_TOKEN || '').trim();
const pickup = () => (process.env.DELHIVERY_PICKUP || '').split('|')[0].trim();
// Each listed pickup name is also tried in a few spellings. A name Delhivery doesn't recognise books nothing, so trying them is safe.
function pickupNames() {
  const raw = (process.env.DELHIVERY_PICKUP || '').split('|').map((x) => x.trim()).filter(Boolean);
  const out = [];
  const add = (n) => { if (n && !out.includes(n)) out.push(n); };
  raw.forEach((n) => { add(n); add(n.toUpperCase()); add(n.toLowerCase()); add(n.replace(/\b\w/g, (ch) => ch.toUpperCase())); add(n + ' '); });
  return out.slice(0, 12);
}
const delhiveryOn = () => Boolean(token() && pickup());
const RETURN = { name: 'Beauty Mart', add: 'Azad Nagar 4th Cross, Bhatkal', city: 'Bhatkal', state: 'Karnataka', pin: '581320', phone: '9980881230' };
const head = () => ({ Authorization: 'Token ' + token(), Accept: 'application/json' });

// { known, cod, prepaid, city, state } — known:false when Delhivery does not deliver to the pincode at all.
async function serviceable(pin) {
  const r = await fetch(base() + '/c/api/pin-codes/json/?filter_codes=' + encodeURIComponent(pin), { headers: head() });
  if (!r.ok) throw new Error('delhivery_http_' + r.status);
  const j = await r.json().catch(() => ({}));
  const pc = j && j.delivery_codes && j.delivery_codes[0] && j.delivery_codes[0].postal_code;
  if (!pc) return { known: false, cod: false, prepaid: false, city: '', state: '' };
  return { known: true, cod: String(pc.cod).toUpperCase() === 'Y', prepaid: String(pc.pre_paid).toUpperCase() === 'Y', city: pc.city || '', state: pc.state_code || '' };
}

// Books one shipment. c: cleaned customer; cart: from cartFrom(); total: amount the courier collects (COD) or the order value.
async function createShipment({ ref, c, cart, total, pay }) {
  const box = parcel(cart);
  const shipment = {
    name: c.name, add: [c.address, c.landmark ? 'Near ' + c.landmark : ''].filter(Boolean).join(', '), pin: c.pin, city: c.city, state: c.state, country: 'India',
    phone: c.phone, order: ref, payment_mode: pay === 'cod' ? 'COD' : 'Prepaid', cod_amount: pay === 'cod' ? String(total) : '0', total_amount: String(total),
    products_desc: cart.lines.map((l) => l.name + ' x' + l.qty).join(', ').slice(0, 200), quantity: String(cart.lines.reduce((a, l) => a + l.qty, 0)),
    order_date: new Date().toISOString().slice(0, 19).replace('T', ' '), weight: String(Math.round(box.weight * 1000)),
    shipment_length: String(box.length), shipment_width: String(box.breadth), shipment_height: String(box.height),
    seller_name: 'Beauty Mart', seller_add: RETURN.add, return_name: RETURN.name, return_add: RETURN.add, return_city: RETURN.city, return_state: RETURN.state,
    return_pin: RETURN.pin, return_country: 'India', return_phone: RETURN.phone, shipping_mode: process.env.DELHIVERY_MODE || 'Surface', address_type: 'home', waybill: ''
  };
  let last = '';
  for (const name of pickupNames()) {
    const data = { shipments: [shipment], pickup_location: { name } };
    const r = await fetch(base() + '/api/cmu/create.json', {
      method: 'POST', headers: Object.assign(head(), { 'Content-Type': 'application/x-www-form-urlencoded' }),
      body: 'format=json&data=' + encodeURIComponent(JSON.stringify(data))
    });
    const j = await r.json().catch(() => ({}));
    const pkg = j && Array.isArray(j.packages) && j.packages[0];
    if (r.ok && pkg && pkg.waybill && String(pkg.status).toLowerCase() === 'success') return { ok: true, awb: String(pkg.waybill), pickup: name };
    last = String((pkg && (Array.isArray(pkg.remarks) ? pkg.remarks.join('; ') : pkg.remarks)) || j.rmk || j.error || ('HTTP ' + r.status));
    if (!/ClientWarehouse|warehouse|pickup/i.test(last)) break; // a different problem: another name won't help
  }
  return { ok: false, error: (last + ' (pickup names tried: ' + pickupNames().map((n) => JSON.stringify(n)).join(', ') + ')').slice(0, 400) };
}

// Tracking by waybill. Returns the same customer-safe shape the tracking page already understands.
async function track(awb) {
  const r = await fetch(base() + '/api/v1/packages/json/?waybill=' + encodeURIComponent(awb), { headers: head() });
  const j = r.ok ? await r.json().catch(() => null) : null;
  const sh = j && Array.isArray(j.ShipmentData) && j.ShipmentData[0] && j.ShipmentData[0].Shipment;
  if (!sh) return { found: false, reason: r.ok ? 'unknown_awb' : 'lookup_failed' };
  const st = sh.Status || {};
  const status = String(st.Status || '').trim();
  const scans = Array.isArray(sh.Scans) ? sh.Scans.map((x) => x && x.ScanDetail).filter(Boolean) : [];
  const waiting = !status || /manifest|not picked|pickup scheduled|open/i.test(status);
  return {
    found: true, shipped: !waiting, courier: 'Delhivery', awb: String(sh.AWB || awb),
    status: waiting ? '' : (String(st.Instructions || '').trim() && /pending|transit/i.test(status) ? status + ': ' + String(st.Instructions).trim() : status),
    expected: String(sh.ExpectedDeliveryDate || sh.PromisedDeliveryDate || '').trim(),
    delivered_on: /deliver/i.test(status) && !/undeliver|not deliver/i.test(status) ? String(st.StatusDateTime || '').trim() : '',
    track_url: 'https://www.delhivery.com/track/package/' + encodeURIComponent(String(sh.AWB || awb)),
    events: scans.slice(-12).reverse().map((s) => ({ date: String(s.ScanDateTime || ''), text: String(s.Instructions || s.Scan || ''), place: String(s.ScannedLocation || '') }))
  };
}

module.exports = { delhiveryOn, serviceable, createShipment, track, pickupNames };
