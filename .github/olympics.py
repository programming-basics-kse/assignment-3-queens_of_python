import argparse
import csv
from collections import defaultdict

def write_output(output_file, result):
    if output_file:
        with open(output_file, mode='w', encoding='utf-8') as file:
            file.write("\n".join(result))
            print(f"Результати були записані в файл {output_file}")
    else:
        print("\n".join(result))

def load_data(file_path):
    countries_data = defaultdict(list)
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                country_name = row['Team']
                country_code = row['NOC']
                year = row['Year']
                medal = row['Medal']
                name = row['Name']
                sport = row['Sport']
                if medal != 'NA' and medal != '':
                    countries_data[country_name].append((year, medal, name, sport))
                    countries_data[country_code].append((year, medal, name, sport))
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдений.")
    return countries_data

def process_medals(args, countries_data):
    medalists = []
    country_medals = {'Gold': 0, 'Silver': 0, 'Bronze': 0}

    for country, data in countries_data.items():
        if country == args.country:
            for year, medal, name, sport in data:
                if year == args.year:
                    medalists.append({'name': name, 'sport': sport, 'medal': medal})
                    if medal == 'Gold':
                        country_medals['Gold'] += 1
                    elif medal == 'Silver':
                        country_medals['Silver'] += 1
                    elif medal == 'Bronze':
                        country_medals['Bronze'] += 1

    result = []
    result.append(f"Топ-10 медалістів з {args.country} на Олімпіаді {args.year}:")
    count = 0
    for medalist in medalists:
        if medalist['medal'] != 'NA':
            count += 1
            result.append(f"{count}. {medalist['name']} - {medalist['sport']} - {medalist['medal']}")
        if count == 10:
            break

    result.append("\nЗагальна кількість медалей для країни:")
    result.append(f"Золото: {country_medals['Gold']}, Срібло: {country_medals['Silver']}, Бронза: {country_medals['Bronze']}")

    write_output(args.output, result)

def process_total(args, countries_data):
    country_medals = defaultdict(lambda: {'Gold': 0, 'Silver': 0, 'Bronze': 0})

    for country, data in countries_data.items():
        for year, medal, _, _ in data:
            if year == args.year:
                if medal == 'Gold':
                    country_medals[country]['Gold'] += 1
                elif medal == 'Silver':
                    country_medals[country]['Silver'] += 1
                elif medal == 'Bronze':
                    country_medals[country]['Bronze'] += 1

    result = []
    result.append(f"Статистика медалей для {args.year} Олімпіади:")
    for country, medals in country_medals.items():
        result.append(f"{country} - Золото: {medals['Gold']}, Срібло: {medals['Silver']}, Бронза: {medals['Bronze']}")

    write_output(args.output, result)

def process_interactive(args, countries_data):
    while True:
        country_input = input("Введіть назву країни (або 'exit' для виходу): ")
        if country_input.lower() == 'exit':
            break

        if country_input in countries_data:
            country_years = countries_data[country_input]
            first_participation = min(country_years, key=lambda x: x[0])
            print(f"Перша участь {country_input}: Рік {first_participation[0]}")

            medal_count = defaultdict(int)
            for year, medal, _, _ in country_years:
                medal_count[year] += 1
            best_year = max(medal_count, key=medal_count.get)
            print(f"Найуспішніший рік для {country_input}: {best_year} з {medal_count[best_year]} медалями")

            worst_year = min(medal_count, key=medal_count.get)
            print(f"Найгірший рік для {country_input}: {worst_year} з {medal_count[worst_year]} медалями")

            medal_types = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
            for _, medal, _, _ in country_years:
                if medal == 'Gold':
                    medal_types['Gold'] += 1
                elif medal == 'Silver':
                    medal_types['Silver'] += 1
                elif medal == 'Bronze':
                    medal_types['Bronze'] += 1
            total_years = len(set(year for year, _, _, _ in country_years))
            print(f"Середня кількість медалей за рік для {country_input}: Золото: {medal_types['Gold'] / total_years:.2f}, Срібло: {medal_types['Silver'] / total_years:.2f}, Бронза: {medal_types['Bronze'] / total_years:.2f}")
        else:
            print(f"Країна'{country_input}' не знайдено в даних.")

def main():
    parser = argparse.ArgumentParser(description="Олімпійські медалі: пошук та статистика")
    parser.add_argument("file", help="Шлях до файлу з даними")
    subparsers = parser.add_subparsers(dest="command", required=True)

    medals_parser = subparsers.add_parser("medals", help="Отримати статистику медалей для країни та року")
    medals_parser.add_argument("country", help="Країна (назва або код)")
    medals_parser.add_argument("year", help="Рік Олімпіади")
    medals_parser.add_argument("-output", help="Файл для виведення результатів")
    medals_parser.set_defaults(func=process_medals)

    total_parser = subparsers.add_parser("total", help="Отримати статистику медалей для всіх країн на певній Олімпіаді")
    total_parser.add_argument("year", help="Рік Олімпіади")
    total_parser.add_argument("-output", help="Файл для виведення результатів")
    total_parser.set_defaults(func=process_total)

    interactive_parser = subparsers.add_parser("interactive", help="Запустити інтерактивний режим")
    interactive_parser.set_defaults(func=process_interactive)

    args = parser.parse_args()
    countries_data = load_data(args.file)

    args.func(args, countries_data)

if __name__ == "__main__":
    main()
