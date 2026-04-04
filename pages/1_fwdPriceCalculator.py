import streamlit as st
from pricing import no_income_forwards, known_income_forwards, known_yield_forwards

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Forward Pricing",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Forward Pricing")
st.divider()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Contract Settings")
st.sidebar.caption("Select your contract type and fill in the parameters.")

contract_type = st.sidebar.selectbox(
    "Contract Type",
    ["No Income", "Known Income", "Known Yield"],
    help="No Income: non-dividend paying stock | Known Income: coupon bond | Known Yield: stock index or FX"
)

# ============================================================
# NO INCOME
# ============================================================

if contract_type == "No Income":
    """
    Forward pricing for an asset with no income (e.g. non-dividend paying stock).
    """
    st.subheader("🔹 No Income Forward")
    st.latex(r"F_0 = S \cdot e^{rT}")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        spot_price = st.number_input("Spot Price ($)", min_value=0.0, step=1.0, help="Current market price of the underlying asset")
    with col2:
        risk_free_rate = st.number_input("Risk-Free Rate (%)", min_value=0.0, step=0.1, help="Continuously compounded annual risk-free rate")
    with col3:
        time = st.number_input("Time to Maturity (months)", min_value=1, step=1, help="Duration of the forward contract in months")

    st.divider()
    clicked = st.button("Calculate Forward Price", type="primary")

    if clicked:
        data = no_income_forwards(spot_price, risk_free_rate, time)

        st.subheader("📊 Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Spot Price",     f"${data['spot_price']}")
        col2.metric("Risk-Free Rate", f"{data['rate']}%")
        col3.metric("Maturity",       f"{data['maturity']} months")

        st.divider()
        st.subheader("🔢 Step-by-Step")
        st.latex(rf"F_0 = {data['spot_price']} \times e^{{({data['rate']}/100) \times ({data['maturity']}/12)}}")
        st.latex(rf"F_0 = \${data['forward_price']}")

        st.success(f"✅ Forward Price: **${data['forward_price']}**")

# ============================================================
# KNOWN INCOME
# ============================================================

if contract_type == "Known Income":
    """
    Forward pricing for an asset that pays a known cash income during the contract
    (e.g. a coupon-paying bond).
    """
    st.subheader("🔹 Known Income Forward")
    st.latex(r"F_0 = (S - PV(I)) \cdot e^{RT} \quad \text{where} \quad PV(I) = I \cdot e^{-rt}")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        spot_price = st.number_input("Spot Price ($)", min_value=0.0, step=1.0, help="Current market price of the underlying asset")
    with col2:
        risk_free_rate = st.number_input("Risk-Free Rate (%)", min_value=0.0, step=0.1, help="Continuously compounded rate for the full contract period")
    with col3:
        time = st.number_input("Time to Maturity (months)", min_value=1, step=1, help="Duration of the forward contract in months")

    col4, col5, col6 = st.columns(3)
    with col4:
        income = st.number_input("Income ($)", min_value=0.0, step=1.0, help="Known cash income paid by the asset (e.g. coupon)")
    with col5:
        income_rate = st.number_input("Income Discount Rate (%)", min_value=0.0, step=0.1, help="Continuously compounded rate for discounting the income")
    with col6:
        income_time = st.number_input("Income Payment Time (months)", min_value=1, step=1, help="Month at which the income is paid")

    st.divider()

    clicked = st.button("Calculate Forward Price", type="primary")
    if clicked:
        data = known_income_forwards(spot_price, risk_free_rate, time, income, income_rate, income_time)

        st.subheader("📊 Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Spot Price",     f"${data['spot_price']}")
        col2.metric("Risk-Free Rate", f"{data['rate']}%")
        col3.metric("Maturity",       f"{data['maturity']} months")

        col4, col5, col6 = st.columns(3)
        col4.metric("Income",         f"${data['income']}")
        col5.metric("PV of Income",   f"${data['pv_income']}")
        col6.metric("Income Month",   f"Month {data['income_time']}")

        st.divider()
        st.subheader("🔢 Step-by-Step")
        st.latex(rf"PV(I) = {data['income']} \times e^{{-({data['income_rate']}/100) \times ({data['income_time']}/12)}} = \${data['pv_income']}")
        st.latex(rf"F_0 = ({data['spot_price']} - {data['pv_income']}) \times e^{{({data['rate']}/100) \times ({data['maturity']}/12)}}")
        st.latex(rf"F_0 = \${data['forward_price']}")

        st.success(f"✅ Forward Price: **${data['forward_price']}**")

# ============================================================
# KNOWN YIELD
# ============================================================

if contract_type == "Known Yield":
    """
    Forward pricing for an asset with a known continuous yield
    (e.g. stock index or foreign currency).
    """
    st.subheader("🔹 Known Yield Forward")
    st.latex(r"F_0 = S \cdot e^{(R - y)T}")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        spot_price = st.number_input("Spot Price ($)", min_value=0.0, step=1.0, help="Current market price of the underlying asset")
    with col2:
        risk_free_rate = st.number_input("Risk-Free Rate (%)", min_value=0.0, step=0.1, help="Continuously compounded annual risk-free rate")
    with col3:
        time = st.number_input("Time to Maturity (months)", min_value=1, step=1, help="Duration of the forward contract in months")
    with col4:
        yield_rate = st.number_input("Yield (%)", min_value=0.0, step=0.1, help="Continuously compounded yield of the asset")

    st.divider()
    clicked = st.button("Calculate Forward Price", type="primary")

    if clicked:
        data = known_yield_forwards(spot_price, risk_free_rate, time, yield_rate)

        st.subheader("📊 Results")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Spot Price",     f"${data['spot_price']}")
        col2.metric("Risk-Free Rate", f"{data['rate']}%")
        col3.metric("Maturity",       f"{data['maturity']} months")
        col4.metric("Yield",          f"{data['yield']}%")

        st.divider()
        st.subheader("🔢 Step-by-Step")
        st.latex(rf"F_0 = {data['spot_price']} \times e^{{(({data['rate']} - {data['yield']})/100) \times ({data['maturity']}/12)}}")
        st.latex(rf"F_0 = \${data['forward_price']}")

        st.success(f"✅ Forward Price: **${data['forward_price']}**")