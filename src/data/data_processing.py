"""
Data Processing Module for PS4 Sales Analysis

This module provides functions for loading, cleaning, and preprocessing
the sales data of PlayStation 4 games.
"""

import os
import pandas as pd
import numpy as np


def load_data(file_path=None):
    """
    Loads game sales data from a CSV file.

    Parameters:
    -----------
    file_path : str, optional
        Path to the CSV file with data. If not specified, the default path is used.

    Returns:
    --------
    pandas.DataFrame
        DataFrame with game sales data
    """
    if file_path is None:
        # Determine the path relative to the project root
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, 'data', 'raw', 'ps4_sales.csv')

    # Load data from the CSV file
    df = pd.read_csv(file_path)
    return df


def clean_data(df):
    """
    Cleans the data by removing missing values and incorrect entries.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with raw data

    Returns:
    --------
    pandas.DataFrame
        DataFrame with cleaned data
    """
    # Create a copy of the dataframe
    df_cleaned = df.copy()

    # Check for missing values
    if df_cleaned.isnull().sum().sum() > 0:
        # Remove rows with missing values
        df_cleaned = df_cleaned.dropna()

    # Check for rows with zero or negative sales
    numeric_columns = ['North America', 'europe',
                       'japan', 'Rest of World', 'global']
    mask = (df_cleaned[numeric_columns] >= 0).all(axis=1)
    df_cleaned = df_cleaned[mask]

    # Check that the sum of regional sales equals global sales (with tolerance)
    df_cleaned['sum_regions'] = df_cleaned['North America'] + \
        df_cleaned['europe'] + df_cleaned['japan'] + \
        df_cleaned['Rest of World']
    mask = np.isclose(df_cleaned['sum_regions'],
                      df_cleaned['global'], atol=0.1)
    df_cleaned = df_cleaned[mask]

    # Remove the temporary column
    df_cleaned = df_cleaned.drop('sum_regions', axis=1)

    return df_cleaned


def get_summary_stats(df):
    """
    Calculates basic statistical indicators for the dataset.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with game sales data

    Returns:
    --------
    dict
        Dictionary with basic statistical indicators
    """
    # Number of games
    num_games = len(df)

    # Year range
    years = df['year'].dropna().astype(int).unique()
    years = sorted(years)
    years_range = f"{min(years)} - {max(years)}"

    # Number of genres
    num_genres = df['genre'].nunique()

    # Number of publishers
    num_publishers = df['publisher'].nunique()

    # Total global sales
    total_global_sales = df['global'].sum()

    # Return statistics as a dictionary
    stats = {
        'Number of games': num_games,
        'Year range': years_range,
        'Number of genres': num_genres,
        'Number of publishers': num_publishers,
        'Total global sales (M)': total_global_sales
    }

    return stats


def preprocess_data(df):
    """
    Preprocesses the data by adding useful columns and categorizing data.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with cleaned data

    Returns:
    --------
    pandas.DataFrame
        DataFrame with preprocessed data
    """
    # Create a copy of the dataframe
    df_processed = df.copy()

    # Convert year to integer type (handling potential NaNs)
    df_processed['year'] = pd.to_numeric(df_processed['year'], errors='coerce')
    df_processed['year'] = df_processed['year'].fillna(0).astype(int)

    # Add a column with the console lifecycle phase
    def get_lifecycle_phase(year):
        if year in [2013, 2014, 2015]:
            return 'Early'
        elif year in [2016, 2017, 2018]:
            return 'Middle'
        elif year in [2019, 2020, 2021, 2022]:
            return 'Late'
        else:
            return 'Unknown'

    df_processed['lifecycle_phase'] = df_processed['year'].apply(
        get_lifecycle_phase)

    # Add a column with the sum of regional sales
    df_processed['regional_sales_sum'] = df_processed['North America'] + \
        df_processed['europe'] + df_processed['japan'] + \
        df_processed['Rest of World']

    # Add columns with regional sales percentages
    for region in ['North America', 'europe', 'japan', 'Rest of World']:
        df_processed[f'{region}_percent'] = (
            df_processed[region] / df_processed['global']) * 100

    return df_processed


def save_processed_data(df, output_path=None):
    """
    Saves the processed data to a CSV file.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with processed data
    output_path : str, optional
        Path to save the file. If not specified, the default path is used.

    Returns:
    --------
    str
        Path where the file was saved
    """
    if output_path is None:
        # Determine the path relative to the project root
        base_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(base_dir, 'data', 'processed')

        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'ps4_sales_processed.csv')

    # Save data to CSV file
    df.to_csv(output_path, index=False)

    return output_path


if __name__ == "__main__":
    # Demonstrate function usage
    print("Loading data...")
    df_raw = load_data()
    print(f"Loaded {len(df_raw)} rows.")

    print("\nCleaning data...")
    df_cleaned = clean_data(df_raw)
    print(f"After cleaning, {len(df_cleaned)} rows remain.")

    print("\nCalculating statistics...")
    stats = get_summary_stats(df_cleaned)
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\nPreprocessing data...")
    df_processed = preprocess_data(df_cleaned)
    print(f"Shape of processed dataframe: {df_processed.shape}")

    print("\nSaving data...")
    output_path = save_processed_data(df_processed)
    print(f"Data saved to {output_path}")
