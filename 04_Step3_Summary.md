# Step 3: Statistical Hypothesis Testing and Anomaly Detection - COMPLETE ✓

## What Was Created

### 1. **Python Module**: `statistical_tests.py` (600+ lines)

**Purpose**: Validate EDA findings through rigorous statistical testing and detect anomalous patterns

**6 Core Functions**:

---

#### **Function 1: `chi_square_test_quality_by_age()`**

**What it tests**: Are quality categories independent of age groups?

**Test Logic**:
1. Creates contingency table (age groups × quality categories)
2. Calculates expected frequencies assuming independence
3. Compares observed vs expected using Chi-square statistic: χ² = Σ[(O-E)²/E]
4. Large χ² → variables are related

**Hypotheses**:
- **H₀ (Null)**: Quality categories are independent of age (no relationship)
- **H₁ (Alternative)**: Quality depends on age (relationship exists)

**Decision Rule**:
- If p-value < 0.05: Reject H₀ → Age affects quality ✓
- If p-value ≥ 0.05: Fail to reject H₀ → No relationship

**Output**:
- Chi-square statistic
- P-value
- Degrees of freedom
- Cramér's V (effect size: 0.1=small, 0.3=medium, 0.5=large)

**Governance Implication**:
- Significant result justifies age-specific enrollment protocols

---

#### **Function 2: `anova_test_quality_by_age()`**

**What it tests**: Do mean quality scores differ across age groups?

**Test Logic**:
1. Calculates **between-group variance** (how different are group means?)
2. Calculates **within-group variance** (how spread out is data in each group?)
3. Computes F-statistic = Between variance / Within variance
4. Large F → groups have different means

**Hypotheses**:
- **H₀**: All age groups have same mean quality
- **H₁**: At least one group has different mean

**Assumptions**:
- Normality: Data in each group is normally distributed
- Homogeneity: Equal variances across groups
- Independence: Observations are independent

**Decision Rule**:
- If p-value < 0.05: Reject H₀ → Means differ ✓
- If p-value ≥ 0.05: Fail to reject H₀ → No difference

**Output**:
- F-statistic
- P-value
- Eta-squared (η²): Proportion of variance explained by age
  - 0.01 = small (1%)
  - 0.06 = medium (6%)
  - 0.14+ = large (14%+)

**Governance Implication**:
- Identifies which age groups need quality improvement

---

#### **Function 3: `kruskal_wallis_test()`**

**What it tests**: Do quality distributions differ (non-parametric)?

**Test Logic**:
1. Ranks all quality scores from lowest to highest (ignoring groups)
2. Calculates average rank for each age group
3. If distributions are similar → average ranks should be similar
4. Computes H-statistic based on rank differences

**Hypotheses**:
- **H₀**: All groups have same distribution
- **H₁**: At least one group has different distribution

**Advantages over ANOVA**:
- ✓ No normality assumption
- ✓ Robust to outliers (uses ranks, not raw values)
- ✓ Works with ordinal data

**When to use**:
- ANOVA assumptions violated
- Data has outliers
- Want conservative results

**Decision Rule**:
- If p-value < 0.05: Distributions differ ✓
- If p-value ≥ 0.05: No difference

**Governance Implication**:
- If both ANOVA and Kruskal-Wallis significant → Very strong evidence

---

#### **Function 4: `isolation_forest_anomaly_detection()`**

**What it does**: Detects unusual age-quality combinations using machine learning

**Algorithm Logic**:
1. Builds 100 random decision trees on the data
2. **Anomalies** are easier to isolate (fewer splits needed)
3. **Normal points** require more splits to isolate
4. Assigns anomaly score: -1 = anomaly, 1 = normal

**Intuition**:
- Like finding a person in a crowd
- Someone standing alone (anomaly) is easy to find
- Someone in the middle (normal) takes more effort

**Parameters**:
- **Contamination**: Expected % of anomalies (default: 5%)
- **Features**: Age, Quality Score, etc.

**What it detects**:
- Unusually low quality for young age → Enrollment issue?
- Unusually high quality for elderly → Best practice?
- Data entry errors
- Exceptional enrollment centers

**Output**:
- Anomaly labels (-1 or 1)
- Anomaly scores (lower = more anomalous)
- Statistics (count, rate)

**Governance Implication**:
- **Positive anomalies** (better than expected): Learn best practices
- **Negative anomalies** (worse than expected): Fix quality issues

---

#### **Function 5: `detect_age_quality_anomalies()`**

**What it does**: Statistical anomaly detection using z-scores

**Algorithm Logic**:
1. For each age group: Calculate mean (μ) and std dev (σ)
2. For each record: Calculate z-score = (score - μ) / σ
3. Flag records with |z| > 2 (beyond ±2 standard deviations)

**Intuition**:
- In normal distribution, ~95% of data falls within ±2σ
- Records outside this range are unusual for their age group

**Anomaly Types**:
- **Positive (z > 2)**: Unusually high quality for age group
  - Example: 70-year-old with excellent biometrics
  - Action: Investigate what made enrollment successful
  
- **Negative (z < -2)**: Unusually low quality for age group
  - Example: 25-year-old with poor biometrics
  - Action: Investigate enrollment center issues

**Parameters**:
- **threshold_std**: Number of std devs (default: 2.0)

**Output**:
- Anomaly flags (True/False)
- Z-scores
- Anomaly types (High/Low/Normal)
- Statistics by age group

**Governance Implication**:
- Positive → Learn and replicate
- Negative → Investigate and fix

---

#### **Function 6: `generate_statistical_report()`**

**What it does**: Consolidates all test results into comprehensive summary

**Purpose**: Evidence-based conclusions for governance

**Output**: Formatted report with:
- All test results (significant/not significant)
- P-values and effect sizes
- Anomaly statistics
- Overall conclusion
- Governance recommendations

---

## 2. **Jupyter Notebook**: `03_statistical_hypothesis_testing.ipynb`

**9 Comprehensive Sections**:

### Section 1: Setup and Data Loading
- Import statistical testing module
- Load cleaned datasets
- Configure environment

### Section 2: Chi-Square Test
- **Detailed explanation** of test logic
- **Hypotheses** clearly stated
- **Contingency table** displayed
- **Results** with interpretation
- **Governance implications**

### Section 3: One-Way ANOVA
- **Test logic** explained step-by-step
- **Assumptions** listed
- **Group means** compared
- **F-statistic and p-value** interpreted
- **Effect size** (eta-squared) calculated
- **Identifies** best and worst age groups

### Section 4: Kruskal-Wallis Test
- **Non-parametric alternative** explained
- **Advantages over ANOVA** listed
- **When to use** guidance
- **Results** compared with ANOVA
- **Robustness** emphasized

### Section 5: Isolation Forest Anomaly Detection
- **ML algorithm** explained with intuition
- **Scatter plot** visualization (normal vs anomalies)
- **Anomaly examples** displayed
- **Governance actions** for each type

### Section 6: Statistical Anomaly Detection (Z-Score)
- **Z-score method** explained
- **Positive vs negative anomalies** distinguished
- **Two visualizations**:
  1. Scatter plot with anomalies highlighted
  2. Anomaly count by age group
- **Examples** of each anomaly type

### Section 7: Comprehensive Statistical Report
- **Consolidates all results**
- **Overall conclusion** based on all tests
- **Governance recommendations** if significant

### Section 8: Save Results
- Test summary CSV
- Anomaly detection summary CSV
- Statistical report TXT
- Detected anomalies CSV (for investigation)

### Section 9: Key Findings
- **Summary of all tests**
- **Anomaly statistics**
- **Governance recommendations**
- **Next steps**

---

## Test Logic Explanations

### Chi-Square Test Logic:

```
Observed Frequencies (O) vs Expected Frequencies (E)

If age and quality are independent:
E = (row total × column total) / grand total

Chi-square statistic:
χ² = Σ [(O - E)² / E]

Large χ² → observed differs from expected → relationship exists
```

**Example**:
- If elderly had same quality distribution as young adults (independence)
- But we observe more "Poor" quality in elderly
- Then χ² will be large → reject independence

---

### ANOVA Test Logic:

```
Between-group variance (SSB):
How much do group means differ from overall mean?

Within-group variance (SSW):
How much do individuals differ from their group mean?

F-statistic = SSB / SSW

Large F → between-group differences >> within-group differences
→ Groups have different means
```

**Example**:
- If all age groups had quality scores 40-100 (large within-group variance)
- But elderly average 50, young adults average 80 (large between-group difference)
- Then F will be large → means differ

---

### Kruskal-Wallis Logic:

```
1. Rank all scores: 1, 2, 3, ..., N
2. Calculate average rank for each group
3. If distributions are same → average ranks should be similar

H-statistic measures rank differences
Large H → distributions differ
```

**Example**:
- Elderly: Ranks mostly 1-1000 (low quality)
- Young adults: Ranks mostly 9000-10000 (high quality)
- Average ranks very different → H large → distributions differ

---

### Isolation Forest Logic:

```
For each point:
1. Build random decision tree
2. Count splits needed to isolate point
3. Anomalies need fewer splits (easy to isolate)
4. Normal points need more splits (buried in crowd)

Anomaly score = average path length across trees
```

**Example**:
- 25-year-old with quality 30 (unusual)
  - Tree 1: 2 splits to isolate
  - Tree 2: 1 split to isolate
  - Average: 1.5 splits → ANOMALY
  
- 25-year-old with quality 75 (normal)
  - Tree 1: 8 splits to isolate
  - Tree 2: 9 splits to isolate
  - Average: 8.5 splits → NORMAL

---

### Z-Score Logic:

```
For each age group:
μ = mean quality
σ = standard deviation

For each record:
z = (score - μ) / σ

|z| > 2 → more than 2 std devs from mean → ANOMALY
```

**Example**:
- Elderly group: μ = 50, σ = 10
- Record: 70-year-old with quality 75
- z = (75 - 50) / 10 = 2.5
- |2.5| > 2 → POSITIVE ANOMALY (unusually high)

---

## Outputs Generated

### Statistical Tables (CSV):
1. `statistical_test_summary.csv` - All test results
2. `anomaly_detection_summary.csv` - Anomaly statistics
3. `detected_anomalies.csv` - Individual anomalous records

### Visualizations (PNG, 300 DPI):
1. `09_isolation_forest_anomalies.png` - Scatter plot with ML anomalies
2. `10_statistical_anomalies.png` - Two-panel anomaly visualization

### Report (TXT):
1. `statistical_report.txt` - Comprehensive summary for governance

---

## Governance Decision Framework

### If All Tests Significant:

**Evidence**: Strong statistical proof that age affects quality

**Recommended Actions**:
1. **Immediate**: Implement age-specific enrollment protocols
2. **Technology**: Deploy specialized biometric devices for elderly
3. **Process**: Provide assisted enrollment for vulnerable groups
4. **Investigation**: Analyze positive anomalies for best practices
5. **Quality Control**: Address negative anomalies
6. **Campaigns**: Prioritize re-enrollment for low-quality age groups

### If Mixed Results:

**Evidence**: Some tests significant, others not

**Recommended Actions**:
1. Collect more data
2. Check data quality
3. Investigate confounding factors
4. Consider alternative analyses

---

## Statistical Rigor

### Multiple Testing:
- **3 different tests** for same hypothesis (Chi-square, ANOVA, Kruskal-Wallis)
- If all agree → Very strong evidence
- If disagree → Need to understand why

### Parametric + Non-Parametric:
- **ANOVA**: Assumes normality
- **Kruskal-Wallis**: No normality assumption
- Both significant → Robust conclusion

### ML + Statistical Anomaly Detection:
- **Isolation Forest**: Unsupervised ML approach
- **Z-Score**: Traditional statistical approach
- Agreement → High confidence in anomalies

---

## Key Achievements

✅ **Comprehensive hypothesis testing** (3 methods)  
✅ **Dual anomaly detection** (ML + statistical)  
✅ **Detailed logic explanations** for each test  
✅ **Clear governance implications** for each finding  
✅ **Publication-quality visualizations**  
✅ **Exportable results** (CSV, TXT)  
✅ **Evidence-based recommendations**  

---

**Status**: Step 3 COMPLETE - Statistical validation achieved! 📊

**UIDAI Data Hackathon 2026** | Backend Analytics Project
