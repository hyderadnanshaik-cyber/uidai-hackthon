"""
Visualization Module for UIDAI Biometric Update Analysis
==========================================================

This module provides functions to create publication-quality visualizations
for the UIDAI hackathon analysis and final PDF report.

Author: UIDAI Hackathon 2026 Team
Date: January 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, List, Tuple
import warnings

warnings.filterwarnings('ignore')

# Set default style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def plot_age_distribution(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    save_path: Optional[str] = None
) -> None:
    """
    Create bar chart of age group distribution.
    
    **What it shows**: Number of records in each age category
    **Insight**: Identifies over/under-represented demographics
    """
    plt.figure(figsize=(10, 6))
    
    age_counts = df[age_group_column].value_counts().sort_index()
    
    ax = age_counts.plot(kind='bar', color='steelblue', edgecolor='black', alpha=0.7)
    plt.title('Distribution of Enrolments by Age Group', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Age Group', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Enrolments', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for i, v in enumerate(age_counts.values):
        ax.text(i, v + max(age_counts.values)*0.01, f'{v:,}', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_quality_by_age(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_column: str = 'Biometric_Quality_Score',
    save_path: Optional[str] = None
) -> None:
    """
    Create box plot of biometric quality scores by age group.
    
    **What it shows**: Distribution of quality scores within each age group
    **Insight**: Reveals which age groups have quality challenges
    """
    plt.figure(figsize=(12, 6))
    
    # Create box plot
    sns.boxplot(data=df, x=age_group_column, y=quality_column, palette='Set2')
    
    plt.title('Biometric Quality Scores by Age Group', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Age Group', fontsize=12, fontweight='bold')
    plt.ylabel('Biometric Quality Score', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    
    # Add horizontal line at quality threshold (60 = Fair/Good boundary)
    plt.axhline(y=60, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Fair/Good Threshold')
    plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_quality_categories_by_age(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_category_column: str = 'Quality_Category',
    save_path: Optional[str] = None
) -> None:
    """
    Create stacked bar chart of quality categories by age group.
    
    **What it shows**: Percentage of each quality level within age groups
    **Insight**: Identifies which ages need re-enrollment most
    """
    plt.figure(figsize=(12, 7))
    
    # Create cross-tabulation with percentages
    crosstab = pd.crosstab(df[age_group_column], df[quality_category_column], normalize='index') * 100
    
    # Plot stacked bar chart
    ax = crosstab.plot(kind='bar', stacked=True, colormap='RdYlGn', edgecolor='black', alpha=0.8)
    
    plt.title('Biometric Quality Distribution by Age Group', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Age Group', fontsize=12, fontweight='bold')
    plt.ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Quality Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.ylim(0, 100)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_mean_quality_by_age(
    quality_stats: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    save_path: Optional[str] = None
) -> None:
    """
    Create line plot of mean quality scores by age group.
    
    **What it shows**: Trend of quality scores across age groups
    **Insight**: Visualizes quality degradation with age
    """
    plt.figure(figsize=(10, 6))
    
    # Extract data
    age_groups = quality_stats[age_group_column]
    mean_quality = quality_stats['Mean_Quality']
    
    # Create line plot with markers
    plt.plot(age_groups, mean_quality, marker='o', linewidth=3, markersize=10, color='darkblue')
    
    # Add value labels
    for i, (ag, mq) in enumerate(zip(age_groups, mean_quality)):
        plt.text(i, mq + 1, f'{mq:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.title('Mean Biometric Quality Score by Age Group', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Age Group', fontsize=12, fontweight='bold')
    plt.ylabel('Mean Quality Score', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.ylim(bottom=0)
    
    # Add threshold lines
    plt.axhline(y=60, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Fair Threshold')
    plt.axhline(y=40, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Poor Threshold')
    plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_update_rates_by_age(
    update_stats: pd.DataFrame,
    save_path: Optional[str] = None
) -> None:
    """
    Create bar chart of update rates by age group.
    
    **What it shows**: Updates per 1000 enrolments for each age group
    **Insight**: Identifies which demographics update most frequently
    """
    plt.figure(figsize=(10, 6))
    
    age_groups = update_stats['Age_Group']
    update_rates = update_stats['Updates_per_1000']
    
    ax = plt.bar(range(len(age_groups)), update_rates, color='coral', edgecolor='black', alpha=0.7)
    
    plt.title('Update Rate by Age Group', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Age Group', fontsize=12, fontweight='bold')
    plt.ylabel('Updates per 1,000 Enrolments', fontsize=12, fontweight='bold')
    plt.xticks(range(len(age_groups)), age_groups, rotation=45, ha='right')
    
    # Add value labels
    for i, v in enumerate(update_rates):
        plt.text(i, v + max(update_rates)*0.01, f'{v:.1f}', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_update_types_heatmap(
    crosstab_pct: pd.DataFrame,
    save_path: Optional[str] = None
) -> None:
    """
    Create heatmap of update types by age group.
    
    **What it shows**: Percentage of each update type within age groups
    **Insight**: Reveals age-specific update needs
    """
    plt.figure(figsize=(12, 6))
    
    sns.heatmap(crosstab_pct, annot=True, fmt='.1f', cmap='YlOrRd', 
                linewidths=0.5, cbar_kws={'label': 'Percentage (%)'})
    
    plt.title('Update Type Distribution by Age Group (%)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Update Type', fontsize=12, fontweight='bold')
    plt.ylabel('Age Group', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def plot_correlation_heatmap(
    corr_matrix: pd.DataFrame,
    save_path: Optional[str] = None
) -> None:
    """
    Create correlation heatmap.
    
    **What it shows**: Relationships between numerical variables
    **Insight**: Identifies statistical associations
    """
    plt.figure(figsize=(10, 8))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, vmin=-1, vmax=1, square=True,
                linewidths=0.5, cbar_kws={'label': 'Correlation Coefficient'})
    
    plt.title('Correlation Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


def create_multi_panel_summary(
    df: pd.DataFrame,
    age_group_column: str = 'Age_Group',
    quality_column: str = 'Biometric_Quality_Score',
    quality_category_column: str = 'Quality_Category',
    save_path: Optional[str] = None
) -> None:
    """
    Create comprehensive 4-panel summary visualization.
    
    **What it shows**: Complete overview of age-quality patterns
    **Insight**: Single-page summary for report
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Biometric Quality Analysis by Age Group - Summary Dashboard', 
                 fontsize=18, fontweight='bold', y=0.995)
    
    # Panel 1: Age distribution
    ax1 = axes[0, 0]
    age_counts = df[age_group_column].value_counts().sort_index()
    age_counts.plot(kind='bar', ax=ax1, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_title('Age Group Distribution', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Age Group', fontweight='bold')
    ax1.set_ylabel('Count', fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    
    # Panel 2: Quality box plot
    ax2 = axes[0, 1]
    sns.boxplot(data=df, x=age_group_column, y=quality_column, ax=ax2, palette='Set2')
    ax2.set_title('Quality Score Distribution by Age', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Age Group', fontweight='bold')
    ax2.set_ylabel('Quality Score', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.axhline(y=60, color='red', linestyle='--', alpha=0.5)
    
    # Panel 3: Mean quality trend
    ax3 = axes[1, 0]
    quality_by_age = df.groupby(age_group_column)[quality_column].mean().sort_index()
    ax3.plot(range(len(quality_by_age)), quality_by_age.values, 
             marker='o', linewidth=3, markersize=10, color='darkblue')
    ax3.set_title('Mean Quality Score Trend', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Age Group', fontweight='bold')
    ax3.set_ylabel('Mean Quality Score', fontweight='bold')
    ax3.set_xticks(range(len(quality_by_age)))
    ax3.set_xticklabels(quality_by_age.index, rotation=45, ha='right')
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=60, color='orange', linestyle='--', alpha=0.5)
    
    # Panel 4: Quality categories stacked bar
    ax4 = axes[1, 1]
    crosstab = pd.crosstab(df[age_group_column], df[quality_category_column], normalize='index') * 100
    crosstab.plot(kind='bar', stacked=True, ax=ax4, colormap='RdYlGn', edgecolor='black', alpha=0.8)
    ax4.set_title('Quality Category Distribution', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Age Group', fontweight='bold')
    ax4.set_ylabel('Percentage (%)', fontweight='bold')
    ax4.tick_params(axis='x', rotation=45)
    ax4.legend(title='Quality', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {save_path}")
    
    plt.show()


if __name__ == "__main__":
    print("Visualization Module - UIDAI Hackathon 2026")
    print("This module provides publication-quality visualization functions.")
    print("\nKey functions:")
    print("  - plot_age_distribution(): Age group bar chart")
    print("  - plot_quality_by_age(): Quality box plot by age")
    print("  - plot_quality_categories_by_age(): Stacked bar chart")
    print("  - plot_mean_quality_by_age(): Quality trend line")
    print("  - plot_update_rates_by_age(): Update rate bar chart")
    print("  - plot_update_types_heatmap(): Update type heatmap")
    print("  - plot_correlation_heatmap(): Correlation matrix")
    print("  - create_multi_panel_summary(): 4-panel dashboard")
