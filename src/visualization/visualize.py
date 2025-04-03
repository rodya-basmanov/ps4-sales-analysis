"""
Visualization Module for PS4 Sales Analysis

This module provides functions for creating visualizations of PS4 sales data.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def set_style():
    """Set custom style for plots"""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.figsize'] = (12, 7)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 11
    plt.rcParams['figure.titlesize'] = 16


def save_figure(fig, filename, dir_path=None):
    """
    Save figure to specified directory

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure to save
    filename : str
        Filename for the figure
    dir_path : str, optional
        Directory to save the figure. If None, default path is used.
    """
    if dir_path is None:
        # Default path relative to project root
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        dir_path = os.path.join(base_dir, 'reports', 'figures')

    # Create directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)

    # Save figure
    filepath = os.path.join(dir_path, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Figure saved to {filepath}")

    return filepath


def plot_regional_sales(df, region_names=None):
    """
    Create bar chart of mean sales by region

    Parameters:
    -----------
    df : pandas.DataFrame
        PS4 sales data
    region_names : dict, optional
        Dictionary mapping region codes to display names

    Returns:
    --------
    matplotlib.figure.Figure
        Figure object containing the plot
    """
    # Set default styles
    set_style()

    # If region names not provided, use defaults
    if region_names is None:
        # Using English names for consistency
        region_names = {
            'North America': 'North America',
            'europe': 'Europe',
            'japan': 'Japan',
            'Rest of World': 'Rest of World',
            'global': 'Global'
        }

    # Calculate mean sales for each region
    numeric_columns = ['North America', 'europe',
                       'japan', 'Rest of World', 'global']
    means = {}
    for column in numeric_columns:
        means[column] = df[column].mean()

    # Create dictionary with display names as keys
    display_means = {region_names.get(k, k): v for k, v in means.items()}

    # Create figure and axis
    fig, ax = plt.subplots()

    # Create bar chart
    colors = ['blue', 'green', 'red', 'orange', 'purple']
    bars = ax.bar(display_means.keys(), display_means.values(), color=colors)

    # Add values above bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom')

    # Add labels and title
    ax.set_title('Average Sales by Region (M copies)')
    ax.set_xlabel('Region')
    ax.set_ylabel('Average Sales (M)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


def plot_year_dynamics(df):
    """
    Create line and bar chart of sales dynamics by year

    Parameters:
    -----------
    df : pandas.DataFrame
        PS4 sales data

    Returns:
    --------
    matplotlib.figure.Figure
        Figure object containing the plot
    """
    # Set default styles
    set_style()

    # Group by year
    yearly_counts = df.groupby('year').size()
    yearly_global_mean = df.groupby('year')['global'].mean()

    # Create figure with two y-axes
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Plot line for mean sales
    line = ax1.plot(yearly_global_mean.index, yearly_global_mean, 'b-', marker='o',
                    linewidth=2, label='Average Sales (M)')

    # Plot bars for number of games
    bars = ax2.bar(yearly_counts.index, yearly_counts, alpha=0.3, color='gray',
                   label='Number of Games')

    # Add value labels to line points
    for i, value in enumerate(yearly_global_mean):
        if not np.isnan(value) and value > 0:
            year = yearly_global_mean.index[i]
            ax1.annotate(f'{value:.2f}', (year, value), textcoords="offset points",
                         xytext=(0, 10), ha='center')

    # Set labels and title
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Average Sales (M)', color='b')
    ax2.set_ylabel('Number of Games', color='gray')
    plt.title('Dynamics of Average Sales and Number of Games by Year')

    # Add legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper right')

    # Add grid for y-axis
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    return fig


def plot_genre_heatmap(df):
    """
    Create heatmap of genre preferences by region

    Parameters:
    -----------
    df : pandas.DataFrame
        PS4 sales data

    Returns:
    --------
    matplotlib.figure.Figure
        Figure object containing the plot
    """
    # Set default styles
    set_style()

    # Get top 10 genres by overall count
    top10_genres = df.groupby('genre').size().sort_values(
        ascending=False).head(10).index.tolist()

    # Map region names
    region_names = {
        'North America': 'North America',
        'europe': 'Europe',
        'japan': 'Japan',
        'Rest of World': 'Rest of World'
    }

    # Create pivot table with mean sales by genre and region
    pivot_data = pd.DataFrame()
    for region in ['North America', 'europe', 'japan', 'Rest of World']:
        genre_region_means = df[df['genre'].isin(top10_genres)].groupby('genre')[
            region].mean()
        pivot_data[region_names[region]] = genre_region_means

    # Normalize data for better visualization
    pivot_norm = pivot_data.div(pivot_data.max(axis=0), axis=1)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create heatmap
    im = ax.pcolormesh(pivot_norm, cmap='YlOrRd')
    fig.colorbar(im, ax=ax, label='Relative Sales')

    # Set ticks and labels
    ax.set_xticks(np.arange(0.5, len(pivot_data.columns)))
    ax.set_yticks(np.arange(0.5, len(pivot_data.index)))
    ax.set_xticklabels(pivot_data.columns, rotation=45)
    ax.set_yticklabels(pivot_data.index)

    # Set title
    ax.set_title('Heatmap of Genre Popularity by Region (Relative Sales)')

    plt.tight_layout()

    return fig


def plot_correlation_scatter(df):
    """
    Create scatter plot showing correlation between number of games and average sales

    Parameters:
    -----------
    df : pandas.DataFrame
        PS4 sales data

    Returns:
    --------
    matplotlib.figure.Figure
        Figure object containing the plot
    """
    # Set default styles
    set_style()

    # Group by year
    yearly_counts = df.groupby('year').size()
    yearly_global_mean = df.groupby('year')['global'].mean()
    yearly_global_sum = df.groupby('year')['global'].sum()

    # Create figure
    fig, ax = plt.subplots()

    # Create scatter plot
    scatter = ax.scatter(yearly_counts, yearly_global_mean,
                         s=yearly_global_sum*3, alpha=0.6,
                         c=yearly_counts.index, cmap='viridis')

    # Add year labels to points
    for i, year in enumerate(yearly_counts.index):
        if year != 0 and not np.isnan(yearly_global_mean.iloc[i]):
            ax.annotate(str(year),
                        (yearly_counts.iloc[i], yearly_global_mean.iloc[i]),
                        textcoords="offset points", xytext=(5, 5), ha='left')

    # Add trend line
    z = np.polyfit(yearly_counts, yearly_global_mean, 1)
    p = np.poly1d(z)
    ax.plot(yearly_counts, p(yearly_counts), "r--", alpha=0.6)

    # Calculate correlation coefficient
    corr = yearly_counts.corr(yearly_global_mean)

    # Add labels and title
    ax.set_xlabel('Number of Games Released')
    ax.set_ylabel('Average Sales (M)')
    ax.set_title(
        f'Relationship Between Number of Games and Average Sales\nCorrelation: {corr:.2f}')

    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    return fig


def create_all_visualizations(df):
    """
    Create and save all visualizations for the analysis

    Parameters:
    -----------
    df : pandas.DataFrame
        PS4 sales data

    Returns:
    --------
    list
        List of paths to saved figures
    """
    # Create output directory for figures
    base_dir = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(base_dir, 'reports', 'figures')
    os.makedirs(output_dir, exist_ok=True)

    # Create and save regional sales plot
    fig1 = plot_regional_sales(df)
    path1 = save_figure(fig1, 'regional_sales.png', output_dir)
    plt.close(fig1)

    # Create and save year dynamics plot
    fig2 = plot_year_dynamics(df)
    path2 = save_figure(fig2, 'year_dynamics.png', output_dir)
    plt.close(fig2)

    # Create and save genre heatmap
    fig3 = plot_genre_heatmap(df)
    path3 = save_figure(fig3, 'genre_heatmap.png', output_dir)
    plt.close(fig3)

    # Create and save correlation scatter plot
    fig4 = plot_correlation_scatter(df)
    path4 = save_figure(fig4, 'correlation_scatter.png', output_dir)
    plt.close(fig4)

    return [path1, path2, path3, path4]


if __name__ == "__main__":
    # This block executes when the script is run directly
    from ps4_sales_analysis.src.data.data_processing import load_data, preprocess_data

    # Load and preprocess data
    df_raw = load_data()
    df = preprocess_data(df_raw)

    # Create all visualizations
    figure_paths = create_all_visualizations(df)

    print("All visualizations have been created successfully!")
