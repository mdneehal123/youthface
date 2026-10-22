const { pushLead } = require('./_orderdesk');
const guard = require('./_guard');

// Checkout lead capture: a shopper who ticked "You may message me on WhatsApp..." at checkout.
// Passed to the private Order Desk so the owner can message them herself. It never blocks checkout, so every
// valid-looking request answers { ok: true } even if Order Desk is not set up or is down.
const clean = (v, n) => String(v == null ? '' : v).replace(/[\u0000-\u001f\u007f-\u009f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, n);

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ ok: false }); }
  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch (e) { b = {}; } }
  b = b && typeof b === 'object' ? b : {};
  if (b.consent !== true) return res.status(400).json({ ok: false });
  const phone = String(b.phone == null ? '' : b.phone).replace(/\D/g, '').slice(-10);
  if (!/^[6-9]\d{9}$/.test(phone)) return res.status(400).json({ ok: false });
  try {
    if (!(await guard.limit('lead:' + phone, 5, 3600)) || !(await guard.limit('lead', 600, 3600))) return res.status(200).json({ ok: true });
    const r = await pushLead({ phone, name: clean(b.name, 80), product: clean(b.product, 120) });
    if (!r.ok) console.error('lead not sent:', r.error);
  } catch (e) { console.error('lead error'); }
  return res.status(200).json({ ok: true });
};
