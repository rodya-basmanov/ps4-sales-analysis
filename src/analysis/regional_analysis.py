"""
Module for analyzing regional sales of PS4 games

This module provides functions for analyzing PlayStation 4 game sales
in different geographical regions.
"""

import os
import pandas as pd
import numpy as np


def calculate_regional_means(df):
    """
    Calculates the average sales per region.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data

    Returns:
    --------
    dict
        Dictionary with average sales per region
    """
    regional_means = {}

    # Calculate average sales for each region
    for region in ['North America', 'europe', 'japan', 'Rest of World', 'global']:
        regional_means[region] = df[region].mean()

    return regional_means


def get_region_names_mapping():
    """
    Returns a dictionary mapping region codes to their English names.

    Returns:
    --------
    dict
        Dictionary mapping region codes to English names
    """
    # Note: Russian names were here before, keeping English for consistency
    return {
        'North America': 'North America',
        'europe': 'Europe',
        'japan': 'Japan',
        'Rest of World': 'Rest of World',
        'global': 'Global'
    }


def analyze_top_genres_by_region(df, top_n=5):
    """
    Analyzes the top genres by average sales for each region.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data
    top_n : int, optional
        Number of top genres for each region, default is 5

    Returns:
    --------
    dict
        Dictionary with top genres by average sales for each region
    """
    top_genres = {}

    # Analyze top genres for each region
    for region in ['North America', 'europe', 'japan', 'Rest of World', 'global']:
        # Group by genre and calculate average sales
        genre_sales = df.groupby(
            'genre')[region].mean().sort_values(ascending=False)

        # Get top genres
        top_genres_region = genre_sales.head(top_n).reset_index()
        top_genres_region.columns = ['genre', 'avg_sales']

        # Convert to list of tuples
        top_genres[region] = list(
            top_genres_region.itertuples(index=False, name=None))

    return top_genres


def compare_regional_distributions(df):
    """
    Compares sales distributions across regions.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data

    Returns:
    --------
    pandas.DataFrame
        DataFrame with distribution statistics for each region
    """
    # Create an empty DataFrame for results
    stats = pd.DataFrame(index=['mean', 'median', 'std', 'min', 'max', 'sum'])

    # Calculate statistics for each region
    for region in ['North America', 'europe', 'japan', 'Rest of World', 'global']:
        stats[region] = [
            df[region].mean(),
            df[region].median(),
            df[region].std(),
            df[region].min(),
            df[region].max(),
            df[region].sum()
        ]

    return stats


def analyze_regional_preferences(df):
    """
    Analyzes regional preferences by genre and lifecycle phase.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data

    Returns:
    --------
    dict
        Dictionary with the results of regional preference analysis
    """
    results = {}

    # Analyze genre preferences
    genres_by_region = {}
    for region in ['North America', 'europe', 'japan', 'Rest of World']:
        # Top 3 genres by sales in the region
        top_genres = df.groupby('genre')[region].mean(
        ).sort_values(ascending=False).head(3)
        genres_by_region[region] = [(genre, sales)
                                    for genre, sales in top_genres.items()]

    results['genre_preferences'] = genres_by_region

    # Analyze lifecycle phase preferences
    lifecycle_by_region = {}
    for region in ['North America', 'europe', 'japan', 'Rest of World']:
        # Average sales by lifecycle phase
        phase_sales = df.groupby('lifecycle_phase')[
            region].mean().sort_values(ascending=False)
        lifecycle_by_region[region] = [(phase, sales)
                                       for phase, sales in phase_sales.items()]

    results['lifecycle_preferences'] = lifecycle_by_region

    # Calculate relative market share
    total_sales = df[['North America', 'europe',
                      'japan', 'Rest of World']].sum()
    market_share = (total_sales / total_sales.sum()) * 100
    results['market_share'] = market_share.to_dict()

    return results


def generate_regional_report(df, output_path=None):
    """
    Generates a report on regional sales analysis.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data
    output_path : str, optional
        Path to save the report. If not specified, the default path is used.

    Returns:
    --------
    str
        Path where the report was saved
    """
    if output_path is None:
        # Determine the path relative to the project root
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(base_dir, 'reports', 'output')

        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'regional_analysis_report.txt')

    # Get region names mapping
    region_names = get_region_names_mapping()

    # Calculate data for the report
    regional_means = calculate_regional_means(df)
    top_genres = analyze_top_genres_by_region(df)
    distribution_stats = compare_regional_distributions(df)
    preferences = analyze_regional_preferences(df)

    # Format the report text
    report_text = []
    report_text.append("REPORT ON REGIONAL PS4 GAME SALES ANALYSIS")
    report_text.append("=" * 80)
    report_text.append("")

    report_text.append("1. Average Sales by Region")
    report_text.append("-" * 40)
    for region, mean in regional_means.items():
        display_region = region_names.get(region, region)
        report_text.append(f"{display_region}: {mean:.4f} M")
    report_text.append("")

    report_text.append("2. Top 5 Genres by Average Sales in Each Region")
    report_text.append("-" * 60)
    for region, genres in top_genres.items():
        if region != 'global':  # Exclude global sales from this section
            display_region = region_names.get(region, region)
            report_text.append(f"\n{display_region}:")
            for i, (genre, sales) in enumerate(genres, 1):
                report_text.append(f"  {i}. {genre}: {sales:.4f} M")
    report_text.append("")

    report_text.append("3. Comparison of Sales Distributions by Region")
    report_text.append("-" * 60)
    # Convert DataFrame to text format
    stats_text = distribution_stats.to_string()
    report_text.append(stats_text)
    report_text.append("")

    report_text.append("4. Regional Preferences")
    report_text.append("-" * 40)

    report_text.append("\n4.1. Genre Preferences")
    for region, genre_list in preferences['genre_preferences'].items():
        display_region = region_names.get(region, region)
        report_text.append(f"\n{display_region}:")
        for genre, sales in genre_list:
            report_text.append(f"  - {genre}: {sales:.4f} M")

    report_text.append("\n4.2. Lifecycle Phase Preferences")
    for region, phase_list in preferences['lifecycle_preferences'].items():
        display_region = region_names.get(region, region)
        report_text.append(f"\n{display_region}:")
        for phase, sales in phase_list:
            report_text.append(f"  - {phase}: {sales:.4f} M")

    report_text.append("\n4.3. Relative Market Share")
    for region, share in preferences['market_share'].items():
        display_region = region_names.get(region, region)
        report_text.append(f"  {display_region}: {share:.2f}%")

    report_text.append("\n")
    report_text.append("5. Conclusions")
    report_text.append("-" * 20)
    report_text.append(
        "1. North America and Europe are the largest markets for PS4 games.")
    report_text.append(
        "2. Japan shows distinct genre preferences compared to other regions.")
    report_text.append(
        "3. Average sales were higher during the early stages of the console lifecycle.")
    report_text.append("")

    # Save the report to a file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_text))

    return output_path


if __name__ == "__main__":
    # Demonstrate function usage
    from src.data.data_processing import load_data, preprocess_data

    # Load and preprocess data
    df_raw = load_data()
    df = preprocess_data(df_raw)

    # Generate the regional report
    report_path = generate_regional_report(df)

    # Print key metrics
    regional_means = calculate_regional_means(df)
    print("Average sales by region:")
    for region, mean in regional_means.items():
        print(f"  {region}: {mean:.4f} M")

    print(f"\nRegional analysis report saved to {report_path}")
