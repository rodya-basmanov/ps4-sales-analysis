import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
df = pd.read_csv('ps4_sales.csv')

# Выбор числовых столбцов
numeric_columns = ['North America', 'europe',
                   'japan', 'Rest of World', 'global']

# Общее количество записей
N = len(df)

# Рассчитываем сумму для каждого числового столбца
sums = {}
for column in numeric_columns:
    sum_value = df[column].sum()
    sums[column] = sum_value

# Рассчитываем среднее значение для каждого числового столбца
means = {}
for column in numeric_columns:
    mean_value = sums[column] / N
    means[column] = mean_value

# Отображаем названия регионов на русском для графика
region_names = {
    'North America': 'Северная Америка',
    'europe': 'Европа',
    'japan': 'Япония',
    'Rest of World': 'Остальной мир',
    'global': 'Глобально'
}

# Используем все регионы, включая глобальный
region_means = {region_names[k]: v for k, v in means.items()}

try:
    # Создание графика средних значений по регионам
    plt.figure(figsize=(12, 7))
    colors = ['blue', 'green', 'red', 'orange', 'purple']
    bars = plt.bar(region_means.keys(), region_means.values(), color=colors)

    # Добавляем значения над столбцами
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                 f'{height:.3f}', ha='center', va='bottom')

    plt.title('Среднее значение продаж по регионам (sum(X)/N)')
    plt.xlabel('Регион')
    plt.ylabel('Среднее значение продаж (млн)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('mean_sales_by_region_with_global.png')
    print("График средних продаж по регионам (с глобальным) сохранен в файл 'mean_sales_by_region_with_global.png'")

    # Создание графика только для регионов (без глобального) для сравнения
    region_means_no_global = {k: v for k,
                              v in region_means.items() if k != 'Глобально'}
    plt.figure(figsize=(10, 6))
    plt.bar(region_means_no_global.keys(),
            region_means_no_global.values(), color=colors[:4])
    plt.title('Среднее значение продаж по регионам (без глобального)')
    plt.xlabel('Регион')
    plt.ylabel('Среднее значение продаж (млн)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('mean_sales_by_region.png')
    print("График средних продаж по регионам (без глобального) сохранен в файл 'mean_sales_by_region.png'")

    # Создание графика по годам
    year_means = df.groupby('year')['global'].mean()
    plt.figure(figsize=(10, 6))
    year_means.plot(kind='bar', color='purple')
    plt.title('Среднее значение глобальных продаж по годам (sum(X)/N)')
    plt.xlabel('Год')
    plt.ylabel('Среднее значение продаж (млн)')
    plt.tight_layout()
    plt.savefig('mean_sales_by_year.png')
    print("График средних продаж по годам сохранен в файл 'mean_sales_by_year.png'")

except Exception as e:
    print(f"Не удалось создать визуализацию: {e}")
    print("Возможно, отсутствуют необходимые библиотеки. Установите matplotlib: pip install matplotlib")

# Выводим данные в консоль в текстовом виде
print("\nСреднее значение продаж по регионам (sum(X)/N):")
for region, mean in means.items():
    print(f"{region_names[region]}: {mean:.4f} млн")

print("\nСреднее значение глобальных продаж по годам (sum(X)/N):")
print(year_means)
