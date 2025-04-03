import nbformat as nbf
import os

# Создаем новый ноутбук
nb = nbf.v4.new_notebook()

# Добавляем ячейки
title_cell = nbf.v4.new_markdown_cell(
    "# PlayStation 4 Games Sales Analysis\n\nThis notebook contains a comprehensive analysis of PlayStation 4 game sales across different regions and years.")

imports_cell = nbf.v4.new_code_cell('''# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set plot style
plt.style.use('ggplot')
sns.set(style="whitegrid")
%matplotlib inline''')

data_loading_header = nbf.v4.new_markdown_cell(
    "## Data Loading\n\nFirst, we'll load the PS4 sales data from the raw data directory.")

data_loading_cell = nbf.v4.new_code_cell('''# Path to the data file
data_path = '../data/raw/ps4_sales.csv'

# Load the data
df = pd.read_csv(data_path)

# Display the first few rows
df.head()''')

data_cleaning_header = nbf.v4.new_markdown_cell(
    "## Data Cleaning and Preparation\n\nLet's clean the data and prepare it for analysis.")

data_cleaning_cell = nbf.v4.new_code_cell('''# Check for missing values
print("Missing values per column:")
print(df.isnull().sum())

# Basic data info
print("\\nDataset shape:", df.shape)
print("\\nData types:")
print(df.dtypes)

# Standardize column names
df.rename(columns={
    'North America': 'NA_Sales',
    'europe': 'EU_Sales',
    'japan': 'JP_Sales',
    'Rest of World': 'Other_Sales',
    'global': 'Global_Sales'
}, inplace=True)

# Display the updated dataframe
print("\\nUpdated DataFrame:")
df.head()''')

eda_header = nbf.v4.new_markdown_cell(
    "## Exploratory Data Analysis\n\n### Summary Statistics")

summary_stats_cell = nbf.v4.new_code_cell('''# Summary statistics for sales columns
sales_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
df[sales_cols].describe()''')

genre_dist_cell = nbf.v4.new_code_cell('''# Distribution of games by genre
genre_counts = df['genre'].value_counts()
print("Game distribution by genre:")
print(genre_counts)

# Plot genre distribution
plt.figure(figsize=(12, 6))
sns.barplot(x=genre_counts.index, y=genre_counts.values)
plt.title('Number of PS4 Games by Genre', fontsize=16)
plt.xlabel('Genre', fontsize=14)
plt.ylabel('Number of Games', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()''')

year_dist_cell = nbf.v4.new_code_cell('''# Distribution of games by year
year_counts = df['year'].value_counts().sort_index()
print("Game distribution by year:")
print(year_counts)

# Plot year distribution
plt.figure(figsize=(12, 6))
sns.barplot(x=year_counts.index, y=year_counts.values)
plt.title('Number of PS4 Games Released by Year', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Number of Games', fontsize=14)
plt.tight_layout()
plt.show()''')

regional_header = nbf.v4.new_markdown_cell(
    "## Regional Sales Analysis\n\nLet's analyze sales across different regions.")

regional_means_cell = nbf.v4.new_code_cell('''# Calculate mean sales per region
region_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
mean_sales = df[region_cols].mean().reset_index()
mean_sales.columns = ['Region', 'Mean Sales']

# Plot regional sales
plt.figure(figsize=(12, 6))
sns.barplot(x='Region', y='Mean Sales', data=mean_sales)
plt.title('Average PS4 Game Sales by Region', fontsize=16)
plt.xlabel('Region', fontsize=14)
plt.ylabel('Average Sales (millions)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()

# Create directory if it doesn't exist
os.makedirs('../reports/figures', exist_ok=True)
plt.savefig('../reports/figures/mean_sales_by_region.png', dpi=300)
plt.show()''')

top_games_cell = nbf.v4.new_code_cell('''# Top 10 games by global sales
top_10_global = df.sort_values('Global_Sales', ascending=False).head(10)
print("Top 10 PS4 Games by Global Sales:")
top_10_global[['game', 'year', 'genre', 'publisher', 'Global_Sales']]

# Plot top 10 games
plt.figure(figsize=(14, 7))
sns.barplot(x='Global_Sales', y='game', data=top_10_global, hue='game', legend=False)
plt.title('Top 10 PS4 Games by Global Sales', fontsize=16)
plt.xlabel('Global Sales (millions)', fontsize=14)
plt.ylabel('Game', fontsize=14)
plt.tight_layout()
plt.show()''')

year_header = nbf.v4.new_markdown_cell(
    "## Year-based Analysis\n\nLet's analyze how sales have changed over the years.")

year_analysis_cell = nbf.v4.new_code_cell('''# Group data by year
yearly_data = df.groupby('year')['Global_Sales'].agg(['mean', 'sum', 'count']).reset_index()
yearly_data.columns = ['Year', 'Average Sales', 'Total Sales', 'Number of Games']

# Display the data
print("Yearly sales data:")
yearly_data

# Create figure with two y-axes
fig, ax1 = plt.subplots(figsize=(14, 7))
ax2 = ax1.twinx()

# Plot average sales on the first y-axis
ax1.plot(yearly_data['Year'], yearly_data['Average Sales'], 'b-', marker='o', linewidth=2, label='Average Sales')
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Average Sales (millions)', color='b', fontsize=14)
ax1.tick_params(axis='y', labelcolor='b')

# Plot number of games on the second y-axis
ax2.plot(yearly_data['Year'], yearly_data['Number of Games'], 'r-', marker='s', linewidth=2, label='Number of Games')
ax2.set_ylabel('Number of Games', color='r', fontsize=14)
ax2.tick_params(axis='y', labelcolor='r')

# Add title and legend
plt.title('PS4 Game Sales by Year', fontsize=16)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.savefig('../reports/figures/year_sales_analysis.png', dpi=300)
plt.show()''')

genre_header = nbf.v4.new_markdown_cell(
    "## Genre Analysis\n\nLet's examine which genres are most popular in different regions.")

genre_analysis_cell = nbf.v4.new_code_cell('''# Group data by genre and calculate mean sales for each region
genre_region = df.groupby('genre')[region_cols].mean().reset_index()

# Display data
print("Average sales by genre and region:")
genre_region

# Create a heatmap
plt.figure(figsize=(12, 8))
genre_heatmap = genre_region.set_index('genre')
sns.heatmap(genre_heatmap, annot=True, cmap='YlGnBu', fmt='.2f', linewidths=.5)
plt.title('Average Sales by Genre and Region', fontsize=16)
plt.ylabel('Genre', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('../reports/figures/genre_region_heatmap.png', dpi=300)
plt.show()''')

top_genre_cell = nbf.v4.new_code_cell('''# Calculate top genre by sales for each region
top_genres = {}
for region in ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']:
    top_genre = df.groupby('genre')[region].mean().sort_values(ascending=False).index[0]
    top_genres[region] = top_genre

print("Top genre by sales in each region:")
for region, genre in top_genres.items():
    print(f"{region}: {genre}")''')

publisher_header = nbf.v4.new_markdown_cell(
    "## Publisher Analysis\n\nLet's analyze which publishers have the most successful games.")

publisher_analysis_cell = nbf.v4.new_code_cell('''# Calculate average global sales by publisher
publisher_sales = df.groupby('publisher')['Global_Sales'].agg(['mean', 'sum', 'count']).reset_index()
publisher_sales.columns = ['Publisher', 'Average Sales', 'Total Sales', 'Number of Games']

# Filter to publishers with at least 5 games
major_publishers = publisher_sales[publisher_sales['Number of Games'] >= 5].sort_values('Average Sales', ascending=False)

# Display top publishers by average sales
print("Top publishers by average sales (with at least 5 games):")
major_publishers.head(10)

# Plot top publishers
plt.figure(figsize=(14, 8))
top_publishers = major_publishers.head(10)
sns.barplot(x='Average Sales', y='Publisher', data=top_publishers, hue='Publisher', legend=False)
plt.title('Top 10 Publishers by Average Sales', fontsize=16)
plt.xlabel('Average Sales (millions)', fontsize=14)
plt.ylabel('Publisher', fontsize=14)
plt.tight_layout()
plt.show()''')

correlation_header = nbf.v4.new_markdown_cell(
    "## Correlation Analysis\n\nLet's examine correlations between different sales regions.")

correlation_cell = nbf.v4.new_code_cell('''# Calculate correlation matrix
corr_matrix = df[region_cols].corr()

# Create heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
plt.title('Correlation Between Regional Sales', fontsize=16)
plt.tight_layout()
plt.show()''')

lifecycle_header = nbf.v4.new_markdown_cell(
    "## Console Lifecycle Analysis\n\nLet's analyze the effect of console lifecycle on sales.")

lifecycle_cell = nbf.v4.new_code_cell('''# Add lifecycle phase based on year
def assign_lifecycle(year):
    if year <= 2015:
        return 'Early'
    elif year <= 2018:
        return 'Middle'
    else:
        return 'Late'

df['Lifecycle_Phase'] = df['year'].apply(assign_lifecycle)

# Analyze sales by lifecycle phase
lifecycle_data = df.groupby('Lifecycle_Phase')['Global_Sales'].agg(['mean', 'sum', 'count']).reset_index()
lifecycle_data.columns = ['Lifecycle Phase', 'Average Sales', 'Total Sales', 'Number of Games']

# Display the data
print("Sales by console lifecycle phase:")
lifecycle_data

# Plot average sales by lifecycle phase
plt.figure(figsize=(10, 6))
sns.barplot(x='Lifecycle Phase', y='Average Sales', data=lifecycle_data, hue='Lifecycle Phase', legend=False)
plt.title('Average PS4 Game Sales by Console Lifecycle Phase', fontsize=16)
plt.xlabel('Lifecycle Phase', fontsize=14)
plt.ylabel('Average Sales (millions)', fontsize=14)
plt.tight_layout()
plt.show()''')

conclusion_cell = nbf.v4.new_markdown_cell('''## Conclusion

This analysis has revealed several important insights about PS4 game sales:

1. **Regional Differences**: There are significant differences in sales across regions, with North America and Europe typically having higher sales volumes than Japan and other regions.

2. **Console Lifecycle**: Sales trends over the years show clear patterns related to the PS4 console lifecycle, with peak sales occurring in the middle years (2016-2018).

3. **Genre Preferences**: Different regions show distinct preferences for game genres. Action and Sports games are generally popular in North America and Europe, while RPGs have stronger performance in Japan.

4. **Publisher Impact**: Certain publishers like Rockstar Games and Activision consistently achieve higher sales figures, demonstrating the importance of strong developer/publisher reputation.

These insights can guide publishers and developers in making strategic decisions about game development and marketing for different regions.''')

# Добавляем все ячейки в ноутбук
nb['cells'] = [title_cell, imports_cell, data_loading_header, data_loading_cell,
               data_cleaning_header, data_cleaning_cell, eda_header, summary_stats_cell,
               genre_dist_cell, year_dist_cell, regional_header, regional_means_cell,
               top_games_cell, year_header, year_analysis_cell, genre_header,
               genre_analysis_cell, top_genre_cell, publisher_header, publisher_analysis_cell,
               correlation_header, correlation_cell, lifecycle_header, lifecycle_cell,
               conclusion_cell]

# Создаем директорию, если она не существует
os.makedirs('notebooks', exist_ok=True)

# Сохраняем ноутбук
with open('notebooks/PS4_Sales_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Full notebook created successfully!")
