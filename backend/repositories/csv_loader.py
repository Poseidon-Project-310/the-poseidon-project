# backend/repositories/csv_loader.py
from __future__ import annotations
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Callable

# Constants
EXPECTED_COLUMNS = [
    "order_id", "restaurant_id", "food_item", "order_time", "delivery_time",
    "delivery_distance", "order_value", "delivery_method", "traffic_condition",
    "weather_condition", "delivery_time_actual", "delivery_delay", "route_taken",
    "customer_id", "age", "gender", "location", "order_history", "customer_rating",
    "preferred_cuisine", "order_frequency", "loyalty_program", "food_temperature",
    "food_freshness", "packaging_quality", "food_condition", "customer_satisfaction",
    "small_route", "bike_friendly_route", "route_type", "route_efficiency",
    "predicted_delivery_mode", "traffic_avoidance",
]


def get_default_path() -> Path:
    """
    Returns the absolute path to the data file
    """
    return Path(__file__).parent.parent / "data" / "food_delivery.csv"


def _parse_bool(value: Any) -> Optional[bool]:
    # Parses through
    s = str(value).strip().lower()
    if s in {"true", "t", "1", "yes", "y"}: return True
    if s in {"false", "f", "0", "no", "n"}: return False
    return None


def _to_int(value: Any) -> Optional[int]:
    # Translates to int
    try: return int(str(value).strip())
    except (ValueError, TypeError): return None


def _to_float(value: Any) -> Optional[float]:
    # Translates to float
    try: return float(str(value).strip())
    except (ValueError, TypeError): return None


def _is_not_blank(value: Any) -> Optional[str]:
    # Checks if blank
    s = str(value).strip()
    return s if s else None

# --- Core Functions ---

def load_csv(path: Optional[str | Path] = None) -> List[Dict[str, Any]]:
    """
    Loads CSV and returns rows as list of dicts.
    """
    csv_path = Path(path or get_default_path())
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def validate_csv(
    path: Optional[str | Path] = None,
    expected_cols: List[str] = EXPECTED_COLUMNS,
    limit: int = 50
) -> Tuple[bool, List[str]]:
    """
    Validates structure and data
    """
    csv_path = Path(path or get_default_path())
    errors: List[str] = []

    if not csv_path.exists():
        return False, [f"File missing: {csv_path}"]

    # Define validation rules
    rules: Dict[str, Callable] = {
        "customer_id": _is_not_blank,
        "restaurant_id": _to_int,
        "age": _to_int,
        "delivery_distance": _to_float,
        "order_value": _to_float,
        "route_efficiency": _to_float,
        "small_route": _parse_bool,
        "bike_friendly_route": _parse_bool,
    }

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        # Checks header
        if not reader.fieldnames:
            return False, ["CSV has no header"]
        if list(reader.fieldnames) != expected_cols:
            errors.append("Header mismatch: columns out of order or missing")

        # Checks row values
        row_count = 0
        for row in reader:
            row_count += 1
            if row_count > limit:
                break

            for col, validator in rules.items():
                if validator(row.get(col)) is None:
                    errors.append(f"Invalid {col} at row {row_count}: '{row.get(col)}'")
                    return False, errors # Fail fast on data issues

        if row_count == 0:
            errors.append("CSV is empty (no data rows)")

    return len(errors) == 0, errors
