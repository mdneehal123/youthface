// Abuse protection without tracking people: limits are counted per mobile number or for the whole shop, never per IP address.
// Uses the Redis database (Upstash) when it is connected; otherwise a per-instance memory counter, so a burst is still slowed down.
const kv = require('./_kv');

const mem = new Map(); // key -> { n, until }
function memLimit(key, max, sec) {
  const now = Date.now();
  let e = mem.get(key);
  if (!e || e.until < now) { e = { n: 0, until: now + sec * 1000 }; mem.set(key, e); }
  e.n++;
  if (mem.size > 5000) { for (const [k, v] of mem) { if (v.until < now) mem.delete(k); } }
  return e.n <= max;
}

// true while under the limit (max hits per window seconds); fails open if the database has a hiccup
async function limit(key, max, sec) {
  if (!kv.cfg()) return memLimit(key, max, sec);
  try {
    const [n] = await kv.pipe([['INCR', 'rl:' + key], ['EXPIRE', 'rl:' + key, sec, 'NX']]);
    return n <= max;
  } catch (e) { return true; }
}

module.exports = { limit };
