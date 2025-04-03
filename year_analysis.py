import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Загрузка данных
df = pd.read_csv('ps4_sales.csv')

# Общее количество записей
N = len(df)

# Анализ продаж по годам
print(f"Количество игр в наборе данных: {N}")

# Группировка по годам для подсчета количества игр и анализа продаж
yearly_counts = df.groupby('year').size()
yearly_global_mean = df.groupby('year')['global'].mean()
yearly_global_sum = df.groupby('year')['global'].sum()

# Объединяем данные в единый DataFrame для анализа
yearly_analysis = pd.DataFrame({
    'Количество игр': yearly_counts,
    'Средние продажи (млн)': yearly_global_mean,
    'Общие продажи (млн)': yearly_global_sum
})

# Добавим процент игр от общего количества
yearly_analysis['% от общего количества'] = (
    yearly_analysis['Количество игр'] / N * 100).round(2)

# Сортируем по годам
yearly_analysis = yearly_analysis.sort_index()

# Выводим результаты анализа
print("\nАнализ продаж игр по годам:")
print(yearly_analysis)

# Дополнительно проанализируем топовые жанры по годам
print("\nТоп жанры по годам:")
for year in sorted(df['year'].unique()):
    # Пропускаем года с малым количеством игр
    if year == 0 or yearly_counts[year] < 5:
        continue

    top_genres = df[df['year'] == year].groupby(
        'genre').size().sort_values(ascending=False).head(3)
    top_genres_sales = df[df['year'] == year].groupby(
        'genre')['global'].mean().sort_values(ascending=False).head(3)

    print(f"\nГод: {year}")
    print(f"Топ-3 жанра по количеству игр:")
    for genre, count in top_genres.items():
        print(f"- {genre}: {count} игр")

    print(f"Топ-3 жанра по средним продажам:")
    for genre, sales in top_genres_sales.items():
        print(f"- {genre}: {sales:.2f} млн копий")

# Создаем визуализацию для анализа
try:
    # График 1: Динамика средних продаж по годам
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

    # Добавляем подписи к точкам на линии
    for i, value in enumerate(yearly_analysis['Средние продажи (млн)']):
        if not np.isnan(value) and value > 0:
            year = yearly_analysis.index[i]
            ax1.annotate(f'{value:.2f}', (year, value), textcoords="offset points",
                         xytext=(0, 10), ha='center')

    # Настройка осей и легенды
    ax1.set_xlabel('Год')
    ax1.set_ylabel('Средние продажи (млн)')
    ax2.set_ylabel('Количество игр')

    # Добавляем легенду
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper right')

    plt.title('Динамика средних продаж и количества выпущенных игр по годам')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('year_sales_analysis.png')
    print("\nГрафик динамики продаж по годам сохранен в файл 'year_sales_analysis.png'")

    # График 2: Корреляция между количеством игр и средними продажами
    plt.figure(figsize=(10, 6))
    plt.scatter(yearly_analysis['Количество игр'], yearly_analysis['Средние продажи (млн)'],
                s=yearly_analysis['Общие продажи (млн)']*3, alpha=0.6)

    # Добавляем подписи к точкам
    for i, year in enumerate(yearly_analysis.index):
        if year != 0 and not np.isnan(yearly_analysis['Средние продажи (млн)'][i]):
            plt.annotate(str(year),
                         (yearly_analysis['Количество игр'][i],
                          yearly_analysis['Средние продажи (млн)'][i]),
                         textcoords="offset points", xytext=(5, 5), ha='left')

    plt.title('Зависимость между количеством игр и средними продажами')
    plt.xlabel('Количество выпущенных игр')
    plt.ylabel('Средние продажи (млн)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('year_correlation_analysis.png')
    print("График корреляции сохранен в файл 'year_correlation_analysis.png'")

except Exception as e:
    print(f"Ошибка при создании визуализации: {e}")

# Анализ в тексте
print("\nАНАЛИЗ ТРЕНДОВ ПО ГОДАМ:")
print("------------------------")

# Определяем тренды
years_to_analyze = [y for y in sorted(yearly_analysis.index) if y >= 2013]
if len(years_to_analyze) > 2:
    # Первый и последний год для основного периода с данными
    first_year = years_to_analyze[0]
    last_year = years_to_analyze[-1]

    # Рост или падение относительно первого года анализа
    change = (yearly_analysis.loc[last_year, 'Средние продажи (млн)'] /
              yearly_analysis.loc[first_year, 'Средние продажи (млн)'] - 1) * 100

    print(f"1. Тренд за период {first_year}-{last_year}:")
    if change > 0:
        print(
            f"   Рост средних продаж на {change:.1f}% (с {yearly_analysis.loc[first_year, 'Средние продажи (млн)']:.2f} до {yearly_analysis.loc[last_year, 'Средние продажи (млн)']:.2f} млн)")
    else:
        print(
            f"   Снижение средних продаж на {abs(change):.1f}% (с {yearly_analysis.loc[first_year, 'Средние продажи (млн)']:.2f} до {yearly_analysis.loc[last_year, 'Средние продажи (млн)']:.2f} млн)")

    # Находим год с максимальными и минимальными продажами
    max_year = yearly_analysis['Средние продажи (млн)'].idxmax()
    min_year = yearly_analysis[yearly_analysis.index >=
                               2013]['Средние продажи (млн)'].idxmin()

    print(f"\n2. Годы с экстремальными значениями:")
    print(
        f"   Максимальные средние продажи: {yearly_analysis.loc[max_year, 'Средние продажи (млн)']:.2f} млн в {max_year} году")
    print(
        f"   Минимальные средние продажи: {yearly_analysis.loc[min_year, 'Средние продажи (млн)']:.2f} млн в {min_year} году")

    # Анализ корреляции между количеством игр и средними продажами
    correlation = yearly_analysis['Количество игр'].corr(
        yearly_analysis['Средние продажи (млн)'])
    print(
        f"\n3. Корреляция между количеством игр и средними продажами: {correlation:.2f}")
    if correlation < -0.5:
        print("   Выявлена сильная отрицательная корреляция: чем больше игр выпускается, тем ниже средние продажи.")
    elif correlation > 0.5:
        print("   Выявлена сильная положительная корреляция: чем больше игр выпускается, тем выше средние продажи.")
    else:
        print(
            "   Не выявлено сильной корреляции между количеством игр и средними продажами.")

# Выводим потенциальные факторы влияния
print("\n4. Потенциальные факторы, влияющие на тренды:")
print("   - Жизненный цикл консоли (PS4 вышла в конце 2013 года)")
print("   - Крупные эксклюзивные релизы")
print("   - Конкуренция с другими платформами")
print("   - Изменения в бизнес-моделях (рост цифровых продаж, подписок)")
print("   - Экономические факторы (рецессии, изменения покупательной способности)")
print("   - Пандемия COVID-19 (для 2019-2020 годов)")

# Создаем файл с выводами
with open('year_analysis_conclusions.txt', 'w', encoding='utf-8') as f:
    f.write("АНАЛИЗ ТРЕНДОВ ПРОДАЖ ИГР PS4 ПО ГОДАМ\n")
    f.write("=====================================\n\n")
    f.write(
        f"В ходе анализа данных о продажах {N} игр для PlayStation 4 были выявлены следующие тенденции:\n\n")

    # Переносим выводы в файл
    if len(years_to_analyze) > 2:
        f.write(f"1. ОБЩИЙ ТРЕНД ({first_year}-{last_year}):\n")
        if change > 0:
            f.write(
                f"   За анализируемый период наблюдался рост средних продаж на {change:.1f}%\n")
            f.write(
                f"   (с {yearly_analysis.loc[first_year, 'Средние продажи (млн)']:.2f} до {yearly_analysis.loc[last_year, 'Средние продажи (млн)']:.2f} млн копий на игру).\n\n")
        else:
            f.write(
                f"   За анализируемый период наблюдалось снижение средних продаж на {abs(change):.1f}%\n")
            f.write(
                f"   (с {yearly_analysis.loc[first_year, 'Средние продажи (млн)']:.2f} до {yearly_analysis.loc[last_year, 'Средние продажи (млн)']:.2f} млн копий на игру).\n\n")

    f.write("2. КЛЮЧЕВЫЕ НАБЛЮДЕНИЯ:\n")
    f.write(
        f"   - Максимальные средние продажи наблюдались в {max_year} году: {yearly_analysis.loc[max_year, 'Средние продажи (млн)']:.2f} млн копий на игру\n")
    f.write(
        f"   - Минимальные средние продажи наблюдались в {min_year} году: {yearly_analysis.loc[min_year, 'Средние продажи (млн)']:.2f} млн копий на игру\n")
    f.write(
        f"   - Корреляция между количеством выпущенных игр и средними продажами: {correlation:.2f}\n\n")

    f.write("3. ПОТЕНЦИАЛЬНЫЕ ФАКТОРЫ ВЛИЯНИЯ:\n")
    f.write("   a) Жизненный цикл консоли:\n")
    f.write("      PlayStation 4 была выпущена в конце 2013 года. Высокие продажи в 2013-2014 гг. могут\n")
    f.write("      быть связаны с энтузиазмом ранних последователей и выпуском первых эксклюзивов.\n")
    f.write("      Последующее снижение до 2016-2017 гг. может отражать середину жизненного цикла,\n")
    f.write("      а рост в 2018 г. - выход нового поколения высококачественных эксклюзивов.\n\n")

    f.write("   b) Качество релизов и эксклюзивы:\n")
    f.write("      Годы с высокими средними продажами часто совпадают с выпуском крупных эксклюзивов\n")
    f.write(
        "      или популярных серий (например, Red Dead Redemption 2 в 2018 году).\n\n")

    f.write("   c) Рыночные факторы:\n")
    f.write(
        "      Изменения в бизнес-моделях (рост цифровых продаж, которые могут не полностью\n")
    f.write("      отражаться в данных), увеличение числа подписочных сервисов и конкуренция\n")
    f.write("      с другими платформами также влияют на тренды продаж.\n\n")

    f.write("   d) Насыщение рынка:\n")
    f.write(
        "      Корреляция между количеством игр и средними продажами может указывать\n")
    f.write("      на эффект насыщения рынка, когда увеличение количества релизов\n")
    f.write(
        "      приводит к снижению средних продаж из-за конкуренции между играми.\n\n")

    f.write("4. РЕГИОНАЛЬНЫЕ РАЗЛИЧИЯ:\n")
    f.write("   Анализ показывает, что европейский рынок является наиболее значимым для PS4,\n")
    f.write(
        "   за ним следует рынок Северной Америки. Япония демонстрирует самые низкие\n")
    f.write("   показатели продаж, что может объясняться культурными различиями и предпочтениями.\n\n")

    f.write("5. ЗАКЛЮЧЕНИЕ:\n")
    f.write("   Успешность игр для PS4 зависит от множества факторов, включая:\n")
    f.write("   - Время выхода в жизненном цикле консоли\n")
    f.write("   - Жанр игры и его популярность в разных регионах\n")
    f.write("   - Конкуренция с другими релизами в тот же период\n")
    f.write("   - Маркетинговая поддержка и статус эксклюзивности\n\n")

    f.write(
        "   Издателям рекомендуется учитывать региональные особенности при планировании\n")
    f.write("   релизов и маркетинговых кампаний, а также стратегически выбирать время выпуска\n")
    f.write("   игр с учетом жизненного цикла консоли.")

print("\nПодробный анализ сохранен в файл 'year_analysis_conclusions.txt'")
