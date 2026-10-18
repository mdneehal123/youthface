const delhivery = require('./_delhivery');
const shiprocket = require('./_shiprocket');
const guard = require('./_guard');
const { stateFor } = require('./_shared');

// Looks up a delivery pincode: city, state, whether it is delivered to, and whether Cash on Delivery is available there.
// COD availability comes from Delhivery (the courier that delivers COD orders). Response:
//   { ok, city, state, days, cod: true|false|null, serviceable: true|false|null }
// Used only to help the customer fill the form. Any failure returns { ok: false } and the form carries on as before.
const title = (v) => String(v || '').trim().toLowerCase().replace(/\b[a-z]/g, (c) => c.toUpperCase()).slice(0, 60);

async function lookup(pin) {
  if (delhivery.delhiveryOn()) {
    const s = await delhivery.serviceable(pin);
    if (!s.known) return { ok: true, city: '', state: stateFor(pin), days: 0, cod: false, serviceable: false };
    return { ok: true, city: title(s.city), state: stateFor(pin), days: 0, cod: s.cod, serviceable: s.cod || s.prepaid };
  }
  // Delhivery not set up yet: the old Shiprocket lookup, if it is still connected (city and delivery days only).
  if (shiprocket.settings()) return shiprocket.pincode(pin);
  return { ok: false };
}

module.exports = async (req, res) => {
  const pin = String((req.query && req.query.pin) || '').trim();
  if (!/^[1-9]\d{5}$/.test(pin)) { res.setHeader('Cache-Control', 'no-store'); return res.status(400).json({ ok: false }); }
  if (!(await guard.limit('pin', 3000, 3600))) { res.setHeader('Cache-Control', 'no-store'); return res.status(200).json({ ok: false }); }
  try {
    const out = await lookup(pin);
    // The same pincode gives the same answer for everyone, so let the CDN keep it for half a day.
    res.setHeader('Cache-Control', out.ok ? 'public, s-maxage=43200, max-age=3600' : 'no-store');
    return res.status(200).json(out);
  } catch (e) {
    console.error('pincode lookup failed', e && e.message);
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ ok: false });
  }
};
