"""
Report Generation Module for UIDAI Biometric Update Analysis
==============================================================

This module provides functions to create publication-quality visualizations
and summary tables for the final PDF report.

Author: UIDAI Hackathon 2026 Team
Date: January 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import warnings

warnings.filterwarnings('ignore')

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10


def create_age_distribution_chart(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    save_path: Optional[str] = None,
    title: str = 'Aadhaar Enrolment Distribution by Age Group'
) -> None:
    """
    Create professional age distribution bar chart for report.
    
    **What it shows**: Number and percentage of enrolments in each age category
    **Why include**: Demonstrates demographic coverage and representation
    **Governance insight**: Identifies underserved populations
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with age groups
    age_group_column : str
        Name of age group column
    save_path : str, optional
        Path to save figure
    title : str
        Chart title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate distribution
    age_counts = df[age_group_column].value_counts().sort_index()
    age_pct = (age_counts / len(df) * 100).round(1)
    
    # Create bar chart
    bars = ax.bar(range(len(age_counts)), age_counts.values, 
                   color='steelblue', edgecolor='black', alpha=0.8, linewidth=1.5)
    
    # Add value labels with percentages
    for i, (count, pct) in enumerate(zip(age_counts.values, age_pct.values)):
        ax.text(i, count + max(age_counts.values)*0.01, 
                f'{count:,}\n({pct}%)', 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Formatting
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Age Group', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Enrolments', fontsize=13, fontweight='bold')
    ax.set_xticks(range(len(age_counts)))
    ax.set_xticklabels(age_counts.index, rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def create_quality_comparison_chart(
    quality_stats: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    save_path: Optional[str] = None
) -> None:
    """
    Create dual-axis chart comparing quality scores and sample sizes.
    
    **What it shows**: Mean quality score per age group with confidence intervals
    **Why include**: Core finding - quality degradation with age
    **Governance insight**: Identifies which age groups need intervention
    
    Parameters:
    -----------
    quality_stats : pd.DataFrame
        Quality statistics by age group (from analyzer.py)
    age_group_column : str
        Name of age group column
    save_path : str, optional
        Path to save figure
    """
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    age_groups = quality_stats[age_group_column]
    mean_quality = quality_stats['Mean_Quality']
    std_quality = quality_stats['Std_Dev']
    counts = quality_stats['Count']
    
    # Primary axis: Mean quality with error bars
    x_pos = np.arange(len(age_groups))
    ax1.errorbar(x_pos, mean_quality, yerr=std_quality, 
                 fmt='o-', linewidth=3, markersize=10, 
                 color='darkblue', ecolor='gray', capsize=5, capthick=2,
                 label='Mean Quality ± Std Dev')
    
    # Add threshold lines
    ax1.axhline(y=60, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Fair Threshold (60)')
    ax1.axhline(y=40, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Poor Threshold (40)')
    
    # Formatting primary axis
    ax1.set_xlabel('Age Group', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Mean Biometric Quality Score', fontsize=13, fontweight='bold', color='darkblue')
    ax1.tick_params(axis='y', labelcolor='darkblue')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(age_groups, rotation=45, ha='right')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_ylim(bottom=0)
    
    # Secondary axis: Sample size
    ax2 = ax1.twinx()
    ax2.bar(x_pos, counts, alpha=0.3, color='lightgray', edgecolor='black', 
            linewidth=1, label='Sample Size')
    ax2.set_ylabel('Number of Enrolments', fontsize=13, fontweight='bold', color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')
    
    # Title and legends
    plt.title('Biometric Quality Score by Age Group with Sample Sizes', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', framealpha=0.9)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def create_temporal_trend_chart(
    df: pd.DataFrame,
    date_column: str = 'Enrolment_Date',
    quality_column: str = 'Biometric_Quality_Score',
    freq: str = 'M',
    save_path: Optional[str] = None
) -> None:
    """
    Create time-series chart showing quality trends over time.
    
    **What it shows**: How biometric quality has changed over enrollment period
    **Why include**: Reveals system improvements or degradation over time
    **Governance insight**: Identifies when quality issues emerged
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with dates and quality scores
    date_column : str
        Name of date column
    quality_column : str
        Name of quality score column
    freq : str
        Frequency for aggregation ('M'=monthly, 'Q'=quarterly, 'Y'=yearly)
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Prepare data
    df_temp = df.copy()
    df_temp[date_column] = pd.to_datetime(df_temp[date_column])
    df_temp = df_temp.set_index(date_column)
    
    # Aggregate by time period
    quality_trend = df_temp[quality_column].resample(freq).agg(['mean', 'count'])
    
    # Plot mean quality
    ax.plot(quality_trend.index, quality_trend['mean'], 
            linewidth=3, marker='o', markersize=6, color='darkgreen', label='Mean Quality')
    
    # Add moving average
    if len(quality_trend) > 3:
        ma = quality_trend['mean'].rolling(window=3, center=True).mean()
        ax.plot(quality_trend.index, ma, linewidth=2, linestyle='--', 
                color='red', alpha=0.7, label='3-Period Moving Average')
    
    # Add threshold line
    ax.axhline(y=60, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Fair Threshold')
    
    # Formatting
    ax.set_title('Biometric Quality Trend Over Time', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Time Period', fontsize=13, fontweight='bold')
    ax.set_ylabel('Mean Biometric Quality Score', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='best', framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def create_anomaly_summary_chart(
    df_with_anomalies: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    anomaly_type_column: str = 'anomaly_type',
    save_path: Optional[str] = None
) -> None:
    """
    Create stacked bar chart showing anomaly distribution by age group.
    
    **What it shows**: Number of positive/negative anomalies in each age group
    **Why include**: Highlights exceptional cases requiring investigation
    **Governance insight**: Identifies where to learn best practices or fix issues
    
    Parameters:
    -----------
    df_with_anomalies : pd.DataFrame
        Dataset with anomaly classifications
    age_group_column : str
        Name of age group column
    anomaly_type_column : str
        Name of anomaly type column
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Create cross-tabulation
    anomaly_crosstab = pd.crosstab(
        df_with_anomalies[age_group_column],
        df_with_anomalies[anomaly_type_column]
    )
    
    # Reorder columns for better visualization
    column_order = ['Unusually Low Quality', 'Normal', 'Unusually High Quality']
    anomaly_crosstab = anomaly_crosstab[[col for col in column_order if col in anomaly_crosstab.columns]]
    
    # Create stacked bar chart
    anomaly_crosstab.plot(kind='bar', stacked=True, ax=ax,
                          color=['#d62728', '#7f7f7f', '#2ca02c'],
                          edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Formatting
    ax.set_title('Anomaly Distribution by Age Group', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Age Group', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Records', fontsize=13, fontweight='bold')
    ax.legend(title='Anomaly Type', title_fontsize=11, framealpha=0.9, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.tick_params(axis='x', rotation=45)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def create_executive_summary_table(
    age_dist_stats: pd.DataFrame,
    quality_stats: pd.DataFrame,
    test_results: Dict,
    save_path: Optional[str] = None
) -> pd.DataFrame:
    """
    Create executive summary table with key metrics.
    
    **What it shows**: One-page summary of all critical findings
    **Why include**: Quick reference for decision-makers
    **Governance insight**: Actionable metrics at a glance
    
    Parameters:
    -----------
    age_dist_stats : pd.DataFrame
        Age distribution statistics
    quality_stats : pd.DataFrame
        Quality statistics by age
    test_results : dict
        Statistical test results
    save_path : str, optional
        Path to save table as CSV
        
    Returns:
    --------
    pd.DataFrame
        Executive summary table
    """
    print(f"\n{'='*80}")
    print("EXECUTIVE SUMMARY TABLE")
    print(f"{'='*80}")
    
    # Merge statistics
    summary = age_dist_stats.merge(
        quality_stats[['Age_Group', 'Mean_Quality', 'Std_Dev']],
        on='Age_Group',
        how='left'
    )
    
    # Add quality rating
    summary['Quality_Rating'] = summary['Mean_Quality'].apply(
        lambda x: 'Excellent' if x >= 81 else 
                  'Good' if x >= 61 else 
                  'Fair' if x >= 41 else 
                  'Poor'
    )
    
    # Rename columns for clarity
    summary = summary.rename(columns={
        'Age_Group': 'Age Group',
        'Count': 'Enrolments',
        'Percentage': '% of Total',
        'Mean_Quality': 'Avg Quality',
        'Std_Dev': 'Std Dev',
        'Quality_Rating': 'Rating'
    })
    
    # Reorder columns
    summary = summary[['Age Group', 'Enrolments', '% of Total', 'Avg Quality', 'Std Dev', 'Rating']]
    
    print("\nKey Metrics by Age Group:")
    print(summary.to_string(index=False))
    
    # Add statistical test summary
    print(f"\n{'='*80}")
    print("STATISTICAL TEST RESULTS")
    print(f"{'='*80}")
    print(f"Chi-Square Test: {'SIGNIFICANT' if test_results.get('chi2_significant', False) else 'NOT SIGNIFICANT'}")
    print(f"  → P-value: {test_results.get('chi2_pvalue', 'N/A')}")
    print(f"ANOVA Test: {'SIGNIFICANT' if test_results.get('anova_significant', False) else 'NOT SIGNIFICANT'}")
    print(f"  → P-value: {test_results.get('anova_pvalue', 'N/A')}")
    
    if save_path:
        summary.to_csv(save_path, index=False)
        print(f"\n✓ Saved: {save_path}")
    
    return summary


def create_recommendations_table(
    quality_stats: pd.DataFrame,
    anomaly_stats: Dict,
    save_path: Optional[str] = None
) -> pd.DataFrame:
    """
    Create governance recommendations table by age group.
    
    **What it shows**: Specific actions for each age group
    **Why include**: Translates findings into actionable steps
    **Governance insight**: Implementation roadmap for UIDAI
    
    Parameters:
    -----------
    quality_stats : pd.DataFrame
        Quality statistics by age
    anomaly_stats : dict
        Anomaly detection statistics
    save_path : str, optional
        Path to save table
        
    Returns:
    --------
    pd.DataFrame
        Recommendations table
    """
    print(f"\n{'='*80}")
    print("GOVERNANCE RECOMMENDATIONS BY AGE GROUP")
    print(f"{'='*80}")
    
    recommendations = []
    
    for _, row in quality_stats.iterrows():
        age_group = row['Age_Group']
        mean_quality = row['Mean_Quality']
        
        # Determine priority and actions
        if mean_quality < 50:
            priority = 'HIGH'
            actions = [
                'Deploy specialized biometric devices',
                'Implement assisted enrollment',
                'Conduct targeted re-enrollment campaign',
                'Train operators on age-specific challenges'
            ]
        elif mean_quality < 65:
            priority = 'MEDIUM'
            actions = [
                'Monitor quality trends closely',
                'Provide additional enrollment support',
                'Consider multi-modal biometrics',
                'Improve operator training'
            ]
        else:
            priority = 'LOW'
            actions = [
                'Maintain current protocols',
                'Share best practices',
                'Monitor for quality degradation'
            ]
        
        recommendations.append({
            'Age_Group': age_group,
            'Current_Quality': f"{mean_quality:.1f}",
            'Priority': priority,
            'Primary_Action': actions[0],
            'Secondary_Actions': '; '.join(actions[1:])
        })
    
    rec_df = pd.DataFrame(recommendations)
    
    print("\nRecommended Actions:")
    for _, row in rec_df.iterrows():
        print(f"\n{row['Age_Group']} (Quality: {row['Current_Quality']}) - Priority: {row['Priority']}")
        print(f"  → {row['Primary_Action']}")
        print(f"  → {row['Secondary_Actions']}")
    
    if save_path:
        rec_df.to_csv(save_path, index=False)
        print(f"\n✓ Saved: {save_path}")
    
    return rec_df


def create_final_report_dashboard(
    df: pd.DataFrame,
    quality_stats: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_column: str = 'Biometric_Quality_Score',
    quality_category_column: str = 'Quality_Category',
    save_path: Optional[str] = None
) -> None:
    """
    Create comprehensive 6-panel dashboard for final report.
    
    **What it shows**: Complete visual summary on one page
    **Why include**: Single-page overview for executive presentation
    **Governance insight**: All key findings at a glance
    
    Parameters:
    -----------
    df : pd.DataFrame
        Full dataset
    quality_stats : pd.DataFrame
        Quality statistics by age
    age_group_column : str
        Name of age group column
    quality_column : str
        Name of quality score column
    quality_category_column : str
        Name of quality category column
    save_path : str, optional
        Path to save figure
    """
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Panel 1: Age Distribution
    ax1 = fig.add_subplot(gs[0, 0])
    age_counts = df[age_group_column].value_counts().sort_index()
    ax1.bar(range(len(age_counts)), age_counts.values, color='steelblue', edgecolor='black', alpha=0.8)
    ax1.set_title('Age Group Distribution', fontsize=13, fontweight='bold')
    ax1.set_xlabel('Age Group', fontweight='bold')
    ax1.set_ylabel('Count', fontweight='bold')
    ax1.set_xticks(range(len(age_counts)))
    ax1.set_xticklabels(age_counts.index, rotation=45, ha='right', fontsize=9)
    ax1.grid(axis='y', alpha=0.3)
    
    # Panel 2: Quality Box Plot
    ax2 = fig.add_subplot(gs[0, 1])
    df_plot = df[[age_group_column, quality_column]].dropna()
    sns.boxplot(data=df_plot, x=age_group_column, y=quality_column, ax=ax2, palette='Set2')
    ax2.axhline(y=60, color='red', linestyle='--', alpha=0.5)
    ax2.set_title('Quality Distribution by Age', fontsize=13, fontweight='bold')
    ax2.set_xlabel('Age Group', fontweight='bold')
    ax2.set_ylabel('Quality Score', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45, labelsize=9)
    
    # Panel 3: Mean Quality Trend
    ax3 = fig.add_subplot(gs[1, 0])
    age_groups = quality_stats['Age_Group']
    mean_quality = quality_stats['Mean_Quality']
    ax3.plot(range(len(age_groups)), mean_quality.values, marker='o', linewidth=3, markersize=8, color='darkblue')
    ax3.axhline(y=60, color='orange', linestyle='--', alpha=0.5, label='Fair Threshold')
    ax3.set_title('Mean Quality Trend', fontsize=13, fontweight='bold')
    ax3.set_xlabel('Age Group', fontweight='bold')
    ax3.set_ylabel('Mean Quality', fontweight='bold')
    ax3.set_xticks(range(len(age_groups)))
    ax3.set_xticklabels(age_groups, rotation=45, ha='right', fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.legend(fontsize=9)
    
    # Panel 4: Quality Categories Stacked
    ax4 = fig.add_subplot(gs[1, 1])
    crosstab = pd.crosstab(df[age_group_column], df[quality_category_column], normalize='index') * 100
    crosstab.plot(kind='bar', stacked=True, ax=ax4, colormap='RdYlGn', edgecolor='black', alpha=0.8)
    ax4.set_title('Quality Category Distribution', fontsize=13, fontweight='bold')
    ax4.set_xlabel('Age Group', fontweight='bold')
    ax4.set_ylabel('Percentage (%)', fontweight='bold')
    ax4.tick_params(axis='x', rotation=45, labelsize=9)
    ax4.legend(title='Quality', fontsize=8, title_fontsize=9, loc='upper left')
    
    # Panel 5: Summary Statistics Table
    ax5 = fig.add_subplot(gs[2, :])
    ax5.axis('tight')
    ax5.axis('off')
    
    # Create summary table data
    table_data = []
    for _, row in quality_stats.iterrows():
        table_data.append([
            row['Age_Group'],
            f"{row['Count']:,}",
            f"{row['Mean_Quality']:.1f}",
            f"{row['Median_Quality']:.1f}",
            f"{row['Std_Dev']:.1f}",
            f"{row['Min_Quality']:.0f}",
            f"{row['Max_Quality']:.0f}"
        ])
    
    table = ax5.table(cellText=table_data,
                      colLabels=['Age Group', 'Count', 'Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                      cellLoc='center',
                      loc='center',
                      bbox=[0, 0, 1, 1])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header
    for i in range(7):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data) + 1):
        for j in range(7):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#E7E6E6')
    
    # Main title
    fig.suptitle('Biometric Quality Analysis - Executive Dashboard', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


if __name__ == "__main__":
    print("Report Generation Module - UIDAI Hackathon 2026")
    print("This module provides publication-quality visualization and table functions.")
    print("\nKey functions:")
    print("  - create_age_distribution_chart(): Age group bar chart")
    print("  - create_quality_comparison_chart(): Quality scores with error bars")
    print("  - create_temporal_trend_chart(): Time-series quality trends")
    print("  - create_anomaly_summary_chart(): Anomaly distribution")
    print("  - create_executive_summary_table(): Key metrics table")
    print("  - create_recommendations_table(): Governance actions")
    print("  - create_final_report_dashboard(): 6-panel comprehensive dashboard")
