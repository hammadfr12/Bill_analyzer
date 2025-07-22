import re, datetime as dt
from backend.models import Receipt

# ────────────────────────────────────────────────
# Patterns
# ────────────────────────────────────────────────
DATE_RE = re.compile(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b")

# Lines we trust for the grand total
TOTAL_RE = re.compile(r"(?i)(grand\s+)?total|amount\s+due")

# Allow spaces inside the number group (e.g. "2 360.00")
DIGIT_RE = re.compile(
    r"[₹€$£¥]?\s*\d[\d,\s]*\.?\d{0,2}"
    r"|Rs\.?\s*\d[\d,\s]*\.?\d{0,2}"
)

# Fallback: any symbol-prefixed amount
SYM_FALLBACK = re.compile(r"[₹€$£¥]\s?\d[\d,]*\.?\d{0,2}")

VENDOR_RE = re.compile(
    r"(?i)(invoice|from|vendor|store|college|school|organisation?|supplier|sold by)[:\s]+([A-Za-z0-9 &]{3,})"
)

EXCLUDE = ("SUB", "GST", "%", "TAX")

# ────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────
def parse_date(text: str) -> dt.date:
    if (m := DATE_RE.search(text)):
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"):
            try:
                return dt.datetime.strptime(m.group(1), fmt).date()
            except ValueError:
                continue
    return dt.date.today()


def guess_vendor(lines: list[str]) -> str:
    if (m := VENDOR_RE.search(" ".join(lines))):
        return m.group(2).strip()
    for ln in lines[:8]:
        if ln.isupper() and len(ln) > 3 and "TOTAL" not in ln:
            return ln.title()
    return "Unknown"


def extract_amount(lines: list[str]) -> str:
    # Scan from bottom-up for TOTAL / AMOUNT DUE lines without GST / SUB tokens
    for ln in reversed(lines):
        up = ln.upper()
        if TOTAL_RE.search(up) and not any(w in up for w in EXCLUDE):
            # take the right-most numeric token on that line
            matches = DIGIT_RE.findall(ln)
            if matches:
                return matches[-1].strip()
    # Fallback to last symbol-prefixed amount anywhere
    joined = " ".join(lines)
    sym_hits = SYM_FALLBACK.findall(joined)
    return sym_hits[-1].strip() if sym_hits else "0"

# ────────────────────────────────────────────────
# Main entry
# ────────────────────────────────────────────────
def parse(text: str) -> Receipt:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    vendor     = guess_vendor(lines)
    bill_date  = parse_date(" ".join(lines))
    amount_raw = extract_amount(lines)

    return Receipt(vendor=vendor, bill_date=bill_date, amount_raw=amount_raw)
