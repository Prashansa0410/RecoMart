# 🚀 SHANKAR - QUICK START GUIDE

## Your Role: Data Ingestion
You are responsible for getting raw data into the project so the rest of the team can process it.

---

## ✅ Pre-requisites
- Python 3.8+
- pip/conda
- Download power (for CSV data)

---

## 📋 Your Tasks (In Order)

### 1️⃣ Environment Setup (One-time)
```bash
# Navigate to project
cd RecoMart

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Download CSV Data
**Dataset**: https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store

Steps:
1. Go to Kaggle link
2. Download `2019-Oct.csv` file (2.1GB file)
3. Place in **RecoMart/** (project root directory)

✅ File should be at: `RecoMart/2019-Oct.csv`

### 3️⃣ Run Ingestion Pipeline
```bash
python scripts/data_ingestion.py
```

This will:
- ✅ Load first 30,000 rows from CSV
- ✅ Fetch product data from API (https://fakestoreapi.com/products)
- ✅ Save both to `/data/raw/`
- ✅ Create logs at `/logs/ingestion.log`

**Expected output:**
```
data/raw/sample_data.csv       (30k rows)
data/raw/api_products.csv      (20 products from API)
logs/ingestion.log             (execution log)
```

---

## 🎯 Success Criteria

Run the script and verify:
- [ ] `data/raw/sample_data.csv` exists (30k rows)
- [ ] `data/raw/api_products.csv` exists (~20 rows)
- [ ] `logs/ingestion.log` shows ✅ success messages
- [ ] No errors in log file

**Log should contain:**
```
✅ CSV loaded successfully
✅ API data fetched successfully
✅ Data saved to raw folder
```

---

## ⚠️ Common Issues

### Issue: "2019-Oct.csv not found"
**Solution**: Make sure file is in project root, not subfolder
```
RecoMart/
├── 2019-Oct.csv          ← Here, not in data/ folder
├── data/
├── scripts/
├── ...
```

### Issue: API fetch times out
**Solution**: Check internet connection, run again
```bash
python scripts/data_ingestion.py  # Retry
```

### Issue: Module not found errors
**Solution**: Make sure virtual environment is activated
```bash
# Check activation
(.venv) C:\path\to\RecoMart>  # Should see (.venv)

# If not:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

---

## 📊 What Happens Next?

Once you complete these steps:

1. **Prashansa** (Processing):
   - Cleans your data
   - Merges CSV + API data
   - Creates quality reports

2. **Aniket** (Features):
   - Creates features from cleaned data
   - Generates feature matrix

3. **Flavia** (Model):
   - Trains recommendation model
   - Evaluates performance

---

## 📝 Important Reminders

✅ **DO:**
- Save intermediate CSVs in `/data/raw/`
- Keep exact column names (no changes)
- Check logs for errors
- Run `python scripts/data_ingestion.py` once

❌ **DON'T:**
- Delete raw data files
- Change column names
- Add extra columns
- Run pipeline multiple times (overwrites data)

---

## 🎉 You're Done When:

```
✅ data/raw/sample_data.csv created
✅ data/raw/api_products.csv created
✅ logs/ingestion.log shows success
✅ Data ready for Prashansa
```

Then message Prashansa: **"Raw data ready for processing"**

---

## 💡 Troubleshooting Commands

```bash
# Check if files created
dir data/raw/

# View logs
type logs/ingestion.log

# Test API manually (PowerShell)
Invoke-WebRequest -Uri "https://fakestoreapi.com/products" -Method Get
```

---

## ❓ Questions?

Check:
1. `/logs/ingestion.log` - error messages
2. `README.md` - full project overview
3. `TEAM_ROLES.md` - team structure

**Need help?** Show error from `logs/ingestion.log`
