import re

_SYMBOL_LOOKUP = {
    "₹": "INR", "$": "USD", "€": "EUR", "£": "GBP",
    "¥": "JPY", "฿": "THB", "RS": "INR"          # handles Rs / Rs.
}

# -----------------------------------------------------------------
# detect_currency
# -----------------------------------------------------------------
def detect_currency(raw: str, default: str = "INR") -> tuple[str, float]:
    """
    Extract `(currency_code, amount)` from `raw`.
    • Supports symbols (₹€$£¥฿) OR keywords  Rs / Rs.
    • If no symbol/keyword, assumes `default` (INR) and still parses number.
    """
    txt = raw.upper().replace("RS.", "RS").replace("RS ", "RS")
    # Try explicit symbol or RS
    sym_match = re.search(r"(₹|€|\$|£|¥|฿|RS)", txt)
    code      = _SYMBOL_LOOKUP.get(sym_match.group(1), default) if sym_match else default

    # Remove everything except digits, dot, comma, then convert
    num_str = re.sub(r"[^\d.,]", "", txt)
    num_str = num_str.replace(",", "")            # ditch thousand‐separators
    amount  = float(num_str) if num_str else 0.0

    return code, amount


# Optional live converter (not used for storage)
from forex_python.converter import CurrencyRates
cr = CurrencyRates()

def convert(amount: float, src: str, tgt: str = "USD") -> float:
    if src == tgt:
        return amount
    try:
        return round(amount * cr.get_rate(src, tgt), 2)
    except Exception:
        return amount
