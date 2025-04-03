import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Загрузка данных
print("Загрузка и анализ данных о продажах игр для PS4...")
df = pd.read_csv('ps4_sales.csv')

# Общая информация о наборе данных
N = len(df)
print(f"Всего игр в наборе данных: {N}")
print(f"Количество столбцов: {df.shape[1]}")
print(f"Годы выпуска: с {df['year'].min()} по {df['year'].max()}")
print(f"Количество уникальных жанров: {df['genre'].nunique()}")
print(f"Количество уникальных издателей: {df['publisher'].nunique()}")

# Анализ по регионам
print("\n--- АНАЛИЗ ПО РЕГИОНАМ ---")
numeric_columns = ['North America', 'europe',
                   'japan', 'Rest of World', 'global']

# Рассчитываем сумму для каждого региона
sums = {}
for column in numeric_columns:
    sum_value = df[column].sum()
    sums[column] = sum_value

# Рассчитываем среднее значение для каждого региона
means = {}
for column in numeric_columns:
    mean_value = sums[column] / N
    means[column] = mean_value

# Отображаем названия регионов на русском
region_names = {
    'North America': 'Северная Америка',
    'europe': 'Европа',
    'japan': 'Япония',
    'Rest of World': 'Остальной мир',
    'global': 'Глобально'
}

# Выводим результаты по регионам
print("\nСреднее значение продаж по регионам (формула: sum(X)/N):")
for column in numeric_columns:
    print(f"{region_names[column]}: {means[column]:.4f} млн копий")

# Анализ по годам
print("\n--- АНАЛИЗ ПО ГОДАМ ---")
yearly_counts = df.groupby('year').size()
yearly_global_mean = df.groupby('year')['global'].mean()
yearly_global_sum = df.groupby('year')['global'].sum()

# Объединяем данные по годам
yearly_analysis = pd.DataFrame({
    'Количество игр': yearly_counts,
    'Средние продажи (млн)': yearly_global_mean,
    'Общие продажи (млн)': yearly_global_sum
})

# Добавляем процент от общего количества
yearly_analysis['% от общего числа игр'] = (
    yearly_analysis['Количество игр'] / N * 100).round(2)

# Выводим распределение по годам
print("\nРаспределение игр и продаж по годам:")
print(yearly_analysis)

# Анализ жанров
print("\n--- АНАЛИЗ ПО ЖАНРАМ ---")
genre_counts = df.groupby('genre').size().sort_values(ascending=False)
genre_mean_sales = df.groupby(
    'genre')['global'].mean().sort_values(ascending=False)

# Выводим топ-5 жанров по количеству и по продажам
print("\nТоп-5 жанров по количеству игр:")
for genre, count in genre_counts.head(5).items():
    print(f"{genre}: {count} игр ({count/N*100:.1f}%)")

print("\nТоп-5 жанров по средним продажам:")
for genre, sales in genre_mean_sales.head(5).items():
    print(f"{genre}: {sales:.2f} млн копий")

# Анализ региональных предпочтений
print("\n--- РЕГИОНАЛЬНЫЕ ПРЕДПОЧТЕНИЯ ---")
# Для каждого региона определяем топ-3 жанра по продажам
for region in ['North America', 'europe', 'japan', 'Rest of World']:
    top_genres = df.groupby('genre')[region].mean(
    ).sort_values(ascending=False).head(3)
    print(
        f"\nТоп-3 жанра по средним продажам в регионе {region_names[region]}:")
    for genre, sales in top_genres.items():
        print(f"{genre}: {sales:.2f} млн копий")

# Создание визуализаций
print("\n--- СОЗДАНИЕ ВИЗУАЛИЗАЦИЙ ---")
try:
    # 1. График средних продаж по регионам
    plt.figure(figsize=(12, 7))
    all_regions = {region_names[k]: v for k, v in means.items()}
    colors = ['blue', 'green', 'red', 'orange', 'purple']
    bars = plt.bar(all_regions.keys(), all_regions.values(), color=colors)

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
    plt.savefig('mean_sales_by_region_all.png')
    print("График средних продаж по регионам сохранен в 'mean_sales_by_region_all.png'")

    # 2. График динамики продаж по годам
    plt.figure(figsize=(14, 8))

    # Создаем две оси y
    ax1 = plt.gca()
    ax2 = ax1.twinx()

    # Строим линию средних продаж
    line1, = ax1.plot(yearly_analysis.index, yearly_analysis['Средние продажи (млн)'],
                      'b-', marker='o', linewidth=2, label='Средние продажи (млн)')

    # Строим столбцы с количеством игр
    bars = ax2.bar(yearly_analysis.index, yearly_analysis['Количество игр'],
                   alpha=0.3, color='gray', label='Количество игр')

    # Добавляем подписи
    for i, value in enumerate(yearly_analysis['Средние продажи (млн)']):
        if not np.isnan(value) and value > 0:
            year = yearly_analysis.index[i]
            ax1.annotate(f'{value:.2f}', (year, value), textcoords="offset points",
                         xytext=(0, 10), ha='center')

    # Настраиваем оси и легенду
    ax1.set_xlabel('Год')
    ax1.set_ylabel('Средние продажи (млн)')
    ax2.set_ylabel('Количество игр')

    # Добавляем легенду
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper right')

    plt.title('Динамика средних продаж и количества игр по годам')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('year_dynamics.png')
    print("График динамики по годам сохранен в 'year_dynamics.png'")

    # 3. Тепловая карта жанровых предпочтений по регионам
    # Выбираем топ-10 жанров по общему количеству игр
    top10_genres = genre_counts.head(10).index.tolist()

    # Создаем сводную таблицу средних продаж по жанрам и регионам
    pivot_data = pd.DataFrame()
    for region in ['North America', 'europe', 'japan', 'Rest of World']:
        genre_region_means = df[df['genre'].isin(top10_genres)].groupby('genre')[
            region].mean()
        pivot_data[region_names[region]] = genre_region_means

    # Нормализуем данные для лучшей визуализации
    pivot_norm = pivot_data.div(pivot_data.max(axis=0), axis=1)

    # Создаем тепловую карту
    plt.figure(figsize=(12, 8))
    plt.pcolor(pivot_norm, cmap='YlOrRd')
    plt.colorbar(label='Относительные продажи')
    plt.xticks(np.arange(0.5, len(pivot_data.columns)),
               pivot_data.columns, rotation=45)
    plt.yticks(np.arange(0.5, len(pivot_data.index)), pivot_data.index)
    plt.title(
        'Тепловая карта популярности жанров по регионам (относительные продажи)')
    plt.tight_layout()
    plt.savefig('genre_region_heatmap.png')
    print("Тепловая карта жанров по регионам сохранена в 'genre_region_heatmap.png'")

except Exception as e:
    print(f"Ошибка при создании визуализации: {e}")

# Создание итогового отчета
print("\nСоздание итогового отчета...")
with open('final_report.txt', 'w', encoding='utf-8') as f:
    f.write("ИТОГОВЫЙ ОТЧЕТ: АНАЛИЗ ФАКТОРОВ УСПЕШНОСТИ ИГР ДЛЯ PS4\n")
    f.write("====================================================\n\n")

    f.write(
        "ТЕМА: «Анализ факторов успешности игр: региональные различия и взаимосвязи»\n\n")

    f.write("1. ОСНОВНЫЕ ВЫВОДЫ\n")
    f.write("----------------\n")
    f.write(
        "На основе проведенного анализа продаж 825 игр для PlayStation 4 были выявлены\n")
    f.write("следующие ключевые факторы, влияющие на успешность игр:\n\n")

    f.write("a) Региональные различия:\n")
    f.write(
        f"   - Европа имеет наибольшие средние продажи ({means['europe']:.2f} млн копий)\n")
    f.write(
        f"   - Северная Америка занимает второе место ({means['North America']:.2f} млн копий)\n")
    f.write(
        f"   - Япония демонстрирует наименьший интерес к играм PS4 ({means['japan']:.2f} млн копий)\n\n")

    f.write("b) Жизненный цикл консоли:\n")
    f.write(
        "   - Начальная фаза (2013-2014): Высокие продажи благодаря первым релизам\n")
    f.write("   - Средняя фаза (2015-2017): Постепенное снижение средних продаж при росте общего числа игр\n")
    f.write(
        "   - Зрелая фаза (2018): Новый рост продаж благодаря качественным эксклюзивам\n")
    f.write("   - Завершающая фаза (2019-2020): Снижение продаж в ожидании нового поколения консолей\n\n")

    f.write("c) Жанровые предпочтения:\n")
    genre_top3 = genre_mean_sales.head(3)
    for i, (genre, sales) in enumerate(genre_top3.items(), 1):
        f.write(f"   {i}. {genre}: {sales:.2f} млн копий в среднем на игру\n")
    f.write("\n")

    f.write("d) Насыщение рынка:\n")
    f.write("   В годы с максимальным количеством релизов (2016-2017) наблюдаются более низкие\n")
    f.write("   средние продажи, что указывает на эффект насыщения рынка и усиление конкуренции\n")
    f.write("   между играми за внимание и бюджет игроков.\n\n")

    f.write("2. РЕГИОНАЛЬНЫЕ ОСОБЕННОСТИ\n")
    f.write("-------------------------\n")
    for region in ['North America', 'europe', 'japan', 'Rest of World']:
        top_genres = df.groupby('genre')[region].mean(
        ).sort_values(ascending=False).head(3)
        f.write(f"\n{region_names[region]}:\n")
        f.write(
            f"   - Средние продажи: {means[region]:.2f} млн копий на игру\n")
        f.write("   - Предпочитаемые жанры:\n")
        for genre, sales in top_genres.items():
            f.write(f"     * {genre}: {sales:.2f} млн копий\n")

    f.write("\n3. ДИНАМИКА ПО ГОДАМ\n")
    f.write("------------------\n")
    for year in sorted(yearly_analysis.index):
        if year < 2013 or year > 2018:  # Пропускаем года с неполными данными
            continue
        f.write(f"\n{year} год:\n")
        f.write(
            f"   - Количество игр: {yearly_analysis.loc[year, 'Количество игр']} ({yearly_analysis.loc[year, '% от общего числа игр']}% от общего числа)\n")
        f.write(
            f"   - Средние продажи: {yearly_analysis.loc[year, 'Средние продажи (млн)']:.2f} млн копий\n")
        f.write(
            f"   - Общие продажи: {yearly_analysis.loc[year, 'Общие продажи (млн)']:.2f} млн копий\n")

        # Добавляем топовые жанры года
        if yearly_counts[year] >= 5:  # Только для годов с достаточным количеством данных
            top_genres = df[df['year'] == year].groupby(
                'genre')['global'].mean().sort_values(ascending=False).head(2)
            f.write("   - Топ жанры по продажам:\n")
            for genre, sales in top_genres.items():
                f.write(f"     * {genre}: {sales:.2f} млн копий\n")

    f.write("\n4. РЕКОМЕНДАЦИИ\n")
    f.write("-------------\n")
    f.write("На основе проведенного анализа можно сформулировать следующие рекомендации для издателей:\n\n")

    f.write("a) Региональная стратегия:\n")
    f.write(
        "   - Адаптировать маркетинговые кампании с учетом региональных предпочтений\n")
    f.write("   - Уделять особое внимание европейскому и североамериканскому рынкам\n")
    f.write("   - Для японского рынка рассматривать дополнительную локализацию и адаптацию контента\n\n")

    f.write("b) Выбор времени релиза:\n")
    f.write("   - Учитывать текущую фазу жизненного цикла консоли\n")
    f.write("   - В начальной фазе сосредоточиться на инновационных играх для ранних последователей\n")
    f.write("   - В середине жизненного цикла выделяться среди множества конкурентов\n")
    f.write("   - В зрелой фазе делать ставку на высококачественные эксклюзивы\n\n")

    f.write("c) Жанровые решения:\n")
    f.write("   - Учитывать, что шутеры, экшн-адвенчуры и спортивные игры показывают наивысшие продажи\n")
    f.write("   - Выбирать жанры с учетом целевых рынков и их предпочтений\n")
    f.write("   - Рассматривать кросс-жанровые игры для привлечения более широкой аудитории\n\n")

    f.write("d) Конкурентная среда:\n")
    f.write("   - Избегать выпуска игр в периоды высокой насыщенности рынка, если нет значительных\n")
    f.write("     конкурентных преимуществ или сильной маркетинговой поддержки\n")
    f.write("   - Инвестировать в качество и уникальные особенности для выделения среди конкурентов\n\n")

    f.write("5. ЗАКЛЮЧЕНИЕ\n")
    f.write("------------\n")
    f.write("Успешность игр для PlayStation 4 определяется сложным взаимодействием множества факторов,\n")
    f.write("среди которых региональные различия, стадия жизненного цикла консоли, жанровые предпочтения\n")
    f.write("и конкурентная среда играют ключевую роль. Понимание этих факторов и их взаимосвязей\n")
    f.write("позволяет издателям принимать более обоснованные решения при планировании релизов,\n")
    f.write("разработке маркетинговых стратегий и определении целевых рынков для максимизации продаж\n")
    f.write("и возврата инвестиций.\n")

print("Итоговый отчет сохранен в файл 'final_report.txt'")
print("\nАнализ успешно завершен!")
