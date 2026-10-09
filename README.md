# Youth Face store (youthfacebeautycream.com)

Static site built by `python3 _build/build.py`, hosted on Vercel, with serverless functions in `api/`.

Vercel environment variables: RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, SHIPROCKET_EMAIL, SHIPROCKET_PASSWORD.

Images keep their old WordPress paths under `wp-content/uploads/2026/10/`. Until those files are added
to this repo, pages load them from the old site; add them before moving the domain.
