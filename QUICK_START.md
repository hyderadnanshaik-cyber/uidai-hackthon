# Quick Start Guide - UIDAI Biometric Update Analysis

## 🚀 Getting Started

This guide will help you run the data loading and cleaning pipeline for your UIDAI hackathon project.

---

## Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This will install all required Python packages:
- pandas, numpy (data manipulation)
- matplotlib, seaborn (visualization)
- scikit-learn, scipy (statistical analysis)
- jupyter (notebooks)

---

## Step 2: Prepare Your Data

### Option A: Use Your UIDAI Datasets

1. Place your UIDAI dataset files in the `data/raw/` folder
2. Name them:
   - `enrolment_data.csv` (or `.xlsx`)
   - `update_data.csv` (or `.xlsx`)

### Option B: Use Sample Data (for testing)

The notebook will automatically create realistic sample data if no files are found.

---

## Step 3: Run the Data Loading Notebook

### Launch Jupyter Notebook:

```powershell
cd notebooks
jupyter notebook
```

This will open Jupyter in your browser.

### Open and Run:

1. Click on `01_data_loading_and_cleaning.ipynb`
2. Run all cells: **Cell → Run All** (or press Shift+Enter for each cell)

---

## What the Notebook Does

### 1. **Loads Data**
   - Reads CSV/Excel files
   - Displays data overview and statistics

### 2. **Cleans Data**
   - Converts date columns to proper format
   - Handles missing values
   - Removes duplicates
   - Standardizes categorical columns

### 3. **Creates Features**
   - **Age Groups**: 0-5, 6-18, 19-40, 41-60, 60+
   - **Biometric Quality Categories**: Poor, Fair, Good, Excellent
   - **Time Features**: Year, Month, Quarter

### 4. **Saves Processed Data**
   - Cleaned datasets saved to `data/processed/`
   - Ready for analysis in next notebooks

---

## Expected Outputs

After running the notebook, you'll have:

✅ **Cleaned Datasets**:
- `data/processed/enrolment_cleaned.csv`
- `data/processed/updates_cleaned.csv`

✅ **Visualizations**:
- Age group distribution chart
- Biometric quality distribution chart

✅ **Data Quality Report**:
- Missing values summary
- Duplicate records count
- Cleaning statistics

---

## Using the Python Modules Directly

You can also use the utility functions in your own scripts:

```python
from scripts.data_loader import load_enrolment_data, load_update_data
from scripts.data_cleaner import create_age_groups, handle_missing_values

# Load data
df = load_enrolment_data('data/raw/enrolment_data.csv')

# Create age groups
df = create_age_groups(df, age_column='Age')

# Handle missing values
df = handle_missing_values(df, strategy='fill_median')
```

---

## Troubleshooting

### Problem: "Module not found" error
**Solution**: Make sure you're in the `notebooks/` directory and the script adds parent directory to path:
```python
import sys
sys.path.append('..')
```

### Problem: "File not found" error
**Solution**: Check that your data files are in `data/raw/` or let the notebook create sample data.

### Problem: Jupyter won't start
**Solution**: 
```powershell
pip install --upgrade jupyter notebook
jupyter notebook
```

---

## Next Steps

Once data loading and cleaning is complete:

1. **Notebook 02**: Exploratory data analysis
2. **Notebook 03**: Statistical analysis (age vs biometric quality)
3. **Notebook 04**: Create visualizations for report
4. **Notebook 05**: Extract insights and recommendations

---

## File Structure

```
Misssion MJ/
├── data/
│   ├── raw/                    # Your original datasets
│   └── processed/              # Cleaned datasets (generated)
├── notebooks/
│   └── 01_data_loading_and_cleaning.ipynb  # Start here!
├── scripts/
│   ├── data_loader.py          # Data loading functions
│   └── data_cleaner.py         # Data cleaning functions
├── requirements.txt            # Python dependencies
└── QUICK_START.md             # This file
```

---

## Need Help?

- Check the docstrings in `data_loader.py` and `data_cleaner.py` for function documentation
- Each notebook cell has explanatory markdown
- All functions print progress messages to help you understand what's happening

---

**Ready to analyze Aadhaar data! 🎯**

UIDAI Data Hackathon 2026 | Backend Analytics Project
