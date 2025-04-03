import nbformat as nbf
import os

# Создаем новый ноутбук
nb = nbf.v4.new_notebook()

# Добавляем ячейки
text_cell = nbf.v4.new_markdown_cell(
    "# PlayStation 4 Games Sales Analysis\n\nThis notebook contains a comprehensive analysis of PlayStation 4 game sales across different regions and years.")

code_cell1 = nbf.v4.new_code_cell('''# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set plot style
plt.style.use('ggplot')
sns.set(style="whitegrid")
%matplotlib inline''')

text_cell2 = nbf.v4.new_markdown_cell(
    "## Data Loading\n\nFirst, we'll load the PS4 sales data from the raw data directory.")

code_cell2 = nbf.v4.new_code_cell('''# Path to the data file
data_path = '../data/raw/ps4_sales.csv'

# Load the data
df = pd.read_csv(data_path)

# Display the first few rows
df.head()''')

# Добавляем ячейки в ноутбук
nb['cells'] = [text_cell, code_cell1, text_cell2, code_cell2]

# Создаем директорию, если она не существует
os.makedirs('notebooks', exist_ok=True)

# Сохраняем ноутбук
with open('notebooks/PS4_Sales_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook created successfully!")
