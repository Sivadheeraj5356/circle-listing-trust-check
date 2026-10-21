import unittest

from listing_trust_check import evaluate_listing


GOOD_LISTING = {
    "title": "iPhone 13 128GB Blue",
    "category": "Phones",
    "condition": "good",
    "price_inr": 34500,
    "photos": ["front.jpg", "back.jpg", "screen-on.jpg"],
    "description": "Used for 18 months. Battery health 86%. Includes original cable and box. No screen or body damage.",
    "seller_city": "Bengaluru",
}


class ListingTrustCheckTests(unittest.TestCase):
    def test_good_listing_passes(self):
        result = evaluate_listing(GOOD_LISTING)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["score"], 100)

    def test_missing_required_field_fails_check(self):
        listing = dict(GOOD_LISTING)
        del listing["seller_city"]
        result = evaluate_listing(listing)
        self.assertEqual(result["status"], "review")
        self.assertIn("required_fields", {check["name"] for check in result["checks"] if not check["passed"]})

    def test_short_description_needs_review(self):
        listing = dict(GOOD_LISTING, description="Good phone")
        result = evaluate_listing(listing)
        self.assertEqual(result["status"], "review")

    def test_two_photos_need_review(self):
        listing = dict(GOOD_LISTING, photos=["front.jpg", "back.jpg"])
        result = evaluate_listing(listing)
        self.assertEqual(result["status"], "review")

    def test_unknown_condition_needs_review(self):
        listing = dict(GOOD_LISTING, condition="mint-ish")
        result = evaluate_listing(listing)
        self.assertEqual(result["status"], "review")

    def test_implausible_price_fails(self):
        listing = dict(GOOD_LISTING, price_inr=0)
        result = evaluate_listing(listing)
        self.assertEqual(result["status"], "review")


if __name__ == "__main__":
    unittest.main()
