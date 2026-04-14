from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd


@dataclass
class UserProfile:
    user_id: int
    profile_type: str  # "budget", "average", "high"
    spend_multiplier: float


CATEGORY_CONFIG = {
    "dining": {
        "prob": 0.25,
        "amount_mean": 40,
        "amount_sigma": 0.5,
        "min": 15,
        "max": 80,
    },
    "groceries": {
        "prob": 0.15,
        "amount_mean": 80,
        "amount_sigma": 0.6,
        "min": 40,
        "max": 180,
    },
    "travel": {
        "prob": 0.05,
        "amount_mean": 600,
        "amount_sigma": 1.0,
        "min": 200,
        "max": 2000,
    },
    "gas": {
        "prob": 0.10,
        "amount_mean": 50,
        "amount_sigma": 0.4,
        "min": 30,
        "max": 75,
    },
    "entertainment": {
        "prob": 0.12,
        "amount_mean": 60,
        "amount_sigma": 0.7,
        "min": 20,
        "max": 150,
    },
    "shopping": {
        "prob": 0.20,
        "amount_mean": 120,
        "amount_sigma": 0.8,
        "min": 25,
        "max": 300,
    },
    "bills": {
        "prob": 0.08,
        "amount_mean": 110,
        "amount_sigma": 0.4,
        "min": 50,
        "max": 200,
    },
    "other": {
        "prob": 0.05,
        "amount_mean": 40,
        "amount_sigma": 0.7,
        "min": 10,
        "max": 100,
    },
}


def _generate_user_profiles(num_users: int, rng: np.random.Generator) -> List[UserProfile]:
    """Create user profiles with different spending behavior."""
    profile_probs = [0.7, 0.2, 0.1]  # budget, average, high
    profile_types = rng.choice(
        ["budget", "average", "high"], size=num_users, p=profile_probs
    )
    multipliers = {
        "budget": 0.7,
        "average": 1.0,
        "high": 1.6,
    }
    return [
        UserProfile(
            user_id=i + 1,
            profile_type=profile_types[i],
            spend_multiplier=multipliers[profile_types[i]],
        )
        for i in range(num_users)
    ]


def _sample_category(n: int, rng: np.random.Generator) -> np.ndarray:
    categories = list(CATEGORY_CONFIG.keys())
    probs = [CATEGORY_CONFIG[c]["prob"] for c in categories]
    return rng.choice(categories, size=n, p=probs)


def _sample_dates(
    n: int,
    start: date,
    end: date,
    categories: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample dates with simple temporal patterns per category."""
    days_range = (end - start).days
    base_offsets = rng.integers(0, days_range + 1, size=n)
    dates = np.array([start + timedelta(days=int(d)) for d in base_offsets])

    # Apply simple weekday/seasonality adjustments
    for i in range(n):
        cat = categories[i]
        d = dates[i]

        # Dining: more on Fri-Sun
        if cat == "dining":
            if d.weekday() < 4 and rng.random() < 0.6:  # Mon-Thu
                # shift to upcoming Fri-Sun
                shift = (4 - d.weekday()) % 7  # 0-6
                shift += rng.integers(0, 3)  # Fri-Sun
                dates[i] = d + timedelta(days=int(shift))

        # Groceries: weekly pattern (snap to same weekday)
        elif cat == "groceries":
            if rng.random() < 0.7:
                # snap to Sat or Sun
                target_weekday = rng.choice([5, 6])  # Sat or Sun
                delta = (target_weekday - d.weekday()) % 7
                dates[i] = d + timedelta(days=int(delta))

        # Gas: every ~2 weeks feeling by favoring Mon-Thu
        elif cat == "gas":
            if d.weekday() >= 5 and rng.random() < 0.6:  # weekend -> move to weekday
                shift = rng.integers(1, 5)
                dates[i] = d + timedelta(days=int(shift))

        # Travel: bias toward summer and December
        elif cat == "travel":
            month = d.month
            if month not in (6, 7, 8, 12) and rng.random() < 0.6:
                # move to a random summer/Dec month
                target_month = rng.choice([6, 7, 8, 12])
                year = d.year
                target = date(year, int(target_month), rng.integers(1, 28))
                # keep within range
                if target < start:
                    target = start
                if target > end:
                    target = end
                dates[i] = target

        # Bills: approximate monthly on same date - handled separately below

    # Bills: enforce monthly cadence per user later in amount/date generation
    return dates


def _sample_amounts(
    n: int,
    categories: np.ndarray,
    user_multipliers: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    amounts = np.zeros(n, dtype=float)
    for i in range(n):
        cat = categories[i]
        cfg = CATEGORY_CONFIG[cat]
        base = rng.lognormal(
            mean=np.log(cfg["amount_mean"]),
            sigma=cfg["amount_sigma"],
        )
        amt = base * user_multipliers[i]
        amt = float(np.clip(amt, cfg["min"], cfg["max"]))
        amounts[i] = round(amt, 2)
    return amounts


def _generate_bills_for_user(
    user: UserProfile,
    start: date,
    end: date,
    rng: np.random.Generator,
) -> List[Tuple[int, date, float, str]]:
    """Generate monthly 'bills' for a single user."""
    results: List[Tuple[int, date, float, str]] = []
    # Pick a consistent bill day
    bill_day = int(rng.integers(1, 29))

    # Walk months from start to end
    current = date(start.year, start.month, 1)
    while current <= end:
        year = current.year
        month = current.month
        day = min(
            bill_day,
            28,  # keep it simple
        )
        d = date(year, month, day)
        if start <= d <= end:
            cfg = CATEGORY_CONFIG["bills"]
            base = rng.lognormal(
                mean=np.log(cfg["amount_mean"]),
                sigma=cfg["amount_sigma"],
            )
            amt = base * user.spend_multiplier
            amt = float(np.clip(amt, cfg["min"], cfg["max"]))
            results.append(
                (user.user_id, d, round(amt, 2), "bills"),
            )
        # Move to next month
        if month == 12:
            current = date(year + 1, 1, 1)
        else:
            current = date(year, month + 1, 1)

    return results


def generate_transactions(
    num_users: int = 500,
    num_transactions: int = 50_000,
    output_path: str | Path = "../../data/raw/transactions.csv",
    seed: int | None = 42,
) -> int:
    """
    Generate synthetic credit card transactions and save to CSV.

    Returns the total number of rows written.
    """
    rng = np.random.default_rng(seed)

    end_date = date.today()
    start_date = end_date - timedelta(days=365)

    users = _generate_user_profiles(num_users, rng)

    # First, generate bills separately to enforce monthly pattern.
    bill_records: List[Tuple[int, date, float, str]] = []
    for user in users:
        bill_records.extend(_generate_bills_for_user(user, start_date, end_date, rng))

    # Remaining transactions (non-bills)
    remaining = max(num_transactions - len(bill_records), 0)

    user_ids = [u.user_id for u in users]
    # Sample users for remaining txns
    remaining_user_ids = np.array(
        rng.choice(user_ids, size=remaining, replace=True), dtype=int
    )

    categories = _sample_category(remaining, rng)
    # Avoid generating extra 'bills' here; re-normalize probabilities excluding bills
    mask_non_bills = categories != "bills"
    if not np.all(mask_non_bills):
        # replace any "bills" with other categories proportionally
        alt_categories = [c for c in CATEGORY_CONFIG.keys() if c != "bills"]
        alt_probs = np.array(
            [CATEGORY_CONFIG[c]["prob"] for c in alt_categories], dtype=float
        )
        alt_probs /= alt_probs.sum()
        categories[~mask_non_bills] = rng.choice(
            alt_categories, size=(~mask_non_bills).sum(), p=alt_probs
        )

    # Map user_id -> multiplier
    multiplier_map = {u.user_id: u.spend_multiplier for u in users}
    user_multipliers = np.array(
        [multiplier_map[int(uid)] for uid in remaining_user_ids], dtype=float
    )

    dates = _sample_dates(remaining, start_date, end_date, categories, rng)
    amounts = _sample_amounts(remaining, categories, user_multipliers, rng)

    # Build DataFrame for remaining txns
    merchant_names = np.array(
        [
            rng.choice(
                [
                    "Starbucks",
                    "McDonald's",
                    "Whole Foods",
                    "Costco",
                    "Shell",
                    "Amazon",
                    "Netflix",
                    "Uber",
                    "Delta Airlines",
                    "Generic Merchant",
                ]
            )
            for _ in range(remaining)
        ]
    )

    tx_ids_remaining = np.array([str(uuid.uuid4()) for _ in range(remaining)])

    df_remaining = pd.DataFrame(
        {
            "user_id": remaining_user_ids,
            "date": dates,
            "amount": amounts,
            "category": categories,
            "merchant_name": merchant_names,
            "transaction_id": tx_ids_remaining,
        }
    )

    # Build DataFrame for bills
    if bill_records:
        bill_user_ids = [r[0] for r in bill_records]
        bill_dates = [r[1] for r in bill_records]
        bill_amounts = [r[2] for r in bill_records]
        bill_categories = [r[3] for r in bill_records]
        bill_merchants = ["Utility Provider" for _ in bill_records]
        bill_tx_ids = [str(uuid.uuid4()) for _ in bill_records]

        df_bills = pd.DataFrame(
            {
                "user_id": bill_user_ids,
                "date": bill_dates,
                "amount": bill_amounts,
                "category": bill_categories,
                "merchant_name": bill_merchants,
                "transaction_id": bill_tx_ids,
            }
        )

        df = pd.concat([df_remaining, df_bills], ignore_index=True)
    else:
        df = df_remaining

    # Shuffle to mix bills and other txns
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)

    # If we overshot, trim; if under, leave as is (typically close to requested)
    if len(df) > num_transactions:
        df = df.iloc[:num_transactions].copy()

    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    return len(df)


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[2] / "data" / "raw" / "transactions.csv"
    rows = generate_transactions(output_path=out)
    print(f"Generated {rows} rows to {out}")

