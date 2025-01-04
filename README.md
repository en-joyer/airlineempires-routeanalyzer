# Airline Empires Route Analysis Tool

I made such a tool to make faster decisions by reducing a lot of information to a single CSV file. I wrote it in my spare time and I was not planning to share it with others. I decided to share it because I quit Airlinempires. I do not plan to update this tool. 

This project uses Playwright to automate the process of extracting route information from the website and saving the data into a CSV file. The script is designed to handle multiple URLs from a text file (`routes.txt`), navigate through each route's page, and collect specific information such as route name, distance, and demand data. The extracted data is then stored in `detaylar.csv`.

## Features

- Extracts route information:
It collects the name of the route, the distance, the current available capacity and demand, the URL of the route in a single line.
- Saves the extracted data in a CSV file.
- Handles errors during scraping to ensure smooth execution.

## Prerequisites

1. Python 3.9 or higher
2. Playwright installed (`playwright.sync_api` is used)
3. Firefox browser installed (used as the automation browser)
4. `auth.json` file for authentication (contains session or user data for the target website)

## Installation

1. Clone the repository:

2. Install required Python packages:
   ```bash
   pip install playwright
   playwright install
   ```
3. ```bash
   npx playwright codegen *.airlineempires.com --save-storage=auth.json
   ```
   Save your cookies and login info with codegen.

## Usage

1. Run main.py
   ```bash
   py main.py
   ```
OR

Run rotaexport.py first, then run route_processor.py
For new potential routes you can use the potansiyel.py

## Output

- **`detaylar.csv`**: Contains the extracted data with the following columns:
  - `URL`: The processed URL.
  - `ROTA`: The route name.
  - `MONTHLY ECONOMY`: Monthly demand.
  - `CURRENT ECONOMY`: Current supply.
  - `DISTANCE`: Distance of the route in miles.
  - `FARK`: The difference between demand and supply.

## Error Handling

- If an error occurs while processing a URL, the script will log the error and continue with the next URL.
- Errors will be printed to the terminal for debugging purposes.

## Notes

- The script uses `time.sleep(10)` in some places to ensure the page is fully loaded. `page.wait_for_selector()` is not always fully work on that website.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

