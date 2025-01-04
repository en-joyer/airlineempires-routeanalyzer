import asyncio
from playwright.async_api import async_playwright
from rotaexport import rotaexport
from route_processor import process_route

# Global user_agent ve auth.json
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3"
auth_file = "auth.json"

async def main():
    # Rota export işlemi
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=auth_file, user_agent=user_agent)
        page = await context.new_page()
        await page.goto("https://ae31.airline-empires.com/routes.php?city=all&order=asc&arr_dep=all&next=1")
        await page.click("text=Routes")
        urls = await rotaexport(page, user_agent, auth_file)  # rotaexport fonksiyonundan dönen URL'leri al
        await browser.close()

    # Rotaların işlenmesi
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=auth_file, user_agent=user_agent)
        await asyncio.gather(*[process_route(url, context) for url in urls])
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
