// Youth Face store: prices are fixed here, on the server, so the amount charged cannot be changed from the browser.
const PRODUCTS = {
  p1: { name: 'Youth Face Beauty Cream 25g, Pack of 1', sku: 'YFB-CREAM-25', price: 549, mrp: 899, kg: 0.06 },
  p2: { name: 'Youth Face Beauty Cream, Pack of 2', sku: 'YFB-CREAM-25x2', price: 999, mrp: 1599, kg: 0.12 },
  p3: { name: 'Youth Face Beauty Cream, Pack of 3', sku: 'YFB-CREAM-25x3', price: 1444, mrp: 1899, kg: 0.18 },
  lotion: { name: 'Youth Face Body Lotion 40ml', sku: 'YFB-LOTION-40', price: 599, mrp: 599, kg: 0.07 },
  combo: { name: 'Youth Face Combo: Beauty Cream 25g + Body Lotion 40ml', sku: 'YFB-COMBO-CL', price: 999, mrp: 1498, kg: 0.13 }
};
const BRAND = 'Youth Face';
// Cash on Delivery needs this much paid online in advance. The rest is collected at the door.
const ADVANCE = 99;
const MAX_QTY = 10;

function keys() {
  const id = process.env.RAZORPAY_KEY_ID;
  const secret = process.env.RAZORPAY_KEY_SECRET;
  return id && secret ? { id, secret } : null;
}

function clean(value, max) {
  return String(value == null ? '' : value).replace(/\s+/g, ' ').trim().slice(0, max);
}

// Accepts [{id, qty}] or the compact "p1:2,lotion:1" form stored on the order. Unknown items are dropped.
function cartFrom(input) {
  let list = input;
  if (typeof input === 'string') list = input.split(',').map((s) => { const [id, q] = s.split(':'); return { id, qty: q }; });
  if (!Array.isArray(list)) return null;
  const merged = {};
  list.forEach((it) => {
    const id = String((it && it.id) || '');
    const qty = Math.floor(Number(it && it.qty));
    if (!PRODUCTS[id] || !(qty >= 1)) return;
    merged[id] = Math.min(MAX_QTY, (merged[id] || 0) + qty);
  });
  const lines = Object.keys(merged).map((id) => Object.assign({ id, qty: merged[id] }, PRODUCTS[id]));
  if (!lines.length) return null;
  const total = lines.reduce((a, l) => a + l.price * l.qty, 0);
  const mrp = lines.reduce((a, l) => a + l.mrp * l.qty, 0);
  const kg = lines.reduce((a, l) => a + l.kg * l.qty, 0);
  const code = lines.map((l) => l.id + ':' + l.qty).join(',');
  const label = lines.map((l) => l.name + (l.qty > 1 ? ' x' + l.qty : '')).join('; ');
  return { lines, total, mrp, kg, code, label };
}

// Turns a paid Razorpay order into what the courier needs. Amounts come from the price table above.
function shipArgs(o) {
  const n = (o && o.notes) || {};
  if (n.brand !== BRAND) return null;
  const cart = cartFrom(String(n.items || ''));
  if (!cart || !n.name) return null;
  const advance = n.mode === 'advance';
  return {
    id: o.id, cart, name: n.name, phone: n.phone, address: n.address, city: n.city, pincode: n.pincode,
    cod: advance,
    discount: advance ? ADVANCE : 0,
    collect: advance ? cart.total - ADVANCE : 0
  };
}

module.exports = { PRODUCTS, BRAND, ADVANCE, keys, clean, cartFrom, shipArgs };
