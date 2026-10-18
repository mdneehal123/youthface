// GET /api/delhivery-check — confirms the Delhivery token works (pincode lookup only; books nothing, shows no secrets).
const { delhiveryOn, serviceable } = require('./_delhivery');
const { deskOn } = require('./_orderdesk');
module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  const pickup = process.env.DELHIVERY_PICKUP || '';
  const out = { on: delhiveryOn(), env: process.env.DELHIVERY_ENV === 'staging' ? 'staging' : 'live', pickupNames: pickup.split('|').filter((x) => x.trim()).length,
    pickupHasExtraSpaces: pickup !== pickup.trim(), tokenLength: (process.env.DELHIVERY_TOKEN || '').trim().length, orderDesk: deskOn() };
  if (!out.on) return res.status(200).json(out);
  try { const s = await serviceable('581320'); out.tokenWorks = s.known; out.sample = { pin: '581320', cod: s.cod, prepaid: s.prepaid }; }
  catch (e) { out.tokenWorks = false; out.error = String((e && e.message) || e).slice(0, 200); }
  return res.status(200).json(out);
};
