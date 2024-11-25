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