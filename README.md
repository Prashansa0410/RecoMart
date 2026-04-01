# RecoMart - Recommendation System Project

## Project Overview
RecoMart is a collaborative ML project to build a product recommendation system using:
- **Data Source 1**: E-commerce behavior CSV (2019-Oct.csv)
- **Data Source 2**: FakeStore API for product details
- **Goal**: Create features and train recommendation model

## Unified Dataset Schema (FROZEN)
```
user_id (int) - User identifier
product_id (int) - Product identifier (COMMON KEY)
event_time (datetime) - Event timestamp
price (float) - Product price
category (string) - Product category
rating (float) - Product rating
```
⚠️ These column names are EXACT - no changes allowed

---

## Team Responsibilities

### **Shankar (Data Ingestion)** - THIS IS YOU
**Output**: `/data/raw/` folder

#### Tasks:
1. **Download CSV**
   - Dataset: https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store
   - File: `2019-Oct.csv`
   - Place in project root

2. **Sample Data**
   - Load first 30,000 rows
   - Save to: `data/raw/sample_data.csv`

3. **Fetch API Data**
   - Endpoint: https://fakestoreapi.com/products
   - Convert JSON → DataFrame
   - Save to: `data/raw/api_products.csv`

4. **Create Logs**
   - Save to: `logs/ingestion.log`
   - Include:
     - CSV loaded successfully
     - API fetched successfully
     - Data saved to raw folder

---

### **Prashansa (Processing + Validation)**
**Output**: `/data/processed/` + `/reports/`
- Clean data (missing values, duplicates)
- Merge on product_id
- Create Data Quality Report (PDF)
- Generate EDA plots

---

### **Aniket (Feature Engineering)**
**Output**: `/data/features/`
- Create features: purchase_count, user_activity, product_popularity
- Output: `features/feature_data.csv`

---

### **Flavia (Model Training)**
**Output**: `/models/`
- Train recommendation model
- Evaluate metrics: Precision@K, Recall@K
- Model + results documentation

---

## Getting Started (Shankar)

### Step 1: Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download CSV
- Go to: https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store
- Download `2019-Oct.csv` (or csv file for October 2019)
- Place in project root directory

### Step 3: Run Ingestion Pipeline
```bash
python scripts/data_ingestion.py
```

This will:
- Load 30k rows from CSV
- Fetch 20 products from API
- Save both to `/data/raw/`
- Create logs in `/logs/ingestion.log`

---

## Project Structure

```
RecoMart/
│
├── data/
│   ├── raw/                    # YOUR OUTPUT
│   │   ├── sample_data.csv      (30k rows from CSV)
│   │   ├── api_products.csv     (API data)
│   │
│   ├── processed/              # Prashansa's output
│   │   └── cleaned_data.csv
│   │
│   └── features/               # Aniket's output
│       └── feature_data.csv
│
├── logs/                        # YOUR OUTPUT
│   └── ingestion.log
│
├── scripts/
│   └── data_ingestion.py        # YOUR SCRIPT
│
├── notebooks/
├── models/                      # Flavia's output
├── reports/                     # Prashansa's output
│
├── requirements.txt
└── README.md
```

---

## Checklist Before Handoff to Prashansa

- [ ] 2019-Oct.csv downloaded
- [ ] `data/raw/sample_data.csv` created (30k rows)
- [ ] `data/raw/api_products.csv` created
- [ ] `logs/ingestion.log` shows success
- [ ] Folder structure matches above
- [ ] No extra columns added
- [ ] product_id in valid range (1-20 for API)

---
Checklist Before Handoff to Aniket

⬜ data/processed/cleaned_data.csv created
⬜ No missing values in key columns (user_id, product_id, price)
⬜ No duplicate rows in processed data
⬜ product_id mapped correctly (1–20 range)
⬜ API data successfully merged (price, category present)
⬜ event_time converted to proper datetime format
⬜ Only required columns present (no unnecessary columns)
⬜ Data size looks correct (~30K rows after cleaning)

EDA & Reports
⬜ reports/eda_plots/product_popularity.png created
⬜ reports/eda_plots/user_activity.png created
⬜ reports/data_quality_report.pdf generated
⬜ PDF includes stats + visualizations

Logs & Validation
⬜ logs/processing.log shows successful execution
⬜ No errors in pipeline logs
⬜ run_pipeline.py executes Step 2 successfully

Folder Structure
⬜ data/processed/ folder exists
⬜ reports/ folder properly structured
⬜ No unnecessary files in repo



## 🔗 Important Links

- **CSV Dataset**: https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store
- **API**: https://fakestoreapi.com/products
- **Team Collaboration**: Follow parallel work agreement

---

## Notes

- DO NOT modify schema column names
- DO NOT add extra columns
- If product_id range is wrong, data won't merge correctly
- Save ALL intermediate outputs (raw data)
- Check logs for any errors

Run `python scripts/data_ingestion.py` to start! 
