import streamlit as st
import pandas as pd
import plotly.express as px
from pypdf import PdfReader

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="PropAgent AI",
    page_icon="?",
    layout="wide"
)

st.title("? PropAgent AI")
st.subheader("Commercial Real Estate Due Diligence Dashboard")

st.write(
    "Upload a lease agreement and automatically scan for financial risk clauses while generating underwriting metrics."
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.header("Property Information")

uploaded_file = st.sidebar.file_uploader(
    "Upload Lease Agreement (PDF)",
    type=["pdf"]
)

target_zip = st.sidebar.text_input(
    "Zip Code",
    value="10001"
)

property_type = st.sidebar.selectbox(
    "Property Type",
    [
        "Office",
        "Retail",
        "Industrial",
        "Multi-Family"
    ]
)

purchase_price = st.sidebar.number_input(
    "Purchase Price ($)",
    min_value=1000000,
    value=5000000,
    step=500000
)

# -------------------------------------------------
# PDF Processing
# -------------------------------------------------

risk_keywords = [
    "uncapped",
    "maintenance",
    "structural",
    "capital repairs",
    "escalation",
    "pro-rata"
]


def process_pdf(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    risks = []

    for line in text.split("\n"):
        lower = line.lower()

        if any(word in lower for word in risk_keywords):
            risks.append(line.strip())

    return risks


# -------------------------------------------------
# Run Analysis
# -------------------------------------------------

if st.sidebar.button("Run Multi-Agent Underwriting"):

    st.success("Analysis Complete")

    discovered_risks = []

    if uploaded_file is not None:
        discovered_risks = process_pdf(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("? Market Scout")

        st.info(
            f"""
Property Type: **{property_type}**

Zip Code: **{target_zip}**

Average Market Rent:
**$45.50 / Sq Ft**

Vacancy Rate:
**8.4%**
"""
        )

    with col2:

        st.subheader("? Lease Risk Auditor")

        if discovered_risks:

            st.error("Potential Risk Clauses Found")

            for risk in discovered_risks[:5]:
                st.write("?", risk)

        else:

            st.success("No risk clauses detected.")

    st.divider()

    st.header("Financial Underwriting")

    sqft = 50000

    market_rent = 45.50

    gross_income = sqft * market_rent

    expense_ratio = 0.42 if discovered_risks else 0.35

    expenses = gross_income * expense_ratio

    noi = gross_income - expenses

    cap_rate = (noi / purchase_price) * 100

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Gross Income",
        f"${gross_income:,.0f}"
    )

    m2.metric(
        "Net Operating Income",
        f"${noi:,.0f}"
    )

    m3.metric(
        "Cap Rate",
        f"{cap_rate:.2f}%"
    )

    years = list(range(1, 11))

    projected = []

    current = noi

    for _ in years:
        projected.append(current)
        current *= 1.03

    df = pd.DataFrame({
        "Year": years,
        "Projected NOI": projected
    })

    fig = px.area(
        df,
        x="Year",
        y="Projected NOI",
        title="10-Year NOI Projection"
    )

    st.plotly_chart(fig, use_container_width=True)

else:

    st.info(
        "Upload a PDF and click **Run Multi-Agent Underwriting**."
    )