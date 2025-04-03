"""
Module for analyzing PS4 game sales by year

This module provides functions for analyzing changes in PlayStation 4 game sales
over the years and at different stages of the console's lifecycle.
"""

import os
import pandas as pd
import numpy as np


def analyze_yearly_trends(df):
    """
    Analyzes sales trends by year.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data

    Returns:
    --------
    pandas.DataFrame
        DataFrame with sales indicators by year
    """
    # Group data by release year
    yearly_data = df.groupby('year').agg({
        'global': ['mean', 'sum', 'count']
    })

    # Rename columns
    yearly_data.columns = ['average_sales', 'total_sales', 'num_games']

    # Sort by release year (excluding 0 if present)
    if 0 in yearly_data.index:
        yearly_data = yearly_data.drop(0)

    yearly_data = yearly_data.sort_index()

    # Calculate percentage of total games
    total_games = yearly_data['num_games'].sum()
    yearly_data['percent_of_total'] = (
        yearly_data['num_games'] / total_games) * 100

    return yearly_data


def analyze_top_genres_by_year(df, top_n=3):
    """
    Analyzes the top genres by sales for each year.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data
    top_n : int, optional
        Number of top genres for each year, default is 3

    Returns:
    --------
    dict
        Dictionary with top genres by average sales for each year
    """
    # Filter out games with unknown release year
    df_valid_years = df[df['year'] > 0]

    # Get unique years
    years = sorted(df_valid_years['year'].unique())

    # Create a dictionary to store results
    top_genres_by_year = {}

    # Analyze top genres for each year
    for year in years:
        # Get data only for the current year
        df_year = df_valid_years[df_valid_years['year'] == year]

        # Group by genre and calculate average sales
        genre_sales = df_year.groupby(
            'genre')['global'].mean().sort_values(ascending=False)

        # Get top genres
        top_genres = genre_sales.head(top_n).reset_index()
        top_genres.columns = ['genre', 'avg_sales']

        # Convert to list of tuples
        top_genres_by_year[year] = list(
            top_genres.itertuples(index=False, name=None))

    return top_genres_by_year


def calculate_year_to_year_change(df):
    """
    Calculates year-to-year changes in sales.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data

    Returns:
    --------
    pandas.DataFrame
        DataFrame with percentage changes by year
    """
    # Analyze yearly trends
    yearly_trends = analyze_yearly_trends(df)

    # Calculate percentage changes
    changes = pd.DataFrame(index=yearly_trends.index)
    changes['avg_sales_pct_change'] = yearly_trends['average_sales'].pct_change() * \
        100
    changes['total_sales_pct_change'] = yearly_trends['total_sales'].pct_change() * \
        100
    changes['num_games_pct_change'] = yearly_trends['num_games'].pct_change() * \
        100

    # Add absolute values for reference
    changes['average_sales'] = yearly_trends['average_sales']
    changes['total_sales'] = yearly_trends['total_sales']
    changes['num_games'] = yearly_trends['num_games']

    return changes


def analyze_lifecycle_effect(df):
    """
    Analyzes the impact of the console lifecycle on sales.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data

    Returns:
    --------
    dict
        Dictionary with metrics by lifecycle phase
    """
    # Group data by lifecycle phase
    lifecycle_data = df.groupby('lifecycle_phase').agg({
        'global': ['mean', 'median', 'sum', 'count'],
        'year': pd.Series.nunique
    })

    # Rename columns
    lifecycle_data.columns = [
        'avg_sales', 'median_sales', 'total_sales', 'num_games', 'num_years'
    ]

    # Remove the 'Unknown' phase if it exists
    if 'Unknown' in lifecycle_data.index:
        lifecycle_data = lifecycle_data.drop('Unknown')

    # Sort phases in the correct order
    phase_order = ['Early', 'Middle', 'Late']
    lifecycle_data = lifecycle_data.reindex(phase_order)

    # Calculate additional metrics
    lifecycle_data['games_per_year'] = lifecycle_data['num_games'] / \
        lifecycle_data['num_years']
    lifecycle_data['sales_per_year'] = lifecycle_data['total_sales'] / \
        lifecycle_data['num_years']

    # Convert to dictionary
    result = {}
    for phase in lifecycle_data.index:
        result[phase] = lifecycle_data.loc[phase].to_dict()

    return result


def calculate_correlation_games_vs_sales(df):
    """
    Calculates the correlation between the number of released games and average sales.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data

    Returns:
    --------
    dict
        Dictionary with correlation coefficients
    """
    # Analyze yearly trends
    yearly_trends = analyze_yearly_trends(df)

    # Calculate correlation between number of games and average sales
    corr_num_vs_avg = yearly_trends['num_games'].corr(
        yearly_trends['average_sales'])

    # Calculate correlation between number of games and total sales
    corr_num_vs_total = yearly_trends['num_games'].corr(
        yearly_trends['total_sales'])

    return {
        'correlation_num_vs_avg_sales': corr_num_vs_avg,
        'correlation_num_vs_total_sales': corr_num_vs_total
    }


def generate_year_analysis_report(df, output_path=None):
    """
    Generates a report on the yearly sales analysis.

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

        output_path = os.path.join(output_dir, 'year_analysis_report.txt')

    # Calculate data for the report
    yearly_trends = analyze_yearly_trends(df)
    top_genres_by_year = analyze_top_genres_by_year(df)
    year_to_year_changes = calculate_year_to_year_change(df)
    lifecycle_effect = analyze_lifecycle_effect(df)
    correlation = calculate_correlation_games_vs_sales(df)

    # Format the report text
    report_text = []
    report_text.append("REPORT ON YEARLY PS4 GAME SALES ANALYSIS")
    report_text.append("=" * 80)
    report_text.append("")

    report_text.append("1. Sales Trends by Year")
    report_text.append("-" * 40)
    report_text.append(yearly_trends.to_string())
    report_text.append("")

    report_text.append("2. Year-to-Year Percentage Changes in Sales")
    report_text.append("-" * 60)
    report_text.append(year_to_year_changes.to_string())
    report_text.append("")

    report_text.append("3. Top Genres by Year")
    report_text.append("-" * 30)
    for year, genres in sorted(top_genres_by_year.items()):
        report_text.append(f"\n{year}:")
        for i, (genre, sales) in enumerate(genres, 1):
            report_text.append(f"  {i}. {genre}: {sales:.4f} M")
    report_text.append("")

    report_text.append("4. Impact of Console Lifecycle on Sales")
    report_text.append("-" * 60)

    # Define column headers and their order
    headers = [
        'Phase', 'Avg Sales', 'Median Sales', 'Total Sales',
        'Num Games', 'Num Years', 'Games/Year', 'Sales/Year'
    ]
    # Calculate max width for each column for alignment
    max_widths = {header: len(header) for header in headers}
    for phase, data in lifecycle_effect.items():
        max_widths['Phase'] = max(max_widths['Phase'], len(phase))
        max_widths['Avg Sales'] = max(
            max_widths['Avg Sales'], len(f"{data['avg_sales']:.4f}"))
        max_widths['Median Sales'] = max(
            max_widths['Median Sales'], len(f"{data['median_sales']:.4f}"))
        max_widths['Total Sales'] = max(
            max_widths['Total Sales'], len(f"{data['total_sales']:.1f}"))
        max_widths['Num Games'] = max(
            max_widths['Num Games'], len(f"{data['num_games']}"))
        max_widths['Num Years'] = max(
            max_widths['Num Years'], len(f"{data['num_years']}"))
        max_widths['Games/Year'] = max(max_widths['Games/Year'],
                                       len(f"{data['games_per_year']:.1f}"))
        max_widths['Sales/Year'] = max(max_widths['Sales/Year'],
                                       len(f"{data['sales_per_year']:.1f}"))

    header_line = "  ".join(
        f"{header:<{max_widths[header]}}" for header in headers)
    report_text.append(header_line)
    report_text.append("-" * len(header_line))

    # Print data for each phase with alignment
    for phase, data in lifecycle_effect.items():
        row_values = [
            f"{phase:<{max_widths['Phase']}}",
            f"{data['avg_sales']:.4f}".ljust(max_widths['Avg Sales']),
            f"{data['median_sales']:.4f}".ljust(max_widths['Median Sales']),
            f"{data['total_sales']:.1f}".ljust(max_widths['Total Sales']),
            f"{data['num_games']}".ljust(max_widths['Num Games']),
            f"{data['num_years']}".ljust(max_widths['Num Years']),
            f"{data['games_per_year']:.1f}".ljust(max_widths['Games/Year']),
            f"{data['sales_per_year']:.1f}".ljust(max_widths['Sales/Year'])
        ]
        report_text.append("  ".join(row_values))
    report_text.append("")

    report_text.append("5. Correlation between Number of Games and Sales")
    report_text.append("-" * 60)
    report_text.append(
        f"Correlation between num games and avg sales: {correlation['correlation_num_vs_avg_sales']:.4f}")
    report_text.append(
        f"Correlation between num games and total sales: {correlation['correlation_num_vs_total_sales']:.4f}")
    report_text.append("")

    report_text.append("6. Conclusions")
    report_text.append("-" * 20)
    report_text.append(
        "1. The peak of average sales for PS4 games occurred in the middle of the console's lifecycle.")
    report_text.append(
        "2. The number of released games increases each year, but the average sales per game decrease.")
    report_text.append(
        "3. There is an inverse correlation between the number of released games and average sales, which may indicate market dilution.")
    report_text.append(
        "4. Genre preferences change over time, reflecting the evolution of player interests.")
    report_text.append("")

    # Save the report to a file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_text))

    return output_path


if __name__ == "__main__":
    # Demonstrate function usage
    from ps4_sales_analysis.src.data.data_processing import load_data, preprocess_data

    # Load and preprocess data
    df_raw = load_data()
    df = preprocess_data(df_raw)

    # Generate the yearly report
    report_path = generate_year_analysis_report(df)

    # Print key metrics
    yearly_trends = analyze_yearly_trends(df)
    print("Sales trends by year:")
    print(yearly_trends)

    print(f"\nYearly analysis report saved to {report_path}")
