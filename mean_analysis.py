import pandas as pd

# Загрузка данных
df = pd.read_csv('ps4_sales.csv')

# Вывод информации о структуре данных
print("Информация о наборе данных:")
print(f"Количество строк: {df.shape[0]}")
print(f"Количество столбцов: {df.shape[1]}")
print("\nНазвания столбцов:")
print(df.columns.tolist())
print("\nПервые 5 строк данных:")
print(df.head())

# Выбор числовых столбцов (без id и year)
numeric_columns = ['North America', 'europe',
                   'japan', 'Rest of World', 'global']

# Общее количество записей
N = len(df)
print(f"\nОбщее количество записей (N): {N}")

# Рассчитываем сумму для каждого числового столбца
print("\nРасчет суммы значений для каждого региона:")
sums = {}
for column in numeric_columns:
    sum_value = df[column].sum()
    sums[column] = sum_value
    print(f"Сумма значений для '{column}': {sum_value:.2f}")

# Рассчитываем среднее значение для каждого числового столбца
print("\nРасчет среднего значения для каждого региона (формула: sum(X)/N):")
means = {}
for column in numeric_columns:
    mean_value = sums[column] / N
    means[column] = mean_value
    print(f"Среднее значение для '{column}': {mean_value:.4f}")

# Проверка через pandas.mean()
print("\nПроверка через pandas.mean():")
for column in numeric_columns:
    mean_pd = df[column].mean()
    print(f"Среднее значение для '{column}' через pandas: {mean_pd:.4f}")

# Дополнительно: анализ по годам
print("\nАнализ средних продаж по годам:")
year_means = df.groupby('year')['global'].mean()
print(year_means)
