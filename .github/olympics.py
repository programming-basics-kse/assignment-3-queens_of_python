import sys
if len(sys.argv) < 3:
    print("Недостатньо аргументів. Формат:\n"
          "1. olympics.py athlete_events.tsv -medals Країна Рік [-output Файл]\n"
          "2. olympics.py athlete_events.tsv -total Рік\n"
          "3. olympics.py athlete_events.tsv -overall Країна1 Країна2 ...\n"
          "4. olympics.py athlete_events.tsv -interactive")
    sys.exit(1)
file_path = sys.argv[1]
option = sys.argv[2]
if option == '-medals':
    if len(sys.argv) < 5:
        print("Недостатньо аргументів. Формат: olympics.py athlete_events.tsv -medals Країна Рік [-output Файл]")
        sys.exit(1)
    country = sys.argv[3]
    year = sys.argv[4]
    output_file = None
    if len(sys.argv) > 5 and sys.argv[5] == "-output":
        if len(sys.argv) < 7:
            print("Вкажіть ім'я файлу після -output")
            sys.exit(1)
        output_file = sys.argv[6]
    medals = {"Gold": 0, "Silver": 0, "Bronze": 0}
    medalists = []
    with open(file_path, 'rt') as file:
        next(file)
        for line in file:
            line = line[:-1]
            split = line.split("\t")
            id_ = split[0]
            name = split[1]
            sex = split[2]
            age = split[3]
            height = split[4]
            weight = split[5]
            team = split[6]
            noc = split[7]
            games = split[8]
            year_col = split[9]
            season = split[10]
            city = split[11]
            sport = split[12]
            event = split[13]
            medal = split[14]
            if year_col == year and (team == country or noc == country):
                if medal != "NA":  # Тільки медалісти
                    medalists.append(f"{name} - {sport} - {medal}")
                    medals[medal] += 1
    result = "\n".join(medalists[:10]) + "\n"
    result += f"Gold: {medals['Gold']}, Silver: {medals['Silver']}, Bronze: {medals['Bronze']}"
    print(result)
    if output_file:
        with open(output_file, 'w') as file:
            file.write(result)
elif option == '-total':
    if len(sys.argv) < 4:
        print("Недостатньо аргументів. Формат: olympics.py data.csv -total Year")
        sys.exit(1)
    year = sys.argv[3]
    country_medals = {}
    with open(file_path, 'rt') as file:
        next(file)
        for line in file:
            line = line[:-1]
            split = line.split("\t")
            id_ = split[0]
            name = split[1]
            sex = split[2]
            age = split[3]
            height = split[4]
            weight = split[5]
            team = split[6]
            noc = split[7]
            games = split[8]
            year_col = split[9]
            season = split[10]
            city = split[11]
            sport = split[12]
            event = split[13]
            medal = split[14]
            if year_col == year and medal != "NA":
                country = f"{team} ({noc})"
                if country not in country_medals:
                    country_medals[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
                country_medals[country][medal] += 1
    result_lines = []
    for country, counts in sorted(country_medals.items()):
        result_lines.append(f"{country} - Gold: {counts['Gold']}, Silver: {counts['Silver']}, Bronze: {counts['Bronze']}")
    result = "\n".join(result_lines)
    print(result)


elif option == '-overall':
    if len(sys.argv) < 4:
        print("Недостатньо аргументів. Формат: olympics.py data.csv -overall Країна1 Країна2 ...")
        sys.exit(1)
    countries = sys.argv[3:]
    country_years = {country: {} for country in countries}

    with open(file_path, 'rt') as file:
        next(file)
        for line in file:
            line = line[:-1]
            split = line.split("\t")
            id_ = split[0]
            name = split[1]
            sex = split[2]
            age = split[3]
            height = split[4]
            weight = split[5]
            team = split[6]
            noc = split[7]
            games = split[8]
            year_col = split[9]
            season = split[10]
            city = split[11]
            sport = split[12]
            event = split[13]
            medal = split[14]
            if medal != "NA":
                for country in countries:
                    if team == country or noc == country:
                        if year_col not in country_years[country]:
                            country_years[country][year_col] = 0
                        country_years[country][year_col] += 1

    result_lines = []
    for country, years in country_years.items():
        if years:
            max_year = max(years, key=years.get)
            max_count = years[max_year]
            result_lines.append(f"{country} - {max_year} ({max_count} медалей)")
        else:
            result_lines.append(f"{country} - Немає медалей")

    result = "\n".join(result_lines)
    print(result)
elif option == '-interactive':
    country_data = {}
    with open(file_path, 'rt') as file:
        next(file)
        for line in file:
            line = line[:-1]
            split = line.split("\t")
            id_ = split[0]
            name = split[1]
            sex = split[2]
            age = split[3]
            height = split[4]
            weight = split[5]
            team = split[6]
            noc = split[7]
            games = split[8]
            year_col = split[9]
            season = split[10]
            city = split[11]
            sport = split[12]
            event = split[13]
            medal = split[14]
            country_key = f"{team} ({noc})"
            if country_key not in country_data:
                country_data[country_key] = {}
            if year_col not in country_data[country_key]:
                country_data[country_key][year_col] = {
                    "city": city,
                    "medals": {"Gold": 0, "Silver": 0, "Bronze": 0}
                }
            if medal in {"Gold", "Silver", "Bronze"}:
                country_data[country_key][year_col]["medals"][medal] += 1
    print("Введіть країну (назву або код) для перегляду статистики. Введіть 'exit' для виходу.")
    while True:
        user_input = input("Країна: ").strip()
        if user_input.lower() == 'exit':
            print("Інтерактивний режим завершено.")
            break

        matching_countries = [key for key in country_data.keys() if user_input in key]
        if not matching_countries:
            print(f"Країна '{user_input}' не знайдена. Спробуйте ще раз.")
            continue

        for country in matching_countries:
            print(f"\nСтатистика для {country}:")
            years = country_data[country]
            first_year = min(years.keys(), key=int)
            first_city = years[first_year]["city"]

            total_medals = {}
            for year, data in years.items():
                for medal_type, count in data["medals"].items():
                    total_medals[year] = total_medals.get(year, 0) + count

            if total_medals:
                best_year = max(total_medals, key=total_medals.get)
                best_count = total_medals[best_year]
                worst_year = min(total_medals, key=total_medals.get)
                worst_count = total_medals[worst_year]

                avg_gold = sum(data["medals"]["Gold"] for data in years.values()) / len(years)
                avg_silver = sum(data["medals"]["Silver"] for data in years.values()) / len(years)
                avg_bronze = sum(data["medals"]["Bronze"] for data in years.values()) / len(years)

                print(f"Перша участь: {first_year}, {first_city}")
                print(f"Найуспішніша олімпіада: {best_year} ({best_count} медалей)")
                print(f"Найневдаліша олімпіада: {worst_year} ({worst_count} медалей)")
                print(f"Середня кількість медалей: Gold: {avg_gold:.2f}, Silver: {avg_silver:.2f}, Bronze: {avg_bronze:.2f}")
            else:
                print(f"Країна не здобула жодної медалі.")
else:
    print(f"Другий аргумент має бути -medals, -total, -overall або -interactive")
    sys.exit(1)