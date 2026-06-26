import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="EduCost", layout="wide")
DATA_PATH = r"C:\Users\MSI\Documents\EduCost\datasets\dataset2\international_cleaned.csv"
FIG_DIR= r"C:\Users\MSI\Documents\EduCost\figures"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, sep=",")
    for col in ['Country', 'City', 'Program', 'Level']:
        df[col] = df[col].str.strip().str.title()
    if 'Total_Cost_USD' not in df.columns:
        df['Total_Cost_USD'] = (
            df['Tuition_USD'] * df['Duration_Years'] +
            df['Rent_USD'] * 12 * df['Duration_Years'] +
            df['Visa_Fee_USD'] +
            df['Insurance_USD'] * df['Duration_Years']
        ).round(0)
    return df

df = load_data()

###sidebar : filters
st.sidebar.title("Filters")
budget = st.sidebar.number_input(
    "Total budget (USD)", min_value=5000, max_value=500000,value=50000, step=1000
)
niveau = st.sidebar.selectbox(
    "Degree level",options=["All"] + sorted(df['Level'].unique().tolist())
)
specialite = st.sidebar.text_input(
    "Field of study (keyword)",placeholder="e.g. Computer Science, Finance, Engineering"
)

regions_map = {
    "All regions": None,
    "Europe": ["Germany","France","Italy","Netherlands","Spain","Sweden","Norway","Denmark","Finland","Belgium","Austria","Switzerland","Poland","Portugal"],
    "North America": ["United States","Canada","Mexico"],
    "Asia-Pacific": ["Australia","Japan","South Korea","Singapore","China","India","New Zealand","Malaysia"],
}
region = st.sidebar.selectbox("Region", list(regions_map.keys()))
duree_max = st.sidebar.slider("Max duration (years)", 1, 6, 3)

#logic filtering
df_filtered = df.copy()
df_filtered = df_filtered[df_filtered['Total_Cost_USD'] <= budget]
df_filtered = df_filtered[df_filtered['Duration_Years'] <= duree_max]

if niveau != "All":
    df_filtered = df_filtered[df_filtered['Level'] == niveau]

if specialite.strip():
    df_filtered = df_filtered[
        df_filtered['Program'].str.contains(specialite.strip(), case=False, na=False)
    ]

if regions_map[region]:
    df_filtered = df_filtered[df_filtered['Country'].isin(regions_map[region])]

df_filtered = df_filtered.sort_values('Total_Cost_USD').reset_index(drop=True)

### 3tabs
tab1, tab2, tab3 = st.tabs(["Recommender", "EDA Dashboard", "Country Comparison"])

#default:tab: recommnder
with tab1:
    st.title("Find the best study destination for you")
    st.caption("Results are filtered based on your selections in the sidebar.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Your budget", f"${budget:,}")
    col2.metric("Degree level", niveau)
    col3.metric("Field", specialite if specialite else "All")
    col4.metric("Programs found", len(df_filtered))

    st.divider()

    if df_filtered.empty:
        st.warning("No programs match your criteria. Try increasing your budget or broadening your field of study.")
    else:
        st.subheader("Top 5 recommendations")
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        top5 = df_filtered.head(5)

        for idx, (_, row) in enumerate(top5.iterrows()):
            with st.container(border=True):
                c1, c2, c3, c4, c5 = st.columns([1, 2, 3, 2, 2])
                c1.markdown(f"### {medals[idx]}")
                c2.markdown(f"**{row['Country']}**  \n{row['City'] if pd.notna(row['City']) else ''}")
                c3.markdown(f"**{row['Program']}**  \n{row['Level']} · {int(row['Duration_Years'])} yr(s)")
                tuition = "Free" if row['Tuition_USD'] == 0 else f"${row['Tuition_USD']:,.0f}/yr"
                c4.metric("Tuition", tuition)
                c5.metric("Total cost", f"${row['Total_Cost_USD']:,.0f}")

        st.subheader("All matching programs")
        st.dataframe(
            df_filtered[['Country', 'City', 'Program', 'Level',
                          'Tuition_USD', 'Duration_Years', 'Rent_USD', 'Total_Cost_USD']]
            .rename(columns={
                'Tuition_USD': 'Tuition (USD/yr)',
                'Duration_Years': 'Duration (yrs)',
                'Rent_USD': 'Rent (USD/mo)',
                'Total_Cost_USD': 'Total Cost (USD)'
            })
            .head(50).reset_index(drop=True),
            use_container_width=True
        )

####tab2: eda dashboard
with tab2:
    st.title("EDA Dashboard — International Education Costs")
    st.caption(f"Dataset: {len(df):,} programs across {df['Country'].nunique()} countries")

    # KPI cards
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total programs", f"{len(df):,}")
    k2.metric("Countries", df['Country'].nunique())
    k3.metric("Median tuition", f"${df[df['Tuition_USD']>0]['Tuition_USD'].median():,.0f}/yr")
    k4.metric("Free programs", f"{(df['Tuition_USD']==0).sum()} ({(df['Tuition_USD']==0).mean()*100:.0f}%)")

    st.divider()

    def show_fig(filename, caption=""):
        path = os.path.join(FIG_DIR, filename)
        if os.path.exists(path):
            st.image(path, caption=caption, use_container_width=True)
        else:
            st.info(f"Figure not found: {filename}")

    st.subheader("Programs by country")
    show_fig("01_top15_pays.png")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution by level")
        show_fig("02_niveau_distribution.png")
    with col2:
        st.subheader("Tuition distribution — histogram")
        show_fig("03_tuition_distribution_histogramme.png")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tuition distribution — boxplot")
        show_fig("04_tuition_distribution_boxplot.png")
    with col2:
        st.subheader("Median costs by country")
        show_fig("05_frais_par_pays.png")
    st.subheader("Costs by degree level")
    show_fig("06_frais_par_niveau.png")
    st.subheader("Heatmap — Tuition by country & level")
    show_fig("07_heatmap.png")
    st.subheader("Top 15 programs — frequency")
    show_fig("08_top15_programmes_fréquence.png")

####tab3: coparaison by countries
with tab3:
    st.title("Compare countries")
    st.caption("Use the filters below to compare countries on your own criteria.")

    # Filters inside the tab
    col1, col2, col3 = st.columns(3)
    with col1:
        pays_list = sorted(df['Country'].unique())
        choix = st.multiselect("Select countries", pays_list, default=["Germany", "Canada", "Australia", "France"])
    with col2:
        level_filter = st.selectbox("Degree level", ["All"] + sorted(df['Level'].unique().tolist()),key="comp_level")
    with col3:
        field_filter = st.text_input("Field of study (keyword)", placeholder="e.g. Engineering",key="comp_field")

    if not choix:
        st.info("Select at least one country to compare.")
    else:
        df_comp = df[df['Country'].isin(choix)].copy()
        if level_filter != "All":
            df_comp = df_comp[df_comp['Level'] == level_filter]
        if field_filter.strip():
            df_comp = df_comp[
                df_comp['Program'].str.contains(field_filter.strip(), case=False, na=False)
            ]
        if df_comp.empty:
            st.warning("No data for this combination. Try changing the filters.")
        else:
            # Summary table
            st.subheader("Summary by country")
            summary = df_comp.groupby('Country').agg(
                Programs=('Tuition_USD', 'count'),
                Median_Tuition=('Tuition_USD', 'median'),
                Median_Rent=('Rent_USD','median'),
                Median_Total=('Total_Cost_USD','median'),
                Free_Programs=('Tuition_USD', lambda x: (x == 0).sum())
            ).round(0).reset_index()
            summary.columns = ['Country', 'Programs', 'Median Tuition (USD/yr)','Median Rent (USD/mo)', 'Median Total Cost (USD)', 'Free Programs']
            st.dataframe(summary, use_container_width=True)
            
            # Detailed programs table
            st.subheader("All matching programs")
            st.dataframe(
                df_comp[['Country', 'City', 'Program', 'Level',
                          'Tuition_USD', 'Duration_Years', 'Rent_USD', 'Total_Cost_USD']]
                .sort_values('Total_Cost_USD')
                .rename(columns={
                    'Tuition_USD': 'Tuition (USD/yr)',
                    'Duration_Years': 'Duration (yrs)',
                    'Rent_USD': 'Rent (USD/mo)',
                    'Total_Cost_USD': 'Total Cost (USD)'
                })
                .reset_index(drop=True),
                use_container_width=True
            )