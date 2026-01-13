"""
Data Analysis Module for UIDAI Biometric Update Analysis
==========================================================

This module provides functions to perform exploratory data analysis (EDA)
on Aadhaar datasets, with a focus on age-group-wise biometric update patterns.

Author: UIDAI Hackathon 2026 Team
Date: January 2026
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


def analyze_age_distribution(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group'
) -> pd.DataFrame:
    """
    Analyze the distribution of records across age groups.
    
    **What it does**: Shows how many people are in each age category
    **Why it matters**: Identifies which age groups are most/least represented
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age group information
    age_group_column : str
        Name of the age group column
        
    Returns:
    --------
    pd.DataFrame
        Age distribution statistics
        
    Example:
    --------
    >>> age_stats = analyze_age_distribution(df_enrolment)
    """
    print(f"\n{'='*70}")
    print("AGE GROUP DISTRIBUTION ANALYSIS")
    print(f"{'='*70}")
    
    # Calculate distribution
    age_dist = df[age_group_column].value_counts().sort_index()
    age_pct = (age_dist / len(df) * 100).round(2)
    
    # Create summary DataFrame
    summary = pd.DataFrame({
        'Age_Group': age_dist.index,
        'Count': age_dist.values,
        'Percentage': age_pct.values
    })
    
    print("\nAge Group Distribution:")
    print(summary.to_string(index=False))
    
    # Identify largest and smallest groups
    largest = summary.loc[summary['Count'].idxmax()]
    smallest = summary.loc[summary['Count'].idxmin()]
    
    print(f"\n📊 Key Findings:")
    print(f"  • Largest group: {largest['Age_Group']} ({largest['Count']:,} records, {largest['Percentage']:.1f}%)")
    print(f"  • Smallest group: {smallest['Age_Group']} ({smallest['Count']:,} records, {smallest['Percentage']:.1f}%)")
    
    return summary


def analyze_biometric_quality_by_age(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_column: str = 'Biometric_Quality_Score'
) -> pd.DataFrame:
    """
    Analyze biometric quality scores across different age groups.
    
    **What it does**: Calculates average biometric quality for each age group
    **Why it matters**: Reveals which age groups face biometric capture challenges
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age groups and quality scores
    age_group_column : str
        Name of the age group column
    quality_column : str
        Name of the biometric quality score column
        
    Returns:
    --------
    pd.DataFrame
        Quality statistics by age group
        
    Example:
    --------
    >>> quality_stats = analyze_biometric_quality_by_age(df_enrolment)
    """
    print(f"\n{'='*70}")
    print("BIOMETRIC QUALITY BY AGE GROUP")
    print(f"{'='*70}")
    
    # Calculate statistics by age group
    quality_stats = df.groupby(age_group_column)[quality_column].agg([
        ('Count', 'count'),
        ('Mean_Quality', 'mean'),
        ('Median_Quality', 'median'),
        ('Std_Dev', 'std'),
        ('Min_Quality', 'min'),
        ('Max_Quality', 'max')
    ]).round(2)
    
    quality_stats = quality_stats.reset_index()
    
    print("\nQuality Statistics by Age Group:")
    print(quality_stats.to_string(index=False))
    
    # Identify best and worst quality groups
    best = quality_stats.loc[quality_stats['Mean_Quality'].idxmax()]
    worst = quality_stats.loc[quality_stats['Mean_Quality'].idxmin()]
    
    print(f"\n📊 Key Findings:")
    print(f"  • Highest quality: {best[age_group_column]} (avg: {best['Mean_Quality']:.1f})")
    print(f"  • Lowest quality: {worst[age_group_column]} (avg: {worst['Mean_Quality']:.1f})")
    print(f"  • Quality gap: {best['Mean_Quality'] - worst['Mean_Quality']:.1f} points")
    
    return quality_stats


def analyze_quality_categories_by_age(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_category_column: str = 'Quality_Category'
) -> pd.DataFrame:
    """
    Cross-tabulate quality categories by age groups.
    
    **What it does**: Shows distribution of quality levels within each age group
    **Why it matters**: Identifies which age groups need re-enrollment most
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age groups and quality categories
    age_group_column : str
        Name of the age group column
    quality_category_column : str
        Name of the quality category column
        
    Returns:
    --------
    pd.DataFrame
        Cross-tabulation with percentages
        
    Example:
    --------
    >>> crosstab = analyze_quality_categories_by_age(df_enrolment)
    """
    print(f"\n{'='*70}")
    print("QUALITY CATEGORIES BY AGE GROUP (Cross-Tabulation)")
    print(f"{'='*70}")
    
    # Create cross-tabulation
    crosstab = pd.crosstab(
        df[age_group_column],
        df[quality_category_column],
        margins=True,
        margins_name='Total'
    )
    
    print("\nAbsolute Counts:")
    print(crosstab)
    
    # Calculate percentages (row-wise)
    crosstab_pct = pd.crosstab(
        df[age_group_column],
        df[quality_category_column],
        normalize='index'
    ) * 100
    crosstab_pct = crosstab_pct.round(2)
    
    print("\nPercentage Distribution (by Age Group):")
    print(crosstab_pct)
    
    # Analyze poor quality rates by age
    if 'Poor (0-40)' in crosstab_pct.columns:
        poor_rates = crosstab_pct['Poor (0-40)'].sort_values(ascending=False)
        print(f"\n📊 Poor Quality Rates by Age Group:")
        for age_group, rate in poor_rates.items():
            print(f"  • {age_group}: {rate:.1f}%")
    
    return crosstab_pct


def analyze_update_patterns_by_age(
    df_updates: pd.DataFrame,
    df_enrolment: pd.DataFrame,
    age_group_column: str = 'Age_Group'
) -> pd.DataFrame:
    """
    Analyze update patterns across age groups by merging datasets.
    
    **What it does**: Links update records to enrolment data to see which ages update most
    **Why it matters**: Reveals which demographics need frequent updates (vulnerability indicator)
    
    Parameters:
    -----------
    df_updates : pd.DataFrame
        Update dataset
    df_enrolment : pd.DataFrame
        Enrolment dataset with age groups
    age_group_column : str
        Name of the age group column
        
    Returns:
    --------
    pd.DataFrame
        Update statistics by age group
        
    Example:
    --------
    >>> update_stats = analyze_update_patterns_by_age(df_updates, df_enrolment)
    """
    print(f"\n{'='*70}")
    print("UPDATE PATTERNS BY AGE GROUP")
    print(f"{'='*70}")
    
    # Merge datasets
    df_merged = df_updates.merge(
        df_enrolment[['Enrolment_ID', age_group_column]],
        on='Enrolment_ID',
        how='left'
    )
    
    # Count updates by age group
    update_counts = df_merged[age_group_column].value_counts().sort_index()
    
    # Calculate update rate (updates per 1000 enrolments)
    enrolment_counts = df_enrolment[age_group_column].value_counts()
    update_rate = (update_counts / enrolment_counts * 1000).round(2)
    
    # Create summary
    summary = pd.DataFrame({
        'Age_Group': update_counts.index,
        'Total_Updates': update_counts.values,
        'Enrolments': [enrolment_counts.get(ag, 0) for ag in update_counts.index],
        'Updates_per_1000': update_rate.values
    })
    
    print("\nUpdate Statistics by Age Group:")
    print(summary.to_string(index=False))
    
    # Identify highest update rate
    highest = summary.loc[summary['Updates_per_1000'].idxmax()]
    print(f"\n📊 Key Finding:")
    print(f"  • Highest update rate: {highest['Age_Group']} ({highest['Updates_per_1000']:.1f} updates per 1000 enrolments)")
    
    return summary


def analyze_update_types_by_age(
    df_updates: pd.DataFrame,
    df_enrolment: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    update_type_column: str = 'Update_Type'
) -> pd.DataFrame:
    """
    Analyze types of updates across age groups.
    
    **What it does**: Shows which update types are most common for each age group
    **Why it matters**: Reveals age-specific needs (e.g., elderly need biometric updates)
    
    Parameters:
    -----------
    df_updates : pd.DataFrame
        Update dataset
    df_enrolment : pd.DataFrame
        Enrolment dataset with age groups
    age_group_column : str
        Name of the age group column
    update_type_column : str
        Name of the update type column
        
    Returns:
    --------
    pd.DataFrame
        Cross-tabulation of update types by age
        
    Example:
    --------
    >>> update_types = analyze_update_types_by_age(df_updates, df_enrolment)
    """
    print(f"\n{'='*70}")
    print("UPDATE TYPES BY AGE GROUP")
    print(f"{'='*70}")
    
    # Merge datasets
    df_merged = df_updates.merge(
        df_enrolment[['Enrolment_ID', age_group_column]],
        on='Enrolment_ID',
        how='left'
    )
    
    # Create cross-tabulation
    crosstab = pd.crosstab(
        df_merged[age_group_column],
        df_merged[update_type_column],
        margins=True,
        margins_name='Total'
    )
    
    print("\nUpdate Type Counts by Age Group:")
    print(crosstab)
    
    # Calculate percentages
    crosstab_pct = pd.crosstab(
        df_merged[age_group_column],
        df_merged[update_type_column],
        normalize='index'
    ) * 100
    crosstab_pct = crosstab_pct.round(2)
    
    print("\nPercentage Distribution (by Age Group):")
    print(crosstab_pct)
    
    # Identify biometric update rates
    if 'Biometric' in crosstab_pct.columns:
        bio_rates = crosstab_pct['Biometric'].sort_values(ascending=False)
        print(f"\n📊 Biometric Update Rates by Age Group:")
        for age_group, rate in bio_rates.items():
            print(f"  • {age_group}: {rate:.1f}%")
    
    return crosstab_pct


def calculate_correlation_matrix(
    df: pd.DataFrame,
    columns: List[str]
) -> pd.DataFrame:
    """
    Calculate correlation matrix for numerical columns.
    
    **What it does**: Shows relationships between variables (e.g., age vs quality)
    **Why it matters**: Identifies statistical relationships for deeper analysis
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    columns : list of str
        Columns to include in correlation analysis
        
    Returns:
    --------
    pd.DataFrame
        Correlation matrix
        
    Example:
    --------
    >>> corr = calculate_correlation_matrix(df, ['Age', 'Biometric_Quality_Score'])
    """
    print(f"\n{'='*70}")
    print("CORRELATION ANALYSIS")
    print(f"{'='*70}")
    
    # Select only numerical columns that exist
    available_cols = [col for col in columns if col in df.columns and df[col].dtype in [np.int64, np.float64]]
    
    if len(available_cols) < 2:
        print("⚠ Not enough numerical columns for correlation analysis")
        return pd.DataFrame()
    
    # Calculate correlation
    corr_matrix = df[available_cols].corr().round(3)
    
    print("\nCorrelation Matrix:")
    print(corr_matrix)
    
    # Identify strong correlations (|r| > 0.5)
    print(f"\n📊 Strong Correlations (|r| > 0.5):")
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.5:
                col1 = corr_matrix.columns[i]
                col2 = corr_matrix.columns[j]
                direction = "positive" if corr_val > 0 else "negative"
                print(f"  • {col1} ↔ {col2}: {corr_val:.3f} ({direction})")
    
    return corr_matrix


def generate_summary_statistics(
    df: pd.DataFrame,
    group_by_column: str,
    numeric_columns: List[str]
) -> pd.DataFrame:
    """
    Generate comprehensive summary statistics grouped by a categorical variable.
    
    **What it does**: Calculates mean, median, std for multiple metrics by group
    **Why it matters**: Provides statistical foundation for insights
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    group_by_column : str
        Column to group by (e.g., Age_Group)
    numeric_columns : list of str
        Numerical columns to summarize
        
    Returns:
    --------
    pd.DataFrame
        Summary statistics
        
    Example:
    --------
    >>> stats = generate_summary_statistics(df, 'Age_Group', ['Biometric_Quality_Score'])
    """
    print(f"\n{'='*70}")
    print(f"SUMMARY STATISTICS BY {group_by_column.upper()}")
    print(f"{'='*70}")
    
    # Filter to existing columns
    available_cols = [col for col in numeric_columns if col in df.columns]
    
    if not available_cols:
        print("⚠ No numerical columns found")
        return pd.DataFrame()
    
    # Calculate statistics
    summary = df.groupby(group_by_column)[available_cols].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(2)
    
    print("\nSummary Statistics:")
    print(summary)
    
    return summary


def identify_outliers(
    df: pd.DataFrame,
    column: str,
    method: str = 'iqr'
) -> Tuple[pd.DataFrame, Dict]:
    """
    Identify outliers in a numerical column.
    
    **What it does**: Finds unusual values that may indicate data quality issues
    **Why it matters**: Ensures analysis is based on clean, reliable data
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset
    column : str
        Column to check for outliers
    method : str
        Method to use: 'iqr' (interquartile range) or 'zscore'
        
    Returns:
    --------
    tuple
        (DataFrame of outliers, statistics dictionary)
        
    Example:
    --------
    >>> outliers, stats = identify_outliers(df, 'Biometric_Quality_Score')
    """
    print(f"\n{'='*70}")
    print(f"OUTLIER DETECTION: {column}")
    print(f"{'='*70}")
    
    if column not in df.columns:
        print(f"⚠ Column '{column}' not found")
        return pd.DataFrame(), {}
    
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        
        stats = {
            'method': 'IQR',
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outlier_count': len(outliers),
            'outlier_percentage': len(outliers) / len(df) * 100
        }
        
        print(f"\nMethod: Interquartile Range (IQR)")
        print(f"Q1: {Q1:.2f}")
        print(f"Q3: {Q3:.2f}")
        print(f"IQR: {IQR:.2f}")
        print(f"Lower Bound: {lower_bound:.2f}")
        print(f"Upper Bound: {upper_bound:.2f}")
        
    else:  # zscore
        mean = df[column].mean()
        std = df[column].std()
        z_scores = np.abs((df[column] - mean) / std)
        outliers = df[z_scores > 3]
        
        stats = {
            'method': 'Z-Score',
            'mean': mean,
            'std': std,
            'threshold': 3,
            'outlier_count': len(outliers),
            'outlier_percentage': len(outliers) / len(df) * 100
        }
        
        print(f"\nMethod: Z-Score (threshold: 3)")
        print(f"Mean: {mean:.2f}")
        print(f"Std Dev: {std:.2f}")
    
    print(f"\n📊 Results:")
    print(f"  • Outliers found: {stats['outlier_count']:,} ({stats['outlier_percentage']:.2f}%)")
    
    return outliers, stats


if __name__ == "__main__":
    # Example usage
    print("Data Analysis Module - UIDAI Hackathon 2026")
    print("This module provides functions for exploratory data analysis.")
    print("\nKey functions:")
    print("  - analyze_age_distribution(): Age group distribution")
    print("  - analyze_biometric_quality_by_age(): Quality scores by age")
    print("  - analyze_quality_categories_by_age(): Quality categories cross-tab")
    print("  - analyze_update_patterns_by_age(): Update frequency by age")
    print("  - analyze_update_types_by_age(): Update types by age")
    print("  - calculate_correlation_matrix(): Variable correlations")
    print("  - generate_summary_statistics(): Grouped statistics")
    print("  - identify_outliers(): Outlier detection")
