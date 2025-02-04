import streamlit as st

# Function to calculate tax under the new regime
def calculate_new_tax(income):
    slabs = [(400000, 0.05), (400000, 0.1), (400000, 0.15), (400000, 0.2), (400000, 0.25), (float('inf'), 0.3)]
    tax_free_limit = 1275000  # ₹12.75 lakh including standard deduction
    tax = 0
    taxable_income = max(0, income - tax_free_limit)

    if income <= tax_free_limit:
        return 0, 0, 0  # No tax below threshold

    # Apply slab-wise tax
    for limit, rate in slabs:
        if taxable_income > 0:
            tax_on_slab = min(taxable_income, limit) * rate
            tax += tax_on_slab
            taxable_income -= limit

    # Marginal relief adjustment
    excess_income = income - 1275000
    if tax > excess_income:
        tax = excess_income  # Apply marginal relief

    cess = 0.04 * tax  # Cess @4%
    total_tax = tax + cess
    return tax, cess, total_tax

# Function to calculate tax under old regime (basic example, should be expanded with deductions)
def calculate_old_tax(income):
    old_slabs = [(250000, 0.05), (250000, 0.1), (500000, 0.2), (float('inf'), 0.3)]
    standard_deduction = 50000
    taxable_income = max(0, income - standard_deduction - 500000)  # Assumed basic exemptions
    tax = 0

    for limit, rate in old_slabs:
        if taxable_income > 0:
            tax += min(taxable_income, limit) * rate
            taxable_income -= limit

    cess = 0.04 * tax
    total_tax = tax + cess
    return tax, cess, total_tax

# Streamlit UI
st.title("💰 Bank-err's Income Tax Calculator for FY 2025-26")
st.markdown("**As per new tax regime**  \n**Marginal income relief applied**", unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["New Tax Regime", "Old Tax Regime"])

with tab1:
    st.subheader("New Tax Regime Calculator")
    income = st.number_input("Enter Your Annual Income (₹)", min_value=0, step=1000, format="%d", key="new_income")

    if st.button("Calculate Tax", key="new_calc"):
        tax, cess, total = calculate_new_tax(income)
        st.write(f"**Total Tax Payable:** ₹{total:,.2f}")
        if st.checkbox("Show Tax & Cess Breakdown", key="new_breakup"):
            st.write(f"- **Income Tax:** ₹{tax:,.2f}")
            st.write(f"- **Cess (4%):** ₹{cess:,.2f}")

with tab2:
    st.subheader("Old Tax Regime Calculator")
    income_old = st.number_input("Enter Your Annual Income (₹)", min_value=0, step=1000, format="%d", key="old_income")

    if st.button("Calculate Tax", key="old_calc"):
        tax_old, cess_old, total_old = calculate_old_tax(income_old)
        st.write(f"**Total Tax Payable:** ₹{total_old:,.2f}")
        if st.checkbox("Show Tax & Cess Breakdown", key="old_breakup"):
            st.write(f"- **Income Tax:** ₹{tax_old:,.2f}")
            st.write(f"- **Cess (4%):** ₹{cess_old:,.2f}")

# Footer with name
st.markdown('<p style="color: cyan; font-size: 16px; font-weight: bold; text-align: center;">Created by - Paramjeet Singh Gusain</p>', unsafe_allow_html=True)
