from playwright.sync_api import sync_playwright
import csv
import re
import time

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
auth_file = "auth.json" #Your auth.json

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context(storage_state=auth_file, user_agent=user_agent)
    page = context.new_page()

    with open("routes.txt", "r") as file, open('detaylar.csv', 'a', newline="") as csvfile:
        fieldnames = ['URL', 'ROTA', 'MONTHLY ECONOMY', 'CURRENT ECONOMY', 'DISTANCE', 'FARK']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 
        for line in file:
            try:
                urlprefix = "https://ae31.airline-empires.com/"
                url = urlprefix + line.strip()
                page.goto(url)
                page.wait_for_load_state("load")
                print(f"Ziyaret Edilen Sayfa: {url}")
                page.click("text=Save")
                page.wait_for_load_state("load")
                time.sleep(10)
                rota = page.inner_text('.tabletitle')
                distance = re.search(r'\((\d+) miles\)', rota)
                if distance:
                    distance = distance.group(1)
                else:
                    distance = ''
                monthly_demand_handle = page.evaluate_handle("chart1.series[0].data.map(point => point.y);")
                monthly_demand = monthly_demand_handle.json_value()
                monthly_demand_handle.dispose()

                seats_on_market_handle = page.evaluate_handle("chart1.series[1].data.map(point => point.y);")
                seats_on_market = seats_on_market_handle.json_value()
                seats_on_market_handle.dispose()

                monthly_economy = monthly_demand[2]
                current_economy = seats_on_market[2]
                fark = monthly_economy - current_economy

                print(f"Rota: {rota}", f"Monthly Economy: {monthly_economy}", f"Current Economy: {current_economy}", f"Distance: {distance}", f"Fark: {fark}")
                writer.writerow({
                    'URL': url,
                    'ROTA': rota,
                    'MONTHLY ECONOMY': monthly_economy,
                    'CURRENT ECONOMY': current_economy,
                    'DISTANCE': distance,
                    'FARK': fark,
                })
                print(f"İşleniyor... {url}")
            except Exception as e:
                print(f"Error processing {url}: {e}")

    browser.close()
