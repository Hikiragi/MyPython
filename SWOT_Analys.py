import pandas as pd
import datetime


def getCriteria(category: str, count: int) -> list:
    print("getCriteria запущена")
    criteria = []
    for i in range(count):
        criteria.append(input(f"Введите критерий {i+1} для категории {category.lower()}: "))
    return criteria


def addMoreCriteria(category: str, existing_criteria: list) -> list:
    while True:
        more = input(f"Хотите добавить еще критериев для категории {category}? (Y/n)").strip().lower()
        if more == "n":
            break
        elif more == "y":
            count = int(input(f"Сколько критериев вы хотите добавить для категории {category}?: "))
            new_criteria = getCriteria(category, count)
            existing_criteria.extend(new_criteria)
        else:
            print("Пожалуйста, введите y/n")
    return existing_criteria


def main():
    categories = ['Преимущества', 'Недостатки', 'Возможности', 'Угрозы']
    swot_data = {category: [] for category in categories}
    Theme = input("Введите тему анализа: ")

    for category in categories:
        count = int(input(f"Сколько критериев хотите добавить для категории {category}?: "))
        swot_data[category] = getCriteria(category, count)
        swot_data[category] = addMoreCriteria(category, swot_data[category])

    # Создание DataFrame для таблицы
    max_length = max(len(swot_data[category]) for category in categories)
    for category in categories:
        while len(swot_data[category]) < max_length:
            swot_data[category].append('')

    df = pd.DataFrame(swot_data)

    # Сохранение таблицы в файл
    df.to_excel(f'SWOT_analysis_{Theme}_{datetime.date.today()}.xlsx', index=False)
    print("SWOT-анализ сохранен в файл 'SWOT_analysis.xlsx'.")


if __name__ == "__main__":
    main()
