#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main script to run the full analysis of PS4 game sales data.
Executes data loading, preprocessing, analysis, and visualization.
"""

import os
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("analysis_log.txt"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def create_project_structure():
    """Creates the necessary directory structure if it doesn't exist"""
    directories = [
        'data/raw',
        'data/processed',
        'reports/figures',
        'reports/output'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Directory created or already exists: {directory}")


def run_full_analysis():
    """Runs the full data analysis cycle"""
    start_time = datetime.now()
    logger.info("Starting PS4 game sales data analysis")

    # Import modules from the project structure
    from src.data.data_processing import (
        load_data, clean_data, preprocess_data, get_summary_stats, save_processed_data
    )
    from src.analysis.regional_analysis import (
        generate_regional_report, calculate_regional_means
    )
    from src.analysis.year_analysis import generate_year_analysis_report
    from src.visualization.visualize import create_all_visualizations

    # Step 1: Load data
    logger.info("Loading raw data...")
    try:
        df_raw = load_data()
        logger.info(
            f"Data loaded successfully: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return

    # Step 2: Clean data
    logger.info("Cleaning data...")
    df_cleaned = clean_data(df_raw)
    logger.info(
        f"Data cleaned: {df_cleaned.shape[0]} rows, {df_cleaned.shape[1]} columns")

    # Step 3: Get summary statistics
    logger.info("Calculating summary statistics...")
    stats = get_summary_stats(df_cleaned)
    logger.info("Summary Statistics:")
    for key, value in stats.items():
        logger.info(f"  - {key}: {value}")

    # Step 4: Preprocess data
    logger.info("Preprocessing data...")
    df_processed = preprocess_data(df_cleaned)
    logger.info(
        f"Data preprocessed: {df_processed.shape[0]} rows, {df_processed.shape[1]} columns")

    # Step 5: Save processed data
    logger.info("Saving processed data...")
    output_path = save_processed_data(df_processed)
    logger.info(f"Processed data saved to {output_path}")

    # Step 6: Regional analysis
    logger.info("Performing regional analysis...")
    regional_means = calculate_regional_means(df_processed)
    logger.info("Average sales by region:")
    for region, value in regional_means.items():
        logger.info(f"  - {region}: {value:.4f} M")

    regional_report_path = generate_regional_report(df_processed)
    logger.info(f"Regional analysis report generated: {regional_report_path}")

    # Step 7: Year analysis
    logger.info("Performing year analysis...")
    year_report_path = generate_year_analysis_report(df_processed)
    logger.info(f"Year analysis report generated: {year_report_path}")

    # Step 8: Create visualizations
    logger.info("Creating visualizations...")
    figure_paths = create_all_visualizations(df_processed)
    logger.info(f"Created {len(figure_paths)} visualizations:")
    for path in figure_paths:
        logger.info(f"  - {path}")

    # Final output
    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f"Analysis completed successfully. Duration: {duration}")
    logger.info("Key Findings Summary:")
    logger.info(f"  1. Games analyzed: {stats.get('Number of games', 'N/A')}")
    logger.info(f"  2. Year range: {stats.get('Year range', 'N/A')}")
    logger.info(f"  3. Genres: {stats.get('Number of genres', 'N/A')}")
    logger.info(f"  4. Publishers: {stats.get('Number of publishers', 'N/A')}")
    logger.info(
        f"  5. Total global sales: {stats.get('Total global sales (M)', 'N/A')} M")


if __name__ == "__main__":
    # Create project structure
    create_project_structure()

    # Run the analysis
    run_full_analysis()
