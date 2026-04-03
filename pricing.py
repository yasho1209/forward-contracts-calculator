""" Pricing of forwards - 
1. No Income forwards
2. Known Income forwards
3. Known Yield forwards
"""

import math
e = math.e

def no_income_forwards(S, r, T):
    """ 
    Calculates the forward price for an asset with no income (e.g. non-dividend paying stock).
    
    Formula: F0 = S * e^(rT)
    
    Parameters:
        S (float) : Current spot price of the underlying asset ($)
        r (float) : Continuously compounded risk-free rate for maturity T (%)
        T (int)   : Time to maturity of the forward contract (months)
    
    Returns:
        dict : {
            "spot_price"    : S,
            "rate"          : r,
            "maturity"      : T,
            "forward_price" : F0
        }
    
    Example:
        >>> no_income_forwards(100, 4, 12)
    """
    r = r / 100 

    forwardPrice = round((S) * (e**(r*(T/12))), 3)

    return {
        "spot_price"    : S,
        "rate"          : r,
        "maturity"      : T,
        "forward_price" : forwardPrice
    }


def known_income_forwards(S, R, T, I, r, t):
    """
    Calculates the forward price for an asset that pays a known cash income
    during the life of the contract (e.g. a coupon-paying bond).

    Formula: F0 = (S - PV(I)) * e^(RT)
             where PV(I) = I * e^(-rt)

    Parameters:
        S (float) : Current spot price of the underlying asset ($)
        R (float) : Continuously compounded risk-free rate for maturity T (%)
        T (int)   : Time to maturity of the forward contract (months)
        I (float) : Known income paid by the asset during the contract life ($)
        r (float) : Continuously compounded risk-free rate for time t (%)
        t (int)   : Time at which the income is paid (months)

    Returns:
        dict : {
            "spot_price"    : S,
            "rate"          : R,
            "maturity"      : T,
            "income"        : I,
            "income_rate"   : r,
            "income_time"   : t,
            "pv_income"     : PV(I),
            "forward_price" : F0
        }

    Example:
        >>> known_income_forwards(900, 4, 9, 40, 3, 4)
    """
    R = R / 100 
    r = r / 100

    PV = round(I * (e ** (-r*(t/12))), 3)
    forwardPrice = round((S - PV) * (e**(R*(T/12))), 3)

    return {
        "spot_price"    : S,
        "rate"          : R,
        "maturity"      : T,
        "income"        : I,
        "income_rate"   : r,
        "income_time"   : t,
        "forward_price" : forwardPrice
    }


def known_yield_forwards(S, R, T, y):
    """
    Calculates the forward price for an asset with a known continuous yield
    (e.g. a stock index or foreign currency).

    Formula: F0 = S * e^((R - y) * T)

    Parameters:
        S (float) : Current spot price of the underlying asset ($)
        R (float) : Continuously compounded risk-free rate for maturity T (%)
        T (int)   : Time to maturity of the forward contract (months)
        y (float) : Continuously compounded yield of the asset (%)

    Returns:
        dict : {
            "spot_price"    : S,
            "rate"          : R,
            "maturity"      : T,
            "yield"         : y,
            "forward_price" : F0
        }

    Example:
        >>> known_yield_forwards(25, 10, 6, 3.96)
    """
    R = R / 100 
    y = y / 100

    forwardPrice = round((S) * (e**((R-y)*(T/12))), 3)

    return {
        "spot_price"    : S,
        "rate"          : R,
        "maturity"      : T,
        "yield"         : round(y, 3),
        "forward_price" : forwardPrice
    }

if __name__ == "__main__":
    print("\n" + "="*50)
    print("No Income Forwards")
    print("="*50)
    print(no_income_forwards(100, 4, 12))

    print("\n" + "="*50)
    print("Known Income Forwards")
    print("="*50)
    print(known_income_forwards(900, 4, 9, 40, 3, 4))

    print("\n" + "="*50)
    print("Known Yield Forwards")
    print("="*50)
    print(known_yield_forwards(25, 10, 6, 3.96))