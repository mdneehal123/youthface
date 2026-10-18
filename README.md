# Youth Face store (youthfacebeautycream.com)

Static site built by `python3 _build/build.py` (writes the pages into the repository root; commit the built files too),
hosted on Vercel, with serverless functions in `api/`. Prices live in `api/_shared.js` and `_build/build.py` and must match.

## How orders flow

| Payment | What happens |
|---|---|
| **Pay online** (Razorpay, full amount) | `api/create-order` prices the cart on the server (combo rule included) and opens Razorpay for the full amount. `api/verify` checks the signature, confirms with Razorpay that the payment is captured/authorized for this order and for the server price, and sends the order to the **Order Desk** as PAID (`pay: "upi"`, `paid: true`, payment id). Paid orders are **not** booked with Delhivery and no longer sent to Shiprocket. |
| **Cash on Delivery** (nothing paid upfront) | `api/cod-order` prices the cart on the server, checks Delhivery COD availability for the pincode (409 with a clear message if COD is not available there), books the **Delhivery** shipment (COD amount = order total) and always saves the order in the **Order Desk**: booked → courier Delhivery + AWB + "print the label from the Delhivery panel"; booking failed → "⚠ COD website order — Delhivery booking failed: …" so it can be booked by hand. The customer sees the Delhivery tracking number on the success screen. Rate-limited per mobile number and for the whole shop. The browser makes one order number per checkout, so a retry (double tap, slow network) gets the first answer back and never books a second parcel. |
| **WhatsApp** | Opens WhatsApp with the order text (also the only option if neither Razorpay, Delhivery nor the Order Desk is set up). |

Order numbers are `YC` + 8 digits (YC = youthfacebeautycream.com, so they are told apart from youthfacebeauty.com orders).
Order Desk brand id: `yf`; product ids: Pack of 1 = `yf1`, Pack of 2 = `yf2`, Pack of 3 = `yf3`, Body Lotion = `yf4`.
The Combo has no Order Desk id and is kept by its name and price as sold.

Parcel weight for Delhivery = product weights in `api/_shared.js` + about 50 g packing; box 10×10×8 cm (1 unit),
15×12×8 (2–3), 20×15×10 (more).

Shiprocket is no longer used for orders; `api/_shiprocket.js` only tracks parcels booked before the switch (and answers
pincode lookups while Delhivery is not set up), and only if its old env vars are still set.

There are 8 serverless functions (the Vercel Hobby limit is 12): `cod-order`, `config`, `create-order`,
`delhivery-check`, `pincode`, `reorder`, `track`, `verify`. Files starting with `_` are shared code, not functions.

## Environment variables (Vercel project settings)

| Name | Value |
|---|---|
| `WEB_ORDER_KEY` | Same secret key as the Order Desk project |
| `ORDERDESK_URL` | Optional, default `https://www.skinday.shop` |
| `DELHIVERY_TOKEN` | Delhivery API token |
| `DELHIVERY_PICKUP` | `mohammed nihal\|Beauty Mart` (pickup names as registered in Delhivery, separated by `\|`; spelling variants are tried if Delhivery rejects the warehouse name) |
| `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` | Razorpay keys |
| Optional | `KV_REST_API_URL` + `KV_REST_API_TOKEN` (Upstash Redis): shares rate limits and retry protection across server instances and lets COD orders be tracked by order number or mobile + pincode. Without it the site still works (per-instance memory, tracking by Delhivery AWB). |
| Optional | `DELHIVERY_ENV=staging`, `DELHIVERY_MODE=Express`; `SHIPROCKET_EMAIL`, `SHIPROCKET_PASSWORD` only for tracking older parcels; `ADMIN_KEY` for the owner page `/reorder/` |

Check after deploying: `/api/config` shows which services are on, `/api/delhivery-check` checks the Delhivery token
(pincode lookup only, books nothing, shows no secrets).

## TEMPORARY: ₹1 test sample

For testing online payments only: `sample` (₹1) in `api/_shared.js` and `assets/products.json` (from `STORE_ITEMS`
in `_build/build.py`), and the hidden, noindex page `/sample-test/` which adds it to the cart and opens checkout.
**Remove all three after testing** and rebuild.

Images keep their old WordPress paths under `wp-content/uploads/2026/10/`. Until those files are added
to this repo, pages load them from the old site; add them before moving the domain.
