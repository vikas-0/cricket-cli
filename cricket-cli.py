import argparse
import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Function to scrape match details
def scrape_match_details(driver):
    # Navigate to the URL of the page to scrape
    url = 'https://www.cricbuzz.com'
    driver.get(url)

    # Allow some time for the page to load (adjust the time as needed)
    time.sleep(3)

    # Find the container element by its ID
    match_container = driver.find_element(By.ID, 'match_menu_container')

    # Find all <li> elements within the container
    li_elements = match_container.find_elements(By.TAG_NAME, 'li')

    # Regular expression pattern to match epoch time
    epoch_pattern = r'\((\d+) \|'

    match_details = []

    # Print details of all <a> elements within each <li>
    for idx, li in enumerate(li_elements, start=1):
        a_tag = li.find_element(By.TAG_NAME, 'a')  # Find the <a> tag within the <li>
        text = a_tag.text
        href = a_tag.get_attribute('href')
        title = a_tag.get_attribute('title')

        # Initialize the ng-if attribute value and epoch time
        ng_if_value = None
        epoch_time = None

        # Look for a child element with the attribute ng-if
        try:
            child_with_ng_if = a_tag.find_element(By.CSS_SELECTOR, '[ng-if]')
            ng_if_value = child_with_ng_if.get_attribute('ng-if')

            # Extract epoch time from ng-if attribute using regex
            match = re.search(epoch_pattern, ng_if_value)
            if match:
                epoch_time = int(match.group(1)) // 1000  # Convert milliseconds to seconds

        except:
            # If no child element with ng-if is found, set epoch_time to None
            epoch_time = None

        # Convert epoch time to ISO format or set to None if epoch_time is None
        iso_time = datetime.utcfromtimestamp(epoch_time).isoformat() if epoch_time else None

        # Extract match ID from href using regex
        match_id = None
        match_id_match = re.search(r'/(\d+)/', href)
        if match_id_match:
            match_id = match_id_match.group(1)

        match_details.append({
            'index': idx,
            'match_id': match_id,
            'title': title,
            'iso_time': iso_time
        })

    return match_details

# Function to scrape match commentary
def scrape_match_commentary(driver, match_id):
    url = f'https://www.cricbuzz.com/live-cricket-scores/{match_id}'
    driver.get(url)

    time.sleep(3)  # Adjust as needed

    try:
        # Find all commentary elements under ng-show="!isCommentaryRendered"
        commentary_elements = driver.find_element(By.CSS_SELECTOR, '[ng-show="!isCommentaryRendered"]').find_elements(By.TAG_NAME, "div")

        commentary = []
        for element in commentary_elements:  # Limit to last 10 commentary entries or less
            commentary.append(element.get_attribute('innerText').strip())

        return commentary[::-1]  # Reverse the commentary list

    except Exception as e:
        print(f"Error fetching commentary: {str(e)}")
        return []

# Function to run the CLI tool
def run_cli():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='CLI Tool for Cricket Match Details Scraping')
    parser.add_argument('--list', action='store_true', help='List current match details')
    parser.add_argument('--commentary', type=str, metavar='MATCH_ID', help='Show last 10 match commentaries for given match ID')
    parser.add_argument('--watch', action='store_true', help='Watch live commentary updates for given match ID every 10 seconds')

    # Parse command-line arguments
    args = parser.parse_args()

    # Set up Chrome options (optional)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome (no GUI)

    # Specify the path to the ChromeDriver executable
    webdriver_service = Service('./chromedriver')

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    try:
        # Handle CLI commands
        if args.list:
            match_details = scrape_match_details(driver)
            for match in match_details:
                print(f"{match['index']}. Match ID: {match['match_id']}, Title: {match['title']}, ISO Time: {match['iso_time']}")

        elif args.commentary:
            match_id = args.commentary
            commentary = scrape_match_commentary(driver, match_id)

            if commentary:
                print(f"Last {len(commentary)} commentaries for Match ID {match_id}:")
                for idx, comment in enumerate(commentary, start=1):
                    print(f"{comment}\n\n")
            else:
                print(f"No commentary found for Match ID {match_id}")

            # If watch flag is set, enter watch mode
            if args.watch:
                last_commentary = commentary

                while True:
                    commentary = scrape_match_commentary(driver, match_id)

                    if commentary:
                        # Print new comments since last check
                        if last_commentary:
                            new_comments = [comment for comment in commentary if comment not in last_commentary]
                            if new_comments:
                                print(f"New commentaries for Match ID {match_id}:")
                                for comment in new_comments:
                                    print(f"{comment}\n\n")

                        last_commentary = commentary

                    time.sleep(10)

        else:
            print("No valid command provided. Use --list, --commentary MATCH_ID, or --watch.")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    run_cli()
