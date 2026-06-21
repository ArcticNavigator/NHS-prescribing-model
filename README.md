# NHS Prescribing Overspending Predictor - Random Forest Machine Learning App (2025)

**A live machine learning app that predicts which GP practices will overspend on NHS prescribing. Upload a real NHS prescribing file and get back a ranked list of at-risk practices built with a Random Forest model that is 95.4% accurate.**

[![Live Model App](https://img.shields.io/badge/▶%20Try%20the%20Live%20App-7B68EE?style=for-the-badge)](https://nhs-prescribing-model-ah5jesmyr8b6y6gbeqzah5.streamlit.app)
[![scikit-learn](https://img.shields.io/badge/Random%20Forest-scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

---

## Try the live app

### 👉 [Open the NHS Overspending Predictor](https://nhs-prescribing-model-ah5jesmyr8b6y6gbeqzah5.streamlit.app)

Upload a raw NHS prescribing file → the app cleans it, runs the model, and shows you which GP practices are predicted to overspend.

---

## What is this?

This is a machine learning web app that acts as an **early warning tool for NHS prescribing overspending**. The NHS currently finds out about overspending only after the money is gone. This app predicts it ahead of time.

You upload a raw monthly prescribing file from the NHS Business Services Authority (NHSBSA) Open Data Portal. The app does everything else:

1. **Cleans the raw data** automatically (the same cleaning pipeline used to train the model).
2. **Groups it** by practice, drug category and month.
3. **Predicts the expected cost** for each practice using a trained Random Forest model.
4. **Flags at-risk practices** where actual spending is more than 20% above what the model predicted.
5. **Shows a ranked chart** and lets you download the results as a CSV.

---

## How the model performs

- **Random Forest Regressor** trained on NHS EPD SNOMED 2025 data.
- **95.4% accuracy (R² = 0.954)** on held-out November–December test data.
- Beats a Linear Regression baseline (R² = 0.55) by 40 percentage points, because prescribing cost is driven by non-linear interactions between drug category, volume and pricing.
- Cross-validated (5-fold) with a mean R² of 0.966 and a standard deviation of just 0.0006, the model is stable across different data splits.
- Identified **2,417 at-risk GP practices** in the test period.

### What drives the predictions

The single biggest predictor is **prescription volume (ITEMS, 61%)**, followed by **drug category (16%)**. Together they explain 77% of all cost variation. Geographic location adds less than 1% confirming that prescribing cost depends on *what* is prescribed, not *where*.

---

## How to use it

1. Go to the [NHSBSA Open Data Portal](https://opendata.nhsbsa.net/dataset/english-prescribing-dataset-epd-with-snomed-code).
2. Open a monthly EPD SNOMED file and use the filter to download data for a single ICB (this keeps the file small enough to upload).
3. Open the [live app](https://nhs-prescribing-model-ah5jesmyr8b6y6gbeqzah5.streamlit.app) and upload that file.
4. Click **Clean Data & Run Prediction**.
5. Review the at-risk practices and download the results.

> The app is designed for single-ICB monthly extracts. The full national file is too large to upload on a free hosting tier.

---

## Tech stack

- **scikit-learn** - Random Forest model and label encoders
- **Streamlit** - the web app
- **pandas** - data cleaning and aggregation
- **Plotly** - the at-risk practices chart
- **joblib** - saving and loading the trained model
- **Streamlit Community Cloud** - hosting

---

## The model inputs

The model is trained on eight features, built by grouping raw prescribing rows by practice, ICB, drug category, month and quarter:

`total_items, total_quantity, total_adq, avg_nic_ratio, ICB_CODE (encoded), BNF_CHAPTER_CODE (encoded), MONTH, QUARTER`

The target is total actual cost per practice, per drug category, per month.

---

## Run it locally

```bash
# Clone the repository
git clone https://github.com/ArcticNavigator/NHS-prescribing-model.git
cd NHS-prescribing-model

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run model_app.py
```

---

## Related repositories

- **Full project** → [NHS-Prescribe-Seek](https://github.com/ArcticNavigator/NHS-Prescribe-Seek) (notebook, dashboard and model together)
- **Interactive dashboard** → [NHS-prescribing-dashboard](https://github.com/ArcticNavigator/NHS-prescribing-dashboard) (explore all the findings)

---

## Data source

English Prescribing Dataset (EPD) with SNOMED code - NHS Business Services Authority Open Data Portal: https://opendata.nhsbsa.net/dataset/english-prescribing-dataset-epd-with-snomed-code

---

## Author

Built by **ArcticNavigator**.

---

*Keywords: NHS overspending prediction, machine learning healthcare, Random Forest model NHS, NHS prescribing prediction app, GP practice cost prediction, scikit-learn healthcare model, predictive analytics NHS, NHS EPD SNOMED machine learning, healthcare ML deployment, Streamlit machine learning app, NHS budget forecasting, prescribing cost model England, at-risk practice detection.*
