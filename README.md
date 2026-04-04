# Forward Contracts Calculator 📈

A Python + Streamlit app for pricing and valuing forward contracts, built from scratch following **Hull — Options, Futures & Other Derivatives (Chapter 5)**.

## Features

- **Forward Pricing** — Calculate F₀ for three asset types using continuous compounding
- **Forward Valuation** — Value an existing forward contract at any point in its life
- **Visualisations** — Interactive charts showing forward price vs maturity and forward value drift over time

## Contract Types Supported

| Type | Example Assets | Formula |
|---|---|---|
| No Income | Non-dividend paying stocks | `F₀ = S·e^(rT)` |
| Known Income | Coupon-paying bonds | `F₀ = (S - PV(I))·e^(rT)` |
| Known Yield | Stock indices, FX | `F₀ = S·e^((r-y)T)` |

## Project Structure
forward-contracts-calculator/
├── app.py          # Streamlit pricing page
├── pricing.py      # Forward price calculations
├── valuation.py    # Forward value calculations
├── charts.py       # Matplotlib visualisations
└── pages/
├── valuation.py   # Streamlit valuation page
└── charts.py      # Streamlit charts page

## Installation
```bash
git clone https://github.com/yasho1209/forward-contracts-calculator.git
cd forward-contracts-calculator
pip install streamlit matplotlib pandas
streamlit run app.py
```

## Pages
**Page 1 — Forward Price Calculator**
Input spot price, risk-free rate, and maturity to get the forward price with full step-by-step workings.
**Page 2 — Forward Valuation**
Input an existing contract's agreed price K, current spot, and time remaining to get the current forward value and P&L status.
**Page 3 — Charts**
Visualise how forward price grows with maturity across all three asset types, and how forward value drifts over the contract life given a custom spot price path.

## Reference
Hull, J.C. (2022). *Options, Futures, and Other Derivatives* (11th ed.). Pearson. Chapter 5.