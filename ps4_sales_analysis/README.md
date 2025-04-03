# PS4 Games Sales Analysis

![PlayStation 4](https://placehold.co/600x300/5073b8/white?text=PS4+Sales+Analysis)

## Project Description

This project represents a comprehensive analysis of sales data for PlayStation 4 games. The project includes data collection, processing, analysis, and visualization of game sales across different regions and years.

### Main Objectives:

1. Identifying regional differences in PS4 game sales
2. Analyzing sales trend changes over years and at different stages of the console lifecycle
3. Identifying the most popular game genres by region
4. Examining the relationship between the number of games released and average sales

## Project Structure

```
ps4_sales_analysis/
│
├── data/                         # Data directory
│   ├── raw/                      # Raw data
│   └── processed/                # Processed data
│
├── reports/                      # Reports directory
│   ├── figures/                  # Visualizations
│   └── output/                   # Text reports
│
├── src/                          # Source code
│   ├── data/                     # Data processing modules
│   │   └── data_processing.py    # Module for loading and processing data
│   │
│   ├── analysis/                 # Analysis modules
│   │   ├── regional_analysis.py  # Analysis of sales by region
│   │   └── year_analysis.py      # Analysis of sales by year
│   │
│   └── visualization/            # Visualization modules
│       └── visualize.py          # Module for creating visualizations
│
├── run_analysis.py               # Main script for running the analysis
└── README.md                     # Project documentation
```

## Technologies Used

- **Python 3.8+**: Main programming language
- **Pandas**: Data processing and analysis
- **NumPy**: Scientific computing and array operations
- **Matplotlib**: Creating visualizations

## Installation and Usage

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Data Preparation

Place the source PS4 sales data file in the `data/raw/` directory under the name `ps4_sales.csv`. The file should contain the following columns:
- Rank: Game ranking by sales
- Name: Game name
- Platform: Platform (in this case, PS4)
- Year: Release year
- Genre: Game genre
- Publisher: Game publisher
- North America: Sales in North America (in millions of copies)
- europe: Sales in Europe (in millions of copies)
- japan: Sales in Japan (in millions of copies)
- Rest of World: Sales in the rest of the world (in millions of copies)
- global: Global sales (in millions of copies)

### Running the Analysis

```bash
python run_analysis.py
```

## Analysis Results

After running the analysis, the following results will be created in the `reports/` directory:

### Reports (reports/output/)

- **regional_analysis_report.txt**: Detailed analysis of sales by region
- **year_analysis_report.txt**: Analysis of sales by year and console lifecycle stages

### Visualizations (reports/figures/)

- **regional_sales.png**: Bar chart of average sales by region
- **year_dynamics.png**: Graph of sales dynamics and number of games by year
- **genre_heatmap.png**: Heat map of genre popularity by region
- **correlation_scatter.png**: Scatter plot showing the relationship between the number of games and average sales

## Key Findings

1. **Regional Differences**: Significant differences have been identified in the preferences of players from different regions. North America and Europe show similar trends, while Japan has distinct preferences in game genres.

2. **Console Lifecycle**: PS4 game sales peaked in the middle of the console's lifecycle (2016-2018). The number of games released continued to grow in later stages, but average sales per game declined.

3. **Genre Preferences**: Action and Sports are the leading genres in sales in North America and Europe, while RPG and Fighting are highly popular in Japan.

## Author

- **Name**: Rodion Basmanov
- **Email**: your.email@example.com
- **GitHub**: [rodya-basmanov](https://github.com/rodya-basmanov)

## License

This project is distributed under the MIT License. See the LICENSE file for details. 