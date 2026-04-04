import streamlit as st
import pandas as pd
from charts import chart1, chart2

st.set_page_config(
    page_title="Forward Valuation Over Time",
    page_icon="⏳",
    layout="wide"
)

st.title("⏳ Forward Valuation Over Time")
st.divider()

chartType = st.segmented_control(
    "Type of Chart",
    ["Forward Price vs Time to Maturity", "Forward Value Over Time"]
)

# ============================================================
# CHART 1 — Forward Price vs Time to Maturity
# ============================================================

if chartType == "Forward Price vs Time to Maturity":
    st.subheader("Forward Price vs Time to Maturity")
    st.caption("Fix a spot price and see how forward price grows across different maturities for all three asset types.")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        S  = st.number_input("Spot Price ($)",              min_value=0.0, step=1.0,  help="Current price of the underlying asset")
        r  = st.number_input("Risk-Free Rate (%)",          min_value=0.0, step=0.1,  help="Continuously compounded risk-free rate")
    with col2:
        I  = st.number_input("Income ($)",                  min_value=0.0, step=1.0,  help="Known cash income paid by the asset")
        Ir = st.number_input("Income Discount Rate (%)",    min_value=0.0, step=0.1,  help="Risk-free rate used to discount the income")
    with col3:
        T  = st.number_input("Income Payment Month",        min_value=1,   step=1,    help="Month at which the income is paid")
        y  = st.number_input("Yield (%)",                   min_value=0.0, step=0.1,  help="Continuously compounded yield of the asset")

    if st.button("Show Chart", type="primary"):
        fig = chart1(S, r, I, Ir, T, y)
        st.pyplot(fig)


# ============================================================
# CHART 2 — Forward Value Over Time
# ============================================================

elif chartType == "Forward Value Over Time":
    st.subheader("Forward Value Over Time")
    st.caption("Input a spot price path and see how the forward value drifts over the contract life.")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        K        = st.number_input("Agreed Price K ($)",        min_value=0.0, step=1.0,  help="Delivery price agreed at inception")
        r        = st.number_input("Risk-Free Rate (%)",        min_value=0.0, step=0.1,  help="Continuously compounded risk-free rate")
    with col2:
        I        = st.number_input("Income ($)",                min_value=0.0, step=1.0,  help="Known cash income paid by the asset")
        Ir       = st.number_input("Income Discount Rate (%)",  min_value=0.0, step=0.1,  help="Risk-free rate used to discount the income")
    with col3:
        T        = st.number_input("Income Payment Month",      min_value=1,   step=1,    help="Month at which the income is paid")
        y        = st.number_input("Yield (%)",                 min_value=0.0, step=0.1,  help="Continuously compounded yield of the asset")
    with col4:
        position = st.selectbox("Position", ["Long", "Short"],                            help="Long = agreed to buy | Short = agreed to sell")

    st.divider()
    st.markdown("**Enter spot price for each month (Month 0 → Month 11):**")

    # editable table for spot price path
    default_df = pd.DataFrame({
        "Month"      : list(range(12)),
        "Spot Price" : [float(K)] * 12
    })

    edited_df   = st.data_editor(default_df, hide_index=True, use_container_width=True)
    spot_prices = edited_df["Spot Price"].tolist()

    if st.button("Show Chart", type="primary"):
        if len(spot_prices) != 12:
            st.error("Please ensure all 12 months have a spot price.")
        else:
            fig = chart2(K, r, spot_prices, position, I, Ir, T, y)
            st.pyplot(fig)