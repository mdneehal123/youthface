// Youth Face store: prices are fixed here, on the server, so the amount charged cannot be changed from the browser.
const PRODUCTS = {
  p1: { name: 'Youth Face Beauty Cream 25g, Pack of 1', sku: 'YFB-CREAM-25', price: 549, mrp: 899, kg: 0.06 },
  p2: { name: 'Youth Face Beauty Cream, Pack of 2', sku: 'YFB-CREAM-25x2', price: 999, mrp: 1599, kg: 0.12 },
  p3: { name: 'Youth Face Beauty Cream, Pack of 3', sku: 'YFB-CREAM-25x3', price: 1444, mrp: 1899, kg: 0.18 },
  lotion: { name: 'Youth Face Body Lotion 40ml', sku: 'YFB-LOTION-40', price: 599, mrp: 599, kg: 0.07 },
  combo: { name: 'Youth Face Combo: Beauty Cream 25g + Body Lotion 40ml', sku: 'YFB-COMBO-CL', price: 999, mrp: 1498, kg: 0.13 },
  // TEMPORARY ₹1 test item for checking online payments (page /sample-test/). Remove after testing.
  sample: { name: 'Youth Face Test Sample (Rs 1)', sku: 'YFB-TEST', price: 1, mrp: 1, kg: 0.05 }
};
const BRAND = 'Youth Face';
// Orders placed before the switch could be "advance" Cash on Delivery orders (Rs 99 paid online, the rest at the door).
// Used only to read those old orders back; new Cash on Delivery orders have nothing paid upfront.
const LEGACY_ADVANCE = 99;
const MAX_QTY = 10;
// Order Desk (owner's order inbox): brand id, order number prefix, and product ids for items that are exactly an Order Desk product.
// The combo has no Order Desk product id: it is kept by its name and price as sold.
const DESK_BRAND = 'yf';
const REF_PREFIX = 'YC'; // YC = youthfacebeautycream.com, so these orders are told apart from youthfacebeauty.com's
const DESK_ID = { p1: 'yf1', p2: 'yf2', p3: 'yf3', lotion: 'yf4' };

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
  // A Pack of 1 cream and a Body Lotion bought together are charged at the combo price (same rule as the cart page).
  const pairs = Math.min(merged.p1 || 0, merged.lotion || 0, MAX_QTY - (merged.combo || 0));
  if (pairs > 0) {
    merged.combo = (merged.combo || 0) + pairs; merged.p1 -= pairs; merged.lotion -= pairs;
    if (!merged.p1) delete merged.p1;
    if (!merged.lotion) delete merged.lotion;
  }
  const lines = Object.keys(merged).map((id) => Object.assign({ id, qty: merged[id] }, PRODUCTS[id]));
  if (!lines.length) return null;
  const total = lines.reduce((a, l) => a + l.price * l.qty, 0);
  const mrp = lines.reduce((a, l) => a + l.mrp * l.qty, 0);
  const kg = lines.reduce((a, l) => a + l.kg * l.qty, 0);
  const code = lines.map((l) => l.id + ':' + l.qty).join(',');
  const label = lines.map((l) => l.name + (l.qty > 1 ? ' x' + l.qty : '')).join('; ');
  return { lines, total, mrp, kg, code, label };
}

// Website order number (YC + 8 digits). The browser makes one per checkout so a retry never books twice;
// anything else is replaced with a fresh number.
function orderRef(input) {
  const v = String(input || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  if (new RegExp('^' + REF_PREFIX + '\\d{8}$').test(v)) return v;
  return REF_PREFIX + String(require('crypto').randomInt(0, 1e8)).padStart(8, '0');
}

// Parcel size by number of jars/bottles. Weight is the products plus about 50 g of packing (same spec the shop used with Shiprocket).
function parcel(cart) {
  const units = cart.lines.reduce((a, l) => a + l.qty * (/x3$/.test(l.sku) ? 3 : /x2$|COMBO/.test(l.sku) ? 2 : 1), 0);
  const weight = Math.max(0.1, Math.round((cart.kg + 0.05) * 100) / 100);
  if (units <= 1) return { weight, length: 10, breadth: 10, height: 8 };
  if (units <= 3) return { weight, length: 15, breadth: 12, height: 8 };
  return { weight, length: 20, breadth: 15, height: 10 };
}

// State from the first two digits of the pincode (the checkout does not ask for the state).
const STATE_BY_PREFIX = {
  11: 'Delhi', 12: 'Haryana', 13: 'Haryana', 14: 'Punjab', 15: 'Punjab', 16: 'Punjab', 17: 'Himachal Pradesh',
  18: 'Jammu and Kashmir', 19: 'Jammu and Kashmir', 20: 'Uttar Pradesh', 21: 'Uttar Pradesh', 22: 'Uttar Pradesh',
  23: 'Uttar Pradesh', 24: 'Uttar Pradesh', 25: 'Uttar Pradesh', 26: 'Uttarakhand', 27: 'Uttar Pradesh', 28: 'Uttar Pradesh',
  30: 'Rajasthan', 31: 'Rajasthan', 32: 'Rajasthan', 33: 'Rajasthan', 34: 'Rajasthan', 36: 'Gujarat', 37: 'Gujarat',
  38: 'Gujarat', 39: 'Gujarat', 40: 'Maharashtra', 41: 'Maharashtra', 42: 'Maharashtra', 43: 'Maharashtra', 44: 'Maharashtra',
  45: 'Madhya Pradesh', 46: 'Madhya Pradesh', 47: 'Madhya Pradesh', 48: 'Madhya Pradesh', 49: 'Chhattisgarh',
  50: 'Telangana', 51: 'Andhra Pradesh', 52: 'Andhra Pradesh', 53: 'Andhra Pradesh', 56: 'Karnataka', 57: 'Karnataka',
  58: 'Karnataka', 59: 'Karnataka', 60: 'Tamil Nadu', 61: 'Tamil Nadu', 62: 'Tamil Nadu', 63: 'Tamil Nadu', 64: 'Tamil Nadu',
  65: 'Tamil Nadu', 66: 'Tamil Nadu', 67: 'Kerala', 68: 'Kerala', 69: 'Kerala', 70: 'West Bengal', 71: 'West Bengal',
  72: 'West Bengal', 73: 'West Bengal', 74: 'West Bengal', 75: 'Odisha', 76: 'Odisha', 77: 'Odisha', 78: 'Assam',
  79: 'Assam', 80: 'Bihar', 81: 'Bihar', 82: 'Jharkhand', 83: 'Jharkhand', 84: 'Bihar', 85: 'Bihar'
};
function stateFor(pin) { return STATE_BY_PREFIX[Number(String(pin || '').slice(0, 2))] || ''; }

// Checkout details, cleaned and checked. Returns null if something is missing.
function customer(b) {
  b = b || {};
  const c = {
    name: clean(b.name, 80), phone: clean(b.phone, 20).replace(/\D/g, '').slice(-10), email: clean(b.email, 120),
    address: clean(b.address, 250), landmark: clean(b.landmark, 120), city: clean(b.city, 60), pin: clean(b.pincode || b.pin, 6)
  };
  if (c.name.length < 2 || !/^[6-9]\d{9}$/.test(c.phone) || c.address.length < 8 || c.city.length < 2 || !/^[1-9]\d{5}$/.test(c.pin)) return null;
  c.state = clean(b.state, 60) || stateFor(c.pin);
  return c;
}

// Reads an order back from its Razorpay notes (written by api/create-order.js, so they can be trusted).
// Older orders may be "advance" Cash on Delivery orders: for those, the courier collects what was not paid online.
function shipArgs(o) {
  const n = (o && o.notes) || {};
  if (n.brand !== BRAND) return null;
  const cart = cartFrom(String(n.items || ''));
  if (!cart || !n.name) return null;
  const legacyCod = n.mode === 'advance';
  return {
    id: o.id, ref: n.ref || '', cart, name: n.name, phone: n.phone, address: n.address, city: n.city, pincode: n.pincode,
    cod: legacyCod, collect: legacyCod ? Math.max(0, cart.total - LEGACY_ADVANCE) : 0, paid: legacyCod ? null : cart.total
  };
}

module.exports = { PRODUCTS, BRAND, LEGACY_ADVANCE, DESK_BRAND, DESK_ID, REF_PREFIX, keys, clean, cartFrom, shipArgs, orderRef, parcel, stateFor, customer };
