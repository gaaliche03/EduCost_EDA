# EduCost — International Education Explorer

EduCost is a data science project combining exploratory data analysis (EDA) of international education costs with an interactive Streamlit application that recommends the best study destinations based on a student's budget, field of study and preferences.

---

## Project Objective

International students face a complex decision when choosing where to study abroad: tuition fees, cost of living, visa fees, insurance, and duration of study all combine to make the total cost hard to estimate and compare.

**EduCost aims to:**
1. Explore and analyze real-world datasets on international education costs
2. Compare two different datasets to determine which provides the most value
3. Build an interactive tool that helps students filter, compare, and discover programs that fit their budget and goals

---

## Project Structure

```
EduCost/
│
├── datasets/
│   ├── dataset1/
│   │   ├── aboard-Sheet.csv                      # Raw abroad programs dataset (489 rows, 4 cols)
│   │   ├── aboard_cleaned.csv                    # Cleaned version of the abroad dataset (488 rows)
│   │   └── EduCost_eda_dataset1.ipynb            # EDA notebook — Dataset 1 (abroad programs)
│   └── dataset2/
│       ├── International_Education_Costs.csv     # Raw dataset (907 rows, 12 cols)
│       ├── international_cleaned.csv             # ✅ Cleaned dataset used in the app (907 rows, 13 cols)
│       └── EduCost_eda_dataset2.ipynb            # EDA notebook — Dataset 2 ✅ chosen
│
├── figures/                                      # Visualizations exported from EduCost_eda_dataset2.ipynb, displayed in app.py
│   ├── 01_top15_pays.png
│   ├── 02_niveau_distribution.png
│   ├── 03_tuition_distribution_histogramme.png
│   ├── 04_tuition_distribution_boxplot.png
│   ├── 05_frais_par_pays.png
│   ├── 06_frais_par_niveau.png
│   ├── 07_heatmap.png
│   └── 08_top15_programmes_frequence.png
│
└── app.py                                        # Streamlit application
```

---

## Datasets

Two distinct data sources were explored and compared during this project.

### Dataset 1 — `International_Education_Costs.csv` → `international_cleaned.csv` ✅ (used in app)
- **Source:** [Kaggle — International Education Costs]([https://www.kaggle.com/](https://www.kaggle.com/datasets/adilshamim8/cost-of-international-education)
- **Raw file:** `International_Education_Costs.csv` — 907 rows × 12 columns
- **Cleaned file:** `international_cleaned.csv` — 907 rows × 13 columns
- **Columns:** Country, City, University, Program, Level, Duration_Years, Tuition_USD, Rent_USD, Visa_Fee_USD, Insurance_USD, Living_Cost_Index, Exchange_Rate
- **Cleaning steps performed:** stripped whitespace, standardized text casing, converted numeric columns, dropped rows with missing Country or Tuition, engineered `Total_Cost_USD`
- **Coverage after cleaning:** 71 countries, 92 programs, 3 degree levels (Bachelor, Master, PhD)

**Total cost formula applied during cleaning:**
```
Total_Cost_USD = (Tuition_USD × Duration_Years)
               + (Rent_USD × 12 × Duration_Years)
               + Visa_Fee_USD
               + (Insurance_USD × Duration_Years)
```

### Dataset 2 — `aboard_cleaned.csv` / `abroad__-_Sheet1.csv`
- **Source:** Kaggle — study abroad fees dataset (https://www.kaggle.com/datasets/shivampawale/abroad-study-cost-predictor)
- **Size:** ~489 rows × 4–6 columns
- **Columns:** Country, Course Type, Course (Specialization), Fees (USD)
- **Why not retained:** Too limited — no living costs, no rent, no visa or insurance data. Impossible to compute a realistic total cost for comparison.

---

##  EDA — Key Findings

The full analysis is in `EduCost_eda_dataset2.ipynb`. Key insights:

- **Free programs exist** — several European countries (notably Germany) offer tuition-free programs
- **Wide cost range** — total costs vary from under $5,000 to over $200,000 depending on country and program
- **USA and Australia** are among the most expensive destinations; Germany and Norway among the most affordable
- **PhD programs** tend to have lower or zero tuition but longer duration
- **Rent** is often a larger cost driver than tuition, especially in cities like London, Singapore, and Sydney
- **Heatmap analysis** reveals that tuition varies significantly by both country and degree level

---

## Streamlit Application

The app (`app.py`) has three tabs:

### Tab 1 — Recommender 🎯
Filter programs by:
- Total budget (USD)
- Degree level (Bachelor / Master / PhD)
- Field of study (keyword search)
- Region (Europe, North America, Asia-Pacific)
- Maximum duration (years)

Displays the **Top 5 recommendations** ranked by total cost, plus a full table of all matching programs.

### Tab 2 — EDA Dashboard 
Static visualizations from the EDA notebook, displayed directly in the app:
- Programs by country (top 15)
- Distribution by degree level
- Tuition distribution (histogram + boxplot)
- Median costs by country
- Costs by degree level
- Heatmap: tuition by country & level
- Top 15 programs by frequency

### Tab 3 — Country Comparison 
Select multiple countries and compare them side-by-side on:
- Median tuition
- Median rent
- Median total cost
- Number of free programs

Includes a bar chart and detailed program table, filterable by level and field.

