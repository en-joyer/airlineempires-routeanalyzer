import csv
from itertools import combinations
from urllib.parse import parse_qs, urlparse

def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader if row]  # Assume URL is in the first column

def parse_url(url):
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        city1 = query.get('city1', [None])[0]
        city2 = query.get('city2', [None])[0]
        if city1 and city2:
            return city1, city2
        else:
            print(f"Warning: Invalid URL format: {url}")
            return None, None
    except Exception as e:
        print(f"Error parsing URL {url}: {str(e)}")
        return None, None

def get_all_cities(routes):
    cities = set()
    for route in routes:
        city1, city2 = parse_url(route)
        if city1 and city2:
            cities.add(city1)
            cities.add(city2)
    return list(cities)

def generate_potential_routes(cities, existing_routes):
    potential_routes = []
    existing_pairs = set((parse_url(route) for route in existing_routes))
    for city1, city2 in combinations(cities, 2):
        if (city1, city2) not in existing_pairs and (city2, city1) not in existing_pairs:
            route = f"https://ae31.airline-empires.com/route_details.php?city1={city1}&city2={city2}"
            potential_routes.append((route, city1, city2))
    return potential_routes

def write_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'CITY1', 'CITY2'])  # Header
        writer.writerows(data)

def main():
    input_file = "detaylar.csv"
    output_file = "potansiyel.csv"

    try:
        existing_routes = read_csv(input_file)
        all_cities = get_all_cities(existing_routes)
        if not all_cities:
            print("Error: No valid cities found in the input file.")
            return
        potential_routes = generate_potential_routes(all_cities, existing_routes)
        write_csv(output_file, potential_routes)
        print(f"Potansiyel rotalar {output_file} dosyasına kaydedildi.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()