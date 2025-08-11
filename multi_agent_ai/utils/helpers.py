# small helpers (e.g., normalize currency, parse simple CSV rows)
import re

def normalize_transactions(rows):
    # rows: list[str] like "Uber - 3500"
    out = []
    for r in rows:
        # try to find amount
        m = re.search(r"([\d,.]+)", r)
        amt = m.group(1) if m else "0"
        out.append(f"{r} - {amt}")
    return out