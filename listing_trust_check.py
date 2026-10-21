#!/usr/bin/env python3
"""Check whether a pre-owned marketplace listing has enough trust signals."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ALLOWED_CONDITIONS = {"new", "like new", "excellent", "good", "fair", "needs repair"}
REQUIRED_FIELDS = ("title", "category", "condition", "price_inr", "photos", "description", "seller_city")


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def evaluate_listing(listing: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic trust assessment for one listing."""
    missing = [field for field in REQUIRED_FIELDS if field not in listing or listing[field] in (None, "", [])]
    checks: list[Check] = []

    title = _text(listing.get("title"))
    checks.append(Check("title_specific", len(title) >= 8, "title should identify the item"))

    category = _text(listing.get("category"))
    checks.append(Check("category_present", bool(category), "category is required"))

    condition = _text(listing.get("condition")).lower()
    checks.append(Check("condition_clear", condition in ALLOWED_CONDITIONS, "use a clear condition label"))

    price = listing.get("price_inr")
    price_ok = isinstance(price, (int, float)) and not isinstance(price, bool) and 100 <= price <= 2_000_000
    checks.append(Check("price_plausible", price_ok, "price must be between ₹100 and ₹20,00,000"))

    photos = listing.get("photos")
    photo_count = len(photos) if isinstance(photos, list) else 0
    checks.append(Check("photo_coverage", photo_count >= 3, "include at least three photos"))

    description = _text(listing.get("description"))
    checks.append(Check("description_complete", len(description) >= 40, "describe condition, usage and included accessories"))

    seller_city = _text(listing.get("seller_city"))
    checks.append(Check("seller_location", bool(seller_city), "seller city is required"))

    checks.append(Check("required_fields", not missing, "missing: " + ", ".join(missing) if missing else "all required fields present"))

    passed = sum(check.passed for check in checks)
    score = round((passed / len(checks)) * 100)
    status = "pass" if score == 100 else "review" if score >= 70 else "fail"
    return {
        "status": status,
        "score": score,
        "checks": [check.__dict__ for check in checks],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("listing_json", type=Path, help="Path to one listing JSON file")
    args = parser.parse_args()
    listing = json.loads(args.listing_json.read_text(encoding="utf-8"))
    print(json.dumps(evaluate_listing(listing), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
