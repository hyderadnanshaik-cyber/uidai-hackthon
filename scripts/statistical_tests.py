"""
Statistical Testing Module for UIDAI Biometric Update Analysis
================================================================

This module provides functions for hypothesis testing and anomaly detection
to validate findings from exploratory data analysis.

Author: UIDAI Hackathon 2026 Team
Date: January 2026
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, f_oneway, kruskal, mannwhitneyu
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


def chi_square_test_quality_by_age(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_category_column: str = 'Quality_Category',
    alpha: float = 0.05
) -> Dict:
    """
    Chi-Square Test: Are quality categories independent of age groups?
    
    **What it tests**: Whether biometric quality distribution differs significantly across age groups
    **Null Hypothesis (H0)**: Quality categories are independent of age groups (no relationship)
    **Alternative Hypothesis (H1)**: Quality categories depend on age groups (relationship exists)
    
    **Logic**:
    - Creates contingency table of age groups × quality categories
    - Calculates expected frequencies if variables were independent
    - Compares observed vs expected frequencies
    - If p-value < 0.05: Reject H0 → Age affects quality (significant relationship)
    - If p-value ≥ 0.05: Fail to reject H0 → No significant relationship
    
    **Governance Implication**:
    - Significant result confirms age-based quality disparities
    - Justifies age-specific enrollment protocols
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age groups and quality categories
    age_group_column : str
        Name of age group column
    quality_category_column : str
        Name of quality category column
    alpha : float
        Significance level (default: 0.05)
        
    Returns:
    --------
    dict
        Test results including chi-square statistic, p-value, and interpretation
    """
    print(f"\n{'='*80}")
    print("CHI-SQUARE TEST: Quality Categories × Age Groups")
    print(f"{'='*80}")
    
    # Create contingency table
    contingency_table = pd.crosstab(df[age_group_column], df[quality_category_column])
    
    print("\nContingency Table (Observed Frequencies):")
    print(contingency_table)
    
    # Perform chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    
    # Determine significance
    is_significant = p_value < alpha
    
    results = {
        'test_name': 'Chi-Square Test of Independence',
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'alpha': alpha,
        'is_significant': is_significant,
        'effect_size': np.sqrt(chi2 / (contingency_table.sum().sum() * (min(contingency_table.shape) - 1)))
    }
    
    print(f"\n📊 Test Results:")
    print(f"  Chi-Square Statistic: {chi2:.4f}")
    print(f"  Degrees of Freedom: {dof}")
    print(f"  P-value: {p_value:.6f}")
    print(f"  Significance Level (α): {alpha}")
    print(f"  Effect Size (Cramér's V): {results['effect_size']:.4f}")
    
    print(f"\n🔍 Interpretation:")
    if is_significant:
        print(f"  ✓ SIGNIFICANT (p < {alpha})")
        print(f"  → Reject null hypothesis")
        print(f"  → Quality categories ARE dependent on age groups")
        print(f"  → Age significantly affects biometric quality distribution")
        print(f"\n  Governance Implication:")
        print(f"  → Age-specific enrollment protocols are justified")
        print(f"  → Different age groups require different service approaches")
    else:
        print(f"  ✗ NOT SIGNIFICANT (p ≥ {alpha})")
        print(f"  → Fail to reject null hypothesis")
        print(f"  → No significant relationship between age and quality")
    
    return results


def anova_test_quality_by_age(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_column: str = 'Biometric_Quality_Score',
    alpha: float = 0.05
) -> Dict:
    """
    One-Way ANOVA: Do mean quality scores differ across age groups?
    
    **What it tests**: Whether average biometric quality varies significantly between age groups
    **Null Hypothesis (H0)**: All age groups have the same mean quality score
    **Alternative Hypothesis (H1)**: At least one age group has different mean quality
    
    **Logic**:
    - Compares variance between groups vs within groups
    - If between-group variance >> within-group variance → groups differ
    - F-statistic measures ratio of between/within variance
    - If p-value < 0.05: Reject H0 → Age groups have different mean quality
    
    **Assumptions**:
    - Normality: Data in each group is normally distributed
    - Homogeneity of variance: Equal variances across groups
    - Independence: Observations are independent
    
    **Governance Implication**:
    - Significant result confirms quality varies by age
    - Identifies need for age-targeted quality improvement
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age groups and quality scores
    age_group_column : str
        Name of age group column
    quality_column : str
        Name of quality score column
    alpha : float
        Significance level
        
    Returns:
    --------
    dict
        Test results including F-statistic, p-value, and interpretation
    """
    print(f"\n{'='*80}")
    print("ONE-WAY ANOVA: Mean Quality Scores Across Age Groups")
    print(f"{'='*80}")
    
    # Group data by age
    groups = [group[quality_column].dropna() for name, group in df.groupby(age_group_column)]
    
    # Display group means
    group_means = df.groupby(age_group_column)[quality_column].mean().sort_index()
    print("\nGroup Means:")
    for age_group, mean_quality in group_means.items():
        print(f"  {age_group}: {mean_quality:.2f}")
    
    # Perform ANOVA
    f_statistic, p_value = f_oneway(*groups)
    
    # Determine significance
    is_significant = p_value < alpha
    
    # Calculate effect size (eta-squared)
    grand_mean = df[quality_column].mean()
    ss_between = sum(len(group) * (group.mean() - grand_mean)**2 for group in groups)
    ss_total = sum((df[quality_column] - grand_mean)**2)
    eta_squared = ss_between / ss_total if ss_total > 0 else 0
    
    results = {
        'test_name': 'One-Way ANOVA',
        'f_statistic': f_statistic,
        'p_value': p_value,
        'alpha': alpha,
        'is_significant': is_significant,
        'eta_squared': eta_squared,
        'group_means': group_means.to_dict()
    }
    
    print(f"\n📊 Test Results:")
    print(f"  F-Statistic: {f_statistic:.4f}")
    print(f"  P-value: {p_value:.6f}")
    print(f"  Significance Level (α): {alpha}")
    print(f"  Effect Size (η²): {eta_squared:.4f}")
    
    print(f"\n🔍 Interpretation:")
    if is_significant:
        print(f"  ✓ SIGNIFICANT (p < {alpha})")
        print(f"  → Reject null hypothesis")
        print(f"  → At least one age group has significantly different mean quality")
        print(f"  → Age significantly affects biometric quality scores")
        
        # Identify highest and lowest
        best_group = group_means.idxmax()
        worst_group = group_means.idxmin()
        print(f"\n  Highest quality: {best_group} ({group_means[best_group]:.2f})")
        print(f"  Lowest quality: {worst_group} ({group_means[worst_group]:.2f})")
        print(f"  Difference: {group_means[best_group] - group_means[worst_group]:.2f} points")
        
        print(f"\n  Governance Implication:")
        print(f"  → {worst_group} requires targeted quality improvement")
        print(f"  → Consider age-specific biometric devices or protocols")
    else:
        print(f"  ✗ NOT SIGNIFICANT (p ≥ {alpha})")
        print(f"  → Fail to reject null hypothesis")
        print(f"  → No significant difference in mean quality across age groups")
    
    return results


def kruskal_wallis_test(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_column: str = 'Biometric_Quality_Score',
    alpha: float = 0.05
) -> Dict:
    """
    Kruskal-Wallis Test: Non-parametric alternative to ANOVA
    
    **What it tests**: Whether quality score distributions differ across age groups
    **When to use**: When ANOVA assumptions (normality, equal variance) are violated
    **Null Hypothesis (H0)**: All age groups have the same distribution
    **Alternative Hypothesis (H1)**: At least one group has different distribution
    
    **Logic**:
    - Ranks all quality scores from lowest to highest
    - Compares average ranks across age groups
    - If groups have similar distributions, average ranks should be similar
    - If p-value < 0.05: Groups have different distributions
    
    **Advantage over ANOVA**:
    - Doesn't assume normality
    - More robust to outliers
    - Works with ordinal data
    
    **Governance Implication**:
    - Confirms quality differences even without normality assumption
    - More conservative test for policy decisions
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age groups and quality scores
    age_group_column : str
        Name of age group column
    quality_column : str
        Name of quality score column
    alpha : float
        Significance level
        
    Returns:
    --------
    dict
        Test results
    """
    print(f"\n{'='*80}")
    print("KRUSKAL-WALLIS TEST: Quality Score Distributions Across Age Groups")
    print(f"{'='*80}")
    print("(Non-parametric alternative to ANOVA)")
    
    # Group data by age
    groups = [group[quality_column].dropna() for name, group in df.groupby(age_group_column)]
    
    # Display group medians
    group_medians = df.groupby(age_group_column)[quality_column].median().sort_index()
    print("\nGroup Medians:")
    for age_group, median_quality in group_medians.items():
        print(f"  {age_group}: {median_quality:.2f}")
    
    # Perform Kruskal-Wallis test
    h_statistic, p_value = kruskal(*groups)
    
    # Determine significance
    is_significant = p_value < alpha
    
    results = {
        'test_name': 'Kruskal-Wallis H Test',
        'h_statistic': h_statistic,
        'p_value': p_value,
        'alpha': alpha,
        'is_significant': is_significant,
        'group_medians': group_medians.to_dict()
    }
    
    print(f"\n📊 Test Results:")
    print(f"  H-Statistic: {h_statistic:.4f}")
    print(f"  P-value: {p_value:.6f}")
    print(f"  Significance Level (α): {alpha}")
    
    print(f"\n🔍 Interpretation:")
    if is_significant:
        print(f"  ✓ SIGNIFICANT (p < {alpha})")
        print(f"  → Reject null hypothesis")
        print(f"  → Age groups have significantly different quality distributions")
        print(f"  → Result robust to non-normality and outliers")
        
        best_group = group_medians.idxmax()
        worst_group = group_medians.idxmin()
        print(f"\n  Highest median: {best_group} ({group_medians[best_group]:.2f})")
        print(f"  Lowest median: {worst_group} ({group_medians[worst_group]:.2f})")
    else:
        print(f"  ✗ NOT SIGNIFICANT (p ≥ {alpha})")
        print(f"  → No significant difference in distributions")
    
    return results


def isolation_forest_anomaly_detection(
    df: pd.DataFrame,
    features: List[str],
    contamination: float = 0.05,
    random_state: int = 42
) -> Tuple[pd.DataFrame, Dict]:
    """
    Isolation Forest: Detect anomalous biometric quality patterns
    
    **What it does**: Identifies unusual combinations of age, quality, and other features
    **How it works**: 
    - Builds random decision trees
    - Anomalies are easier to isolate (fewer splits needed)
    - Normal points require more splits to isolate
    - Assigns anomaly score: -1 = anomaly, 1 = normal
    
    **Logic**:
    - Contamination = expected % of anomalies (default: 5%)
    - Algorithm isolates points that are "different" from majority
    - Useful for finding:
      * Unusually low quality for young age
      * Unusually high quality for elderly
      * Data entry errors
      * Exceptional cases
    
    **Governance Implication**:
    - Anomalies may indicate:
      * Enrollment quality issues at specific centers
      * Special populations needing attention
      * Data quality problems requiring investigation
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with features
    features : list of str
        Feature columns to use for detection
    contamination : float
        Expected proportion of anomalies (0-0.5)
    random_state : int
        Random seed for reproducibility
        
    Returns:
    --------
    tuple
        (DataFrame with anomaly labels, statistics dictionary)
    """
    print(f"\n{'='*80}")
    print("ISOLATION FOREST: Anomaly Detection in Biometric Quality Patterns")
    print(f"{'='*80}")
    
    # Select features
    available_features = [f for f in features if f in df.columns]
    print(f"\nUsing features: {', '.join(available_features)}")
    
    if len(available_features) == 0:
        print("⚠ No valid features found")
        return df, {}
    
    # Prepare data
    X = df[available_features].copy()
    
    # Handle categorical variables (encode if present)
    for col in X.columns:
        if X[col].dtype == 'object':
            X[col] = pd.Categorical(X[col]).codes
    
    # Remove missing values
    X_clean = X.dropna()
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_clean)
    
    # Fit Isolation Forest
    iso_forest = IsolationForest(
        contamination=contamination,
        random_state=random_state,
        n_estimators=100
    )
    
    predictions = iso_forest.fit_predict(X_scaled)
    anomaly_scores = iso_forest.score_samples(X_scaled)
    
    # Add results to dataframe
    df_result = df.copy()
    df_result['Anomaly'] = 0
    df_result.loc[X_clean.index, 'Anomaly'] = predictions
    df_result.loc[X_clean.index, 'Anomaly_Score'] = anomaly_scores
    
    # Calculate statistics
    n_anomalies = (predictions == -1).sum()
    anomaly_rate = n_anomalies / len(predictions) * 100
    
    stats = {
        'total_records': len(df),
        'records_analyzed': len(X_clean),
        'n_anomalies': n_anomalies,
        'anomaly_rate': anomaly_rate,
        'contamination': contamination * 100,
        'features_used': available_features
    }
    
    print(f"\n📊 Anomaly Detection Results:")
    print(f"  Total Records: {stats['total_records']:,}")
    print(f"  Records Analyzed: {stats['records_analyzed']:,}")
    print(f"  Anomalies Detected: {stats['n_anomalies']:,} ({stats['anomaly_rate']:.2f}%)")
    print(f"  Expected Contamination: {stats['contamination']:.1f}%")
    
    # Show anomaly examples
    anomalies = df_result[df_result['Anomaly'] == -1]
    if len(anomalies) > 0:
        print(f"\n🔍 Anomaly Examples (first 5):")
        display_cols = [col for col in ['Age', 'Age_Group', 'Biometric_Quality_Score', 
                                         'Quality_Category', 'Anomaly_Score'] if col in anomalies.columns]
        print(anomalies[display_cols].head().to_string(index=False))
        
        print(f"\n  Governance Implication:")
        print(f"  → Investigate anomalies for:")
        print(f"    • Enrollment center quality issues")
        print(f"    • Special populations requiring attention")
        print(f"    • Data entry errors")
    
    return df_result, stats


def detect_age_quality_anomalies(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_column: str = 'Biometric_Quality_Score',
    threshold_std: float = 2.0
) -> Tuple[pd.DataFrame, Dict]:
    """
    Statistical Anomaly Detection: Identify unusual age-quality combinations
    
    **What it does**: Finds records with quality scores far from their age group's average
    **How it works**:
    - Calculates mean and std dev for each age group
    - Flags records > threshold_std standard deviations from mean
    - Default: 2 std dev (captures ~95% of normal distribution)
    
    **Logic**:
    - If elderly person has excellent quality → Anomaly (investigate why)
    - If young person has poor quality → Anomaly (enrollment issue?)
    - Helps identify exceptional cases and data quality problems
    
    **Governance Implication**:
    - Positive anomalies (better than expected): Learn best practices
    - Negative anomalies (worse than expected): Investigate root causes
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age groups and quality scores
    age_group_column : str
        Name of age group column
    quality_column : str
        Name of quality score column
    threshold_std : float
        Number of standard deviations for anomaly threshold
        
    Returns:
    --------
    tuple
        (DataFrame with anomaly flags, statistics dictionary)
    """
    print(f"\n{'='*80}")
    print("STATISTICAL ANOMALY DETECTION: Age-Quality Combinations")
    print(f"{'='*80}")
    print(f"Threshold: ±{threshold_std} standard deviations from age group mean")
    
    # Calculate group statistics
    group_stats = df.groupby(age_group_column)[quality_column].agg(['mean', 'std']).reset_index()
    group_stats.columns = [age_group_column, 'group_mean', 'group_std']
    
    # Merge with original data
    df_merged = df.merge(group_stats, on=age_group_column)
    
    # Calculate z-scores within each age group
    df_merged['z_score'] = (df_merged[quality_column] - df_merged['group_mean']) / df_merged['group_std']
    
    # Flag anomalies
    df_merged['is_anomaly'] = np.abs(df_merged['z_score']) > threshold_std
    df_merged['anomaly_type'] = 'Normal'
    df_merged.loc[df_merged['z_score'] > threshold_std, 'anomaly_type'] = 'Unusually High Quality'
    df_merged.loc[df_merged['z_score'] < -threshold_std, 'anomaly_type'] = 'Unusually Low Quality'
    
    # Calculate statistics
    n_anomalies = df_merged['is_anomaly'].sum()
    n_high = (df_merged['anomaly_type'] == 'Unusually High Quality').sum()
    n_low = (df_merged['anomaly_type'] == 'Unusually Low Quality').sum()
    
    stats = {
        'total_records': len(df_merged),
        'n_anomalies': n_anomalies,
        'anomaly_rate': n_anomalies / len(df_merged) * 100,
        'n_unusually_high': n_high,
        'n_unusually_low': n_low,
        'threshold_std': threshold_std
    }
    
    print(f"\n📊 Anomaly Detection Results:")
    print(f"  Total Records: {stats['total_records']:,}")
    print(f"  Anomalies Detected: {stats['n_anomalies']:,} ({stats['anomaly_rate']:.2f}%)")
    print(f"  Unusually High Quality: {stats['n_unusually_high']:,}")
    print(f"  Unusually Low Quality: {stats['n_unusually_low']:,}")
    
    # Show examples by age group
    print(f"\n🔍 Anomalies by Age Group:")
    anomaly_by_age = df_merged[df_merged['is_anomaly']].groupby([age_group_column, 'anomaly_type']).size()
    if len(anomaly_by_age) > 0:
        print(anomaly_by_age)
    
    return df_merged, stats


def generate_statistical_report(
    chi2_results: Dict,
    anova_results: Dict,
    kruskal_results: Dict,
    anomaly_stats: Dict
) -> str:
    """
    Generate comprehensive statistical testing report.
    
    **What it does**: Consolidates all test results into readable summary
    **Purpose**: Provides evidence-based conclusions for governance recommendations
    
    Parameters:
    -----------
    chi2_results : dict
        Chi-square test results
    anova_results : dict
        ANOVA test results
    kruskal_results : dict
        Kruskal-Wallis test results
    anomaly_stats : dict
        Anomaly detection statistics
        
    Returns:
    --------
    str
        Formatted statistical report
    """
    report = []
    report.append("="*80)
    report.append("STATISTICAL TESTING SUMMARY REPORT")
    report.append("="*80)
    
    report.append("\n1. CHI-SQUARE TEST (Quality Categories × Age Groups)")
    report.append("-" * 80)
    report.append(f"   Result: {'SIGNIFICANT' if chi2_results['is_significant'] else 'NOT SIGNIFICANT'}")
    report.append(f"   P-value: {chi2_results['p_value']:.6f}")
    report.append(f"   Interpretation: {'Age affects quality distribution' if chi2_results['is_significant'] else 'No relationship found'}")
    
    report.append("\n2. ONE-WAY ANOVA (Mean Quality Scores)")
    report.append("-" * 80)
    report.append(f"   Result: {'SIGNIFICANT' if anova_results['is_significant'] else 'NOT SIGNIFICANT'}")
    report.append(f"   P-value: {anova_results['p_value']:.6f}")
    report.append(f"   Interpretation: {'Age groups have different mean quality' if anova_results['is_significant'] else 'No difference in means'}")
    
    report.append("\n3. KRUSKAL-WALLIS TEST (Non-parametric)")
    report.append("-" * 80)
    report.append(f"   Result: {'SIGNIFICANT' if kruskal_results['is_significant'] else 'NOT SIGNIFICANT'}")
    report.append(f"   P-value: {kruskal_results['p_value']:.6f}")
    report.append(f"   Interpretation: {'Confirms age-quality relationship (robust)' if kruskal_results['is_significant'] else 'No relationship'}")
    
    report.append("\n4. ANOMALY DETECTION")
    report.append("-" * 80)
    report.append(f"   Anomalies Detected: {anomaly_stats.get('n_anomalies', 0):,} ({anomaly_stats.get('anomaly_rate', 0):.2f}%)")
    report.append(f"   Unusually High Quality: {anomaly_stats.get('n_unusually_high', 0):,}")
    report.append(f"   Unusually Low Quality: {anomaly_stats.get('n_unusually_low', 0):,}")
    
    report.append("\n" + "="*80)
    report.append("OVERALL CONCLUSION")
    report.append("="*80)
    
    all_significant = (chi2_results['is_significant'] and 
                      anova_results['is_significant'] and 
                      kruskal_results['is_significant'])
    
    if all_significant:
        report.append("\n✓ STRONG EVIDENCE: All tests confirm age significantly affects biometric quality")
        report.append("\nGovernance Recommendations:")
        report.append("  1. Implement age-specific enrollment protocols")
        report.append("  2. Deploy specialized biometric devices for challenging age groups")
        report.append("  3. Prioritize re-enrollment campaigns for low-quality demographics")
        report.append("  4. Investigate anomalies for quality improvement opportunities")
    else:
        report.append("\n⚠ MIXED EVIDENCE: Some tests show significance, others don't")
        report.append("  → Further investigation recommended")
    
    return "\n".join(report)


if __name__ == "__main__":
    print("Statistical Testing Module - UIDAI Hackathon 2026")
    print("This module provides hypothesis testing and anomaly detection functions.")
    print("\nKey functions:")
    print("  - chi_square_test_quality_by_age(): Test independence of quality and age")
    print("  - anova_test_quality_by_age(): Test mean quality differences")
    print("  - kruskal_wallis_test(): Non-parametric alternative to ANOVA")
    print("  - isolation_forest_anomaly_detection(): ML-based anomaly detection")
    print("  - detect_age_quality_anomalies(): Statistical anomaly detection")
    print("  - generate_statistical_report(): Comprehensive test summary")
