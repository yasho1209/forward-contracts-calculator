import matplotlib.pyplot as plt
from pricing import no_income_forwards, known_income_forwards, known_yield_forwards
from valuation import no_income_forward_valuation, known_income_forward_valuation, known_yield_forward_valuation


# ============================================================
# CHART 1 — Forward Price vs Time to Maturity
# ============================================================

def no_income_ytm(S: float, r: float):
    """
    Returns forward prices of a no-income asset across 1-12 months to maturity.

    Parameters:
        S (float) : Current spot price of the underlying asset ($)
        r (float) : Continuously compounded risk-free rate (%)

    Returns:
        months (list)             : [1, 2, ..., 12]
        noIncome_fwdPrices (list) : Forward price for each month
    """
    months = list(range(1, 13))
    noIncome_fwdPrices = []

    for t in months:
        data = no_income_forwards(S, r, t)
        noIncome_fwdPrices.append(data["forward_price"])

    return months, noIncome_fwdPrices


def known_income_ytm(S: float, r: float, I: float, Ir: float, T: int):
    """
    Returns forward prices of a known income asset across 1-12 months to maturity.

    Parameters:
        S  (float) : Current spot price of the underlying asset ($)
        r  (float) : Continuously compounded risk-free rate (%)
        I  (float) : Known income paid by the asset ($)
        Ir (float) : Continuously compounded risk-free rate for income time (%)
        T  (int)   : Month at which income is paid

    Returns:
        months (list)                : [1, 2, ..., 12]
        knownIncome_fwdPrices (list) : Forward price for each month
    """
    months = list(range(1, 13))
    knownIncome_fwdPrices = []

    for t in months:
        if T <= t:  # income arrives before forward matures
            data = known_income_forwards(S, r, t, I, Ir, T)
            knownIncome_fwdPrices.append(data["forward_price"])
        else:       # income arrives after forward matures, income irrelevant
            data = no_income_forwards(S, r, t)
            knownIncome_fwdPrices.append(data["forward_price"])

    return months, knownIncome_fwdPrices


def known_yield_ytm(S: float, R: float, y: float):
    """
    Returns forward prices of a known yield asset across 1-12 months to maturity.

    Parameters:
        S (float) : Current spot price of the underlying asset ($)
        R (float) : Continuously compounded risk-free rate (%)
        y (float) : Continuously compounded yield of the asset (%)

    Returns:
        months (list)               : [1, 2, ..., 12]
        knownYield_fwdPrices (list) : Forward price for each month
    """
    months = list(range(1, 13))
    knownYield_fwdPrices = []

    for t in months:
        data = known_yield_forwards(S, R, t, y)
        knownYield_fwdPrices.append(data["forward_price"])

    return months, knownYield_fwdPrices


# ============================================================
# CHART 2 — Forward Value over Contract Life
# ============================================================

def no_income_value_chart(K: float, r: float, spot_prices: list, position: str):
    """
    Returns forward values of a no-income forward contract across its 12 month life,
    given a user-provided spot price path.

    Parameters:
        K           (float) : Agreed delivery price at inception ($)
        r           (float) : Continuously compounded risk-free rate (%)
        spot_prices (list)  : Spot price at each month [S0, S1, ..., S11] (12 values)
        position    (str)   : 'long' or 'short'

    Returns:
        months (list)         : [0, 1, ..., 11]
        forward_values (list) : Forward value f at each month
    """
    assert len(spot_prices) == 12, "spot_prices must have exactly 12 values (month 0 to 11)"

    months = list(range(12))
    forward_values = []

    for t in months:
        time_remaining = 12 - t
        data = no_income_forward_valuation(K, spot_prices[t], time_remaining, r, position)
        forward_values.append(data["forward_value"])

    return months, forward_values


def known_income_value_chart(K: float, r: float, spot_prices: list, position: str, I: float, Ir: float, T: int):
    """
    Returns forward values of a known income forward contract across its 12 month life,
    given a user-provided spot price path.

    Parameters:
        K           (float) : Agreed delivery price at inception ($)
        r           (float) : Continuously compounded risk-free rate (%)
        spot_prices (list)  : Spot price at each month [S0, S1, ..., S11] (12 values)
        position    (str)   : 'long' or 'short'
        I           (float) : Known income paid by the asset ($)
        Ir          (float) : Continuously compounded risk-free rate for income time (%)
        T           (int)   : Month at which income is paid

    Returns:
        months (list)         : [0, 1, ..., 11]
        forward_values (list) : Forward value f at each month
    """
    assert len(spot_prices) == 12, "spot_prices must have exactly 12 values (month 0 to 11)"

    months = list(range(12))
    forward_values = []

    for t in months:
        time_remaining = 12 - t
        if T > t:   # income still pending
            data = known_income_forward_valuation(K, spot_prices[t], time_remaining, r, position, I, T - t)
        else:       # income already paid, treat as no income
            data = no_income_forward_valuation(K, spot_prices[t], time_remaining, r, position)
        forward_values.append(data["forward_value"])

    return months, forward_values


def known_yield_value_chart(K: float, r: float, spot_prices: list, position: str, y: float):
    """
    Returns forward values of a known yield forward contract across its 12 month life,
    given a user-provided spot price path.

    Parameters:
        K           (float) : Agreed delivery price at inception ($)
        r           (float) : Continuously compounded risk-free rate (%)
        spot_prices (list)  : Spot price at each month [S0, S1, ..., S11] (12 values)
        position    (str)   : 'long' or 'short'
        y           (float) : Continuously compounded yield of the asset (%)

    Returns:
        months (list)         : [0, 1, ..., 11]
        forward_values (list) : Forward value f at each month
    """
    assert len(spot_prices) == 12, "spot_prices must have exactly 12 values (month 0 to 11)"

    months = list(range(12))
    forward_values = []

    for t in months:
        time_remaining = 12 - t
        data = known_yield_forward_valuation(K, spot_prices[t], time_remaining, r, position, y)
        forward_values.append(data["forward_value"])

    return months, forward_values


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # --- Chart 1 ---
    months, no_income_prices    = no_income_ytm(200, 10)
    _,      known_income_prices = known_income_ytm(200, 10, 40, 3, 4)
    _,      known_yield_prices  = known_yield_ytm(200, 10, 3.96)

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(months, no_income_prices,    marker='o', color='steelblue',  label='No Income')
    ax1.plot(months, known_income_prices, marker='o', color='green',      label='Known Income')
    ax1.plot(months, known_yield_prices,  marker='o', color='purple',     label='Known Yield')
    ax1.axvline(x=4, linestyle='--', color='red', label='Coupon Date')
    ax1.set_title('Forward Price vs Time to Maturity\nSpot Price: $200')
    ax1.set_xlabel('Months to Maturity')
    ax1.set_ylabel('Forward Price ($)')
    ax1.legend()
    plt.tight_layout()
    plt.show()

    # --- Chart 2 ---
    spot_prices = [200, 195, 205, 210, 198, 215, 220, 210, 225, 230, 218, 235]

    months2, no_income_values    = no_income_value_chart(200, 10, spot_prices, 'long')
    _,       known_income_values = known_income_value_chart(200, 10, spot_prices, 'long', 40, 3, 4)
    _,       known_yield_values  = known_yield_value_chart(200, 10, spot_prices, 'long', 3.96)

    fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(10, 8))

    ax2.plot(months2, spot_prices, marker='o', color='steelblue', label='Spot Price')
    ax2.axhline(y=200, linestyle='--', color='gray', label='Agreed Price K')
    ax2.axvline(x=4,   linestyle='--', color='red',  label='Coupon Date')
    ax2.set_title('Spot Price Path')
    ax2.set_xlabel('Months Elapsed')
    ax2.set_ylabel('Spot Price ($)')
    ax2.legend()

    ax3.plot(months2, no_income_values,    marker='o', color='darkorange', label='No Income')
    ax3.plot(months2, known_income_values, marker='o', color='green',      label='Known Income')
    ax3.plot(months2, known_yield_values,  marker='o', color='purple',     label='Known Yield')
    ax3.axhline(y=0, linestyle='--', color='gray')
    ax3.axvline(x=4, linestyle='--', color='red', label='Coupon Date')
    ax3.set_title('Forward Value over Contract Life')
    ax3.set_xlabel('Months Elapsed')
    ax3.set_ylabel('Forward Value ($)')
    ax3.legend()

    plt.tight_layout()
    plt.show()