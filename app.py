import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="FinAuditAI",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #F4F7FC;
}

[data-testid="stSidebar"] {
    background-color: #14213D;
}

[data-testid="stSidebar"] * {
    color: white;
}

.main-title {
    color: #172B4D;
    font-size: 34px;
    font-weight: 800;
}

.subtitle {
    color: #718096;
    font-size: 14px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E5EAF2;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    min-height: 115px;
}

.metric-label {
    color: #718096;
    font-size: 14px;
}

.metric-value {
    color: #172B4D;
    font-size: 25px;
    font-weight: bold;
    margin-top: 10px;
}

.section-title {
    color: #172B4D;
    font-size: 22px;
    font-weight: 700;
}

.stButton > button {
    background: linear-gradient(90deg, #315EFB, #7657E8);
    color: white;
    border: none;
    border-radius: 9px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SAMPLE DATA
# ==========================================

def get_sample_data():

    return pd.DataFrame({
        "Transaction_ID": [
            f"TXN{i:04d}" for i in range(1, 21)
        ],
        "Date": pd.date_range(
            end=datetime.today(),
            periods=20
        ),
        "Merchant": [
            "Amazon", "Flipkart", "Uber", "Swiggy",
            "Netflix", "Myntra", "Zomato", "Amazon",
            "Uber", "Flipkart", "Swiggy", "Netflix",
            "Amazon", "Myntra", "Uber", "Zomato",
            "Flipkart", "Amazon", "Swiggy", "Myntra"
        ],
        "Category": [
            "Shopping", "Shopping", "Travel", "Food",
            "Entertainment", "Shopping", "Food", "Shopping",
            "Travel", "Shopping", "Food", "Entertainment",
            "Shopping", "Shopping", "Travel", "Food",
            "Shopping", "Shopping", "Food", "Shopping"
        ],
        "Amount": [
            1200, 2500, 450, 350, 649,
            3200, 550, 1800, 700, 2100,
            400, 649, 1500, 2800, 500,
            600, 1900, 950, 450, 85000
        ],
        "Status": ["Success"] * 20
    })


# ==========================================
# DATA PREPARATION
# ==========================================

def prepare_data(data):

    data = data.copy()

    data.columns = [
        str(column).strip()
        for column in data.columns
    ]

    column_names = {
        column.lower().replace(" ", "_"): column
        for column in data.columns
    }

    amount_column = None

    for name in [
        "amount",
        "transaction_amount",
        "total_amount",
        "value"
    ]:
        if name in column_names:
            amount_column = column_names[name]
            break

    if amount_column is None:
        raise ValueError(
            "Your CSV must contain an Amount column."
        )

    data["Amount"] = pd.to_numeric(
        data[amount_column],
        errors="coerce"
    )

    data = data.dropna(subset=["Amount"])
    data = data[data["Amount"] >= 0].copy()

    if "Date" not in data.columns:
        data["Date"] = pd.Timestamp.today()

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    if "Merchant" not in data.columns:
        data["Merchant"] = "Unknown"

    if "Category" not in data.columns:
        data["Category"] = "Other"

    if "Status" not in data.columns:
        data["Status"] = "Unknown"

    if "Transaction_ID" not in data.columns:
        data["Transaction_ID"] = [
            f"TXN{i:04d}"
            for i in range(1, len(data) + 1)
        ]

    return data


# ==========================================
# ANOMALY DETECTION
# ==========================================

def detect_anomalies(data):

    data = data.copy()

    if data.empty:
        data["Flag"] = False
        data["Risk_Reason"] = ""
        return data

    median_amount = data["Amount"].median()

    threshold = max(
        data["Amount"].quantile(0.99),
        median_amount * 3
    )

    high_amount = data["Amount"] > threshold

    duplicate = data.duplicated(
        subset=["Date", "Merchant", "Amount"],
        keep=False
    )

    data["Flag"] = high_amount | duplicate

    data["Risk_Reason"] = "Normal"

    data.loc[high_amount, "Risk_Reason"] = (
        "Unusually high amount"
    )

    data.loc[duplicate, "Risk_Reason"] = (
        "Possible duplicate transaction"
    )

    data.loc[
        high_amount & duplicate,
        "Risk_Reason"
    ] = "High amount and possible duplicate"

    return data


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 💹 FinAuditAI")

    st.caption("SMART FINANCIAL INTELLIGENCE")

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Transactions",
            "Fraud Detection",
            "Analytics",
            "About"
        ]
    )

    st.markdown("---")

    st.markdown("### 📂 Upload Transactions")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    st.markdown("---")

    st.caption("FinAuditAI Version 1.0")
    st.caption("Financial Audit & Analytics")


# ==========================================
# LOAD TRANSACTION DATA
# ==========================================

if uploaded_file is not None:

    try:
        raw_data = pd.read_csv(uploaded_file)
        df = prepare_data(raw_data)
        data_source = "Uploaded CSV"

    except (ValueError, pd.errors.ParserError) as error:
        st.error(f"CSV Error: {error}")
        st.stop()

else:

    df = get_sample_data()
    data_source = "Demo Data"

df = detect_anomalies(df)

total_transactions = len(df)
total_amount = df["Amount"].sum()

average_amount = (
    df["Amount"].mean()
    if total_transactions > 0
    else 0
)

flagged_count = int(df["Flag"].sum())


# ==========================================
# MAIN HEADER
# ==========================================

st.markdown(
    '<div class="main-title">FinAuditAI Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Smart Financial Transaction Audit & Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    f"Data Source: {data_source} | "
    f"Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
)


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.markdown(
        '<div class="section-title">Financial Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "📄 Transactions", f"{total_transactions:,}"),
        (col2, "💰 Total Amount", f"₹{total_amount:,.2f}"),
        (col3, "📊 Average Amount", f"₹{average_amount:,.2f}"),
        (col4, "🚨 Flagged", f"{flagged_count:,}")
    ]

    for column, label, value in metrics:

        with column:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    left, right = st.columns(2)

    with left:

        st.subheader("📈 Transaction Trends")

        date_data = df.dropna(subset=["Date"])

        if not date_data.empty:

            daily_data = date_data.groupby(
                date_data["Date"].dt.date
            )["Amount"].sum()

            st.line_chart(daily_data)

        else:
            st.info("No valid date information available.")

    with right:

        st.subheader("🛒 Category Analysis")

        category_data = df.groupby(
            "Category"
        )["Amount"].sum()

        st.bar_chart(category_data)

    st.subheader("🚨 Recent Flagged Transactions")

    flagged_data = df[df["Flag"]]

    if not flagged_data.empty:

        st.dataframe(
            flagged_data[
                [
                    "Transaction_ID",
                    "Date",
                    "Merchant",
                    "Amount",
                    "Risk_Reason"
                ]
            ].head(10),
            use_container_width=True
        )

    else:

        st.success("No unusual transactions flagged.")


# ==========================================
# TRANSACTIONS
# ==========================================

elif page == "Transactions":

    st.subheader("📋 Transaction Management")

    search = st.text_input(
        "🔍 Search Merchant or Transaction ID"
    )

    categories = ["All"] + sorted(
        df["Category"].dropna().astype(str).unique()
    )

    selected_category = st.selectbox(
        "Select Category",
        categories
    )

    filtered_data = df.copy()

    if search:

        merchant_match = filtered_data[
            "Merchant"
        ].astype(str).str.contains(
            search,
            case=False,
            na=False
        )

        id_match = filtered_data[
            "Transaction_ID"
        ].astype(str).str.contains(
            search,
            case=False,
            na=False
        )

        filtered_data = filtered_data[
            merchant_match | id_match
        ]

    if selected_category != "All":

        filtered_data = filtered_data[
            filtered_data["Category"] == selected_category
        ]

    st.write(
        f"Total matching transactions: {len(filtered_data)}"
    )

    st.dataframe(
        filtered_data,
        use_container_width=True
    )

    st.download_button(
        "⬇️ Download CSV Report",
        data=filtered_data.to_csv(index=False),
        file_name="finauditai_transactions.csv",
        mime="text/csv"
    )


# ==========================================
# FRAUD DETECTION
# ==========================================

elif page == "Fraud Detection":

    st.subheader("🚨 Anomaly Detection Center")

    st.info(
        "Flagged transactions require manual investigation. "
        "A flag does not prove that fraud has occurred."
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Flagged Transactions",
        flagged_count
    )

    col2.metric(
        "Other Transactions",
        total_transactions - flagged_count
    )

    flagged_data = df[df["Flag"]]

    if not flagged_data.empty:

        st.subheader("⚠️ Transactions Requiring Review")

        st.dataframe(
            flagged_data[
                [
                    "Transaction_ID",
                    "Date",
                    "Merchant",
                    "Category",
                    "Amount",
                    "Risk_Reason"
                ]
            ],
            use_container_width=True
        )

        st.download_button(
            "⬇️ Download Audit Report",
            data=flagged_data.to_csv(index=False),
            file_name="finauditai_audit_report.csv",
            mime="text/csv"
        )

    else:

        st.success("No anomalies detected by current rules.")


# ==========================================
# ANALYTICS
# ==========================================

elif page == "Analytics":

    st.subheader("📊 Financial Analytics")

    st.markdown("### Category-wise Analysis")

    category_summary = df.groupby(
        "Category"
    ).agg(
        Total_Amount=("Amount", "sum"),
        Transaction_Count=("Amount", "count")
    )

    st.dataframe(
        category_summary,
        use_container_width=True
    )

    st.markdown("### Merchant Analysis")

    merchant_summary = df.groupby(
        "Merchant"
    )["Amount"].sum().sort_values(
        ascending=False
    )

    st.bar_chart(merchant_summary)

    st.markdown("### Transaction Status")

    status_summary = df["Status"].value_counts()

    st.bar_chart(status_summary)


# ==========================================
# ABOUT
# ==========================================

elif page == "About":

    st.subheader("💡 About FinAuditAI")

    st.write("""
    FinAuditAI is a financial transaction audit
    and analytics application developed using Python.

    **Core Features**

    - Financial transaction monitoring
    - CSV transaction upload
    - Rule-based anomaly detection
    - Financial analytics
    - Category-wise spending analysis
    - Downloadable audit reports

    **Technology Stack**

    - Python
    - Streamlit
    - Pandas

    **Project Objective**

    To simplify financial transaction analysis
    and identify unusual activities through
    data-driven auditing techniques.
    """)

    st.success("FinAuditAI | Smart Financial Intelligence")


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#718096;">
        © 2026 FinAuditAI | Smart Financial Audit & Analytics
    </div>
    """,
    unsafe_allow_html=True
)