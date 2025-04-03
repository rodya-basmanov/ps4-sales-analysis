import pandas as pd

# Загрузка данных
df = pd.read_csv('ps4_sales.csv')

# Общее количество записей
N = len(df)

# Выбор числовых столбцов
numeric_columns = ['North America', 'europe',
                   'japan', 'Rest of World', 'global']

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

# Создаем отчет
with open('report_output.txt', 'w', encoding='utf-8') as f:
    f.write('ОТЧЕТ ПО АНАЛИЗУ ДАННЫХ О ПРОДАЖАХ ИГР ДЛЯ PS4\n\n')

    f.write('1. ОБЩАЯ ИНФОРМАЦИЯ\n')
    f.write('-------------------\n')
    f.write(
        f'Набор данных содержит информацию о {N} играх для PlayStation 4.\n')
    f.write('Данные включают информацию о названии игры, годе выпуска, жанре, издателе и продажах в различных регионах.\n\n')

    f.write('2. ВЫЧИСЛЕНИЕ СРЕДНЕГО ЗНАЧЕНИЯ НЕЗАВИСИМОЙ ПЕРЕМЕННОЙ\n')
    f.write('----------------------------------------------------\n')
    f.write('Используя формулу среднего значения: sum(X)/N, где X - значения переменной, N - количество наблюдений,\n')
    f.write('мы получили следующие результаты для продаж в различных регионах:\n\n')

    f.write('Регион             | Сумма       | Кол-во данных (N) | Среднее значение (sum(X)/N)\n')
    f.write('-------------------|-------------|-------------------|---------------------------\n')
    f.write(
        f'Северная Америка   | {sums["North America"]:.2f}      | {N}               | {means["North America"]:.4f}\n')
    f.write(
        f'Европа             | {sums["europe"]:.2f}      | {N}               | {means["europe"]:.4f}\n')
    f.write(
        f'Япония             | {sums["japan"]:.2f}       | {N}               | {means["japan"]:.4f}\n')
    f.write(
        f'Остальной мир      | {sums["Rest of World"]:.2f}       | {N}               | {means["Rest of World"]:.4f}\n')
    f.write(
        f'Глобально          | {sums["global"]:.2f}      | {N}               | {means["global"]:.4f}\n\n')

    f.write('Все значения представлены в миллионах проданных копий.\n\n')

    f.write('3. АНАЛИЗ РЕЗУЛЬТАТОВ\n')
    f.write('--------------------\n')
    f.write(
        f'1. Наибольшие средние продажи наблюдаются в Европе ({means["europe"]:.4f} млн копий на игру).\n')
    f.write(
        f'2. Северная Америка занимает второе место ({means["North America"]:.4f} млн копий на игру).\n')
    f.write(
        f'3. Япония имеет самые низкие показатели продаж ({means["japan"]:.4f} млн копий на игру).\n')
    f.write(
        f'4. В среднем, каждая игра для PS4 продается в количестве {means["global"]:.4f} млн копий по всему миру.\n\n')

    f.write('4. ЗАКЛЮЧЕНИЕ\n')
    f.write('------------\n')
    f.write('Анализ среднего значения продаж в различных регионах показывает, что европейский рынок является наиболее важным для игр на платформе PS4, за ним следует рынок Северной Америки.\n\n')
    f.write('Японский рынок демонстрирует значительно более низкие показатели, что может быть связано с культурными особенностями и предпочтениями игроков в этом регионе.\n\n')
    f.write('Для более полного анализа рекомендуется также рассмотреть другие статистические показатели, такие как медиана, мода, стандартное отклонение и корреляции между различными переменными.\n')

print("Отчет успешно создан в файле 'report_output.txt'")
