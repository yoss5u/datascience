import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


website_url = 'https://www.adamchoi.co.uk/teamgoals/detailed'

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off or turn it on if you want to see your script is running correctly
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver 
webdriver_service = Service("/usr/local/bin/chromedriver")

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Get page
browser.get(website_url)

# Get the button that get all the matches
# XPATH --> //TAG[@NAMETAG="TEXT TAG"]
all_matches_button = browser.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()

time.sleep(5)

# Get the list of the country that we want
# Some list have diferent functionality
list_country = browser.find_element(By.ID, 'country')
list_dropdown = Select(list_country)
list_dropdown.select_by_visible_text('Spain')
time.sleep(5)

# Get the list of the season that we want
# Some list have diferent functionality
list_season = browser.find_element(By.ID, 'season')
list_dropdown_season = Select(list_season)
list_dropdown_season.select_by_visible_text('22/23')
time.sleep(5)

# Get all the matches
games = browser.find_elements(By.TAG_NAME, 'tr')
text_games = []
for game in games:
    text_games.append(game.text)

browser.quit()
df = pd.DataFrame({'Games': text_games})
print(df)
df.to_csv('games.csv', index=False)
