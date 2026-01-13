"""
Data Cleaning Module for UIDAI Biometric Update Analysis
==========================================================

This module provides functions to clean and preprocess Aadhaar datasets,
including handling missing values, creating age groups, and standardizing
categorical variables.

Author: UIDAI Hackathon 2026 Team
Date: January 2026
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')


def create_age_groups(
    df: pd.DataFrame,
    age_column: str = 'Age',
    bins: Optional[List[int]] = None,
    labels: Optional[List[str]] = None,
    new_column_name: str = 'Age_Group'
) -> pd.DataFrame:
    """
    Create age group categories from age column.
    
    Default age groups align with UIDAI service patterns:
    - 0-5: Early childhood (birth registration)
    - 6-18: School-age children
    - 19-40: Young adults (employment, marriage)
    - 41-60: Middle-age adults
    - 60+: Elderly (biometric challenges)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset containing age information
    age_column : str
        Name of the age column
    bins : list of int, optional
        Custom age bin boundaries (default: [0, 6, 19, 41, 61, 120])
    labels : list of str, optional
        Custom labels for age groups
    new_column_name : str
        Name for the new age group column
        
    Returns:
    --------
    pd.DataFrame
        Dataset with new age group column
        
    Example:
    --------
    >>> df = create_age_groups(df, age_column='Age')
    >>> print(df['Age_Group'].value_counts())
    """
    df = df.copy()
    
    # Default bins and labels
    if bins is None:
        bins = [0, 6, 19, 41, 61, 120]
    if labels is None:
        labels = ['0-5 (Child)', '6-18 (Youth)', '19-40 (Young Adult)', 
                  '41-60 (Middle Age)', '60+ (Elderly)']
    
    print(f"Creating age groups from column: {age_column}")
    
    if age_column not in df.columns:
        print(f"  ✗ Error: Column '{age_column}' not found in dataset")
        return df
    
    # Handle missing values
    missing_count = df[age_column].isnull().sum()
    if missing_count > 0:
        print(f"  ⚠ Warning: {missing_count:,} missing values in {age_column}")
    
    # Create age groups
    df[new_column_name] = pd.cut(
        df[age_column],
        bins=bins,
        labels=labels,
        include_lowest=True,
        right=False
    )
    
    print(f"  ✓ Created {new_column_name} column")
    print(f"\nAge Group Distribution:")
    print(df[new_column_name].value_counts().sort_index())
    
    return df


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = 'report',
    threshold: float = 0.5
) -> pd.DataFrame:
    """
    Handle missing values in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to process
    strategy : str
        Strategy for handling missing values:
        - 'report': Only report missing values (default)
        - 'drop_rows': Drop rows with any missing values
        - 'drop_cols': Drop columns with missing % > threshold
        - 'fill_mode': Fill categorical columns with mode
        - 'fill_median': Fill numerical columns with median
    threshold : float
        Threshold for dropping columns (0-1)
        
    Returns:
    --------
    pd.DataFrame
        Processed dataset
        
    Example:
    --------
    >>> df_clean = handle_missing_values(df, strategy='drop_cols', threshold=0.3)
    """
    df = df.copy()
    
    print(f"\n{'='*60}")
    print("Missing Values Analysis")
    print(f"{'='*60}")
    
    # Calculate missing values
    missing_stats = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum().values,
        'Missing_Percent': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    missing_stats = missing_stats[missing_stats['Missing_Count'] > 0].sort_values(
        'Missing_Percent', ascending=False
    )
    
    if len(missing_stats) == 0:
        print("✓ No missing values found in dataset")
        return df
    
    print(f"\nColumns with missing values: {len(missing_stats)}")
    print(missing_stats.to_string(index=False))
    
    # Apply strategy
    if strategy == 'report':
        print("\n→ Strategy: Report only (no changes made)")
        
    elif strategy == 'drop_rows':
        original_len = len(df)
        df = df.dropna()
        dropped = original_len - len(df)
        print(f"\n→ Strategy: Drop rows with missing values")
        print(f"  Dropped {dropped:,} rows ({dropped/original_len*100:.2f}%)")
        
    elif strategy == 'drop_cols':
        cols_to_drop = missing_stats[missing_stats['Missing_Percent'] > threshold*100]['Column'].tolist()
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            print(f"\n→ Strategy: Drop columns with >{threshold*100}% missing")
            print(f"  Dropped columns: {', '.join(cols_to_drop)}")
        else:
            print(f"\n→ No columns exceed {threshold*100}% missing threshold")
            
    elif strategy == 'fill_mode':
        print(f"\n→ Strategy: Fill categorical columns with mode")
        for col in df.select_dtypes(include=['object', 'category']).columns:
            if df[col].isnull().sum() > 0:
                mode_value = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
                df[col].fillna(mode_value, inplace=True)
                print(f"  Filled {col} with mode: {mode_value}")
                
    elif strategy == 'fill_median':
        print(f"\n→ Strategy: Fill numerical columns with median")
        for col in df.select_dtypes(include=[np.number]).columns:
            if df[col].isnull().sum() > 0:
                median_value = df[col].median()
                df[col].fillna(median_value, inplace=True)
                print(f"  Filled {col} with median: {median_value:.2f}")
    
    return df


def standardize_categorical_columns(
    df: pd.DataFrame,
    columns: List[str],
    case: str = 'title'
) -> pd.DataFrame:
    """
    Standardize categorical column values (remove whitespace, fix case).
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to process
    columns : list of str
        List of column names to standardize
    case : str
        Case transformation: 'title', 'upper', 'lower'
        
    Returns:
    --------
    pd.DataFrame
        Dataset with standardized columns
        
    Example:
    --------
    >>> df = standardize_categorical_columns(df, ['State', 'Gender'], case='title')
    """
    df = df.copy()
    
    print(f"\nStandardizing categorical columns...")
    
    for col in columns:
        if col not in df.columns:
            print(f"  ⚠ Column '{col}' not found, skipping")
            continue
            
        if df[col].dtype == 'object':
            # Remove leading/trailing whitespace
            df[col] = df[col].str.strip()
            
            # Apply case transformation
            if case == 'title':
                df[col] = df[col].str.title()
            elif case == 'upper':
                df[col] = df[col].str.upper()
            elif case == 'lower':
                df[col] = df[col].str.lower()
            
            print(f"  ✓ Standardized {col} ({case} case)")
        else:
            print(f"  ⚠ {col} is not a text column, skipping")
    
    return df


def remove_duplicates(
    df: pd.DataFrame,
    subset: Optional[List[str]] = None,
    keep: str = 'first'
) -> pd.DataFrame:
    """
    Remove duplicate rows from dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to process
    subset : list of str, optional
        Columns to consider for identifying duplicates
    keep : str
        Which duplicate to keep: 'first', 'last', or False (remove all)
        
    Returns:
    --------
    pd.DataFrame
        Dataset with duplicates removed
        
    Example:
    --------
    >>> df_clean = remove_duplicates(df, subset=['Aadhaar_ID'], keep='first')
    """
    df = df.copy()
    
    original_len = len(df)
    duplicate_count = df.duplicated(subset=subset, keep=keep).sum()
    
    if duplicate_count == 0:
        print("✓ No duplicate rows found")
        return df
    
    df = df.drop_duplicates(subset=subset, keep=keep)
    
    print(f"\n{'='*60}")
    print("Duplicate Removal")
    print(f"{'='*60}")
    print(f"Original records: {original_len:,}")
    print(f"Duplicate records: {duplicate_count:,} ({duplicate_count/original_len*100:.2f}%)")
    print(f"Records after removal: {len(df):,}")
    
    return df


def filter_by_date_range(
    df: pd.DataFrame,
    date_column: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Filter dataset by date range.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to filter
    date_column : str
        Name of the date column
    start_date : str, optional
        Start date (format: 'YYYY-MM-DD')
    end_date : str, optional
        End date (format: 'YYYY-MM-DD')
        
    Returns:
    --------
    pd.DataFrame
        Filtered dataset
        
    Example:
    --------
    >>> df_filtered = filter_by_date_range(df, 'Update_Date', '2020-01-01', '2023-12-31')
    """
    df = df.copy()
    
    if date_column not in df.columns:
        print(f"✗ Error: Column '{date_column}' not found")
        return df
    
    original_len = len(df)
    
    if start_date:
        df = df[df[date_column] >= pd.to_datetime(start_date)]
        print(f"Filtered records after {start_date}: {len(df):,}")
    
    if end_date:
        df = df[df[date_column] <= pd.to_datetime(end_date)]
        print(f"Filtered records before {end_date}: {len(df):,}")
    
    removed = original_len - len(df)
    print(f"Total records removed: {removed:,} ({removed/original_len*100:.2f}%)")
    
    return df


def create_biometric_quality_categories(
    df: pd.DataFrame,
    quality_column: str = 'Biometric_Quality_Score',
    new_column_name: str = 'Quality_Category'
) -> pd.DataFrame:
    """
    Categorize biometric quality scores into quality levels.
    
    Categories:
    - Poor: 0-40 (likely to need re-enrollment)
    - Fair: 41-60 (may need re-enrollment)
    - Good: 61-80 (acceptable quality)
    - Excellent: 81-100 (high quality)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset containing biometric quality scores
    quality_column : str
        Name of the quality score column
    new_column_name : str
        Name for the new category column
        
    Returns:
    --------
    pd.DataFrame
        Dataset with quality category column
        
    Example:
    --------
    >>> df = create_biometric_quality_categories(df)
    """
    df = df.copy()
    
    if quality_column not in df.columns:
        print(f"✗ Error: Column '{quality_column}' not found")
        return df
    
    bins = [0, 41, 61, 81, 101]
    labels = ['Poor (0-40)', 'Fair (41-60)', 'Good (61-80)', 'Excellent (81-100)']
    
    df[new_column_name] = pd.cut(
        df[quality_column],
        bins=bins,
        labels=labels,
        include_lowest=True,
        right=False
    )
    
    print(f"✓ Created {new_column_name} from {quality_column}")
    print(f"\nQuality Distribution:")
    print(df[new_column_name].value_counts().sort_index())
    
    return df


def get_cleaning_summary(df_original: pd.DataFrame, df_cleaned: pd.DataFrame) -> Dict:
    """
    Generate summary of data cleaning operations.
    
    Parameters:
    -----------
    df_original : pd.DataFrame
        Original dataset before cleaning
    df_cleaned : pd.DataFrame
        Dataset after cleaning
        
    Returns:
    --------
    dict
        Summary statistics
        
    Example:
    --------
    >>> summary = get_cleaning_summary(df_raw, df_clean)
    """
    summary = {
        'original_records': len(df_original),
        'cleaned_records': len(df_cleaned),
        'records_removed': len(df_original) - len(df_cleaned),
        'removal_percentage': ((len(df_original) - len(df_cleaned)) / len(df_original) * 100),
        'original_columns': len(df_original.columns),
        'cleaned_columns': len(df_cleaned.columns),
        'columns_removed': len(df_original.columns) - len(df_cleaned.columns)
    }
    
    print(f"\n{'='*60}")
    print("Data Cleaning Summary")
    print(f"{'='*60}")
    print(f"Original Records: {summary['original_records']:,}")
    print(f"Cleaned Records: {summary['cleaned_records']:,}")
    print(f"Records Removed: {summary['records_removed']:,} ({summary['removal_percentage']:.2f}%)")
    print(f"\nOriginal Columns: {summary['original_columns']}")
    print(f"Cleaned Columns: {summary['cleaned_columns']}")
    print(f"Columns Removed: {summary['columns_removed']}")
    
    return summary


if __name__ == "__main__":
    # Example usage
    print("Data Cleaning Module - UIDAI Hackathon 2026")
    print("This module provides functions to clean and preprocess Aadhaar datasets.")
    print("\nKey functions:")
    print("  - create_age_groups(): Create age group categories")
    print("  - handle_missing_values(): Handle missing data")
    print("  - standardize_categorical_columns(): Standardize text columns")
    print("  - remove_duplicates(): Remove duplicate records")
    print("  - create_biometric_quality_categories(): Categorize quality scores")
