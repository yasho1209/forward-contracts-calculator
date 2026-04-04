import streamlit as st
from valuation import no_income_forward_valuation, known_income_forward_valuation, known_yield_forward_valuation

st.set_page_config(
    page_title="Forward Valuation",
    page_icon="📉",
    layout="wide"
)

st.title("📉 Forward Valuation")
st.divider()

st.sidebar.header("⚙️ Contract Settings")
st.sidebar.caption("Select your contract type and fill in the parameters.")

contract_type = st.sidebar.selectbox(
    "Contract Type",
    ["No Income", "Known Income", "Known Yield"],
    help="No Income: non-dividend paying stock | Known Income: coupon bond | Known Yield: stock index or FX"
)

st.sidebar.divider()
st.sidebar.markdown("""
**Contract Types:**
- **No Income** — Non-dividend paying stocks
- **Known Income** — Coupon-paying bonds
- **Known Yield** — Stock indices, foreign currencies
""")


# ============================================================
# NO INCOME
# ============================================================

if contract_type == "No Income":
    """
    Forward valuation for assets with no income (e.g. non-dividend paying stocks).
    """
    st.subheader("🔹 No Income Forward Valuation")
    st.latex(r"f = (F_{new} - K) \cdot e^{-rT}, \quad F_{new} = S \cdot e^{rT}")
    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        spot_price     = st.number_input("Spot Price ($)",             min_value=0.0, step=1.0, help="Current market price of the underlying asset")
    with col2:
        strike_price   = st.number_input("Agreed Price K ($)",         min_value=0.0, step=1.0, help="Delivery price agreed at inception of the contract")
    with col3:
        risk_free_rate = st.number_input("Risk-Free Rate (%)",         min_value=0.0, step=0.1, help="Continuously compounded annual risk-free rate")
    with col4:
        time           = st.number_input("Time Remaining (months)",    min_value=1,   step=1,   help="Time remaining until contract maturity")
    with col5:
        position       = st.selectbox("Position", ["Long", "Short"], help="Long = agreed to buy | Short = agreed to sell")

    st.divider()
    clicked = st.button("Calculate Forward Value", type="primary")

    if clicked:
        data = no_income_forward_valuation(strike_price, spot_price, time, risk_free_rate, position)

        st.subheader("📊 Results")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Spot Price",      f"${data['spot_price']}")
        col2.metric("Agreed Price K",  f"${data['agreed_price']}")
        col3.metric("New Fwd Price",   f"${data['forward_price']}")
        col4.metric("Position",        data['position'].capitalize())
        col5.metric("Forward Value",   f"${data['forward_value']}")

        st.divider()
        st.subheader("🔢 Step-by-Step")
        st.latex(rf"F_{{new}} = {data['spot_price']} \times e^{{({data['rate']}/100) \times ({data['maturity']}/12)}}")
        st.latex(rf"F_{{new}} = \${data['forward_price']}")
        st.latex(rf"f = ({data['forward_price']} - {data['agreed_price']}) \times e^{{-({data['rate']}/100) \times ({data['maturity']}/12)}}")
        st.latex(rf"f = \${data['forward_value']}")

        if data['forward_value'] > 0:
            st.success(f"✅ In Profit — Forward Value: **${data['forward_value']}**")
        else:
            st.error(f"❌ At a Loss — Forward Value: **${data['forward_value']}**")


# ============================================================
# KNOWN INCOME
# ============================================================

elif contract_type == "Known Income":
    """
    Forward valuation for assets that pay a known cash income (e.g. coupon-paying bonds).
    """
    st.subheader("🔹 Known Income Forward Valuation")
    st.latex(r"f = (F_{new} - K) \cdot e^{-rT}, \quad F_{new} = (S - PV(I)) \cdot e^{rT}, \quad PV(I) = I \cdot e^{-rt}")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        spot_price     = st.number_input("Spot Price ($)",             min_value=0.0, step=1.0, help="Current market price of the underlying asset")
        strike_price   = st.number_input("Agreed Price K ($)",         min_value=0.0, step=1.0, help="Delivery price agreed at inception of the contract")
    with col2:
        risk_free_rate = st.number_input("Risk-Free Rate (%)",         min_value=0.0, step=0.1, help="Continuously compounded annual risk-free rate")
        time           = st.number_input("Time Remaining (months)",    min_value=1,   step=1,   help="Time remaining until contract maturity")
        position       = st.selectbox("Position", ["Long", "Short"],                            help="Long = agreed to buy | Short = agreed to sell")
    with col3:
        income         = st.number_input("Income ($)",                 min_value=0.0, step=1.0, help="Known cash income still to be paid by the asset")
        income_time    = st.number_input("Income Payment Month",       min_value=1,   step=1,   help="Months remaining until income is paid")

    st.divider()
    clicked = st.button("Calculate Forward Value", type="primary")

    if clicked:
        data = known_income_forward_valuation(strike_price, spot_price, time, risk_free_rate, position, income, income_time)

        st.subheader("📊 Results")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Spot Price",      f"${data['spot_price']}")
        col2.metric("Agreed Price K",  f"${data['agreed_price']}")
        col3.metric("PV of Income",    f"${data['pv_income']}")
        col4.metric("New Fwd Price",   f"${data['forward_price']}")
        col5.metric("Position",        data['position'].capitalize())
        col6.metric("Forward Value",   f"${data['forward_value']}")

        st.divider()
        st.subheader("🔢 Step-by-Step")
        st.latex(rf"PV(I) = {data['income']} \times e^{{-({data['rate']}/100) \times ({data['income_time']}/12)}}")
        st.latex(rf"PV(I) = \${data['pv_income']}")
        st.latex(rf"F_{{new}} = ({data['spot_price']} - {data['pv_income']}) \times e^{{({data['rate']}/100) \times ({data['maturity']}/12)}}")
        st.latex(rf"F_{{new}} = \${data['forward_price']}")
        st.latex(rf"f = ({data['forward_price']} - {data['agreed_price']}) \times e^{{-({data['rate']}/100) \times ({data['maturity']}/12)}}")
        st.latex(rf"f = \${data['forward_value']}")

        if data['forward_value'] > 0:
            st.success(f"✅ In Profit — Forward Value: **${data['forward_value']}**")
        else:
            st.error(f"❌ At a Loss — Forward Value: **${data['forward_value']}**")


# ============================================================
# KNOWN YIELD
# ============================================================

elif contract_type == "Known Yield":
    """
    Forward valuation for assets with a known continuous yield (e.g. stock indices, foreign currencies).
    """
    st.subheader("🔹 Known Yield Forward Valuation")
    st.latex(r"f = (F_{new} - K) \cdot e^{-rT}, \quad F_{new} = S \cdot e^{(r-y)T}")
    st.divider()

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        spot_price     = st.number_input("Spot Price ($)",             min_value=0.0, step=1.0, help="Current market price of the underlying asset")
    with col2:
        strike_price   = st.number_input("Agreed Price K ($)",         min_value=0.0, step=1.0, help="Delivery price agreed at inception of the contract")
    with col3:
        risk_free_rate = st.number_input("Risk-Free Rate (%)",         min_value=0.0, step=0.1, help="Continuously compounded annual risk-free rate")
    with col4:
        time           = st.number_input("Time Remaining (months)",    min_value=1,   step=1,   help="Time remaining until contract maturity")
    with col5:
        yield_rate     = st.number_input("Yield (%)",                  min_value=0.0, step=0.1, help="Continuously compounded yield of the asset")
    with col6:
        position       = st.selectbox("Position", ["Long", "Short"],                            help="Long = agreed to buy | Short = agreed to sell")

    st.divider()
    clicked = st.button("Calculate Forward Value", type="primary")

    if clicked:
        data = known_yield_forward_valuation(strike_price, spot_price, time, risk_free_rate, position, yield_rate)

        st.subheader("📊 Results")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Spot Price",      f"${data['spot_price']}")
        col2.metric("Agreed Price K",  f"${data['agreed_price']}")
        col3.metric("New Fwd Price",   f"${data['forward_price']}")
        col4.metric("Position",        data['position'].capitalize())
        col5.metric("Forward Value",   f"${data['forward_value']}")

        st.divider()
        st.subheader("🔢 Step-by-Step")
        st.latex(rf"F_{{new}} = {data['spot_price']} \times e^{{(({data['rate']}/100) - ({data['yield']}/100)) \times ({data['maturity']}/12)}}")
        st.latex(rf"F_{{new}} = \${data['forward_price']}")
        st.latex(rf"f = ({data['forward_price']} - {data['agreed_price']}) \times e^{{-({data['rate']}/100) \times ({data['maturity']}/12)}}")
        st.latex(rf"f = \${data['forward_value']}")

        if data['forward_value'] > 0:
            st.success(f"✅ In Profit — Forward Value: **${data['forward_value']}**")
        else:
            st.error(f"❌ At a Loss — Forward Value: **${data['forward_value']}**")