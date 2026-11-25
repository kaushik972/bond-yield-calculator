"""Bond yield calculator.

For each bond in bonds.csv (name,face,coupon_rate,price,years,coupons_per_year)
prints current yield, yield to maturity (solved by bisection) and
Macaulay duration. A single bond can also be priced from a yield.

Usage:
    python bond_yield.py
    python bond_yield.py --price-from-yield --face 1000 --coupon-rate 0.05 --years 5 --yield 0.06
"""
import argparse
import csv


def price_from_yield(face, coupon_rate, years, ytm, per_year=1):
    coupon = face * coupon_rate / per_year
    n = int(years * per_year)
    r = ytm / per_year
    pv = sum(coupon / (1 + r) ** t for t in range(1, n + 1))
    return pv + face / (1 + r) ** n


def ytm(face, coupon_rate, price, years, per_year=1):
    lo, hi = -0.9, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if price_from_yield(face, coupon_rate, years, mid, per_year) > price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def duration(face, coupon_rate, years, ytm_value, per_year=1):
    coupon = face * coupon_rate / per_year
    n = int(years * per_year)
    r = ytm_value / per_year
    price = price_from_yield(face, coupon_rate, years, ytm_value, per_year)
    weighted = 0.0
    for t in range(1, n + 1):
        cf = coupon + (face if t == n else 0)
        weighted += (t / per_year) * cf / (1 + r) ** t
    return weighted / price


def main():
    p = argparse.ArgumentParser(description="Bond yield calculator")
    p.add_argument("--file", default="bonds.csv")
    p.add_argument("--price-from-yield", action="store_true",
                   help="Price one bond from a yield instead of reading the CSV")
    p.add_argument("--face", type=float, default=1000.0)
    p.add_argument("--coupon-rate", type=float, default=0.05)
    p.add_argument("--years", type=float, default=5.0)
    p.add_argument("--yield", dest="yield_", type=float, default=0.06)
    a = p.parse_args()
    if a.price_from_yield:
        price = price_from_yield(a.face, a.coupon_rate, a.years, a.yield_)
        print(f"Price at {a.yield_:.2%} yield: {price:,.2f}")
        return
    with open(a.file, newline="") as f:
        for row in csv.DictReader(f):
            face = float(row["face"])
            coupon_rate = float(row["coupon_rate"])
            price = float(row["price"])
            years = float(row["years"])
            per_year = int(row.get("coupons_per_year") or 1)
            y = ytm(face, coupon_rate, price, years, per_year)
            current = face * coupon_rate / price
            dur = duration(face, coupon_rate, years, y, per_year)
            print(f"{row['name']}: price {price:,.2f}, coupon {coupon_rate:.1%}")
            print(f"  Current yield: {current:.2%} | YTM: {y:.2%} | "
                  f"Macaulay duration: {dur:.2f} yrs")


if __name__ == "__main__":
    main()
