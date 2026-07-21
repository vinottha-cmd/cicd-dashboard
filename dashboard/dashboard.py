import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Loan Prediction Dashboard", layout="wide")

st.title("Loan Prediction Dashboard")

st.write(
    """
    This dashboard displays the processed Loan Prediction dataset
    and allows stakeholders to search and filter records interactively.
    """
)

BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / "data" / "processed_dataset.csv"


@st.cache_data
def load_data():
    return pd.read_csv(data_path)


data = load_data()

if data.empty:
    st.warning("No data to display.")
    st.stop()


# =========================
# Sidebar Filters
# =========================

st.sidebar.header("Search and Filter Options")

# Search
search_term = st.sidebar.text_input("Search by any field")

filtered_data = data.copy()

if search_term:
    filtered_data = filtered_data[
        filtered_data.apply(
            lambda row: row.astype(str)
            .str.contains(search_term, case=False, na=False)
            .any(),
            axis=1
        )
    ]


# Gender Filter
if "Gender" in filtered_data.columns:
    gender = st.sidebar.selectbox(
        "Gender",
        ["All"] + sorted(filtered_data["Gender"].dropna().unique().tolist())
    )
    if gender != "All":
        filtered_data = filtered_data[
            filtered_data["Gender"] == gender
        ]


# Education Filter
if "Education" in filtered_data.columns:
    education = st.sidebar.selectbox(
        "Education",
        ["All"] + sorted(filtered_data["Education"].dropna().unique().tolist())
    )
    if education != "All":
        filtered_data = filtered_data[
            filtered_data["Education"] == education
        ]


# Property Area Filter
if "Property_Area" in filtered_data.columns:
    property_area = st.sidebar.selectbox(
        "Property Area",
        ["All"] + sorted(filtered_data["Property_Area"].dropna().unique().tolist())
    )
    if property_area != "All":
        filtered_data = filtered_data[
            filtered_data["Property_Area"] == property_area
        ]


# Loan Status Filter
if "Loan_Status" in filtered_data.columns:
    loan_status = st.sidebar.selectbox(
        "Loan Status",
        ["All"] + sorted(filtered_data["Loan_Status"].dropna().unique().tolist())
    )
    if loan_status != "All":
        filtered_data = filtered_data[
            filtered_data["Loan_Status"] == loan_status
        ]


# Applicant Income Slider
if "ApplicantIncome" in filtered_data.columns and not filtered_data.empty:
    min_income = int(filtered_data["ApplicantIncome"].min())
    max_income = int(filtered_data["ApplicantIncome"].max())

    income_range = st.sidebar.slider(
        "Applicant Income",
        min_income,
        max_income,
        (min_income, max_income)
    )

    filtered_data = filtered_data[
        (filtered_data["ApplicantIncome"] >= income_range[0]) &
        (filtered_data["ApplicantIncome"] <= income_range[1])
    ]


# Loan Amount Slider
if "LoanAmount" in filtered_data.columns and not filtered_data.empty:
    min_loan = int(filtered_data["LoanAmount"].min())
    max_loan = int(filtered_data["LoanAmount"].max())

    loan_range = st.sidebar.slider(
        "Loan Amount",
        min_loan,
        max_loan,
        (min_loan, max_loan)
    )

    filtered_data = filtered_data[
        (filtered_data["LoanAmount"] >= loan_range[0]) &
        (filtered_data["LoanAmount"] <= loan_range[1])
    ]


# =========================
# Dashboard Summary
# =========================

st.subheader("Dataset Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_data))

if "Loan_Status" in filtered_data.columns:
    approved = (filtered_data["Loan_Status"] == "Y").sum()
    rejected = (filtered_data["Loan_Status"] == "N").sum()

    col2.metric("Approved Loans", approved)
    col3.metric("Rejected Loans", rejected)


# =========================
# Display Dataset
# =========================

st.subheader("Filtered Results")

if filtered_data.empty:
    st.warning("No records match the selected filters.")
else:
    st.dataframe(filtered_data, use_container_width=True)
