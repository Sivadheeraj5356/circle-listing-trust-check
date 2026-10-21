# Circle Listing Trust Check

A small Python utility for reviewing whether a pre-owned marketplace listing gives buyers enough trust signals before it goes live.

Circle's marketplace has to earn trust from both buyers and sellers. This checker keeps that idea concrete: clear condition, plausible pricing, photo coverage, useful descriptions, seller location and required listing metadata.

## Run

```bash
python3 listing_trust_check.py examples/iphone_13.json
```

The command prints a JSON report with a 0-100 score, `pass` / `review` / `fail` status, and the exact checks that need attention.

## Test

```bash
python3 -m unittest -v
```

## Input shape

```json
{
  "title": "iPhone 13 128GB Blue",
  "category": "Phones",
  "condition": "good",
  "price_inr": 34500,
  "photos": ["front.jpg", "back.jpg", "screen-on.jpg"],
  "description": "Used for 18 months. Battery health 86%. Includes original cable and box. No screen or body damage.",
  "seller_city": "Bengaluru"
}
```

No external services or credentials are used.
