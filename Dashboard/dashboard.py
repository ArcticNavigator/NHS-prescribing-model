import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import json

# Page configuration
st.set_page_config(
    page_title="NHS Prescribing Analysis 2025",
    page_icon="🏥",
    layout="wide"
)

# Data path
DATA = "Dashboard/data/"

# Load GeoJSON
GEOJSON_PATH = "Dashboard/Integrated_Care_Boards_April_2023_EN_BGC_4724716452693616968.geojson"
with open(GEOJSON_PATH, 'r') as f:
    geojson = json.load(f)

# ── Animated metric helper ──────────────────────────────────
def animated_metric(label, value, col):
    # Only animate if text is longer than 12 characters
    needs_animation = len(str(value)) > 20
    
    if needs_animation:
        animation_style = """
            animation: marquee 3s ease-in-out infinite alternate;
        """
        keyframes = """
        <style>
        @keyframes marquee {
            0% { transform: translateX(0%); }
            100% { transform: translateX(-30%); }
        }
        </style>
        """
    else:
        animation_style = ""
        keyframes = ""

    col.markdown(f"""
    {keyframes}
    <div style='background-color:#f0f2f6; padding:15px; border-radius:8px; 
    text-align:center; overflow:hidden;'>
        <p style='font-size:13px; color:grey; margin:0 0 5px 0;'>{label}</p>
        <div style='overflow:hidden; white-space:nowrap;'>
            <span style='font-size:22px; font-weight:bold; 
            display:inline-block; {animation_style}'>
            {value}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.image(
    "Dashboard/nhs_logo.png.png",
    width=150
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    [
        "Introduction",
        "Chapter 0 - Building the Data",
        "Chapter 1 - What is NHS Prescribing?",
        "Chapter 2 - Where is the Money Going?",
        "Chapter 3 - Who is Overspending?",
        "Chapter 4 - Can We Predict Overspending?",
        "Chapter 5 - Can We Forecast Spikes?",
        "Chapter 6 - Does Time of Year Explain Spikes?"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**UEA NBS-7143B**")
st.sidebar.markdown("Business Analytics Methods")






# ============================================================
# PAGE 1 — INTRODUCTION
# ============================================================
if page == "Introduction":

    st.title("🏥 NHS Primary Care Prescribing Analysis 2025")
    st.markdown("---")

    # Business question
    st.markdown("""
    <div style='background-color:#20B2AA; padding:20px; border-radius:10px; color:white;'>
    <h3>Business Question</h3>
    <p style='font-size:18px;'>Where is the NHS overspending on primary care prescribing in England, 
    and can we predict which GP practices will exceed their expected costs before it happens?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Key headline numbers
    st.subheader("Key Numbers at a Glance")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    animated_metric("Total Spend", "£10.54B", col1)
    animated_metric("Prescriptions", "1.27B", col2)
    animated_metric("GP Practices", "5,764", col3)
    animated_metric("ICBs", "42", col4)
    animated_metric("Drug Categories", "21", col5)
    animated_metric("Months of Data", "12", col6)

    st.markdown("---")

    # Analytical questions per chapter
    st.subheader("How This Analysis is Structured")
    st.markdown("""
    This dashboard looks at one big question across six chapters.
    Each chapter builds on the previous one, moving from understanding what is being prescribed,
    to where the money goes, to who is overspending, to predicting and forecasting future overspending.
    """)

    chapters = [
        {
            "chapter": "Chapter 0 - Building the Data",
            "question": "How do we combine, clean and prepare 12 monthly prescription files into one reliable dataset and what data quality issues emerge?",
            "color": "#e8f8f7"
        },
        {
            "chapter": "Chapter 1 - What is NHS Prescribing?",
            "question": "Which drug categories account for the highest prescription volumes and costs in 2025 and where does cost diverge from volume?",
            "color": "#e8f8f7"
        },
        {
            "chapter": "Chapter 2 - Where is the Money Going?",
            "question": "Which ICBs and regions consistently spend the most per prescription across all 12 months and is this driven by drug mix, volume, or prescribing behaviour?",
            "color": "#e8f8f7"
        },
        {
            "chapter": "Chapter 3 - Who is Overspending?",
            "question": "Which GP practices show the largest and most persistent gap between their actual spending and what would be expected for a practice in their region?",
            "color": "#e8f8f7"
        },
        {
            "chapter": "Chapter 4 - Can We Predict Overspending?",
            "question": "Using drug category, prescription volume, region, month, and quarter as inputs, can we build a model that accurately predicts GP practice-level spending and identifies at-risk practices?",
            "color": "#e8f8f7"
        },
        {
            "chapter": "Chapter 5 - Can We Forecast Spikes?",
            "question": "Using monthly spending data from January to October 2025, can we forecast November and December spending accurately enough for NHS budget planning?",
            "color": "#e8f8f7"
        },
        {
            "chapter": "Chapter 6 - Does Time of Year Explain Spikes?",
            "question": "Which drug categories show seasonal patterns across 2025 and does this seasonality vary by region, suggesting local factors are amplifying overspending at specific times of year?",
            "color": "#e8f8f7"
        }
    ]

    for ch in chapters:
        st.markdown(f"""
        <div style='background-color:{ch["color"]}; padding:15px; 
        border-radius:8px; margin-bottom:10px; 
        border-left:4px solid #20B2AA;'>
        <strong>{ch["chapter"]}</strong><br>
        <em>{ch["question"]}</em>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # How chapters connect
    st.subheader("The Story Arc")
    st.markdown("""
    | Step | Chapter | Question |
    |------|---------|----------|
    | 1 | Chapter 1 | **What** is being prescribed and at what cost? |
    | 2 | Chapter 2 | **Where** geographically is the money going? |
    | 3 | Chapter 3 | **Who** is already overspending? |
    | 4 | Chapter 4 | **Can we predict** which practices will overspend next? |
    | 5 | Chapter 5 | **Can we forecast when** the overspending will spike? |
    | 6 | Chapter 6 | **Why** do spikes happen, is it seasonal? |
    """)

    st.markdown("""
    > **The thread connecting all chapters:** Geography answers *where*, 
    seasonality answers *when*, and the prediction work answers *who* and *how much*. 
    We proved that prescribing behaviour, not procurement or regional funding,
    is the primary driver of NHS cost variation.
    """)





# ============================================================
# PAGE 2 — CHAPTER 0: BUILDING THE DATA
# ============================================================
elif page == "Chapter 0 - Building the Data":

    st.title("Chapter 0 - Building the Data")
    st.markdown("---")

    # Analytical question
    st.markdown("""
    <div style='background-color:#20B2AA; padding:15px; border-radius:8px; color:white;'>
    <strong>Analytical Question:</strong> How do we combine, clean and prepare 12 monthly 
    prescription files into one reliable dataset and what data quality issues emerge 
    that could affect every finding that follows?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Context
    st.markdown("""
    Before any analysis can happen, the data must be trustworthy. We started with 12 separate 
    monthly files one for each month of 2025. This chapter explains how they were combined, 
    what was cleaned, and what problems were discovered along the way. Every finding in every 
    chapter depends on this step being done correctly.
    """)

    st.markdown("---")

    # KPI cards
    st.subheader("Key Numbers")
    col1, col2, col3, col4 = st.columns(4)
    animated_metric("Raw Monthly Files", "12 CSVs", col1)
    animated_metric("Total Rows After Merging", "217.7M", col2)
    animated_metric("Final Columns", "18", col3)
    animated_metric("Engineered Columns Added", "4", col4)

    st.markdown("---")

    # Dataset stats table
    st.subheader("What Happened to the Data")
    st.markdown("""
    The table below shows the key facts about the final cleaned dataset. 
    Each row represents a decision made during the cleaning process.
    """)

    ch0 = pd.read_parquet(DATA + 'ch0_summary.parquet')
    st.dataframe(ch0, use_container_width=True, hide_index=True)

    st.markdown("""
    **What this tells us:** The dataset is large which contains 217.7 million rows but clean. 
    Rows were only removed when the practice could not be identified or when no drug 
    cost was recorded. Every remaining row represents a real prescription with a 
    verified cost attached to a known GP practice.
    """)

    st.markdown("---")

    # Engineered columns
    st.subheader("New Columns Created")
    st.markdown("""
    Four columns were created that did not exist in the raw data. 
    These are used in every chapter of the analysis.
    """)

    engineered = pd.DataFrame({
        'Column': ['COST_PER_ITEM', 'NIC_RATIO', 'MONTH', 'QUARTER'],
        'How it is calculated': [
            'ACTUAL_COST divided by ITEMS',
            'ACTUAL_COST divided by NIC (list price)',
            'Extracted from YEAR_MONTH',
            'Derived from MONTH (1-3=Q1, 4-6=Q2, etc)'
        ],
        'Used in': [
            'Chapters 2 and 3 - cost per prescription comparisons',
            'Chapters 2, 3, and 4 - pricing efficiency analysis',
            'Chapters 5 and 6 - seasonal and forecast analysis',
            'Chapter 4 - predictive model input'
        ],
        'Why it matters': [
            'Allows fair comparison between practices of different sizes',
            'Shows whether practices pay close to or below list price',
            'Enables monthly trend and seasonality analysis',
            'Captures quarterly patterns in prescribing behaviour'
        ]
    })
    st.dataframe(engineered, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Data quality issues
    st.subheader("Data Quality Issues Found")
    st.markdown("""
    Several problems were discovered during cleaning that affected how the analysis was designed.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='background-color:#fff3cd; padding:15px; border-radius:8px; 
        border-left:4px solid #ffc107; margin-bottom:10px;'>
        <strong>⚠️ Truncated ICB Names</strong><br>
        The raw data contained 76 variations of ICB names due to text being cut off. 
        These were manually fixed to the correct 42 ICB names using a lookup table.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color:#fff3cd; padding:15px; border-radius:8px; 
        border-left:4px solid #ffc107; margin-bottom:10px;'>
        <strong>⚠️ 10 Practices Renamed Mid-Year</strong><br>
        10 GP practices changed their name during 2025. All analysis groups by 
        PRACTICE_CODE not name so these practices are treated as one entity 
        throughout the full year.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color:#fff3cd; padding:15px; border-radius:8px; 
        border-left:4px solid #ffc107; margin-bottom:10px;'>
        <strong>⚠️ Category 18 Anomaly</strong><br>
        Category 18 (Preparations used in Diagnosis: X-ray contrast media) had only 49 
        prescriptions across the entire year, a data entry anomaly. It was excluded from 
        all chapter analyses to avoid distorting results.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background-color:#fff3cd; padding:15px; border-radius:8px; 
        border-left:4px solid #ffc107; margin-bottom:10px;'>
        <strong>⚠️ GP vs Specialist Services Mixed</strong><br>
        The dataset does not cleanly separate GP practices from specialist services 
        (COVID units, urgent care, anticoagulation clinics). A 3-stage behaviour filter 
        was applied in Chapter 3 to isolate real GP practices.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Limitation box
    st.markdown("""
    <div style='background-color:#f8d7da; padding:15px; border-radius:8px; 
    border-left:4px solid #dc3545;'>
    <strong>🔴 Key Limitation Running Through Every Chapter</strong><br>
    The EPD SNOMED dataset contains no demographic, deprivation, age, disease prevalence, 
    or climate data. We can show WHAT is being prescribed and WHERE it costs most. 
    We can prove that prescribing behaviour but not procurement or volume, is the primary 
    driver of cost variation. What we cannot explain is WHY individual practices make 
    different prescribing choices, as that requires patient clinical data not available 
    in this dataset.
    </div>
    """, unsafe_allow_html=True)





# ============================================================
# PAGE 3 — CHAPTER 1: WHAT IS NHS PRESCRIBING?
# ============================================================
elif page == "Chapter 1 - What is NHS Prescribing?":

    st.title("Chapter 1 - What is NHS Prescribing?")
    st.markdown("---")

    # Analytical question
    st.markdown("""
    <div style='background-color:#20B2AA; padding:15px; border-radius:8px; color:white;'>
    <strong>Analytical Question:</strong> Which drug categories account for the highest 
    prescription volumes and costs in 2025 and where does cost diverge from volume, 
    revealing which categories carry a disproportionate financial burden?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Context
    st.markdown("""
    Before we can spot overspending, we need to understand what the NHS is actually buying. 
    The key insight is not just which category is most expensive, it is whether the most 
    prescribed drugs are also the most expensive. When volume and cost tell different stories, 
    the NHS has a hidden cost problem that standard reporting misses.
    """)

    st.markdown("---")

    # KPI cards
    st.subheader("Key Numbers")
    col1, col2, col3, col4 = st.columns(4)
    animated_metric("Total Spend", "£10.54B", col1)
    animated_metric("Total Prescriptions", "1.27B", col2)
    animated_metric("Most Expensive Category", "Endocrine £2.23B", col3)
    animated_metric("Highest Cost Per Item", "Stoma Appliance £53.69", col4)

    st.markdown("---")

    # Load data
    ch1 = pd.read_parquet(DATA + 'ch1_summary.parquet')

    # Clean category names
    ch1['Category'] = ch1['BNF_CHAPTER_CODE'].str.split(':').str[1].str.strip()

    # --- Bar chart — top 10 by cost ---
    st.subheader("Which Drug Categories Cost the Most?")
    st.markdown("""
    This chart shows total NHS spending per drug category across all of 2025. 
    Look for which categories dominate the budget and whether you would expect 
    them to be the most expensive based on how common they are.
    """)

    top10_cost = ch1.nlargest(10, 'total_cost_millions')
    fig1 = px.bar(
        top10_cost,
        x='total_cost_millions',
        y='Category',
        orientation='h',
        color='total_cost_millions',
        color_continuous_scale='Teal',
        labels={'total_cost_millions': 'Total Cost (£ Millions)', 'Category': ''},
        text='total_cost_millions'
    )
    fig1.update_traces(texttemplate='£%{text:.0f}M', textposition='auto')
    fig1.update_layout(
        height=450,
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **What this tells us:** The Endocrine System is the most expensive category at £2.23B 
    representing 21% of the entire NHS prescribing budget. This is despite it being only the 3rd most 
    prescribed category by volume. The cost burden is driven by drug pricing, not how 
    frequently these drugs are given out.
    """)

    st.markdown("---")

    # --- Bar chart — top 10 by volume ---
    st.subheader("Which Drug Categories are Prescribed the Most?")
    st.markdown("""
    Now look at the same categories ranked by number of prescriptions instead of cost. 
    Notice which categories appear at the top here but were lower in the cost chart above.
    """)

    top10_vol = ch1.nlargest(10, 'total_items_millions')
    fig2 = px.bar(
        top10_vol,
        x='total_items_millions',
        y='Category',
        orientation='h',
        color='total_items_millions',
        color_continuous_scale='Purples',
        labels={'total_items_millions': 'Total Prescriptions (Millions)', 'Category': ''},
        text='total_items_millions'
    )
    fig2.update_traces(texttemplate='%{text:.0f}M', textposition='auto')
    fig2.update_layout(
        height=450,
        showlegend=False,
        coloraxis_showscale=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **What this tells us:** Cardiovascular System leads with 388 million prescriptions
    representing 30.6% of all NHS prescribing yet ranks only 4th in cost. This is because most 
    cardiovascular drugs are cheap generics prescribed constantly. A finance director 
    and a clinical director are looking at completely different priority lists from 
    the same dataset.
    """)

    st.markdown("---")

    # --- Scatter plot — volume vs cost ---
    st.subheader("Where Do Cost and Volume Diverge?")
    st.markdown("""
    This chart plots both dimensions together. Each bubble is a drug category with 
    its position showing total volume (x-axis) and total cost (y-axis).
    Bigger bubbles mean higher cost per item. The dotted lines show the average 
    volume and average cost, dividing the chart into four quadrants. Hover over 
    any bubble to see the category name and exact values.
    """)

    # Calculate mean values for center lines
    mean_items = ch1['total_items_millions'].mean()
    mean_cost = ch1['total_cost_millions'].mean()

    fig3 = px.scatter(
    ch1,
    x='total_items_millions',
    y='total_cost_millions',
    size='cost_per_item',
    color='cost_per_item',
    hover_name='Category',
    color_continuous_scale='RdYlGn_r',
    range_color=[0, 55],
    labels={
        'total_items_millions': 'Total Prescriptions (Millions)',
        'total_cost_millions': 'Total Cost (£ Millions)',
        'cost_per_item': 'Cost Per Item (£)'
        }
    )

    # Add vertical dotted line at mean volume
    fig3.add_vline(
    x=mean_items,
    line_dash='dot',
    line_color='grey',
    line_width=1.5
    )

    # Add horizontal dotted line at mean cost
    fig3.add_hline(
    y=mean_cost,
    line_dash='dot',
    line_color='grey',
    line_width=1.5
    )

    # Add quadrant labels
    fig3.add_annotation(x=5, y=1900, text="High Cost<br>Low Volume",
                    showarrow=False, font=dict(size=10, color='grey'),
                    align='center')
    fig3.add_annotation(x=250, y=1900, text="High Cost<br>High Volume",
                    showarrow=False, font=dict(size=10, color='grey'),
                    align='center')
    fig3.add_annotation(x=30, y=10, text="Low Cost<br>Low Volume",
                    showarrow=False, font=dict(size=10, color='grey'),
                    align='center')
    fig3.add_annotation(x=250, y=50, text="Low Cost<br>High Volume",
                    showarrow=False, font=dict(size=10, color='grey'),
                    align='center')

    fig3.update_layout(height=550)
    fig3.update_coloraxes(colorbar=dict(tickvals=[0, 10, 20, 30, 40, 50]))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    **What this tells us:** Most drug categories sit in the bottom-left quadrant which is
    low volume and low cost. The standout finding is Endocrine System which is sitting 
    above the mean cost line with moderate volume, its expensive drug pricing drives 
    the entire NHS budget. Cardiovascular sits furthest right with high cost the most prescribed 
    category and expensive in total spend, though each individual prescription is 
    cheap because most are generic drugs. CNS sits in the high cost, high volume 
    quadrant alongside Cardiovascular. The red bubble (bottom-left) 
    is Stoma Appliances, highest cost per item at £53.69 but very low volume, 
    making it a hidden financial risk that standard volume reporting would miss completely.
    """)

    st.markdown("---")

    # Unexpected finding box
    st.markdown("""
    <div style='background-color:#e8f4f8; padding:15px; border-radius:8px; 
    border-left:4px solid #17a2b8; margin-bottom:10px;'>
    <strong>🔍 Unexpected Finding - Hidden Expensive Drugs</strong><br>
    Within the high-cost categories, individual drugs carry extreme prices that 
    barely register in volume charts. Nitazoxanide costs £11,056 per item and 
    Letermovir costs £6,619 per item. These drugs are prescribed so rarely they 
    are invisible in volume analysis but each prescription represents a significant 
    financial event that standard reporting would miss.
    </div>
    """, unsafe_allow_html=True)

    # Limitation box
    st.markdown("""
    <div style='background-color:#f8d7da; padding:15px; border-radius:8px; 
    border-left:4px solid #dc3545;'>
    <strong>🔴 Limitation</strong><br>
    This chapter shows what is being prescribed and at what cost. It cannot explain 
    why certain categories cost more than others. That requires clinical data about 
    patient conditions, treatment guidelines, and formulary decisions that are not 
    available in this dataset.
    </div>
    """, unsafe_allow_html=True)




# ============================================================
# PAGE 4 — CHAPTER 2: WHERE IS THE MONEY GOING?
# ============================================================
elif page == "Chapter 2 - Where is the Money Going?":

    st.title("Chapter 2 - Where is the Money Going?")
    st.markdown("---")

    # Analytical question
    st.markdown("""
    <div style='background-color:#20B2AA; padding:15px; border-radius:8px; color:white;'>
    <strong>Analytical Question:</strong> Which ICBs and regions consistently spend the most 
    per prescription across all 12 months of 2025 and is this variation driven by drug mix, 
    volume, or prescribing behaviour?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Context
    st.markdown("""
    England is not uniform. A GP practice in rural Lancashire serves a completely different 
    population to one in central London. We want to know whether certain areas consistently 
    spend more per prescription and critically whether this is something the NHS can change.
    """)

    st.markdown("---")

    # KPI cards
    st.subheader("Key Numbers")
    col1, col2, col3, col4 = st.columns(4)
    animated_metric("Most Expensive ICB", "Hampshire £22.14", col1)
    animated_metric("Cheapest ICB", "NW London £18.04", col2)
    animated_metric("Gap Per Prescription", "£4.10", col3)
    animated_metric("Regional Correlation", ">0.96 all regions", col4)

    st.markdown("---")

    # Load data
    ch2_icb = pd.read_parquet(DATA + 'ch2_icb_summary.parquet')
    ch2_regional = pd.read_parquet(DATA + 'ch2_regional_summary.parquet')
    ch2_corr = pd.read_parquet(DATA + 'ch2_correlation.parquet')
    ch2_icb_heatmap = pd.read_parquet(DATA + 'ch2_icb_heatmap.parquet')
    ch2_map = pd.read_parquet(DATA + 'ch2_map.parquet')
    ch2_seasonal = pd.read_parquet(DATA + 'ch2_seasonal.parquet')

    # Clean ICB names
    ch2_icb['ICB'] = ch2_icb['ICB_NAME'].str.replace('NHS ', '').str.replace('INTEGRATED CARE BOARD', '').str.strip().str.title()

    # --- Bar chart — top 10 and bottom 10 ICBs ---
    st.subheader("Which ICBs Spend the Most and Least Per Prescription?")
    st.markdown("""
    This chart shows the top 10 most expensive and bottom 10 cheapest ICBs by average 
    cost per prescription across all 12 months of 2025. A persistent gap between top 
    and bottom suggests structural differences, not random variation.
    """)

    top10 = ch2_icb.nlargest(10, 'avg_cost_per_item')
    bottom10 = ch2_icb.nsmallest(10, 'avg_cost_per_item')
    combined = pd.concat([top10, bottom10])
    combined['color'] = combined['avg_cost_per_item'].apply(
        lambda x: 'Most Expensive' if x >= top10['avg_cost_per_item'].min() else 'Cheapest'
    )

    fig_icb = px.bar(
        combined.sort_values('avg_cost_per_item'),
        x='avg_cost_per_item',
        y='ICB',
        color='color',
        color_discrete_map={'Most Expensive': '#20B2AA', 'Cheapest': '#7B68EE'},
        orientation='h',
        labels={'avg_cost_per_item': 'Avg Cost Per Prescription (£)', 'ICB': ''},
        text='avg_cost_per_item'
    )
    fig_icb.update_traces(texttemplate='£%{text:.2f}', textposition='auto')
    fig_icb.update_layout(height=600, legend_title='Category')
    st.plotly_chart(fig_icb, use_container_width=True)

    st.markdown("""
    **What this tells us:** Hampshire and Isle of Wight tops at £22.14 while NW London 
    sits at £18.04, a £4.10 gap per prescription. Across millions of prescriptions this 
    represents hundreds of millions of pounds difference. Six of the top ten most expensive 
    ICBs are in the South East.
    """)

    st.markdown("---")

    # --- Line chart — monthly regional trends ---
    st.subheader("How Does Spending Change Month by Month Across Regions?")
    st.markdown("""
    This chart shows how the average cost per prescription changed month by month 
    across all 7 NHS regions. Use the dropdown to focus on a specific region. 
    Look for whether regions move together or differently.
    """)

    regions = ['All Regions'] + sorted(ch2_regional['REGIONAL_OFFICE'].unique().tolist())
    selected_region = st.selectbox("Select Region:", regions)

    if selected_region == 'All Regions':
        filtered = ch2_regional
    else:
        filtered = ch2_regional[ch2_regional['REGIONAL_OFFICE'] == selected_region]

    month_labels = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                    7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    fig_regional = px.line(
        filtered,
        x='MONTH',
        y='avg_cost_per_item',
        color='REGIONAL_OFFICE',
        markers=True,
        labels={
            'avg_cost_per_item': 'Avg Cost Per Prescription (£)',
            'MONTH': 'Month',
            'REGIONAL_OFFICE': 'Region'
        }
    )
    fig_regional.update_layout(
        height=450,
        xaxis=dict(tickvals=list(range(1,13)),
                   ticktext=list(month_labels.values()))
    )
    st.plotly_chart(fig_regional, use_container_width=True)

    st.markdown("""
    **What this tells us:** All 7 regions are correlated above 0.96, they rise and fall 
    at exactly the same time. The February dip appears in every region (28-day month = 
    11.7 million fewer prescriptions). The September-to-December rise is driven by flu 
    vaccines and Endocrine spending. The pattern is national, only the scale differs 
    by region.
    """)

    st.markdown("---")

    # --- Regional correlation heatmap ---
    st.subheader("How Correlated Are NHS Regions With Each Other?")
    st.markdown("""
    This heatmap shows how closely each pair of NHS regions follows the same 
    spending pattern. A score of 1.0 means perfectly synchronised, they move 
    identically month by month. A score close to 0 means they move independently.
    """)

    fig_corr = px.imshow(
        ch2_corr,
        color_continuous_scale='YlGnBu',
        color_continuous_midpoint=0.9800,
        zmin=0.9600, zmax=1.0000,
        text_auto='.4f',
        labels={'color': 'Correlation'},
        aspect='auto',
        range_color=[0.9600, 1.0000]
    )
    fig_corr.update_layout(height=500)
    fig_corr.update_coloraxes(colorbar=dict(tickvals=[0.9600, 0.9700, 0.9800, 0.9900, 1.0000]))
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("""
    **What this tells us:** Every pair of regions has a correlation above 0.96
    shown by the warm teal colour throughout. The diagonal is darkest (1.0 
    each region perfectly correlates with itself). The slightly lighter cells 
    involve South West, it has the lowest correlations with North West (0.9641) 
    and North East & Yorkshire (0.9705), though still above 0.96. This confirms 
    all 7 NHS regions follow the same seasonal pattern, the February dip and 
    October spike happen everywhere simultaneously. The difference between regions 
    is how much they spend, not when they spend it.
    """)

    st.markdown("---")

    # --- ICB heatmap --- 
    st.subheader("All 42 ICBs: Average Cost Per Prescription Across 12 Months")
    st.markdown("""
    This heatmap shows every ICB's average cost per prescription for each month 
    of 2025. Dark orange-red colours mean higher spending dark blue means lower 
    spending. ICBs are sorted from most to least expensive. Look for which ICBs 
    stay the same colour every month, these are the persistent structural outliers.
    """)

    # Pivot for heatmap
    icb_order = ch2_icb_heatmap.groupby('ICB_NAME')['avg_cost_per_item'].mean().sort_values(ascending=False).index.tolist()
    icb_pivot = ch2_icb_heatmap.pivot(
        index='ICB_NAME', columns='MONTH', values='avg_cost_per_item'
    )
    icb_pivot = icb_pivot.reindex(icb_order)
    icb_pivot.columns = list(month_labels.values())
    # Clean ICB names for display
    icb_pivot.index = icb_pivot.index.str.replace('NHS ', '').str.replace(
        'INTEGRATED CARE BOARD', '').str.strip().str.title()
    
    fig_icb_heat = px.imshow(
        icb_pivot,
        color_continuous_scale='RdYlBu_r',
        labels={'color': 'Avg Cost/Item (£)'},
        aspect='auto',
        text_auto='.1f'
    )
    fig_icb_heat.update_layout(height=900)
    st.plotly_chart(fig_icb_heat, use_container_width=True)

    st.markdown("""
    **What this tells us:** Hampshire and Isle of Wight sits at the top in dark 
    orange-red every single month confirming it is the most expensive ICB 
    structurally, not just occasionally. Sussex and Herefordshire follow closely 
    in warm orange. North West London sits at the bottom in dark blue every month, 
    consistently the cheapest. South Yorkshire and North West London anchor the 
    bottom in cool blue. This persistence of the same ICBs in the same colours 
    across all 12 months rules out random variation this is structural difference 
    in prescribing behaviour, not seasonal noise.
    """)

    st.markdown("---")

    # --- 4 Maps ---
    st.subheader("Geographic Spending Patterns Across England")
    st.markdown("""
    These maps show how NHS spending varies geographically across England. 
    Use the dropdown to switch between different spending measures.
    """)

    map_type = st.selectbox(
        "Select Map:",
        [
            "Average Cost Per Prescription",
            "Total Spend (£ Millions)",
            "Total Prescriptions (Millions)",
            "Seasonal Change: Feb vs Dec"
        ]
    )

    # Match ICB names to GeoJSON
    # Get feature names from GeoJSON
    geojson_names = [f['properties']['ICB23NM'] for f in geojson['features']]

    if map_type == "Average Cost Per Prescription":
        fig_map = px.choropleth_mapbox(
            ch2_map,
            geojson=geojson,
            locations='ICB_GEOJSON',
            featureidkey='properties.ICB23NM',
            color='avg_cost_per_item',
            color_continuous_scale='RdYlBu_r',
            mapbox_style='carto-positron',
            zoom=4.8,
            center={'lat': 52.5, 'lon': -1.5},
            labels={'avg_cost_per_item': 'Avg Cost/Prescription (£)'},
            hover_name='ICB_NAME',
            hover_data={'avg_cost_per_item': ':.2f', 'ICB_GEOJSON': False}
        )
        title = "Average Cost Per Prescription by ICB"

    elif map_type == "Total Spend (£ Millions)":
        fig_map = px.choropleth_mapbox(
            ch2_map,
            geojson=geojson,
            locations='ICB_GEOJSON',
            featureidkey='properties.ICB23NM',
            color='total_cost_millions',
            color_continuous_scale='Reds',
            mapbox_style='carto-positron',
            zoom=4.8,
            center={'lat': 52.5, 'lon': -1.5},
            labels={'total_cost_millions': 'Total Spend (£M)'},
            hover_name='ICB_NAME',
            hover_data={'total_cost_millions': ':.1f', 'ICB_GEOJSON': False}
        )
        title = "Total Spend by ICB (£ Millions)"

    elif map_type == "Total Prescriptions (Millions)":
        fig_map = px.choropleth_mapbox(
            ch2_map,
            geojson=geojson,
            locations='ICB_GEOJSON',
            featureidkey='properties.ICB23NM',
            color='total_items_millions',
            color_continuous_scale='Blues',
            mapbox_style='carto-positron',
            zoom=4.8,
            center={'lat': 52.5, 'lon': -1.5},
            labels={'total_items_millions': 'Total Prescriptions (M)'},
            hover_name='ICB_NAME',
            hover_data={'total_items_millions': ':.1f', 'ICB_GEOJSON': False}
        )
        title = "Total Prescriptions by ICB (Millions)"

    else:
        # Feb vs Dec seasonal map
        feb = ch2_seasonal[ch2_seasonal['MONTH'] == 2][['ICB_NAME', 'avg_cost_per_item']].rename(
            columns={'avg_cost_per_item': 'feb_cost'})
        dec = ch2_seasonal[ch2_seasonal['MONTH'] == 12][['ICB_NAME', 'avg_cost_per_item']].rename(
            columns={'avg_cost_per_item': 'dec_cost'})
        seasonal_diff = feb.merge(dec, on='ICB_NAME')
        seasonal_diff['change'] = (seasonal_diff['dec_cost'] - seasonal_diff['feb_cost']).round(2)
        seasonal_diff['ICB_GEOJSON'] = seasonal_diff['ICB_NAME'].map(ch2_map.set_index('ICB_NAME')['ICB_GEOJSON'])

        fig_map = px.choropleth_mapbox(
            seasonal_diff,
            geojson=geojson,
            locations='ICB_GEOJSON',
            featureidkey='properties.ICB23NM',
            color='change',
            color_continuous_scale='RdYlGn',
            mapbox_style='carto-positron',
            zoom=4.8,
            center={'lat': 52.5, 'lon': -1.5},
            labels={'change': 'Dec vs Feb Change (£)'},
            hover_name='ICB_NAME',
            hover_data={'change': ':.2f', 'ICB_GEOJSON': False}
        )
        title = "Seasonal Change: Dec vs Feb Cost Per Prescription"

    fig_map.update_layout(height=600, title=title)
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("""
    **What the maps tell us:** The average cost map shows a clear South East cluster 
    of expensive ICBs. The total spend map tells a different story, North East and 
    Yorkshire is highest in total because of larger population and volume. The 
    prescriptions map confirms volume drives total spend, not cost per item. 
    The seasonal map shows Dec vs Feb change is consistent across all regions 
    confirming the national synchronisation found in the correlation heatmap.
    """)

    st.markdown("---")

    st.subheader("Top 5 Most Expensive ICBs: Monthly Trend")
    st.markdown("""
    This chart shows the monthly spending trend for the top 5 most expensive ICBs. 
    Look carefully at Surrey Heartlands, it behaves differently to the other 4 ICBs 
    in October and November.
    """)

    ch2_top5 = pd.read_parquet(DATA + 'ch2_top5_monthly.parquet')

    # Shorten ICB names for legend
    ch2_top5['ICB_SHORT'] = ch2_top5['ICB_NAME'].str.replace(
        'NHS ', '').str.replace('INTEGRATED CARE BOARD', '').str.strip().str.title()

    fig_top5 = px.line(
        ch2_top5,
        x='MONTH',
        y='avg_cost_per_item',
        color='ICB_SHORT',
        markers=True,
        labels={
            'avg_cost_per_item': 'Avg Cost Per Prescription (£)',
            'MONTH': 'Month',
            'ICB_SHORT': 'ICB'
        }
    )
    fig_top5.update_layout(
        height=450,
        xaxis=dict(
            tickvals=list(range(1,13)),
            ticktext=list(month_labels.values())
        )
    )

    # Highlight Oct-Nov dip for Surrey Heartlands
    fig_top5.add_vrect(
        x0=9.5, x1=11.5,
        fillcolor='yellow', opacity=0.15,
        layer='below', line_width=0,
        annotation_text='Surrey Heartlands anomaly',
        annotation_position='top left',
        annotation_font_size=10
    )

    st.plotly_chart(fig_top5, use_container_width=True)

    st.markdown("""
    **What this tells us:** All 5 ICBs follow the same upward trend from September 
    except Surrey Heartlands, which drops in October and November highlighted in yellow. 
    Every other expensive ICB rises during this period due to flu vaccines and winter 
    prescribing. Surrey Heartlands is the only one that diverges, suggesting a change 
    in local prescribing behaviour during those months that requires clinical investigation.
    """)

    # Anomaly box
    st.markdown("""
    <div style='background-color:#fff3cd; padding:15px; border-radius:8px; 
    border-left:4px solid #ffc107; margin-bottom:10px;'>
    <strong>⚠️ Anomaly - Surrey Heartlands</strong><br>
    Surrey Heartlands ICB shows an unusual drop in October and November, the opposite 
    direction to every other region. This anomaly has no clear explanation in the dataset 
    and would need clinical investigation to understand what changed in prescribing 
    behaviour during those months.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Unexpected finding box
    st.markdown("""
    <div style='background-color:#e8f4f8; padding:15px; border-radius:8px; 
    border-left:4px solid #17a2b8; margin-bottom:10px;'>
    <strong>🔍 Unexpected Finding - Behaviour Not Procurement</strong><br>
    We expected expensive regions to be paying higher prices. The opposite is true, 
    high-cost ICBs actually receive BIGGER NHS discounts AND prescribe LOWER volumes 
    than cheap ICBs. The cause is prescribing behaviour, the choice between branded 
    and generic drugs, not procurement inefficiency. This is something the NHS can 
    actually change through clinical guidelines and formulary decisions.
    </div>
    """, unsafe_allow_html=True)

    # Proven finding box
    st.markdown("""
    <div style='background-color:#d4edda; padding:15px; border-radius:8px; 
    border-left:4px solid #28a745; margin-bottom:10px;'>
    <strong>✅ Proven Finding</strong><br>
    Geographic variation is caused by prescribing behaviour proven by eliminating 
    two alternative explanations using the data itself. It is NOT procurement 
    (expensive ICBs get bigger discounts, not smaller). It is NOT volume 
    (cheap ICBs prescribe more, not less). What remains is the choice of which 
    drugs to prescribe, branded vs generic.
    </div>
    """, unsafe_allow_html=True)

    # Limitation box
    st.markdown("""
    <div style='background-color:#f8d7da; padding:15px; border-radius:8px; 
    border-left:4px solid #dc3545;'>
    <strong>🔴 Limitation</strong><br>
    While we proved prescribing behaviour drives cost variation, we cannot explain 
    why practices in different regions make different prescribing choices. Patient age, 
    deprivation levels, and disease prevalence are plausible causes but are completely 
    absent from this dataset.
    </div>
    """, unsafe_allow_html=True)





# ============================================================
# PAGE 5 — CHAPTER 3: WHO IS OVERSPENDING?
# ============================================================
elif page == "Chapter 3 - Who is Overspending?":

    st.title("Chapter 3 - Who is Overspending?")
    st.markdown("---")

    # Analytical question
    st.markdown("""
    <div style='background-color:#20B2AA; padding:15px; border-radius:8px; color:white;'>
    <strong>Analytical Question:</strong> Which GP practices show the largest and most 
    persistent gap between their actual spending and what would be expected for a practice 
    in their region and do these outlier practices cluster within specific ICBs or 
    consistently overspend on the same drug categories?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Context
    st.markdown("""
    Now we zoom into individual GP practices. We are not asking which practices spend 
    the most in total, we are asking which practices spend significantly MORE than 
    similar practices around them, month after month. A practice that overspends once 
    might have a legitimate reason. A practice that overspends every single month is 
    a systemic problem that demands investigation.
    """)

    st.markdown("---")

    # KPI cards
    st.subheader("Key Numbers")
    col1, col2, col3, col4 = st.columns(4)
    animated_metric("GP Practices Analysed", "5,764", col1)
    animated_metric("Persistent Overspenders", "288 (97.6%/month)", col2)
    animated_metric("Persistent Underspenders", "288 (98.3%/month)", col3)
    animated_metric("Top Overspender", "Modality Partnership +£14.56", col4)

    st.markdown("---")

    # Load data
    ch3 = pd.read_parquet(DATA + 'ch3_outliers.parquet')

    # Classify practices
    top5_pct = ch3['avg_residual'].quantile(0.95)
    bottom5_pct = ch3['avg_residual'].quantile(0.05)
    ch3['category'] = 'Normal'
    ch3.loc[ch3['avg_residual'] >= top5_pct, 'category'] = 'Overspender'
    ch3.loc[ch3['avg_residual'] <= bottom5_pct, 'category'] = 'Underspender'

    # --- Scatter plot ---
    st.subheader("Actual vs Expected Cost Per Prescription")
    st.markdown("""
    Each dot is a GP practice. Teal dots spend more than expected for their region 
    these are the overspenders. Purple dots spend less than expected underspenders. 
    Grey dots are within normal range. The orange star is ARCH HEALTHCARE, the most 
    extreme underspender in the entire dataset. Hover over any dot to see the 
    practice name, ICB, and exact values.
    """)

    color_map = {
        'Overspender': '#20B2AA',
        'Underspender': '#7B68EE',
        'Normal': 'lightgrey'
    }

    # Separate ARCH HEALTHCARE from the rest
    arch = ch3[ch3['PRACTICE_NAME'] == 'ARCH HEALTHCARE']
    rest = ch3[ch3['PRACTICE_NAME'] != 'ARCH HEALTHCARE']

    # Add jitter to make points more visible
    jitter_strength = 0.05
    rest_jittered = rest.copy()
    rest_jittered['avg_expected_cost'] = rest['avg_expected_cost'] + np.random.uniform(
        -jitter_strength, jitter_strength, len(rest))
    rest_jittered['avg_practice_cost'] = rest['avg_practice_cost'] + np.random.uniform(
        -jitter_strength, jitter_strength, len(rest))
    
    # Add size column based on category
    rest_jittered['point_size'] = rest_jittered['category'].map({
        'Normal': 4,
        'Overspender': 6,
        'Underspender': 6
    })

    fig_scatter = px.scatter(
        rest_jittered,
        x='avg_expected_cost',
        y='avg_practice_cost',
        color='category',
        color_discrete_map=color_map,
        size='point_size',
        size_max=8,
        hover_name='PRACTICE_NAME',
        hover_data={
            'ICB_NAME': True,
            'REGIONAL_OFFICE': True,
            'avg_residual': ':.2f',
            'category': False
        },
        labels={
            'avg_expected_cost': 'Expected Cost Per Prescription (£)',
            'avg_practice_cost': 'Actual Cost Per Prescription (£)',
            'avg_residual': 'Residual (£)',
            'ICB_NAME': 'ICB',
            'REGIONAL_OFFICE': 'Region'
        },
        opacity=0.6
    )

    # Set different opacity per category
    for trace in fig_scatter.data:
        if trace.name == 'Normal':
            trace.marker.opacity = 0.4
            trace.marker.line = dict(color='grey', width=1)
        elif trace.name == 'Overspender':
            trace.marker.opacity = 0.6
            trace.marker.line = dict(color='#148f8f', width=1)
            # Darker teal border for overspenders
        elif trace.name == 'Underspender':
            trace.marker.opacity = 0.6
            trace.marker.line = dict(color='#4a3fb5', width=1)
      
    # Add ARCH HEALTHCARE as orange star
    fig_scatter.add_trace(
        go.Scatter(
            x=arch['avg_expected_cost'],
            y=arch['avg_practice_cost'],
            mode='markers',
            marker=dict(
                symbol='star',
                size=10,
                color='orange',
            ),
            name='ARCH HEALTHCARE (Anomaly)',
            hovertemplate=(
                '<b>ARCH HEALTHCARE</b><br>'
                'ICB: NHS Sussex<br>'
                'Actual: £%{y:.2f}<br>'
                'Expected: £%{x:.2f}<br>'
                'Residual: -£13.54<extra></extra>'
            )
        )
    )

    # Add diagonal line
    min_val = 17
    max_val = 24
    fig_scatter.add_shape(
        type='line',
        x0=min_val, y0=min_val,
        x1=max_val, y1=max_val,
        line=dict(color='black', width=1, dash='dash')
    )

    fig_scatter.update_layout(
        height=550,
        legend_title='Practice Type',
        xaxis=dict(range=[17, 24], title='Expected Cost Per Prescription (£)'),
        yaxis=dict(range=[0, 40], title='Actual Cost Per Prescription (£)')
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


    st.markdown("""
    **What this tells us:** Most practices cluster tightly along the diagonal line
    their actual and expected costs are very close. But two clear groups pull away: 
    288 practices consistently sit above the line (overspenders) and 288 consistently 
    sit below (underspenders). 97.6% of overspenders were above expected every single 
    month of 2025. This is not a one-off anomaly, it is a structural pattern.
    The orange star (ARCH HEALTHCARE) sits far below all other practices, it is 
    an extraordinary outlier investigated separately below.
    """)

    # ARCH HEALTHCARE anomaly box
    st.markdown("""
    <div style='background-color:#fff3cd; padding:15px; border-radius:8px; 
    border-left:4px solid #ffc107; margin-bottom:10px;'>
    <strong>⚠️ Anomaly - ARCH HEALTHCARE (G81689)</strong><br>
    ARCH HEALTHCARE in Sussex is the most extreme underspender in the entire dataset 
    spending only £8.37 per prescription against its ICB average of £21.92, a residual 
    of -£13.54. Despite being active all 12 months and prescribing across 20 of 21 drug 
    categories with 90,803 total items, this practice spends extraordinarily little per 
    prescription. It is confirmed as a legitimate NHS GP practice at Morley Street, Brighton. 
    No data anomaly explains this, it appears to reflect genuinely exceptional prescribing 
    efficiency that the NHS should investigate and potentially replicate across other practices.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Filter options
    st.subheader("Top 20 Persistent Overspending Practices")
    st.markdown("""
    These practices spend the most above their ICB average per prescription
    month after month. The bar length shows how much above the expected cost 
    each practice spends on average. Use the filters to focus on a specific region or ICB
    for both overspending and underspending practices.
    """)

    col1, col2 = st.columns(2)
    with col1:
        regions_filter = ['All Regions'] + sorted(ch3['REGIONAL_OFFICE'].unique().tolist())
        selected_region_ch3 = st.selectbox("Filter by Region:", regions_filter, key='ch3_region')
    with col2:
        if selected_region_ch3 != 'All Regions':
            icbs_filter = ['All ICBs'] + sorted(
                ch3[ch3['REGIONAL_OFFICE'] == selected_region_ch3]['ICB_NAME'].unique().tolist()
            )
        else:
            icbs_filter = ['All ICBs'] + sorted(ch3['ICB_NAME'].unique().tolist())
        selected_icb_ch3 = st.selectbox("Filter by ICB:", icbs_filter, key='ch3_icb')

    # Apply filters
    filtered_ch3 = ch3.copy()
    if selected_region_ch3 != 'All Regions':
        filtered_ch3 = filtered_ch3[filtered_ch3['REGIONAL_OFFICE'] == selected_region_ch3]
    if selected_icb_ch3 != 'All ICBs':
        filtered_ch3 = filtered_ch3[filtered_ch3['ICB_NAME'] == selected_icb_ch3]

    # --- Top 20 overspenders bar chart ---
    top20_over = filtered_ch3.nlargest(20, 'avg_residual').copy()
    top20_over['short_name'] = top20_over['PRACTICE_NAME'].str[:35]

    fig_over = px.bar(
        top20_over.sort_values('avg_residual'),
        x='avg_residual',
        y='short_name',
        orientation='h',
        color_discrete_sequence=['#20B2AA'],
        hover_name='PRACTICE_NAME',
        hover_data={
            'ICB_NAME': True,
            'REGIONAL_OFFICE': True,
            'avg_practice_cost': ':.2f',
            'avg_expected_cost': ':.2f',
            'short_name': False
        },
        labels={
            'avg_residual': 'Residual - Above Expected (£)',
            'short_name': '',
            'ICB_NAME': 'ICB',
            'REGIONAL_OFFICE': 'Region',
            'avg_practice_cost': 'Actual Cost (£)',
            'avg_expected_cost': 'Expected Cost (£)'
        },
        text='avg_residual'
    )
    fig_over.update_traces(texttemplate='+£%{text:.2f}', textposition='auto')
    fig_over.update_layout(height=600)
    st.plotly_chart(fig_over, use_container_width=True)

    st.markdown("""
    **What this tells us:** MODALITY PARTNERSHIP AWC in West Yorkshire spends £14.56 
    above its ICB average every prescription. These practices are distributed across 
    all 7 NHS regions. This is not a regional problem, it is a practice-level 
    behaviour problem happening everywhere.
    """)

    st.markdown("---")

    # --- Top 20 underspenders bar chart ---
    st.subheader("Top 20 Persistent Underspending Practices")
    st.markdown("""
    These practices spend the most below their ICB average they are the most 
    efficient prescribers in England. The bar length shows how much below the 
    expected cost each practice spends. Understanding what they do differently 
    could help the NHS reduce costs everywhere.
    """)

    top20_under = filtered_ch3.nsmallest(20, 'avg_residual').copy()
    top20_under['short_name'] = top20_under['PRACTICE_NAME'].str[:35]

    fig_under = px.bar(
        top20_under.sort_values('avg_residual', ascending=False),
        x='avg_residual',
        y='short_name',
        orientation='h',
        color_discrete_sequence=['#7B68EE'],
        hover_name='PRACTICE_NAME',
        hover_data={
            'ICB_NAME': True,
            'REGIONAL_OFFICE': True,
            'avg_practice_cost': ':.2f',
            'avg_expected_cost': ':.2f',
            'short_name': False
        },
        labels={
            'avg_residual': 'Residual - Below Expected (£)',
            'short_name': '',
            'ICB_NAME': 'ICB',
            'REGIONAL_OFFICE': 'Region',
            'avg_practice_cost': 'Actual Cost (£)',
            'avg_expected_cost': 'Expected Cost (£)'
        },
        text='avg_residual'
    )
    fig_under.update_traces(texttemplate='£%{text:.2f}', textposition='auto')
    fig_under.update_layout(height=600)
    st.plotly_chart(fig_under, use_container_width=True)

    st.markdown("""
    **What this tells us:** ARCH HEALTHCARE in Sussex spends £13.54 below its ICB 
    average despite prescribing across 20 of 21 drug categories. Sussex is one of 
    the most expensive ICBs yet this practice prescribes extremely efficiently
    proving that very low cost prescribing is genuinely achievable within any region.
    """)

    st.markdown("---")

    # --- Geographic Distribution Map ---
    st.subheader("Geographic Distribution of Outlier Practices")
    st.markdown("""
    This map shows where overspending and underspending practices are concentrated 
    across England. Use the dropdown to switch between overspenders and underspenders. 
    Darker colours mean more outlier practices in that ICB.
    """)

    # Load ICB counts and map data
    ch3_icb_counts = pd.read_parquet(DATA + 'ch3_icb_counts.parquet')
    ch2_map_data = pd.read_parquet(DATA + 'ch2_map.parquet')

    # Add GeoJSON matched names to ICB counts
    ch3_icb_counts['ICB_GEOJSON'] = ch3_icb_counts['ICB_NAME'].map(
        ch2_map_data.set_index('ICB_NAME')['ICB_GEOJSON']
    )

    # Dropdown to switch between over and underspenders
    map_category = st.selectbox(
        "Select Category:",
        ["Overspenders", "Underspenders"],
        key='ch3_map_category'
    )

    if map_category == "Overspenders":
        map_data = ch3_icb_counts[ch3_icb_counts['category'] == 'Overspender'].copy()
        color_scale = 'Reds'
        color_col = 'count'
        label = 'Number of \nOverspending Practices'
    else:
        map_data = ch3_icb_counts[ch3_icb_counts['category'] == 'Underspender'].copy()
        color_scale = 'Blues'
        color_col = 'count'
        label = 'Number of \nUnderspending Practices'

    # Show top 5 ICBs alongside map
    col_map, col_list = st.columns([2, 1])

    with col_list:
        if map_category == "Overspenders":
            st.markdown("**Top 5 ICBs - Overspenders**")
            top5_icbs = ch3_icb_counts[
                ch3_icb_counts['category'] == 'Overspender'
            ].nlargest(5, 'count')[['ICB_NAME', 'count']].copy()
            top5_icbs['ICB_NAME'] = top5_icbs['ICB_NAME'].str.replace(
                'NHS ', '').str.replace('INTEGRATED CARE BOARD', '').str.strip().str.title()
            top5_icbs.columns = ['ICB', 'Practices']
            top5_icbs = top5_icbs.reset_index(drop=True)
            top5_icbs.index += 1
            st.dataframe(top5_icbs, use_container_width=True)
        else:
            st.markdown("**Top 5 ICBs - Underspenders**")
            top5_icbs = ch3_icb_counts[
                ch3_icb_counts['category'] == 'Underspender'
            ].nlargest(5, 'count')[['ICB_NAME', 'count']].copy()
            top5_icbs['ICB_NAME'] = top5_icbs['ICB_NAME'].str.replace(
                'NHS ', '').str.replace('INTEGRATED CARE BOARD', '').str.strip().str.title()
            top5_icbs.columns = ['ICB', 'Practices']
            top5_icbs = top5_icbs.reset_index(drop=True)
            top5_icbs.index += 1
            st.dataframe(top5_icbs, use_container_width=True)
    with col_map:
        fig_map_ch3 = px.choropleth_mapbox(
            map_data,
            geojson=geojson,
            locations='ICB_GEOJSON',
            featureidkey='properties.ICB23NM',
            color=color_col,
            color_continuous_scale=color_scale,
            mapbox_style='carto-positron',
            zoom=4.8,
            center={'lat': 52.5, 'lon': -1.5},
            labels={color_col: label},
            hover_name='ICB_NAME',
            hover_data={color_col: True, 'ICB_GEOJSON': False}
        )
        fig_map_ch3.update_layout(height=600)
        st.plotly_chart(fig_map_ch3, use_container_width=True)

    st.markdown("""
    **What this tells us:** Overspending practices are spread across all regions and
    this is not a single regional problem. West Yorkshire stands out on both maps, 
    appearing in the top 5 for both overspenders (19 practices) and underspenders 
    (29 practices) confirming that the problem is practice-level behaviour, 
    not regional funding or structure.
    """)

    st.markdown("---")

    # Unexpected findings
    st.markdown("""
    <div style='background-color:#e8f4f8; padding:15px; border-radius:8px; 
    border-left:4px solid #17a2b8; margin-bottom:10px;'>
    <strong>🔍 Unexpected Finding 1 - West Yorkshire Tops Both Lists</strong><br>
    West Yorkshire has the most overspending practices (19) AND the most 
    underspending practices (29). Same region, same commissioner, same funding but 
    completely different practice behaviour. This single fact proves the problem 
    is individual practice decisions, not regional structure or funding allocation.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color:#e8f4f8; padding:15px; border-radius:8px; 
    border-left:4px solid #17a2b8; margin-bottom:10px;'>
    <strong>🔍 Unexpected Finding 2 - It is Not Endocrine or Cardiovascular</strong><br>
    The drug categories driving overspending are NOT the biggest budget categories. 
    The problem is in Nutrition and Blood (+£12.95), Dressings (+£11.66), and 
    Other Drugs (+£10.73) mid-range categories where the choice between 
    branded and generic drugs has the biggest financial impact.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color:#e8f4f8; padding:15px; border-radius:8px; 
    border-left:4px solid #17a2b8; margin-bottom:10px;'>
    <strong>🔍 Unexpected Finding 3 - Overspenders Pay More AND Get Smaller Discounts</strong><br>
    Overspending practices have a NIC ratio of 0.9400 (smallest discount) while 
    underspending practices have 0.9269 (biggest discount). Both factors work 
    against overspending practices simultaneously as they choose more expensive 
    drugs AND receive worse prices.
    </div>
    """, unsafe_allow_html=True)

    # Limitation box
    st.markdown("""
    <div style='background-color:#f8d7da; padding:15px; border-radius:8px; 
    border-left:4px solid #dc3545;'>
    <strong>🔴 Limitation</strong><br>
    The 3-stage filter used to isolate real GP practices may still include a small 
    number of specialist services among the 5,764 practices. The EPD SNOMED dataset 
    has no clean GP vs specialist flag, this is a known data quality limitation. 
    Additionally, the analysis identifies WHERE overspending occurs but cannot 
    explain WHY individual practices make different prescribing choices without 
    patient demographic and clinical data.
    </div>
    """, unsafe_allow_html=True)





# ============================================================
# PAGE 6 — CHAPTER 4: CAN WE PREDICT OVERSPENDING?
# ============================================================
elif page == "Chapter 4 - Can We Predict Overspending?":

    st.title("Chapter 4 - Can We Predict Overspending?")
    st.markdown("---")

    # Analytical question
    st.markdown("""
    <div style='background-color:#20B2AA; padding:15px; border-radius:8px; color:white;'>
    <strong>Analytical Question:</strong> Using drug category, prescription volume, region, 
    month, and quarter as inputs, can we build a model that accurately predicts GP 
    practice-level spending and identifies at-risk practices before overspending happens?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Context
    st.markdown("""
    This is the core of the project. If we can predict what a practice should be spending, 
    we can flag the ones heading towards overspending before it happens, giving NHS 
    commissioners time to intervene rather than discovering the problem after the money 
    is already gone.
    """)

    st.markdown("---")

    # KPI cards
    st.subheader("Key Numbers")
    col1, col2, col3, col4 = st.columns(4)
    animated_metric("Random Forest Accuracy", "R² = 0.9541", col1)
    animated_metric("Baseline Accuracy", "R² = 0.5512", col2)
    animated_metric("At-Risk Practices", "2,417", col3)
    animated_metric("Top At-Risk Practice", "Grovehurst Surgery +59.87%", col4)

    st.markdown("---")

    # Load data
    ch4_models = pd.read_parquet(DATA + 'ch4_model_comparison.parquet')
    ch4_features = pd.read_parquet(DATA + 'ch4_feature_importance.parquet')
    ch4_at_risk = pd.read_parquet(DATA + 'ch4_at_risk.parquet')

    # --- Model comparison bar chart ---
    st.subheader("Which Model Predicts Best?")
    st.markdown("""
    We tested three models. This chart shows how much of the cost variation each 
    model explained. A score of 1.0 means perfect prediction. A score of 0.55 
    means the model only explains just over half the variation which is not good enough 
    for real-world use.
    """)

    fig_models = px.bar(
        ch4_models,
        x='Model',
        y='R2',
        color='Model',
        color_discrete_sequence=["#3963cd", "#7A20B2", "#29B5D1"],
        text='R2',
        labels={'R2': 'R² Score (Accuracy)', 'Model': ''}
    )
    fig_models.update_traces(texttemplate='%{text:.4f}', textposition='auto')
    fig_models.update_layout(
        height=400,
        showlegend=False,
        yaxis=dict(range=[0, 1.05])
    )
    st.plotly_chart(fig_models, use_container_width=True)

    st.markdown("""
    **What this tells us:** Linear Regression only explained 55% of cost variation as 
    it assumed spending increases in a straight line which is not how NHS prescribing 
    works. Random Forest explained 95.4% by learning complex interactions between 
    drug type, volume, and region. The 40-percentage-point improvement justifies 
    the more complex model. Gradient Boosting performed well at 94.1% but slightly 
    below Random Forest so Random Forest was selected.
    """)

    st.markdown("---")

    # --- Feature importance bar chart ---
    st.subheader("What Drives the Predictions?")
    st.markdown("""
    This chart shows which inputs the Random Forest relied on most to make its 
    predictions. A higher percentage means that variable explains more of the 
    cost variation.
    """)

    ch4_features_sorted = ch4_features.sort_values('importance', ascending=True)

    fig_features = px.bar(
        ch4_features_sorted,
        x='importance',
        y='feature',
        orientation='h',
        color='importance',
        color_continuous_scale='Teal',
        text='importance',
        labels={
            'importance': 'Feature Importance (%)',
            'feature': ''
        }
    )
    fig_features.update_traces(texttemplate='%{text:.2f}%', textposition='auto')
    fig_features.update_layout(
        height=400,
        showlegend=False,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_features, use_container_width=True)

    st.markdown("""
    **What this tells us:** Prescription volume (ITEMS) alone accounts for 61.25% 
    of the prediction. Drug category adds another 15.83%. Together volume and drug 
    type explain 77% of all cost variation. Geography (ICB) contributes only 0.66% 
    confirming the Chapter 2 finding that geographic variation is driven by prescribing 
    behaviour, not location. Time variables (Month, Quarter) contribute almost nothing. 
    Costs are driven by what is prescribed, not when.
    """)

    st.markdown("---")

    # --- Predicted vs actual scatter plot ---
    st.subheader("How Accurate Are the Predictions?")
    st.markdown("""
    Each dot is one practice-drug-month combination from the November-December 
    test set. Dots on the diagonal line are perfectly predicted. Teal dots below 
    the line are where actual cost exceeded prediction. These are the at-risk cases 
    the model flags for investigation.
    """)

    # Load full test results
    ch4_test = pd.read_parquet(DATA + 'ch4_test_results.parquet')

    # Separate normal and at-risk
    normal = ch4_test[ch4_test['at_risk'] == False]
    at_risk = ch4_test[ch4_test['at_risk'] == True]

    fig_pred = go.Figure()

    # Normal practices in grey
    fig_pred.add_trace(go.Scattergl(
        x=normal['total_actual_cost'],
        y=normal['predicted_cost'],
        mode='markers',
        marker=dict(color='grey', size=4.5, opacity=0.5),
        name='Normal Practices',
        hovertemplate=(
            'Actual: £%{x:,.0f}<br>'
            'Predicted: £%{y:,.0f}<extra></extra>'
        )
    ))

    # At-risk practices in teal
    fig_pred.add_trace(go.Scattergl(
        x=at_risk['total_actual_cost'],
        y=at_risk['predicted_cost'],
        mode='markers',
        marker=dict(color='#20B2AA', size=5, opacity=0.6),
        name='At-Risk Practices',
        hovertemplate=(
            'Actual: £%{x:,.0f}<br>'
            'Predicted: £%{y:,.0f}<extra></extra>'
        )
    ))

    # Add diagonal line
    max_val = ch4_test['total_actual_cost'].max() * 1.04
    fig_pred.add_shape(
    type='line',
    x0=0, y0=0,
    x1=max_val, y1=max_val,
    line=dict(color='black', width=1, dash='dash'),
    layer='above'  # Forces it above all traces
    )

    fig_pred.add_trace(go.Scattergl(
    x=[None], y=[None],
    mode='lines',
    line=dict(color='black', width=1, dash='dash'),
    name='Perfect Prediction',
    showlegend=True
    ))

    fig_pred.update_layout(
        height=550,
        xaxis_title='Actual Cost (£)',
        yaxis_title='Predicted Cost (£)',
        legend=dict(x=0.02, y=0.98)
    )
    st.plotly_chart(fig_pred, use_container_width=True)

    st.markdown("""
    **What this tells us:** The at-risk practices (teal) cluster below the diagonal,
    their actual cost was higher than the model predicted. The further below the 
    diagonal, the bigger the gap. These are the practices NHS commissioners should 
    investigate first.
    """)

    st.markdown("---")

    # --- At-risk practices bar chart ---
    st.subheader("Top 20 At-Risk GP Practices")
    st.markdown("""
    These are the practices the NHS should investigate first, ranked by how far 
    their actual spending exceeded the model's prediction. Use the filters to 
    focus on a specific region or ICB.
    """)

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        ch4_at_risk['REGIONAL_OFFICE'] = ch4_at_risk['ICB_NAME'].str.extract(
            r'NHS (\w+)'
        )
        regions_ch4 = ['All Regions'] + sorted(
            ch4_at_risk['ICB_NAME'].str.split('AND').str[0].str.replace(
                'NHS', '').str.strip().unique().tolist()
        )
        # Simple region filter using ICB name
        icbs_ch4 = ['All ICBs'] + sorted(ch4_at_risk['ICB_NAME'].unique().tolist())
        selected_icb_ch4 = st.selectbox("Filter by ICB:", icbs_ch4, key='ch4_icb')

    filtered_ch4 = ch4_at_risk.copy()
    if selected_icb_ch4 != 'All ICBs':
        filtered_ch4 = filtered_ch4[filtered_ch4['ICB_NAME'] == selected_icb_ch4]

    top20_risk = filtered_ch4.nlargest(20, 'pct_overspend').copy()
    top20_risk['short_name'] = top20_risk['PRACTICE_NAME'].str[:35]
    top20_risk['ICB_SHORT'] = top20_risk['ICB_NAME'].str.replace(
        'NHS ', '').str.replace('INTEGRATED CARE BOARD', '').str.strip().str.title()

    fig_risk = px.bar(
        top20_risk.sort_values('pct_overspend'),
        x='pct_overspend',
        y='short_name',
        orientation='h',
        color='pct_overspend',
        color_continuous_scale='Reds',
        text='pct_overspend',
        hover_name='PRACTICE_NAME',
        hover_data={
            'ICB_SHORT': True,
            'total_actual_cost': ':.0f',
            'total_predicted_cost': ':.0f',
            'short_name': False,
            'pct_overspend': False
        },
        labels={
            'pct_overspend': '% Above Predicted',
            'short_name': '',
            'ICB_SHORT': 'ICB',
            'total_actual_cost': 'Actual Cost (£)',
            'total_predicted_cost': 'Predicted Cost (£)'
        }
    )
    fig_risk.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    fig_risk.update_layout(
        height=600,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_risk, use_container_width=True)

    st.markdown("""
    **What this tells us:** GROVEHURST SURGERY in Kent spent 59.87% above predicted 
    in November-December 2025. Hampshire and Isle of Wight has 4 practices in the 
    top 20 which is consistent with its position as the most expensive ICB in Chapter 2. 
    FARNHAM DENE MEDICAL PRACTICE appears in both the Chapter 3 persistent overspender 
    list AND this Chapter 4 at-risk list. Two completely different analytical methods 
    flagging the same practice, strongly validating both findings.
    """)

    st.markdown("---")

    # Unexpected finding
    st.markdown("""
    <div style='background-color:#e8f4f8; padding:15px; border-radius:8px; 
    border-left:4px solid #17a2b8; margin-bottom:10px;'>
    <strong>🔍 Unexpected Finding - Model Fails Where It Matters Most</strong><br>
    The model is least accurate exactly where NHS commissioners need it most,
    Endocrine System (£6,029 average error per practice-drug-month) and Hampshire 
    ICBs (£1,644 average error). This is not a modelling weakness, it reflects 
    missing demographic and clinical data that would explain why these specific 
    combinations are harder to predict. The model cannot compensate for information 
    that simply does not exist in the dataset.
    </div>
    """, unsafe_allow_html=True)

    # Limitation box
    st.markdown("""
    <div style='background-color:#f8d7da; padding:15px; border-radius:8px; 
    border-left:4px solid #dc3545;'>
    <strong>🔴 Limitation</strong><br>
    The model identifies WHICH practices are at risk but cannot explain WHY they 
    overspend, root cause investigation requires patient demographic and clinical 
    data not available in this dataset. The test window is only 2 months (Nov-Dec) 
    which is a small evaluation period. November and December are atypical months 
    (flu vaccination programme and year-end prescribing rush) so results may not 
    represent typical monthly accuracy.
    </div>
    """, unsafe_allow_html=True)





# ============================================================
# PAGE 7 — CHAPTER 5: CAN WE FORECAST SPIKES?
# ============================================================
elif page == "Chapter 5 - Can We Forecast Spikes?":

    st.title("Chapter 5 - Can We Forecast Spikes?")
    st.markdown("---")

    # Analytical question
    st.markdown("""
    <div style='background-color:#20B2AA; padding:15px; border-radius:8px; color:white;'>
    <strong>Analytical Question:</strong> Using monthly spending data from January to October 
    2025, can we build a forecasting model that accurately predicts November and December 
    spending and is the prediction error small enough in pounds and percentage terms 
    to make this a credible planning tool for NHS finance teams?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Context
    st.markdown("""
    Knowing which practices overspend is powerful. But knowing WHEN the overspending 
    is likely to happen gives the NHS time to act before the money is gone. Using the 
    first 10 months of 2025 as training data, we forecast November and December spending 
    for the highest-risk drug categories and test how close our predictions are in 
    actual pounds.
    """)

    st.markdown("---")

    # KPI cards
    st.subheader("Key Numbers")
    col1, col2, col3, col4 = st.columns(4)
    animated_metric("National Forecast MAPE", "5.29%", col1)
    animated_metric("Regional Forecast MAPE", "3.93%", col2)
    animated_metric("Best Predicted Category", "CNS £0.06M error", col3)
    animated_metric("Worst Predicted Category", "Dressings 7.11%", col4)

    st.markdown("---")

    # Load data
    ch5_monthly = pd.read_parquet(DATA + 'ch5_monthly.parquet')
    ch5_national = pd.read_parquet(DATA + 'ch5_national.parquet')
    ch5_hampshire = pd.read_parquet(DATA + 'ch5_hampshire.parquet')

    # Short names mapping
    short_names = {
        '06: Endocrine System': 'Endocrine',
        '02: Cardiovascular System': 'Cardiovascular',
        '09: Nutrition and Blood': 'Nutrition & Blood',
        '20: Dressings': 'Dressings',
        '04: Central Nervous System': 'CNS'
    }

    # Predicted values for Nov-Dec
    predictions = {
        'Endocrine': {11: 200.4, 12: 202.5},
        'Cardiovascular': {11: 92.3, 12: 92.2},
        'Nutrition & Blood': {11: 74.8, 12: 74.3},
        'Dressings': {11: 14.1, 12: 14.0},
        'CNS': {11: 126.3, 12: 127.4}
    }

    month_labels = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                    7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    # --- Line chart — actual vs forecast ---
    st.subheader("Actual vs Forecasted Monthly Spending: High Risk Categories")
    st.markdown("""
    Grey lines show historical spending January to October. Coloured solid lines 
    show actual November and December spending. Coloured dashed lines show the 
    model's forecast for November and December. The vertical dotted line marks 
    where history ends and forecasting begins. Use the dropdown to focus on a 
    specific category.
    """)

    categories = ['All Categories'] + list(short_names.values())
    selected_cat = st.selectbox("Select Category:", categories, key='ch5_cat')

    fig_line = go.Figure()

    colors = {
        'Endocrine': '#2ca02c',
        'Cardiovascular': '#1f77b4',
        'Nutrition & Blood': '#d62728',
        'Dressings': '#9467bd',
        'CNS': '#ff7f0e'
    }

    for cat_code, cat_name in short_names.items():
        if selected_cat != 'All Categories' and cat_name != selected_cat:
            continue

        cat_data = ch5_monthly[ch5_monthly['BNF_CHAPTER_CODE'] == cat_code].sort_values('MONTH')
        color = colors[cat_name]

        # Historical Jan-Oct in grey
        hist = cat_data[cat_data['MONTH'] <= 11]
        fig_line.add_trace(go.Scatter(
            x=hist['MONTH'],
            y=hist['total_cost_millions'],
            mode='lines+markers',
            line=dict(color='lightgrey', width=2),
            marker=dict(size=4),
            showlegend=False,
            hovertemplate=f'{cat_name}<br>Month: %{{x}}<br>Actual: £%{{y:.1f}}M<extra></extra>'
        ))

        # Actual Nov-Dec in color
        actual = cat_data[cat_data['MONTH'] >= 11]
        fig_line.add_trace(go.Scatter(
            x=actual['MONTH'],
            y=actual['total_cost_millions'],
            mode='lines+markers',
            line=dict(color=color, width=2),
            marker=dict(size=6),
            name=f'{cat_name} (Actual)',
            hovertemplate=f'{cat_name}<br>Month: %{{x}}<br>Actual: £%{{y:.1f}}M<extra></extra>'
        ))

        # Forecasted Nov-Dec as dashed
        pred_months = [11, 12]
        pred_vals = [predictions[cat_name][m] for m in pred_months]
        # Connect from Oct
        oct_val = cat_data[cat_data['MONTH'] == 10]['total_cost_millions'].values[0]
        fig_line.add_trace(go.Scatter(
            x=pred_months,
            y=[oct_val] + pred_vals,
            mode='lines+markers',
            line=dict(color=color, width=2, dash='dash'),
            marker=dict(size=6, symbol='square'),
            name=f'{cat_name} (Forecast)',
            hovertemplate=f'{cat_name}<br>Month: %{{x}}<br>Forecast: £%{{y:.1f}}M<extra></extra>'
        ))

    # Vertical line at Nov
    fig_line.add_vline(
        x=10.2,
        line_dash='dot',
        line_color='black',
        line_width=1.5,
        annotation_text='Forecast →',
        annotation_position='top right'
    )

    fig_line.update_layout(
        height=500,
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=list(month_labels.values()),
            title='Month'
        ),
        yaxis_title='Total Cost (£ Millions)',
        legend=dict(x=1.01, y=1, xanchor='left')
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    **What this tells us:** All 5 categories follow their historical trends into 
    November and December. The dashed forecast lines closely track the solid actual 
    lines, the model has learned the spending patterns from the first 10 months and 
    extrapolated them accurately. The model overestimated 4 of 5 categories — 
    predicting slightly more than actually spent, which is the right direction 
    for budget planning.
    """)

    st.markdown("---")

    # --- Bar chart — actual vs predicted Nov-Dec ---
    st.subheader("How Close Were the Forecasts?: Nov-Dec 2025 Average")
    st.markdown("""
    This chart directly compares what the model predicted against what actually 
    happened for each category in November and December combined. The closer the 
    bars are to each other, the more accurate the forecast. (The bar chart shows 
    the average of November and December combined)
    """)

    ch5_national_melted = ch5_national.melt(
        id_vars=['category', 'mape'],
        value_vars=['actual', 'predicted'],
        var_name='type',
        value_name='cost'
    )

    fig_bar = px.bar(
        ch5_national_melted,
        x='category',
        y='cost',
        color='type',
        barmode='group',
        color_discrete_map={'actual': '#20B2AA', 'predicted': '#7B68EE'},
        text='cost',
        labels={
            'cost': 'Avg Cost Nov-Dec (£ Millions)',
            'category': 'Drug Category',
            'type': 'Type'
        }
    )
    fig_bar.update_traces(texttemplate='£%{text:.1f}M', textposition='auto')
    fig_bar.update_layout(height=450, yaxis=dict(range=[0, 230]))
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
    **What this tells us:** CNS was predicted almost perfectly £126.92M actual 
    vs £126.86M predicted, a difference of only £0.06M. The model overestimated 
    4 of 5 categories which is the right direction for budget planning, it prompts 
    finance teams to set aside slightly too much rather than too little, reducing 
    the risk of an unfunded overspend.
    """)

    st.markdown("---")

    # --- MAPE per category ---
    st.subheader("Forecast Accuracy Per Category")
    st.markdown("""
    MAPE (Mean Absolute Percentage Error) shows how far off the forecast was 
    as a percentage of the actual value. A lower MAPE means a more accurate forecast. 
    NHS budget planning typically works within a 5-10% tolerance.
    (MAPE looks at each month separately)
    """)

    fig_mape = px.bar(
        ch5_national.sort_values('mape', ascending=True),
        x='mape',
        y='category',
        orientation='h',
        color='mape',
        color_continuous_scale='RdYlGn_r',
        text='mape',
        labels={
            'mape': 'MAPE (%)',
            'category': ''
        }
    )
    fig_mape.update_traces(texttemplate='%{text:.2f}%', textposition='auto')
    fig_mape.update_layout(
        height=350,
        coloraxis_showscale=False,
        xaxis=dict(range=[0, 9])
    )
    st.plotly_chart(fig_mape, use_container_width=True)

    st.markdown("""
    **What this tells us:** Endocrine System, the most expensive category 
    was forecast most accurately at 3.59% MAPE. Dressings was the hardest to 
    forecast at 7.11%, but this directly connects to Chapter 6 where Dressings 
    is also the most seasonally volatile category. All 5 categories are predicted 
    within 8% well within NHS budget planning tolerance.
    """)

    st.markdown("---")

    # --- Hampshire + Endocrine line chart ---
    st.subheader("Regional Deep-Dive Hampshire & Isle of Wight: Endocrine System")
    st.markdown("""
    This chart shows a regional forecast for the highest-risk ICB and drug category 
    combination. Hampshire and Isle of Wight was selected because it is the most 
    expensive ICB (Chapter 2) and showed the highest prediction error (Chapter 4). 
    Grey shows historical spending, teal shows actual Nov-Dec, red dashed shows forecast.
    """)

    fig_hamp = go.Figure()

    # Historical in grey
    hist_hamp = ch5_hampshire[ch5_hampshire['MONTH'] <= 11]
    fig_hamp.add_trace(go.Scatter(
        x=hist_hamp['MONTH'],
        y=hist_hamp['total_cost_millions'],
        mode='lines+markers',
        line=dict(color='lightgrey', width=2),
        marker=dict(size=4),
        name='Historical (Actual)',
        hovertemplate='Month: %{x}<br>Actual: £%{y:.2f}M<extra></extra>'
    ))

    # Actual Nov-Dec in teal
    actual_hamp = ch5_hampshire[ch5_hampshire['MONTH'] >= 11]
    fig_hamp.add_trace(go.Scatter(
        x=actual_hamp['MONTH'],
        y=actual_hamp['total_cost_millions'],
        mode='lines+markers',
        line=dict(color='#20B2AA', width=2),
        marker=dict(size=8),
        name='Actual (Nov-Dec)',
        hovertemplate='Month: %{x}<br>Actual: £%{y:.2f}M<extra></extra>'
    ))

    # Forecast Nov-Dec in red dashed
    fig_hamp.add_trace(go.Scatter(
        x=[11, 12],
        y=[7.2372, 7.2460],
        mode='lines+markers',
        line=dict(color='#d62728', width=2, dash='dash'),
        marker=dict(size=8, symbol='square'),
        name='Forecasted (Nov-Dec)',
        hovertemplate='Month: %{x}<br>Forecast: £%{y:.2f}M<extra></extra>'
    ))

    # Vertical line
    fig_hamp.add_vline(
        x=10.3,
        line_dash='dot',
        line_color='black',
        line_width=1.5,
        annotation_text='Forecast →',
        annotation_position='top right'
    )

    fig_hamp.update_layout(
        height=450,
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=list(month_labels.values()),
            title='Month'
        ),
        yaxis_title='Total Cost (£ Millions)',
        legend=dict(x=0.02, y=0.98)
    )
    st.plotly_chart(fig_hamp, use_container_width=True)

    # Metrics below chart
    col1, col2, col3 = st.columns(3)
    col1.metric("Regional MAPE", "3.93%")
    col2.metric("Avg Error", "£0.27M")
    col3.metric("RMSE", "£0.31M")

    st.markdown("""
    **What this tells us:** Hampshire Endocrine forecast achieved 3.93% MAPE
    better than the national 5.29%. However this cannot be generalised. Hampshire 
    has a very consistent upward trend through the year which is easy for the model 
    to learn. Only one regional combination was tested so this cannot be used to 
    claim regional forecasting is always superior to national forecasting.
    """)

    st.markdown("---")

    # Unexpected finding
    st.markdown("""
    <div style='background-color:#e8f4f8; padding:15px; border-radius:8px; 
    border-left:4px solid #17a2b8; margin-bottom:10px;'>
    <strong>🔍 Unexpected Finding - Conservative Direction is Good for Budgeting</strong><br>
    The model overestimated 4 of 5 categories predicting slightly more spending 
    than actually occurred. This is the right direction for NHS budget planning: 
    it prompts finance teams to set aside marginally too much rather than too little, 
    reducing the risk of an unfunded overspend. This systematic overestimation is 
    small in scale but consistent enough to be a characteristic of the model rather 
    than random noise.
    </div>
    """, unsafe_allow_html=True)

    # Limitation box
    st.markdown("""
    <div style='background-color:#f8d7da; padding:15px; border-radius:8px; 
    border-left:4px solid #dc3545;'>
    <strong>🔴 Limitation</strong><br>
    ARIMA was rejected as it requires 30-50 data points but we only had 10 months 
    of training data. The lag feature requirement further reduced this to 7 effective 
    training points per category. November and December are atypical months (flu 
    vaccination programme and year-end prescribing rush) so forecast accuracy may 
    not represent typical months. Only one regional combination (Hampshire + Endocrine) 
    was tested as the results cannot be generalised to all ICB-category combinations.
    </div>
    """, unsafe_allow_html=True)





# ============================================================
# PAGE 8 — CHAPTER 6: DOES TIME OF YEAR EXPLAIN SPIKES?
# ============================================================
elif page == "Chapter 6 - Does Time of Year Explain Spikes?":

    st.title("Chapter 6 - Does Time of Year Explain Spikes?")
    st.markdown("---")

    # Analytical question
    st.markdown("""
    <div style='background-color:#20B2AA; padding:15px; border-radius:8px; color:white;'>
    <strong>Analytical Question:</strong> Which drug categories show seasonal patterns 
    across 2025 and does this seasonality vary by region, suggesting local factors 
    are amplifying overspending at specific times of year, requiring targeted regional 
    responses rather than a single national strategy?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Context
    st.markdown("""
    Now that we know where and when overspending happens, we ask the final question: 
    is any of this seasonal? Do certain medicines spike every winter? Does the North West 
    behave differently to the South East? And if seasonality exists, is it consistent 
    enough to be predicted and planned for or does it vary so much between regions 
    that a single national response would be inadequate?
    """)

    st.markdown("---")

    # KPI cards
    st.subheader("Key Numbers")
    col1, col2, col3, col4 = st.columns(4)
    animated_metric("Most Seasonal Category", "Dressings (0.72)", col1)
    animated_metric("Most Stable Category", "Other Drugs (0.10)", col2)
    animated_metric("October Vaccine Spike", "37x normal spending", col3)
    animated_metric("Regional Correlation", ">0.96 all regions", col4)

    st.markdown("---")

    # Load data
    ch6_seasonality = pd.read_parquet(DATA + 'ch6_seasonality.parquet')
    ch6_monthly = pd.read_parquet(DATA + 'ch6_monthly.parquet')
    ch6_regional = pd.read_parquet(DATA + 'ch6_regional.parquet')
    ch6_heatmap = pd.read_parquet(DATA + 'ch6_heatmap.parquet')

    month_labels = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                    7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    # --- Seasonality strength bar chart ---
    st.subheader("Which Drug Categories Are Most Seasonal?")
    st.markdown("""
    This chart ranks all 20 drug categories by how seasonal their spending is. 
    A score of 1.0 means all variation is explained by the time of year. 
    A score of 0 means spending is completely flat year-round. 
    \n**Important:** the strength score must always be read alongside the pound 
    value, a category can be highly seasonal but financially irrelevant if 
    its total spending is tiny.
    """)

    # Flag vaccines specially
    ch6_seasonality['label'] = ch6_seasonality['category'] + ' (' + \
        ch6_seasonality['strength'].round(2).astype(str) + ')'
    ch6_seasonality_sorted = ch6_seasonality.sort_values('strength', ascending=True)

    # Color vaccines differently
    ch6_seasonality_sorted['color'] = ch6_seasonality_sorted['category'].apply(
        lambda x: 'Special Case (Vaccines)' if x == 'Vaccines' else 'Other Categories'
    )

    fig_seasonal = px.bar(
        ch6_seasonality_sorted,
        x='strength',
        y='category',
        color='color',
        orientation='h',
        color_discrete_map={
            'Other Categories': '#20B2AA',
            'Special Case (Vaccines)': 'orange'
        },
        text='strength',
        hover_data={'range_millions': ':.2f', 'color': False},
        labels={
            'strength': 'Seasonality Strength (0-1)',
            'category': '',
            'range_millions': 'Spending Range (£M)'
        }
    )
    fig_seasonal.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_seasonal.update_layout(
        height=600,
        xaxis=dict(range=[0, 0.85]),
        legend_title='Category Type'
    )
    st.plotly_chart(fig_seasonal, use_container_width=True)

    st.markdown("""
    **What this tells us:** Anaesthesia scores highest at 0.72 but its total 
    spending only varies by £0.27M, financially irrelevant. Dressings matches 
    at 0.72 with a £2.54M range, both highly seasonal AND financially significant. 
    Vaccines appear unremarkable at 0.32 but have by far the largest absolute swing 
    at £79.43M, a 37x October spike. Other Drugs is the most stable at 0.10 and its
    spending barely changes month to month.
    """)

    # Unexpected finding — Vaccines
    st.markdown("""
    <div style='background-color:#fff3cd; padding:15px; border-radius:8px; 
    border-left:4px solid #ffc107; margin-bottom:10px;'>
    <strong>⚠️ Unexpected Finding - Vaccines Score Low But Spike Highest</strong><br>
    Vaccines score only 0.32 on the seasonality measure, seventeenth out of twenty
    making them appear unremarkable. But their absolute range is £79.43M, by far 
    the largest swing in the entire dataset. Spending sits at around £2.21M through 
    most of the year then jumps to £81.64M in October, a 37x spike. The metric 
    fails to capture this because it is one enormous concentrated event (the annual 
    flu vaccination programme), not gradual recurring seasonality. This is a planned 
    event the NHS already knows about, completely different from the organic clinical 
    seasonality seen in Dressings or CNS.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Monthly line chart with dropdown ---
    st.subheader("Monthly Spending Pattern by Drug Category")
    st.markdown("""
    Use the dropdown to select any drug category and see how its spending 
    changed month by month throughout 2025. Look for categories with clear 
    peaks and troughs versus categories that stay flat all year.
    """)

    # Short names mapping
    short_names_ch6 = {
        '01: Gastro-Intestinal System': 'Gastro-Intestinal',
        '02: Cardiovascular System': 'Cardiovascular',
        '03: Respiratory System': 'Respiratory',
        '04: Central Nervous System': 'CNS',
        '05: Infections': 'Infections',
        '06: Endocrine System': 'Endocrine',
        '07: Obstetrics, Gynaecology and Urinary-Tract Disorders': 'Obstetrics & Gynae',
        '08: Malignant Disease and Immunosuppression': 'Malignant Disease',
        '09: Nutrition and Blood': 'Nutrition & Blood',
        '10: Musculoskeletal and Joint Diseases': 'Musculoskeletal',
        '11: Eye': 'Eye',
        '12: Ear, Nose and Oropharynx': 'Ear Nose & Throat',
        '13: Skin': 'Skin',
        '14: Immunological Products and Vaccines': 'Vaccines',
        '15: Anaesthesia': 'Anaesthesia',
        '19: Other Drugs and Preparations': 'Other Drugs',
        '20: Dressings': 'Dressings',
        '21: Appliances': 'Appliances',
        '22: Incontinence Appliances': 'Incontinence',
        '23: Stoma Appliances': 'Stoma Appliances'
    }

    ch6_monthly['category_short'] = ch6_monthly['BNF_CHAPTER_CODE'].map(short_names_ch6)

    selected_cat_ch6 = st.selectbox(
        "Select Drug Category:",
        sorted(ch6_monthly['category_short'].dropna().unique().tolist()),
        key='ch6_cat'
    )

    cat_filtered = ch6_monthly[ch6_monthly['category_short'] == selected_cat_ch6]

    # Get seasonality strength for selected category
    cat_strength = ch6_seasonality[
        ch6_seasonality['category'] == selected_cat_ch6
    ]['strength'].values

    strength_text = f"Seasonality Strength: {cat_strength[0]:.2f}" if len(cat_strength) > 0 else ""

    fig_cat_line = px.line(
        cat_filtered,
        x='MONTH',
        y='total_cost_millions',
        markers=True,
        labels={
            'total_cost_millions': 'Total Cost (£ Millions)',
            'MONTH': 'Month'
        },
        color_discrete_sequence=['#20B2AA']
    )
    fig_cat_line.update_layout(
        height=350,
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=list(month_labels.values())
        ),
        title=f"{selected_cat_ch6} - Monthly Spending 2025 | {strength_text}"
    )
    fig_cat_line.add_annotation(
        text=strength_text,
        xref='paper', yref='paper',
        x=0.02, y=0.95,
        showarrow=False,
        font=dict(size=12, color='grey')
    )
    st.plotly_chart(fig_cat_line, use_container_width=True)

    st.markdown("---")

    # --- Regional comparison ---
    st.subheader("Does Seasonality Vary by Region?")
    st.markdown("""
    This chart shows whether all NHS regions follow the same seasonal pattern 
    or whether some regions spike at different times. Use the dropdown to switch 
    between key categories. Look for whether the lines move together (same timing) 
    or diverge (different timing).
    """)

    key_categories_ch6 = {
        '20: Dressings': 'Dressings',
        '04: Central Nervous System': 'CNS',
        '03: Respiratory System': 'Respiratory',
        '14: Immunological Products and Vaccines': 'Vaccines'
    }

    selected_regional_cat = st.selectbox(
        "Select Category:",
        list(key_categories_ch6.values()),
        key='ch6_regional_cat'
    )

    selected_code = [k for k, v in key_categories_ch6.items() 
                     if v == selected_regional_cat][0]
    regional_filtered = ch6_regional[ch6_regional['BNF_CHAPTER_CODE'] == selected_code]

    region_colors = {
        'EAST OF ENGLAND': '#1f77b4',
        'LONDON': '#ff7f0e',
        'MIDLANDS': '#2ca02c',
        'NORTH EAST AND YORKSHIRE': '#d62728',
        'NORTH WEST': '#9467bd',
        'SOUTH EAST': '#8c564b',
        'SOUTH WEST': '#e377c2'
    }

    fig_regional_ch6 = px.line(
        regional_filtered,
        x='MONTH',
        y='total_cost_millions',
        color='REGIONAL_OFFICE',
        markers=True,
        color_discrete_map=region_colors,
        labels={
            'total_cost_millions': 'Total Cost (£ Millions)',
            'MONTH': 'Month',
            'REGIONAL_OFFICE': 'Region'
        }
    )
    fig_regional_ch6.update_layout(
        height=450,
        xaxis=dict(
            tickvals=list(range(1, 13)),
            ticktext=list(month_labels.values())
        ),
        legend=dict(x=1.01, y=1, xanchor='left')
    )
    st.plotly_chart(fig_regional_ch6, use_container_width=True)

    st.markdown("""
    **What this tells us:** All 7 regions are synchronised as they rise and fall 
    in the same months. The difference is magnitude not timing. For Vaccines, 
    all regions spike in October simultaneously as national procurement planning 
    is sufficient. For Dressings and CNS, regions differ in how much they spend, targeted 
    regional responses are needed for these categories.
    """)

    st.markdown("---")

    # --- Heatmap ---
    st.subheader("Monthly Spending by NHS Region: Seasonal Heatmap")
    st.markdown("""
    This heatmap shows total monthly spending by region. Darker red means 
    higher spending. Look across the columns to see which months are consistently 
    expensive and across the rows to see which regions spend the most.
    """)

    ch6_heatmap_pivot = ch6_heatmap.pivot(
        index='REGIONAL_OFFICE',
        columns='MONTH',
        values='total_cost_millions'
    )
    ch6_heatmap_pivot.columns = list(month_labels.values())

    fig_heatmap = px.imshow(
        ch6_heatmap_pivot,
        color_continuous_scale='RdYlBu_r',
        zmin=70,
        zmax=210,
        labels={'color': 'Total Cost (£M)'},
        aspect='auto',
        text_auto='.0f'
    )
    fig_heatmap.update_layout(height=450)
    fig_heatmap.update_coloraxes(colorbar=dict(tickvals=[80, 100, 120, 140, 160, 180, 200]))
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("""
    **What this tells us:** October is the darkest column across all regions driven by 
    the flu vaccine surge. February is the lightest, the short month dip. 
    Midlands is consistently the darkest row with highest total volume. The pattern 
    is national, the scale is regional. Every region follows the same seasonal 
    shape, confirming the >0.96 correlation found in Chapter 2.
    """)

    st.markdown("---")

    # Ch5-Ch6 connection
    st.markdown("""
    <div style='background-color:#e8f4f8; padding:15px; border-radius:8px; 
    border-left:4px solid #17a2b8; margin-bottom:10px;'>
    <strong>🔍 Connection to Chapter 5 - Seasonality Explains Forecast Difficulty</strong><br>
    The categories hardest to forecast in Chapter 5 are the most seasonal ones here. 
    Dressings (most financially seasonal at 0.72) had the worst forecast error at 
    7.11% MAPE. Endocrine (most stable at 0.26) had the best forecast at 3.59% MAPE. 
    Seasonality is not just a historical description, it predicts where forecasting 
    can be trusted and where it should be treated with caution.
    </div>
    """, unsafe_allow_html=True)

    # Limitation box
    st.markdown("""
    <div style='background-color:#f8d7da; padding:15px; border-radius:8px; 
    border-left:4px solid #dc3545;'>
    <strong>🔴 Limitation</strong><br>
    Only one year of data means seasonal patterns cannot be confirmed as genuinely 
    annual as they could be one-off 2025 patterns. A proper seasonal analysis requires 
    at least two full years of data. The data can show that regional variation in 
    magnitude exists but cannot explain why population age, deprivation, and climate 
    are plausible causes but are completely absent from this dataset.
    </div>
    """, unsafe_allow_html=True)