import math

e = math.e

def no_income_forward_valuation(K: float, S: float, t: int, r: float, position: str):
    """
    Calculates the forward value of an existing forward contract on an asset
    with no income (e.g. non-dividend paying stock).

    Formula: F_new = S * e^(rT)
             f = (F_new - K) * e^(-rT)    [Long]
             f = (K - F_new) * e^(-rT)    [Short]

    Parameters:
        K        (float) : Agreed delivery price at inception ($)
        S        (float) : Current spot price of the underlying asset ($)
        t        (int)   : Time remaining to maturity (months)
        r        (float) : Continuously compounded risk-free rate (%)
        position (str)   : 'long'  -> Agreement to buy the underlying
                           'short' -> Agreement to sell the underlying

    Returns:
        dict : {
            "spot_price"    : S,
            "rate"          : r,
            "maturity"      : t,
            "agreed_price"  : K,
            "position"      : position,
            "forward_price" : F_new,
            "forward_value" : f
        }

    Example:
        >>> no_income_forward_valuation(100, 100, 12, 4, 'long')
    """
    r_decimal = r / 100

    F_new = S * (e**(r_decimal*(t/12)))
    forwardValue = (F_new - K) * (e**(-r_decimal*(t/12)))

    if position == 'Short':
        forwardValue = (-forwardValue)

    return {
        "spot_price"    : S,
        "rate"          : r,
        "maturity"      : t,
        "agreed_price"  : K,
        "position"      : position,
        "forward_price" : round(F_new, 3),
        "forward_value" : round(forwardValue, 3)
    }


def known_income_forward_valuation(K: float, S: float, t: int, r: float, position: str, income: float, income_time: int):
    """
    Calculates the forward value of an existing forward contract on an asset
    that pays a known cash income during the remaining life of the contract
    (e.g. a coupon-paying bond).

    Formula: PV(I) = I * e^(-r * income_time)
             F_new = (S - PV(I)) * e^(rT)
             f = (F_new - K) * e^(-rT)    [Long]
             f = (K - F_new) * e^(-rT)    [Short]

    Parameters:
        K           (float) : Agreed delivery price at inception ($)
        S           (float) : Current spot price of the underlying asset ($)
        t           (int)   : Time remaining to maturity (months)
        r           (float) : Continuously compounded risk-free rate (%)
        position    (str)   : 'long'  -> Agreement to buy the underlying
                              'short' -> Agreement to sell the underlying
        income      (float) : Known income to be paid by the asset ($)
        income_time (int)   : Time until income is paid (months)

    Returns:
        dict : {
            "spot_price"    : S,
            "rate"          : r,
            "maturity"      : t,
            "agreed_price"  : K,
            "position"      : position,
            "income"        : income,
            "income_time"   : income_time,
            "pv_income"     : PV(I),
            "forward_price" : F_new,
            "forward_value" : f
        }

    Example:
        >>> known_income_forward_valuation(900, 900, 9, 4, 'long', 40, 4)
    """
    r_decimal = r / 100

    PV = income * (e**(-r_decimal*(income_time/12)))
    F_new = (S - PV) * (e**(r_decimal*(t/12)))
    forwardValue = (F_new - K) * (e**(-r_decimal*(t/12)))

    if position == 'Short':
        forwardValue *= -1

    return {
        "spot_price"    : S,
        "rate"          : r,
        "maturity"      : t,
        "agreed_price"  : K,
        "position"      : position,
        "income"        : income,
        "income_time"   : income_time,
        "pv_income"     : round(PV, 3),
        "forward_price" : round(F_new, 3),
        "forward_value" : round(forwardValue, 3)
    }


def known_yield_forward_valuation(K: float, S: float, t: int, r: float, position: str, y: float):
    """
    Calculates the forward value of an existing forward contract on an asset
    with a known continuous yield (e.g. stock index or foreign currency).

    Formula: F_new = S * e^((r - y) * T)
             f = (F_new - K) * e^(-rT)    [Long]
             f = (K - F_new) * e^(-rT)    [Short]

    Parameters:
        K        (float) : Agreed delivery price at inception ($)
        S        (float) : Current spot price of the underlying asset ($)
        t        (int)   : Time remaining to maturity (months)
        r        (float) : Continuously compounded risk-free rate (%)
        position (str)   : 'long'  -> Agreement to buy the underlying
                           'short' -> Agreement to sell the underlying
        y        (float) : Continuously compounded yield of the asset (%)

    Returns:
        dict : {
            "spot_price"    : S,
            "rate"          : r,
            "maturity"      : t,
            "agreed_price"  : K,
            "position"      : position,
            "yield"         : y,
            "forward_price" : F_new,
            "forward_value" : f
        }

    Example:
        >>> known_yield_forward_valuation(25, 25, 6, 10, 'long', 3.96)
    """
    r_decimal = r / 100
    y_decimal = y / 100

    F_new = S * (e**((r_decimal - y_decimal)*(t/12)))
    forwardValue = (F_new - K) * (e**(-r_decimal*(t/12)))

    if position == 'Short':
        forwardValue = (-1)(forwardValue)

    return {
        "spot_price"    : S,
        "rate"          : r,
        "maturity"      : t,
        "agreed_price"  : K,
        "position"      : position,
        "yield"         : y,
        "forward_price" : round(F_new, 3),
        "forward_value" : round(forwardValue, 3)
    }


if __name__ == "__main__":
    print("\n" + "="*50)
    print("No Income Forward Valuation")
    print("="*50)
    print(no_income_forward_valuation(100, 100, 12, 4, 'short'))

    print("\n" + "="*50)
    print("Known Income Forward Valuation")
    print("="*50)
    print(known_income_forward_valuation(900, 900, 9, 4, 'short', 40, 4))

    print("\n" + "="*50)
    print("Known Yield Forward Valuation")
    print("="*50)
    print(known_yield_forward_valuation(25, 25, 6, 10, 'long', 3.96))