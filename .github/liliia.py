# import argparse
# def get_headers(file_path):
#     with open(file_path, "r") as file:
#         headers = file.readline().strip().split('\t')
#         print(headers)
#         try:
#             team_index = headers.index("Team")
#             noc_index = headers.index("NOC")
#             year_index = headers.index("Year")
#             medal_index = headers.index("Medal")
#             name_index = headers.index("Name")
#             event_index = headers.index("Event")
#             return team_index, noc_index, year_index, medal_index, name_index, event_index
#         except ValueError as e:
#             print(f"Column not found: {e}")
#     # виписуємо індекси колонок, що відповідають за конкретну інформацію, яка там потрібна
# def medalists_func(file_path, country, year, team_index, noc_index, year_index, medal_index, name_index, event_index, output_file=None):
#     medalists = []
#     gold_count = 0
#     silver_count = 0
#     bronze_count = 0
#     with open(file_path, "r") as file:
#         next_line = file.readline()
#         while next_line:
#             row = next_line.strip().split("\t")
#             if (row[team_index] == country or row[noc_index] == country) and row[year_index] == year:
#                 if row[medal_index] != "NA":
#                     medalists.append(f"{row[name_index]} - {row[event_index]} - {row[medal_index]}")
#                     if row[medal_index] == "Gold":
#                         gold_count += 1
#                     elif row[medal_index] == "Silver":
#                         silver_count += 1
#                     elif row[medal_index] == "Bronze":
#                         bronze_count += 1
#             next_line = file.readline()
#     result = "\n".join(medalists[:10])
#     result += f"\n\nMedal count:\nGold: {gold_count}, Silver: {silver_count}, Bronze: {bronze_count}"
#     if output_file:
#         with open(output_file, "w") as out_file:
#             out_file.write(result)
#     print(result)
# def total_medal(file_path, year, team_index, year_index, medal_index):
#     total_medals = {}
#     with open(file_path, "r") as file:
#         next_line = file.readline()
#         while next_line:
#             row = next_line.strip().split("\t")
#             if row[year_index] == year and row[medal_index] != "NA":
#                 country = row[team_index]
#                 if country not in total_medals:
#                     total_medals[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
#                 total_medals[country][row[medal_index]] += 1
#             next_line = file.readline()
#     for country, counts in total_medals.items():
#         print(f"{country} - Gold: {counts['Gold']}, Silver: {counts['Silver']}, Bronze: {counts['Bronze']}")
# def best_overall(file_path, countries, team_index, noc_index, year_index, medal_index):
#     country_years = {country: {} for country in countries}
#     with open(file_path, "r") as file:
#         next_line = file.readline()
#         while next_line:
#             row = next_line.strip().split("\t")
#             country = row[team_index]
#             year = row[year_index]
#             if country in countries and row[medal_index] != "NA":
#                 if year not in country_years[country]:
#                     country_years[country][year] = 0
#                 country_years[country][year] += 1
#             next_line = file.readline()
#     for country, years in country_years.items():
#         if years:
#             best_year = max(years, key=years.get)
#             print(f"{country} - Best Year: {best_year} with {years[best_year]} medals")
#         else:
#             print(f"{country} - No medals")
# def interactive_mode(file_path, team_index, noc_index, year_index, medal_index, name_index, event_index):
#     print("Interactive Mode: Type a country name or code to get statistics (type 'exit' to quit).")
#     while True:
#         country = input("Enter country: ").strip()
#         if country.lower() == "exit":
#             break
#         # це потім щось з цим зробити
#         print(f"Statistics for {country}...")
#         print("First Participation: Year & City")
#         print("Most Successful Olympics: Year & Medal Count")
#         print("Least Successful Olympics: Year & Medal Count")
#         print("Average Medals Per Olympics: Gold, Silver, Bronze")
# def main():
#     parser = argparse.ArgumentParser(description="Olympics Data Analysis Tool")
#     parser.add_argument("file", help="Path to the data file")
#     parser.add_argument("command", choices=["-medals", "-total", "-overall", "-interactive"],
#                         help="Command to execute (-medals, -total, -overall, -interactive)")
#     parser.add_argument("args", nargs="*", help="Additional arguments for the command")
#     args = parser.parse_args()
#     team_index, noc_index, year_index, medal_index, name_index, event_index = get_headers(args.file)
#     if team_index is None:  # Check if any index is missing due to an error in get_headers
#         print("Error: Could not retrieve column indexes.")
#         return
#     if args.command == "-medals":
#         if len(args.args) < 2:
#             print("Error: -medals requires country and year arguments.")
#             return
#         country, year = args.args[:2]
#         output_file = args.args[2] if len(args.args) > 2 and args.args[2] == "-output" else None
#         medalists_func(args.file, country, year, team_index, noc_index, year_index, medal_index, name_index, event_index, output_file)
#     elif args.command == "-total":
#         if len(args.args) < 1:
#             print("Error: -total requires a year argument.")
#             return
#         year = args.args[0]
#         total_medal(args.file, year, team_index, noc_index, year_index, medal_index)
#     elif args.command == "-overall":
#         if len(args.args) < 1:
#             print("Error: -overall requires at least one country.")
#             return
#         countries = args.args
#         best_overall(args.file, countries, team_index, noc_index, year_index, medal_index)
#     elif args.command == "-interactive":
#         interactive_mode(args.file, team_index, noc_index, year_index, medal_index, name_index, event_index)
#     else:
#         print(f"Unknown command: {args.command}")
# if __name__ == '__main__':
#     main()
import argparse


def get_headers(file_path):
    with open(file_path, "r") as file:
        headers = file.readline().strip().split('\t')
        print(headers)
        try:
            team_index = headers.index("Team")
            noc_index = headers.index("NOC")
            year_index = headers.index("Year")
            medal_index = headers.index("Medal")
            name_index = headers.index("Name")
            event_index = headers.index("Event")
            return team_index, noc_index, year_index, medal_index, name_index, event_index
        except ValueError as e:
            print(f"Column not found: {e}")


def medalists_func(file_path, country, year, team_index, noc_index, year_index, medal_index, name_index, event_index):
    medalists = []
    gold_count = 0
    silver_count = 0
    bronze_count = 0
    with open(file_path, "r") as file:
        next_line = file.readline()
        while next_line:
            row = next_line.strip().split("\t")
            if (row[team_index] == country or row[noc_index] == country) and row[year_index] == year:
                if row[medal_index] != "NA":
                    medalists.append(f"{row[name_index]} - {row[event_index]} - {row[medal_index]}")
                    if row[medal_index] == "Gold":
                        gold_count += 1
                    elif row[medal_index] == "Silver":
                        silver_count += 1
                    elif row[medal_index] == "Bronze":
                        bronze_count += 1
            next_line = file.readline()

    result = "\n".join(medalists[:10])
    result += f"\n\nMedal count:\nGold: {gold_count}, Silver: {silver_count}, Bronze: {bronze_count}"
    print(result)


def total_medal(file_path, year, team_index, year_index, medal_index):
    total_medals = {}
    with open(file_path, "r") as file:
        next_line = file.readline()
        while next_line:
            row = next_line.strip().split("\t")
            if row[year_index] == year and row[medal_index] != "NA":
                country = row[team_index]
                if country not in total_medals:
                    total_medals[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
                total_medals[country][row[medal_index]] += 1
            next_line = file.readline()

    for country, counts in total_medals.items():
        print(f"{country} - Gold: {counts['Gold']}, Silver: {counts['Silver']}, Bronze: {counts['Bronze']}")


def best_overall(file_path, countries, team_index, noc_index, year_index, medal_index):
    country_years = {country: {} for country in countries}
    with open(file_path, "r") as file:
        next_line = file.readline()
        while next_line:
            row = next_line.strip().split("\t")
            country = row[team_index]
            year = row[year_index]
            if country in countries and row[medal_index] != "NA":
                if year not in country_years[country]:
                    country_years[country][year] = 0
                country_years[country][year] += 1
            next_line = file.readline()

    for country, years in country_years.items():
        if years:
            best_year = max(years, key=years.get)
            print(f"{country} - Best Year: {best_year} with {years[best_year]} medals")
        else:
            print(f"{country} - No medals")


def main():
    parser = argparse.ArgumentParser(description="Olympics Data Analysis Tool")
    parser.add_argument("file", help="Path to the data file")
    parser.add_argument("command", choices=["-medals", "-total", "-overall"],
                        help="Command to execute (-medals, -total, -overall)")
    parser.add_argument("args", nargs="*", help="Additional arguments for the command")

    args = parser.parse_args()

    team_index, noc_index, year_index, medal_index, name_index, event_index = get_headers(args.file)
    if team_index is None:  # Ensure column indices were correctly retrieved
        print("Error: Could not retrieve column indexes.")
        return

    if args.command == "-medals":
        if len(args.args) < 2:
            print("Error: -medals requires country and year arguments.")