const crypto = require('crypto');
const { keys, BRAND, ADVANCE, cartFrom } = require('./_shared');

// Owner-only lists: paid orders, unfinished orders and customers due a reorder.
// Protected by the ADMIN_KEY environment variable. Returns names and phone numbers, so never open it to the public.
// Only orders tagged brand "Youth Face" are returned, so a shared Razorpay account is fine.
const IST = 5.5 * 3600;
const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function mine(o) { return String((o.notes || {}).brand || '') === BRAND; }
function phoneOf(o) { return String((o.notes || {}).phone || '').replace(/\D/g, '').slice(-10); }
function itemsOf(o) { const c = cartFrom(String((o.notes || {}).items || '')); return c ? c.label : ''; }
function when(sec) {
  const t = new Date((sec + IST) * 1000);
  return t.getUTCDate() + ' ' + MON[t.getUTCMonth()] + ', ' + ((t.getUTCHours() + 11) % 12 + 1) + ':' +
    String(t.getUTCMinutes()).padStart(2, '0') + (t.getUTCHours() < 12 ? ' am' : ' pm');
}

async function list(k, from, to, limit) {
  const auth = { Authorization: 'Basic ' + Buffer.from(k.id + ':' + k.secret).toString('base64') };
  const all = [];
  for (let skip = 0; skip < limit; skip += 100) {
    const r = await fetch('https://api.razorpay.com/v1/orders?count=100&skip=' + skip + '&from=' + from + (to ? '&to=' + to : ''), { headers: auth });
    const d = await r.json();
    if (!r.ok) throw new Error('razorpay_list_failed');
    const items = d.items || [];
    items.forEach((o) => { if (mine(o)) all.push(o); });
    if (items.length < 100) break;
  }
  return all;
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  const admin = process.env.ADMIN_KEY || '';
  const given = String((req.headers && req.headers['x-admin-key']) || '');
  if (admin.length < 8) return res.status(503).json({ error: 'admin_key_not_set' });
  const a = crypto.createHash('sha256').update(admin).digest();
  const b = crypto.createHash('sha256').update(given).digest();
  if (!crypto.timingSafeEqual(a, b)) return res.status(401).json({ error: 'wrong_key' });
  const k = keys();
  if (!k) return res.status(503).json({ error: 'not_configured' });

  const q = req.query || {};
  const now = Math.floor(Date.now() / 1000);
  try {
    if (q.kind === 'orders') {
      const days = Number(q.days) === 7 ? 7 : 1;
      const todayStart = Math.floor((now + IST) / 86400) * 86400 - IST;
      const all = await list(k, todayStart - (days - 1) * 86400, 0, 1000);
      const out = all.filter((o) => o.status === 'paid').map((o) => {
        const n = o.notes || {};
        const cod = n.mode === 'advance';
        const total = Number(n.total) || 0;
        return { id: o.id, at: o.created_at, name: String(n.name || ''), phone: phoneOf(o), items: itemsOf(o),
          city: String(n.city || ''), pincode: String(n.pincode || ''), cod, paid: Math.round(Number(o.amount) / 100),
          collect: cod ? Math.max(0, total - ADVANCE) : 0, when: when(o.created_at) };
      }).sort((x, y) => y.at - x.at);
      const sum = (f) => out.reduce((s, o) => s + f(o), 0);
      return res.status(200).json({ kind: 'orders', days, orders: out, totals: {
        count: out.length, prepaid: out.filter((o) => !o.cod).length, cod: out.filter((o) => o.cod).length,
        received: sum((o) => o.paid), to_collect: sum((o) => o.collect) } });
    }
    if (q.kind === 'abandoned') {
      const all = await list(k, now - 3 * 86400, 0, 500);
      const paid = new Set(all.filter((o) => o.status === 'paid').map(phoneOf));
      const seen = new Set();
      const out = [];
      all.sort((x, y) => y.created_at - x.created_at).forEach((o) => {
        const p = phoneOf(o);
        if (o.status === 'paid' || p.length !== 10 || paid.has(p) || seen.has(p)) return;
        seen.add(p);
        const n = o.notes || {};
        out.push({ id: o.id, name: String(n.name || ''), phone: p, items: itemsOf(o), city: String(n.city || ''),
          amount: Number(n.total) || Math.round(Number(o.amount) / 100), cod: n.mode === 'advance', hours: Math.floor((now - o.created_at) / 3600) });
      });
      return res.status(200).json({ kind: 'abandoned', customers: out });
    }
    if (q.kind === 'refill') {
      // Customers who ticked "remind me" and whose cream should be running low now:
      // from 5 days before to 25 days after (about 30 days per jar) since the order.
      const all = await list(k, now - 200 * 86400, 0, 1000);
      const out = [];
      all.filter((o) => o.status === 'paid' && (o.notes || {}).remind === 'yes').forEach((o) => {
        const n = o.notes || {};
        const c = cartFrom(String(n.items || ''));
        const jars = c ? c.lines.reduce((s2, l) => s2 + l.qty * ({ p1: 1, p2: 2, p3: 3, combo: 1 }[l.id] || 0), 0) : 1;
        const age = Math.floor((now - o.created_at) / 86400);
        const due = Math.max(1, jars) * 30;
        if (age < due - 5 || age > due + 25) return;
        out.push({ id: o.id, name: String(n.name || ''), phone: phoneOf(o), items: itemsOf(o), city: String(n.city || ''),
          amount: Number(n.total) || Math.round(Number(o.amount) / 100), days: age, remind: true });
      });
      const seen = new Set();
      const uniq = out.sort((x, y) => x.days - y.days).filter((c) => (seen.has(c.phone) ? false : seen.add(c.phone)));
      return res.status(200).json({ kind: 'refill', customers: uniq });
    }
    const minDays = Math.max(0, Math.min(365, Number(q.from) || 22));
    const maxDays = Math.max(minDays, Math.min(365, Number(q.to) || 35));
    const all = await list(k, now - maxDays * 86400, now - minDays * 86400, 500);
    const out = all.filter((o) => o.status === 'paid').map((o) => {
      const n = o.notes || {};
      return { id: o.id, name: String(n.name || ''), phone: phoneOf(o), items: itemsOf(o), city: String(n.city || ''),
        amount: Number(n.total) || Math.round(Number(o.amount) / 100), days: Math.floor((now - o.created_at) / 86400), remind: n.remind === 'yes' };
    }).sort((x, y) => y.days - x.days);
    return res.status(200).json({ kind: 'reorder', from: minDays, to: maxDays, customers: out });
  } catch (e) {
    return res.status(502).json({ error: 'lookup_failed' });
  }
};
