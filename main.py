"""Track password expiry from a CSV of users.

CSV columns: username,last_changed,max_age_days
last_changed is YYYY-MM-DD. Usage:
  python3 main.py users.csv [--as-of YYYY-MM-DD] [--warn-days 7]
"""
import argparse
import csv
import sys
from datetime import date, timedelta


def load_users(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_users(rows, as_of, warn_days=7):
    """Return rows sorted by days_left, each with expiry and status."""
    out = []
    for row in rows:
        year, month, day = (int(p) for p in row["last_changed"].split("-"))
        changed = date(year, month, day)
        expiry = changed + timedelta(days=int(row["max_age_days"]))
        days_left = (expiry - as_of).days
        if days_left < 0:
            status = "expired"
        elif days_left <= warn_days:
            status = "expiring-soon"
        else:
            status = "ok"
        out.append({"username": row["username"], "expiry": expiry.isoformat(),
                    "days_left": days_left, "status": status})
    out.sort(key=lambda r: r["days_left"])
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--as-of", default=None,
                        help="Reference date YYYY-MM-DD (default: today)")
    parser.add_argument("--warn-days", type=int, default=7)
    args = parser.parse_args(argv)
    as_of = date.today()
    if args.as_of:
        y, m, d = (int(p) for p in args.as_of.split("-"))
        as_of = date(y, m, d)
    for r in check_users(load_users(args.csv_file), as_of, args.warn_days):
        print(f"{r['username']}: expires {r['expiry']} "
              f"({r['days_left']} days left) [{r['status']}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
