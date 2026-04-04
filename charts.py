import matplotlib.pyplot as plt
from pricing import no_income_forwards, known_income_forwards, known_yield_forwards
from valuation import no_income_forward_valuation, known_income_forward_valuation, known_yield_forward_valuation


# ============================================================
# CHART 1 — Forward Price vs Time to Maturity
# ============================================================

def no_income_ytm(S: float, r: float):
    months = list(range(1, 13))
    noIncome_fwdPrices = []
    for t in months:
        data = no_income_forwards(S, r, t)
        noIncome_fwdPrices.append(data["forward_price"])
    return months, noIncome_fwdPrices


def known_income_ytm(S: float, r: float, I: float, Ir: float, T: int):
    months = list(range(1, 13))
    knownIncome_fwdPrices = []
    for t in months:
        if T <= t:
            data = known_income_forwards(S, r, t, I, Ir, T)
            knownIncome_fwdPrices.append(data["forward_price"])
        else:
            data = no_income_forwards(S, r, t)
            knownIncome_fwdPrices.append(data["forward_price"])
    return months, knownIncome_fwdPrices


def known_yield_ytm(S: float, R: float, y: float):
    months = list(range(1, 13))
    knownYield_fwdPrices = []
    for t in months:
        data = known_yield_forwards(S, R, t, y)
        knownYield_fwdPrices.append(data["forward_price"])
    return months, knownYield_fwdPrices


def no_income_value_chart(K: float, r: float, spot_prices: list, position: str):
    assert len(spot_prices) == 12, "spot_prices must have exactly 12 values (month 0 to 11)"
    months = list(range(12))
    forward_values = []
    for t in months:
        time_remaining = 12 - t
        data = no_income_forward_valuation(K, spot_prices[t], time_remaining, r, position)
        forward_values.append(data["forward_value"])
    return months, forward_values


def known_income_value_chart(K: float, r: float, spot_prices: list, position: str, I: float, Ir: float, T: int):
    assert len(spot_prices) == 12, "spot_prices must have exactly 12 values (month 0 to 11)"
    months = list(range(12))
    forward_values = []
    for t in months:
        time_remaining = 12 - t
        if T > t:
            data = known_income_forward_valuation(K, spot_prices[t], time_remaining, r, position, I, T - t)
        else:
            data = no_income_forward_valuation(K, spot_prices[t], time_remaining, r, position)
        forward_values.append(data["forward_value"])
    return months, forward_values


def known_yield_value_chart(K: float, r: float, spot_prices: list, position: str, y: float):
    assert len(spot_prices) == 12, "spot_prices must have exactly 12 values (month 0 to 11)"
    months = list(range(12))
    forward_values = []
    for t in months:
        time_remaining = 12 - t
        data = known_yield_forward_valuation(K, spot_prices[t], time_remaining, r, position, y)
        forward_values.append(data["forward_value"])
    return months, forward_values


# ============================================================
# CHART FUNCTIONS
# ============================================================

def chart1(S: float, r: float, I: float, Ir: float, T: int, y: float):
    """
    Plots forward price vs time to maturity for all three asset types on one chart.

    Parameters:
        S  (float) : Current spot price of the underlying asset ($)
        r  (float) : Continuously compounded risk-free rate (%)
        I  (float) : Known income paid by the asset ($)
        Ir (float) : Continuously compounded risk-free rate for income discounting (%)
        T  (int)   : Month at which income is paid
        y  (float) : Continuously compounded yield of the asset (%)

    Returns:
        fig : Matplotlib figure object
    """
    months, no_income_prices    = no_income_ytm(S, r)
    _,      known_income_prices = known_income_ytm(S, r, I, Ir, T)
    _,      known_yield_prices  = known_yield_ytm(S, r, y)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(months, no_income_prices,    marker='o', color='steelblue', label='No Income')
    ax.plot(months, known_income_prices, marker='o', color='green',     label='Known Income')
    ax.plot(months, known_yield_prices,  marker='o', color='purple',    label='Known Yield')
    ax.axvline(x=T, linestyle='--', color='red', label=f'Coupon Date (Month {T})')
    ax.set_title(f'Forward Price vs Time to Maturity\nSpot Price: ${S}')
    ax.set_xlabel('Months to Maturity')
    ax.set_ylabel('Forward Price ($)')
    ax.legend()
    plt.tight_layout()

    return fig


def chart2(K: float, r: float, spot_prices: list, position: str, I: float, Ir: float, T: int, y: float):
    """
    Plots spot price path and forward value over the contract life for all three asset types.

    Parameters:
        K           (float) : Agreed delivery price at inception ($)
        r           (float) : Continuously compounded risk-free rate (%)
        spot_prices (list)  : Spot price at each month [S0, S1, ..., S11] (12 values)
        position    (str)   : 'long' or 'short'
        I           (float) : Known income paid by the asset ($)
        Ir          (float) : Continuously compounded risk-free rate for income discounting (%)
        T           (int)   : Month at which income is paid
        y           (float) : Continuously compounded yield of the asset (%)

    Returns:
        fig : Matplotlib figure object
    """
    months, no_income_values    = no_income_value_chart(K, r, spot_prices, position)
    _,      known_income_values = known_income_value_chart(K, r, spot_prices, position, I, Ir, T)
    _,      known_yield_values  = known_yield_value_chart(K, r, spot_prices, position, y)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(months, spot_prices, marker='o', color='steelblue', label='Spot Price')
    ax1.axhline(y=K, linestyle='--', color='gray', label=f'Agreed Price K (${K})')
    ax1.axvline(x=T, linestyle='--', color='red',  label=f'Coupon Date (Month {T})')
    ax1.set_title('Spot Price Path')
    ax1.set_xlabel('Months Elapsed')
    ax1.set_ylabel('Spot Price ($)')
    ax1.legend()

    ax2.plot(months, no_income_values,    marker='o', color='darkorange', label='No Income')
    ax2.plot(months, known_income_values, marker='o', color='green',      label='Known Income')
    ax2.plot(months, known_yield_values,  marker='o', color='purple',     label='Known Yield')
    ax2.axhline(y=0, linestyle='--', color='gray')
    ax2.axvline(x=T, linestyle='--', color='red', label=f'Coupon Date (Month {T})')
    ax2.set_title('Forward Value over Contract Life')
    ax2.set_xlabel('Months Elapsed')
    ax2.set_ylabel('Forward Value ($)')
    ax2.legend()

    plt.tight_layout()

    return fig


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    fig1 = chart1(S=200, r=10, I=40, Ir=3, T=4, y=3.96)
    plt.show()

    spot_prices = [200, 195, 205, 210, 198, 215, 220, 210, 225, 230, 218, 235]
    fig2 = chart2(K=200, r=10, spot_prices=spot_prices, position='long', I=40, Ir=3, T=4, y=3.96)
    plt.show()