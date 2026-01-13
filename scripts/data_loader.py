"""
Data Loader Module for UIDAI Biometric Update Analysis
========================================================

This module provides functions to load Aadhaar enrolment and update datasets
from various file formats (CSV, Excel) and perform initial data type conversions.

Author: UIDAI Hackathon 2026 Team
Date: January 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, Optional, Dict
import warnings

warnings.filterwarnings('ignore')


def load_enrolment_data(
    file_path: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """
    Load Aadhaar enrolment dataset from CSV or Excel file.
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the enrolment dataset file
    **kwargs : dict
        Additional arguments to pass to pandas read function
        
    Returns:
    --------
    pd.DataFrame
        Loaded enrolment dataset
        
    Example:
    --------
    >>> df_enrolment = load_enrolment_data('data/raw/enrolment_data.csv')
    >>> print(f"Loaded {len(df_enrolment)} enrolment records")
    """
    file_path = Path(file_path)
    
    print(f"Loading enrolment data from: {file_path.name}")
    
    # Determine file type and load accordingly
    if file_path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path, **kwargs)
    elif file_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    print(f"✓ Loaded {len(df):,} enrolment records with {len(df.columns)} columns")
    
    return df


def load_update_data(
    file_path: Union[str, Path],
    **kwargs
) -> pd.DataFrame:
    """
    Load Aadhaar update dataset from CSV or Excel file.
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the update dataset file
    **kwargs : dict
        Additional arguments to pass to pandas read function
        
    Returns:
    --------
    pd.DataFrame
        Loaded update dataset
        
    Example:
    --------
    >>> df_updates = load_update_data('data/raw/update_data.csv')
    >>> print(f"Loaded {len(df_updates)} update records")
    """
    file_path = Path(file_path)
    
    print(f"Loading update data from: {file_path.name}")
    
    # Determine file type and load accordingly
    if file_path.suffix.lower() == '.csv':
        df = pd.read_csv(file_path, **kwargs)
    elif file_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    print(f"✓ Loaded {len(df):,} update records with {len(df.columns)} columns")
    
    return df


def get_data_info(df: pd.DataFrame, dataset_name: str = "Dataset") -> Dict:
    """
    Get comprehensive information about the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to analyze
    dataset_name : str
        Name of the dataset for display purposes
        
    Returns:
    --------
    dict
        Dictionary containing dataset statistics
        
    Example:
    --------
    >>> info = get_data_info(df_enrolment, "Enrolment Data")
    """
    print(f"\n{'='*60}")
    print(f"{dataset_name} - Overview")
    print(f"{'='*60}")
    
    info = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'missing_values': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum()
    }
    
    print(f"Total Records: {info['total_records']:,}")
    print(f"Total Columns: {info['total_columns']}")
    print(f"Memory Usage: {info['memory_usage_mb']:.2f} MB")
    print(f"Missing Values: {info['missing_values']:,}")
    print(f"Duplicate Rows: {info['duplicate_rows']:,}")
    
    print(f"\nColumn Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\nData Types:")
    print(df.dtypes.value_counts())
    
    return info


def convert_date_columns(
    df: pd.DataFrame,
    date_columns: list,
    date_format: Optional[str] = None
) -> pd.DataFrame:
    """
    Convert specified columns to datetime format.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset containing date columns
    date_columns : list
        List of column names to convert to datetime
    date_format : str, optional
        Specific date format to use for parsing
        
    Returns:
    --------
    pd.DataFrame
        Dataset with converted date columns
        
    Example:
    --------
    >>> df = convert_date_columns(df, ['Enrolment_Date', 'Update_Date'])
    """
    df = df.copy()
    
    for col in date_columns:
        if col in df.columns:
            print(f"Converting {col} to datetime...")
            try:
                if date_format:
                    df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')
                else:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                print(f"  ✓ Converted {col}")
            except Exception as e:
                print(f"  ✗ Error converting {col}: {str(e)}")
        else:
            print(f"  ⚠ Column {col} not found in dataset")
    
    return df


def save_processed_data(
    df: pd.DataFrame,
    file_name: str,
    output_dir: Union[str, Path] = "data/processed"
) -> None:
    """
    Save processed dataset to CSV file.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to save
    file_name : str
        Name of the output file (with or without .csv extension)
    output_dir : str or Path
        Directory to save the file
        
    Example:
    --------
    >>> save_processed_data(df_clean, 'enrolment_cleaned.csv')
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not file_name.endswith('.csv'):
        file_name += '.csv'
    
    output_path = output_dir / file_name
    
    df.to_csv(output_path, index=False)
    print(f"✓ Saved processed data to: {output_path}")
    print(f"  Records: {len(df):,} | Columns: {len(df.columns)}")


if __name__ == "__main__":
    # Example usage
    print("Data Loader Module - UIDAI Hackathon 2026")
    print("This module provides functions to load and process Aadhaar datasets.")
    print("\nExample usage:")
    print("  from scripts.data_loader import load_enrolment_data, load_update_data")
    print("  df_enrolment = load_enrolment_data('data/raw/enrolment_data.csv')")
    print("  df_updates = load_update_data('data/raw/update_data.csv')")
