# Bond Yield Calculator

Current yield, yield to maturity (YTM) and Macaulay duration for bonds — plain Python, standard library only.

## What it does

- Reads `bonds.csv` (`name,face,coupon_rate,price,years,coupons_per_year`)
- For each bond prints current yield, YTM (solved by bisection) and Macaulay duration
- Can also price a single bond from a yield: `python bond_yield.py --price-from-yield --face 1000 --coupon-rate 0.05 --years 5 --yield 0.06`

## Usage

```bash
python bond_yield.py
```

## Sample data

`bonds.csv` holds three sample bonds: one at par (YTM = coupon), one at a discount (YTM above coupon) and one at a premium (YTM below coupon).

## Notes

A learning tool, not investment advice. It assumes coupons are paid on schedule with no default risk and no taxes.
