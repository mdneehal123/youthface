// LEGACY: orders are no longer sent to Shiprocket (paid orders go to the Order Desk, Cash on Delivery to Delhivery).
// Kept only so orders shipped through Shiprocket before the switch can still be tracked, and as a pincode lookup
// fallback while Delhivery is not set up. Used only when SHIPROCKET_EMAIL and SHIPROCKET_PASSWORD are still set.
const BASE = 'https://apiv2.shiprocket.in/v1/external';

const BOX = { weight: 0.1 };

// Fallback when the pincode lookup is unavailable: first two digits of the pincode.
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

function settings() {
  const email = process.env.SHIPROCKET_EMAIL;
  const password = process.env.SHIPROCKET_PASSWORD;
  return email && password ? { email, password } : null;
}

let cached = { token: '', until: 0 };

async function login(s) {
  if (cached.token && Date.now() < cached.until) return cached.token;
  const r = await fetch(BASE + '/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: s.email, password: s.password })
  });
  const d = await r.json().catch(() => ({}));
  if (!r.ok || !d.token) {
    const e = new Error('shiprocket_login_failed');
    e.detail = { step: 'login', http: r.status, message: String(d.message || '').slice(0, 200) };
    throw e;
  }
  cached = { token: d.token, until: Date.now() + 8 * 24 * 3600 * 1000 };
  return d.token;
}

// Tracking. kind: 'order' (our order id) or 'awb'. Returns a small, customer-safe summary.
async function track(kind, value) {
  const s = settings();
  if (!s) return { found: false, reason: 'off' };
  const token = await login(s);
  const url = kind === 'awb'
    ? BASE + '/courier/track/awb/' + encodeURIComponent(value)
    : BASE + '/courier/track?order_id=' + encodeURIComponent(value);
  const r = await fetch(url, { headers: { Authorization: 'Bearer ' + token } });
  const raw = await r.json().catch(() => null);
  if (!r.ok || !raw) return { found: false, reason: 'lookup_failed', http: r.status };
  // The two endpoints wrap the same data differently.
  let t = raw;
  if (Array.isArray(t)) t = t[0];
  if (t && !t.tracking_data) { const k = Object.keys(t)[0]; if (t[k] && t[k].tracking_data) t = t[k]; }
  const d = t && t.tracking_data;
  if (!d) return { found: false, reason: 'no_data' };
  const sh = (Array.isArray(d.shipment_track) && d.shipment_track[0]) || {};
  const acts = Array.isArray(d.shipment_track_activities) ? d.shipment_track_activities : [];
  if (!sh.awb_code && !acts.length) return kind === 'awb' ? { found: false, reason: 'unknown_awb' } : { found: true, shipped: false };
  return {
    found: true,
    shipped: true,
    status: String(sh.current_status || '').trim(),
    courier: String(sh.courier_name || '').trim(),
    awb: String(sh.awb_code || '').trim(),
    expected: String(d.etd || sh.edd || '').trim(),
    delivered_on: String(sh.delivered_date || '').trim(),
    track_url: /^https:\/\//.test(String(d.track_url || '')) ? d.track_url : '',
    events: acts.slice(0, 12).map((a) => ({ date: String(a.date || ''), text: String(a.activity || a.status || ''), place: String(a.location || '') }))
  };
}


// City, state and estimated delivery days for a pincode. Never throws for an unknown pincode.
const ORIGIN = '581320';
async function pincode(pin) {
  const s = settings();
  if (!s) return { ok: false };
  const token = await login(s);
  const head = { headers: { Authorization: 'Bearer ' + token } };
  const sv = (cod) => fetch(BASE + '/courier/serviceability/?pickup_postcode=' + ORIGIN + '&delivery_postcode=' + encodeURIComponent(pin) + '&weight=' + BOX.weight + '&cod=' + cod, head).then((r) => r.json()).catch(() => null);
  const [a, b, c] = await Promise.all([
    fetch(BASE + '/open/postcode/details?postcode=' + encodeURIComponent(pin), head).then((r) => r.json()).catch(() => null),
    sv(0), sv(1)
  ]);
  const pd = (a && a.postcode_details) || {};
  const name = (v) => String(v || '').trim().toLowerCase().replace(/\b[a-z]/g, (c) => c.toUpperCase()).slice(0, 60);
  const city = name(pd.city), state = name(pd.state) || STATE_BY_PREFIX[Number(pin.slice(0, 2))] || '';
  let days = 0;
  const data = b && b.data;
  const list = data && Array.isArray(data.available_courier_companies) ? data.available_courier_companies : [];
  if (list.length) {
    const pickId = data.shiprocket_recommended_courier_id || data.recommended_courier_company_id;
    const pick = list.find((c) => c.courier_company_id === pickId) || list[0];
    const n = Math.round(Number(pick.estimated_delivery_days));
    if (n >= 1 && n <= 12) days = n;
  }
  // Cash on Delivery: true / false when the courier answered, null when we could not tell.
  const codData = c && c.data;
  const cod = codData && Array.isArray(codData.available_courier_companies) ? codData.available_courier_companies.length > 0 : (c && c.status === 404 ? false : null);
  // Not serviceable only when the courier clearly answered with no couriers for prepaid either.
  const serviceable = data && Array.isArray(data.available_courier_companies) ? list.length > 0 : (b && b.status === 404 ? false : null);
  if (!city && !days && serviceable !== false) return { ok: false };
  return { ok: true, city, state, days, cod, serviceable };
}

module.exports = { settings, track, pincode };
