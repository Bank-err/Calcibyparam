import streamlit as st

# Title and Description
st.title("Bank-err's Income Tax Calculator for FY 2025-26")
st.subheader("Compare tax under both New & Old Regimes")

# Sidebar
st.sidebar.title("Instructions")
st.sidebar.write("1. Enter your annual taxable income before deductions.")
st.sidebar.write("2. Select the tax regime (New or Old).")
st.sidebar.write("3. View tax liability with detailed breakup.")

# User Input: Annual Income
income = st.number_input("Enter Your Annual Income (₹)", min_value=0, step=1000, format="%d")

# Constants
STANDARD_DEDUCTION = 75000
TAX_FREE_LIMIT_NEW = 1275000  # ₹12L + ₹75K Standard Deduction
CESS_RATE = 0.04  # 4% Cess

# New Regime Slabs
TAX_SLABS_NEW = [
    (400000, 0.05),  # ₹4L - ₹8L → 5%
    (400000, 0.10),  # ₹8L - ₹12L → 10%
    (400000, 0.15),  # ₹12L - ₹16L → 15%
    (400000, 0.20),  # ₹16L - ₹20L → 20%
    (400000, 0.25),  # ₹20L - ₹24L → 25%
    (float('inf'), 0.30)  # Above ₹24L → 30%
]

# Old Regime Slabs (For reference; update as needed)
TAX_SLABS_OLD = [
    (250000, 0.05),  # ₹2.5L - ₹5L → 5%
    (250000, 0.10),  # ₹5L - ₹7.5L → 10%
    (250000, 0.15),  # ₹7.5L - ₹10L → 15%
    (250000, 0.20),  # ₹10L - ₹12.5L → 20%
    (250000, 0.25),  # ₹12.5L - ₹15L → 25%
    (float('inf'), 0.30)  # Above ₹15L → 30%
]

# Function to calculate tax
def calculate_tax(income, tax_slabs, tax_free_limit):
    taxable_income = max(0, income - STANDARD_DEDUCTION)
    tax_breakup = []
    total_tax = 0

    if taxable_income <= tax_free_limit:
        return 0, []  # No tax if within free limit

    remaining_income = taxable_income - tax_free_limit

    for slab, rate in tax_slabs:
        if remaining_income > 0:
            taxable_at_this_rate = min(remaining_income, slab)
            tax_amount = taxable_at_this_rate * rate
            tax_breakup.append((taxable_at_this_rate, rate * 100, tax_amount))
            total_tax += tax_amount
            remaining_income -= taxable_at_this_rate

    return total_tax, tax_breakup

# Tabs for New & Old Tax Regime
tab1, tab2 = st.tabs(["New Tax Regime", "Old Tax Regime"])

with tab1:
    st.header("New Tax Regime Calculation")
    tax_new, breakup_new = calculate_tax(income, TAX_SLABS_NEW, TAX_FREE_LIMIT_NEW)
    
    # Marginal Relief Calculation
    if TAX_FREE_LIMIT_NEW < income <= TAX_FREE_LIMIT_NEW + tax_new:
        tax_new = income - TAX_FREE_LIMIT_NEW  # Marginal Relief Adjustment

    cess_new = tax_new * CESS_RATE
    total_tax_new = tax_new + cess_new

    # Display Results
    st.write(f"**Total Tax (Before Cess):** ₹{tax_new:,.2f}")
    st.write(f"**Cess (4%):** ₹{cess_new:,.2f}")
    st.write(f"**Total Tax Payable:** ₹{total_tax_new:,.2f}")

    # Tax Breakdown
    st.subheader("Tax Breakdown (New Regime)")
    for slab, rate, tax in breakup_new:
        st.write(f"**₹{slab:,.0f}** taxed at **{rate}%** = ₹{tax:,.2f}")

with tab2:
    st.header("Old Tax Regime Calculation")
    tax_old, breakup_old = calculate_tax(income, TAX_SLABS_OLD, 250000)  # ₹2.5L basic exemption limit
    
    cess_old = tax_old * CESS_RATE
    total_tax_old = tax_old + cess_old

    # Display Results
    st.write(f"**Total Tax (Before Cess):** ₹{tax_old:,.2f}")
    st.write(f"**Cess (4%):** ₹{cess_old:,.2f}")
    st.write(f"**Total Tax Payable:** ₹{total_tax_old:,.2f}")

    # Tax Breakdown
    st.subheader("Tax Breakdown (Old Regime)")
    for slab, rate, tax in breakup_old:
        st.write(f"**₹{slab:,.0f}** taxed at **{rate}%** = ₹{tax:,.2f}")

# Footer
st.markdown("<h5 style='color:cyan;'>Developed by Paramjeet Singh Gusain</h5>", unsafe_allow_html=True)
