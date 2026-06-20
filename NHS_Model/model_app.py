import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="NHS Overspending Predictor",
    page_icon="🏥",
    layout="wide"
)

# ── Button styling — matches the teal theme used in the dashboard ──
st.markdown("""
<style>
    div.stButton > button[kind="primary"] {
        background-color: red;
        border: none;
        border-radius: 8px;
        padding: 0.6em;
        font-weight: 600;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1a8f89;
        border: none;
    }
    div.stButton > button[kind="secondary"] {
        background-color: white;
        color: #444;
        border: 1.5px solid #cfcfcf;
        border-radius: 8px;
        padding: 0.6em;
        font-weight: 600;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #20B2AA;
        color: #20B2AA;
    }
    div[data-testid="stDownloadButton"] > button {
        background-color: #20B2AA;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 0;
        font-weight: 600;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background-color: #1a8f89;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏥 NHS Prescribing - Overspending Predictor Model")
st.markdown("---")

# ── App state — keeps results across button clicks, lets Finish reset ──
if 'results_ready' not in st.session_state:
    st.session_state.results_ready = False
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0


@st.cache_resource
def load_model():
    model = joblib.load("NHS_Model/rf_model.pkl")
    le_icb = joblib.load("NHS_Model/le_icb.pkl")
    le_bnf = joblib.load("NHS_Model/le_bnf.pkl")
    return model, le_icb, le_bnf

model, le_icb, le_bnf = load_model()


# ── Helper: does the file have a column under any of these names? ──
def has_column(df, *names):
    return any(n in df.columns for n in names)


# ════════════════════════════════════════════════════════════════
# CLEANING — follows the notebook Chapter 0 ETL step by step
# ════════════════════════════════════════════════════════════════
def clean_raw_data(df):
    df = df.copy()

    # Step 1: Rename raw column names to the names used in the pipeline
    df = df.rename(columns={
        'REGIONAL_OFFICE_NAME': 'REGIONAL_OFFICE',
        'BNF_CHAPTER_PLUS_CODE': 'BNF_CHAPTER_CODE',
        'BNF_CHEMICAL_SUBSTANCE': 'DRUG_NAME',
        'BNF_PRESENTATION_NAME': 'DRUG_DESCRIPTION',
        'ADQUSAGE': 'ADQ_USAGE'
    })

    # Step 2: Keep only the columns we use (those that are present)
    keep_columns = [
        'YEAR_MONTH', 'REGIONAL_OFFICE', 'ICB_NAME', 'ICB_CODE',
        'PRACTICE_NAME', 'PRACTICE_CODE', 'POSTCODE',
        'BNF_CHAPTER_CODE', 'DRUG_NAME', 'DRUG_DESCRIPTION',
        'ITEMS', 'TOTAL_QUANTITY', 'ADQ_USAGE', 'NIC',
        'ACTUAL_COST', 'UNIDENTIFIED'
    ]
    df = df[[c for c in keep_columns if c in df.columns]]

    # Step 3: Fix YEAR_MONTH format — 202501 becomes 2025-01
    df['YEAR_MONTH'] = df['YEAR_MONTH'].astype(str)
    df['YEAR_MONTH'] = df['YEAR_MONTH'].apply(
        lambda x: x[:4] + '-' + x[4:] if '-' not in x else x
    )

    # Step 4: Round usage and money columns to 2 decimal places
    df['ADQ_USAGE'] = df['ADQ_USAGE'].round(2)
    df['NIC'] = df['NIC'].round(2)
    df['ACTUAL_COST'] = df['ACTUAL_COST'].round(2)

    # Step 5: TOTAL_QUANTITY should be a whole number
    df['TOTAL_QUANTITY'] = df['TOTAL_QUANTITY'].fillna(0).astype(int)

    # Step 6: Drop unidentified practices, then drop zero-price rows
    if 'UNIDENTIFIED' in df.columns:
        df = df[df['UNIDENTIFIED'] != 'Y']
    df = df[df['NIC'] != 0]

    # Step 7: Add the four engineered columns
    df['COST_PER_ITEM'] = (df['ACTUAL_COST'] / df['ITEMS']).round(2)
    df['NIC_RATIO'] = (df['ACTUAL_COST'] / df['NIC']).round(2)
    df['MONTH'] = df['YEAR_MONTH'].str[5:].astype(int)
    df['QUARTER'] = df['MONTH'].apply(lambda x: (x - 1) // 3 + 1)

    # Step 8: Drop columns no longer needed (POSTCODE and UNIDENTIFIED)
    df = df.drop(columns=[c for c in ['POSTCODE', 'UNIDENTIFIED'] if c in df.columns])

    return df


# ── Group rows exactly as Chapter 4 built model_data ──────────────
def aggregate_for_model(df):
    grouped = df.groupby(
        ['PRACTICE_CODE', 'PRACTICE_NAME', 'ICB_CODE', 'ICB_NAME',
         'BNF_CHAPTER_CODE', 'MONTH', 'QUARTER']
    ).agg(
        total_items=('ITEMS', 'sum'),
        total_quantity=('TOTAL_QUANTITY', 'sum'),
        total_adq=('ADQ_USAGE', 'sum'),
        avg_nic_ratio=('NIC_RATIO', 'mean'),
        total_actual_cost=('ACTUAL_COST', 'sum')
    ).reset_index()
    # Same roundings the notebook used in the DuckDB aggregation
    grouped['avg_nic_ratio'] = grouped['avg_nic_ratio'].round(4)
    grouped['total_actual_cost'] = grouped['total_actual_cost'].round(2)
    return grouped


# ── Encode + predict ───────────────────────────────────────────────
def run_model(df):
    df['ICB_CODE_ENC'] = df['ICB_CODE'].apply(
        lambda x: le_icb.transform([x])[0] if x in le_icb.classes_ else -1
    )
    df['BNF_CHAPTER_ENC'] = df['BNF_CHAPTER_CODE'].apply(
        lambda x: le_bnf.transform([x])[0] if x in le_bnf.classes_ else -1
    )
    features = ['total_items', 'total_quantity', 'total_adq', 'avg_nic_ratio',
                'ICB_CODE_ENC', 'BNF_CHAPTER_ENC', 'MONTH', 'QUARTER']
    df['predicted_cost'] = model.predict(df[features])
    return df


def reset_app():
    st.session_state.results_ready = False
    st.session_state.uploader_key += 1
    for key in ['cleaned_df', 'grouped_df', 'practice_summary',
                'at_risk_practices', 'raw_row_count']:
        st.session_state.pop(key, None)


# ════════════════════════════════════════════════════════════════
# UPLOAD — raw data stays visible at the top
# ════════════════════════════════════════════════════════════════
st.markdown("""
Upload a **raw NHSBSA EPD SNOMED file** (the file you download directly from the 
NHS Open Data Portal, filtered by ICB and month). You do not need to clean it first, 
this app does that for you.
""")

uploaded_file = st.file_uploader(
    "Upload your raw NHSBSA CSV file", type=["csv"],
    key=f"uploader_{st.session_state.uploader_key}"
)

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
    st.success(f"File loaded - {len(raw_df):,} raw rows")

    st.subheader("Raw Data Preview")
    st.dataframe(raw_df.head(5), use_container_width=True)

    # Validate essential columns — accept either raw or renamed versions
    checks = [
        ('YEAR_MONTH',), ('ICB_NAME',), ('ICB_CODE',),
        ('PRACTICE_NAME',), ('PRACTICE_CODE',),
        ('BNF_CHAPTER_PLUS_CODE', 'BNF_CHAPTER_CODE'),
        ('ITEMS',), ('TOTAL_QUANTITY',),
        ('ADQUSAGE', 'ADQ_USAGE'), ('NIC',), ('ACTUAL_COST',)
    ]
    missing = [names[0] for names in checks if not has_column(raw_df, *names)]

    if missing:
        st.error(f"Missing required columns: {missing}")
    else:
        if st.button("Clean Data & Run Prediction", type="primary"):

            with st.spinner("Cleaning data..."):
                cleaned_df = clean_raw_data(raw_df)

            with st.spinner("Grouping by practice, drug category and month..."):
                grouped = aggregate_for_model(cleaned_df)

            with st.spinner("Running predictions..."):
                grouped = run_model(grouped)
                grouped['pct_diff'] = ((grouped['total_actual_cost'] - grouped['predicted_cost'])
                                        / grouped['predicted_cost'] * 100)
                grouped['at_risk'] = grouped['pct_diff'] > 20

                practice_summary = grouped.groupby(
                    ['PRACTICE_CODE', 'PRACTICE_NAME', 'ICB_NAME']
                ).agg(
                    total_actual=('total_actual_cost', 'sum'),
                    total_predicted=('predicted_cost', 'sum')
                ).reset_index()
                practice_summary['pct_overspend'] = (
                    (practice_summary['total_actual'] - practice_summary['total_predicted']) /
                    practice_summary['total_predicted'] * 100
                ).round(2)
                at_risk_practices = practice_summary[
                    practice_summary['pct_overspend'] > 0
                ].sort_values('pct_overspend', ascending=False)

            st.session_state.cleaned_df = cleaned_df
            st.session_state.grouped_df = grouped
            st.session_state.practice_summary = practice_summary
            st.session_state.at_risk_practices = at_risk_practices
            st.session_state.raw_row_count = len(raw_df)
            st.session_state.results_ready = True


# ════════════════════════════════════════════════════════════════
# RESULTS — appear UNDER the raw data once processing is done
# ════════════════════════════════════════════════════════════════
if st.session_state.results_ready:

    cleaned_df = st.session_state.cleaned_df
    grouped = st.session_state.grouped_df
    practice_summary = st.session_state.practice_summary
    at_risk_practices = st.session_state.at_risk_practices

    st.markdown("---")
    st.subheader("Cleaned Data")
    st.markdown(
        "Your uploaded file after the full cleaning pipeline, columns renamed, "
        "values rounded, unidentified practices and zero-price rows removed, and "
        "COST_PER_ITEM, NIC_RATIO, MONTH and QUARTER added."
    )
    st.dataframe(cleaned_df, use_container_width=True)
    st.caption(f"{st.session_state.raw_row_count:,} raw rows  →  {len(cleaned_df):,} clean rows  "
               f"→  {len(grouped):,} practice-category-month combinations for the model.")

    st.markdown("---")
    st.subheader(f"Results - {len(at_risk_practices)} At-Risk Practices Found")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Practices", f"{len(practice_summary):,}")
    col2.metric("At-Risk Practices", f"{len(at_risk_practices):,}")
    col3.metric("Top Overspend",
                f"+{at_risk_practices['pct_overspend'].max():.1f}%"
                if len(at_risk_practices) > 0 else "None")

    if len(at_risk_practices) > 0:
        top20 = at_risk_practices.head(20).copy()
        top20['short_name'] = top20['PRACTICE_NAME'].str[:35]

        fig = px.bar(
            top20.sort_values('pct_overspend'),
            x='pct_overspend', y='short_name', orientation='h',
            color='pct_overspend', color_continuous_scale='Reds',
            text='pct_overspend', hover_name='PRACTICE_NAME',
            hover_data={'ICB_NAME': True, 'total_actual': ':.0f',
                        'total_predicted': ':.0f', 'short_name': False},
            labels={'pct_overspend': '% Above Predicted', 'short_name': '',
                    'ICB_NAME': 'ICB', 'total_actual': 'Actual Cost (£)',
                    'total_predicted': 'Predicted Cost (£)'}
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='auto')
        fig.update_layout(height=850, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No at-risk practices found in this dataset.")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        csv_out = at_risk_practices.to_csv(index=False)
        st.download_button(
            label="Download Data",
            data=csv_out,
            file_name="at_risk_practices.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_b:
        if st.button("Finish", type="secondary", use_container_width=True):
            reset_app()
            st.rerun()

st.markdown("---")
st.markdown("*Built using a Random Forest model trained on NHS EPD SNOMED 2025 data.*")