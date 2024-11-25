import pandas as pd
import datetime

def get_criteria(category: str, count: int) -> list[str]:
    criteria = []
    for i in range(count):
        criteria.append(input(f"Введите критерий {i+1} для категории {category}: "))
    return criteria

def add_more_criteria(category: str, existing_criteria: list[str]) -> list[str]:
    while True:
        more = input(f"Хотите добавить еще критерии для категории {category}? (да/нет): ").strip().lower()
        if more == 'нет':
            break
        elif more == 'да':
            count = int(input(f"Сколько критериев хотите добавить для категории {category}?: "))
            new_criteria = get_criteria(category, count)
            existing_criteria.extend(new_criteria)
        else:
            print("Пожалуйста, введите 'да' или 'нет'.")
    return existing_criteria

def main():
    categories = ['Политические', 'Экономические', 'Социальные', 'Технологиеские']
    pest_data = {category: [] for category in categories}
    theme = input("Введите тему данного анализа: ")

    for category in categories:
        count = int(input(f"Сколько критериев хотите добавить для категории {category}?: "))
        pest_data[category] = get_criteria(category, count)
        pest_data[category] = add_more_criteria(category, pest_data[category])

    # Создание DataFrame для таблицы
    max_length = max(len(pest_data[category]) for category in categories)
    for category in categories:
        while len(pest_data[category]) < max_length:
            pest_data[category].append('')

    df = pd.DataFrame(pest_data)

    # Сохранение таблицы в файл
    df.to_excel(f'PEST_analysis_{theme}_{datetime.date.today()}.xlsx', index=False)
    print("PEST-анализ сохранен в файл 'PEST_analysis.xlsx'.")

if __name__ == "__main__":
    main()
