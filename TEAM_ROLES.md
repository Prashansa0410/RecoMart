# 👥 TEAM ROLES & RESPONSIBILITIES

## Project: RecoMart - E-commerce Recommendation System

**Team Size**: 4 people  
**Goal**: Build a recommendation system using merged CSV + API data  
**Timeline**: Collaborative, parallel work  

---

## 👤 Team Members & Responsibilities

### 1️⃣ **SHANKAR** - Data Ingestion
**Status**: You are HERE ✅

#### Input Sources:
- CSV: https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store
- API: https://fakestoreapi.com/products

#### Deliverables:
```
📁 data/raw/
  ├── sample_data.csv (30k rows from CSV)
  └── api_products.csv (products from API)

📁 logs/
  └── ingestion.log (execution logs)
```

#### Key Outputs:
- 2019-Oct.csv sampled to 30k rows
- 20 products from FakeStore API
- Both saved as CSV with exact schema
- Logs documenting success/failure

#### Script:
```bash
python scripts/data_ingestion.py
```

#### Success Metrics:
- ✅ Files created in `/data/raw/`
- ✅ Log shows "API fetched successfully"
- ✅ Both CSVs have correct column names
- ✅ product_id valid range for merge

---

### 2️⃣ **PRASHANSA** - Data Processing & Validation
**Status**: Waiting for Shankar's output

#### Input:
```
data/raw/sample_data.csv
data/raw/api_products.csv
```

#### Tasks:
1. **Clean Data**
   - Handle missing values
   - Remove duplicates
   - Type conversion
   
2. **Merge**
   - Merge on `product_id`
   - Validate merge
   
3. **Convert Timestamp**
   - Format `event_time` to datetime
   
4. **Quality Reports**
   - Data Quality Report (PDF)
   - Missing values summary
   - Duplicate analysis

5. **EDA Visualizations**
   - Product popularity plot
   - User activity distribution
   - Save to `/reports/eda_plots/`

#### Deliverables:
```
📁 data/processed/
  └── cleaned_data.csv

📁 reports/
  ├── data_quality_report.pdf
  └── eda_plots/
      ├── product_popularity.png
      ├── user_activity.png
      └── ...
```

#### Script:
```bash
python scripts/data_processing.py
```

#### Success Metrics:
- ✅ Cleaned data has exact schema columns
- ✅ No duplicates in output
- ✅ Timestamp properly converted
- ✅ PDF report generated
- ✅ EDA plots show insights

---

### 3️⃣ **ANIKET** - Feature Engineering
**Status**: Waiting for Prashansa's output

#### Input:
```
data/processed/cleaned_data.csv
```

#### Features to Create:

1. **purchase_count**
   - Definition: Total purchases per user
   - Type: Integer
   - Groupby: user_id

2. **user_activity**
   - Definition: Event frequency per user
   - Type: Float
   - Groupby: user_id, time window

3. **product_popularity**
   - Definition: Purchase frequency per product
   - Type: Integer
   - Groupby: product_id

#### Deliverables:
```
📁 data/features/
  └── feature_data.csv
     (includes all original columns + new features)
```

#### Script:
```bash
python scripts/feature_engineering.py
```

#### Feature Definition Document:
Include in code/notebook:
- Feature formula
- Business logic
- Example calculations

#### Success Metrics:
- ✅ All 3 features created
- ✅ Feature shapes valid
- ✅ No NaN in features
- ✅ Feature values make sense (no outliers)

---

### 4️⃣ **FLAVIA** - Model Training & Evaluation
**Status**: Waiting for Aniket's output

#### Input:
```
data/features/feature_data.csv
```

#### Tasks:

1. **Model Selection**
   - Collaborative Filtering (recommended)
   - Build user-product interaction matrix
   
2. **Model Training**
   - Train on interaction matrix
   - Calculate user-user similarity
   
3. **Evaluation**
   - Precision@K
   - Recall@K
   - K = 5 (top-5 recommendations)

4. **Generate Recommendations**
   - For sample users
   - Document top recommendations
   
5. **Save Model**
   - Pickle or joblib format
   - Include model metadata

#### Deliverables:
```
📁 models/
  ├── recommendation_model.pkl
  ├── model_evaluation.txt
  └── sample_recommendations.csv

📁 reports/
  └── model_results.pdf
     (Precision@5, Recall@5, insights)
```

#### Script:
```bash
python scripts/model_training.py
```

#### Success Metrics:
- ✅ Model trains without errors
- ✅ Precision@5 > 0.3
- ✅ Recall@5 > 0.2
- ✅ Sample recommendations generated
- ✅ Model saved for inference

---

## 🔄 Workflow

```
Shankar (Ingestion)
        ↓
    data/raw/
        ↓
Prashansa (Processing)
        ↓
    data/processed/
        ↓
Aniket (Features)
        ↓
    data/features/
        ↓
Flavia (Model)
        ↓
    models/ + results
```

**Important**: Each person waits for previous person's output!

---

## 📊 Column Names (FROZEN SCHEMA)

All team members MUST use these exact names:
```
user_id (int)
product_id (int)
event_time (datetime)
price (float)
category (string)
rating (float)
```

**No changes, no additions** unless discussed.

---

## 📁 Folder Structure Rules

| Folder | Owner | Status |
|--------|-------|--------|
| `data/raw/` | Shankar | ✅ Creates |
| `data/processed/` | Prashansa | ✅ Creates |
| `data/features/` | Aniket | ✅ Creates |
| `logs/` | Shankar | ✅ Creates |
| `reports/` | Prashansa | ✅ Creates |
| `models/` | Flavia | ✅ Creates |
| `scripts/` | Everyone | Individual scripts |
| `notebooks/` | Everyone | Optional EDA |

---

## ✅ Quality Checklist

### Shankar:
- [ ] CSV loaded (30k rows)
- [ ] API data fetched
- [ ] Files in `/data/raw/`
- [ ] Logs created

### Prashansa:
- [ ] Data cleaned
- [ ] Merge successful
- [ ] Quality report (PDF)
- [ ] EDA plots created

### Aniket:
- [ ] All 3 features created
- [ ] No NaNs in output
- [ ] Feature logic documented
- [ ] File in `/data/features/`

### Flavia:
- [ ] Model trained
- [ ] Metrics calculated
- [ ] Recommendations generated
- [ ] Model saved

---

## 🚀 Master Pipeline

Run all at once:
```bash
python run_pipeline.py
```

This orchestrates:
1. Ingestion → `/data/raw/`
2. Processing → `/data/processed/`
3. Features → `/data/features/`
4. Model → `/models/`

---

## 📞 Communication

Use logs to track status:
```
logs/ingestion.log      (Shankar)
logs/processing.log     (Prashansa)
logs/features.log       (Aniket)
logs/model.log          (Flavia)
```

Each log shows:
- What was processed
- How many records
- Any errors
- Timestamp

---

## ⚠️ Important Rules

✅ **Everyone**:
- Use exact column names
- Save intermediate CSVs
- Document in code
- Check logs for errors
- Don't modify schema

❌ **Nobody**:
- Changes column names
- Adds undocumented columns
- Deletes raw data
- Skips quality checks
- Works out of assigned folder

---

## 📝 Deliverables Summary

| Person | Output | Format |
|--------|--------|--------|
| Shankar | Raw data + logs | CSV + TXT |
| Prashansa | Cleaned data + reports | CSV + PDF |
| Aniket | Feature data | CSV |
| Flavia | Model + metrics | PKL + TXT |

---

## 🎯 Final Checklist

All 4 people must deliver:
- [ ] Code runs without errors
- [ ] Output in correct location
- [ ] Logs show success
- [ ] No manual interventions
- [ ] Reproducible & documented

Then: Create report & demo video! 🎥

---

**Next Step for Shankar**: Read `SHANKAR_QUICKSTART.md`
