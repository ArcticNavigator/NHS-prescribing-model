import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

st.set_page_config(
    page_title="NHS Overspending Predictor",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 NHS Prescribing - Overspending Predictor Model")
st.markdown("---")

st.markdown("""
Upload a CSV file with NHS prescribing data to identify which GP practices 
are predicted to overspend. The file must contain these columns:

`PRACTICE_CODE, PRACTICE_NAME, ICB_CODE, ICB_NAME, BNF_CHAPTER_CODE, 
ITEMS, TOTAL_QUANTITY, ADQ_USAGE, NIC, ACTUAL_COST, MONTH, QUARTER`
""")

# Load model and encoders
@st.cache_resource
def load_model():
    model = joblib.load("NHS_Model/rf_model.pkl")
    le_icb = joblib.load("NHS_Model/le_icb.pkl")
    le_bnf = joblib.load("NHS_Model/le_bnf.pkl")
    return model, le_icb, le_bnf

model, le_icb, le_bnf = load_model()

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"File loaded — {len(df):,} rows")

    # Show preview
    st.subheader("Data Preview")
    st.dataframe(df.head(5), use_container_width=True)

    # Check required columns
    required_cols = ['PRACTICE_CODE', 'PRACTICE_NAME', 'ICB_CODE', 'ICB_NAME',
                     'BNF_CHAPTER_CODE', 'ITEMS', 'TOTAL_QUANTITY',
                     'ADQ_USAGE', 'NIC', 'ACTUAL_COST', 'MONTH', 'QUARTER']

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        st.error(f"Missing columns: {missing}")
    else:
        if st.button("Run Prediction", type="primary"):
            with st.spinner("Running predictions..."):

                # Engineer features
                df['NIC_RATIO'] = df['ACTUAL_COST'] / df['NIC'].replace(0, np.nan)
                df['NIC_RATIO'] = df['NIC_RATIO'].fillna(df['NIC_RATIO'].median())

                # Encode categoricals — handle unseen labels
                df['ICB_CODE_ENC'] = df['ICB_CODE'].apply(
                    lambda x: le_icb.transform([x])[0]
                    if x in le_icb.classes_ else -1
                )
                df['BNF_ENC'] = df['BNF_CHAPTER_CODE'].apply(
                    lambda x: le_bnf.transform([x])[0]
                    if x in le_bnf.classes_ else -1
                )

                # Features used in training
                features = ['ITEMS', 'TOTAL_QUANTITY', 'ADQ_USAGE', 'NIC_RATIO',
                            'ICB_CODE_ENC', 'BNF_ENC', 'MONTH', 'QUARTER']

                X = df[features]
                df['predicted_cost'] = model.predict(X)

                # Flag at-risk rows (actual > predicted by more than 10%)
                df['pct_diff'] = ((df['ACTUAL_COST'] - df['predicted_cost'])
                                  / df['predicted_cost'] * 100)
                df['at_risk'] = df['pct_diff'] > 10

                # Aggregate to practice level
                practice_summary = df.groupby(
                    ['PRACTICE_CODE', 'PRACTICE_NAME', 'ICB_NAME']
                ).agg(
                    total_actual=('ACTUAL_COST', 'sum'),
                    total_predicted=('predicted_cost', 'sum'),
                    at_risk_rows=('at_risk', 'sum')
                ).reset_index()

                practice_summary['pct_overspend'] = (
                    (practice_summary['total_actual'] -
                     practice_summary['total_predicted']) /
                    practice_summary['total_predicted'] * 100
                ).round(2)

                at_risk_practices = practice_summary[
                    practice_summary['pct_overspend'] > 10
                ].sort_values('pct_overspend', ascending=False)

            st.markdown("---")
            st.subheader(f"Results — {len(at_risk_practices)} At-Risk Practices Found")

            # Summary metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Practices", f"{len(practice_summary):,}")
            col2.metric("At-Risk Practices", f"{len(at_risk_practices):,}")
            col3.metric("Top Overspend",
                        f"+{at_risk_practices['pct_overspend'].max():.1f}%"
                        if len(at_risk_practices) > 0 else "None")

            if len(at_risk_practices) > 0:
                # Bar chart
                top20 = at_risk_practices.head(20).copy()
                top20['short_name'] = top20['PRACTICE_NAME'].str[:35]

                fig = px.bar(
                    top20.sort_values('pct_overspend'),
                    x='pct_overspend',
                    y='short_name',
                    orientation='h',
                    color='pct_overspend',
                    color_continuous_scale='Reds',
                    text='pct_overspend',
                    hover_name='PRACTICE_NAME',
                    hover_data={
                        'ICB_NAME': True,
                        'total_actual': ':.0f',
                        'total_predicted': ':.0f',
                        'short_name': False
                    },
                    labels={
                        'pct_overspend': '% Above Predicted',
                        'short_name': '',
                        'ICB_NAME': 'ICB',
                        'total_actual': 'Actual Cost (£)',
                        'total_predicted': 'Predicted Cost (£)'
                    }
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(height=600, coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)

                # Download results
                st.subheader("Download Results")
                csv_out = at_risk_practices.to_csv(index=False)
                st.download_button(
                    label="Download At-Risk Practices CSV",
                    data=csv_out,
                    file_name="at_risk_practices.csv",
                    mime="text/csv"
                )
            else:
                st.success("No at-risk practices found in this dataset.")

st.markdown("---")
st.markdown("*Built using a Random Forest model trained on NHS EPD SNOMED 2025 data.*")