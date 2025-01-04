import asyncio
from playwright.async_api import async_playwright
import time

async def collect_hrefs(page):
    hrefs = []
    sayi = 0
    tbody_elements = await page.query_selector_all("tbody")
    for tbody in tbody_elements:
        manage_buttons = await tbody.query_selector_all("text=Manage")
        for button in manage_buttons:
            href = await button.get_attribute("href")
            hrefs.append(href)
            sayi += 1
            print(f"{sayi}. URL to be processed: {href}")
    return hrefs

async def navigate_to_next_page(page):
    await page.wait_for_load_state("load")
    next_button = await page.query_selector("text=Next")
    if next_button:
        await next_button.click()
        time.sleep(1)
        return True
    else:
        return False

async def rotaexport(user_agent, auth_file):
    hrefs = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=auth_file, user_agent=user_agent)
        page = await context.new_page()
        await page.goto("https://ae31.airline-empires.com/routes.php?city=all&order=asc&arr_dep=all&next=1")

        while True:
            hrefs.extend(await collect_hrefs(page))
            next_clicked = await navigate_to_next_page(page)
            if not next_clicked:
                break

        print("Son sayfaya gelindi.")

        with open("routes.txt", "w") as f:
            for href in hrefs:
                f.write(f"{href}\n")

        print("Kapatılıyor...")
        await browser.close()

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
auth_file = "auth.json"
asyncio.run(rotaexport(user_agent, auth_file))
