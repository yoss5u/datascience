import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

'''This class work for initizalice selenium correctly'''
class WebScraping():
    def __init__(self) -> None:
        self.WEB_SITE_URL = 'https://www.adamchoi.co.uk/teamgoals/detailed'
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless') # Ensure GUI is off or turn it on if you want to see your script is running correctly
        self.chrome_options.add_argument('--no-sandbox')
        self.WEB_DRIVER_SERVICE = Service("/usr/local/bin/chromedriver")
        self.browser = webdriver.Chrome(service=self.WEB_DRIVER_SERVICE, options=self.chrome_options)
        self.data = []

    def initializeGetData(self):
        self.browser.get(self.WEB_SITE_URL)
        all_matches_button = self.browser.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
        all_matches_button.click()
        time.sleep(5)

    '''Get what country league you want'''
    def leagueData(self, country):
        list_country = self.browser.find_element(By.ID, 'country')
        list_dropdown = Select(list_country)
        list_dropdown.select_by_visible_text(country)
        time.sleep(5)

    '''Get what season you want'''
    def seasonData(self, season):
        list_season = self.browser.find_element(By.ID, 'season')
        list_dropdown_season = Select(list_season)
        list_dropdown_season.select_by_visible_text(season)
        time.sleep(5)

    '''Get all the games and return a array with every game with the next format [14-08-2022 Almeria 1 - 2 Real Madrid]'''
    def getData(self):
        games = self.browser.find_elements(By.TAG_NAME, 'tr')
        for game in games:
            self.data.append(game.text)
        return self.data

    '''Turn off the selenium'''
    def quitBrowser(self):
        time.sleep(5)
        self.browser.quit()


'''This clase help to clean al data in a dataframe and then save as a CVS file'''
class CleanningData():
    def __init__(self, data) -> None:
        self.data = data
        self.df = pd.DataFrame(columns = ['Date', 'Home Team', 'Away Team', 'Home Team Goals', 'Away Team Goals', 'Home Team Result', 'Away Team Result', 'Home Team Points', 'Away Team Points'])

    def transformDataToDataFrame(self):
        dates = []
        home_teams = []
        away_teams = []
        home_goals = []
        away_goals = []
        home_result = []
        away_result = []
        home_points = []
        away_points = []

        for game in self.data:
            dates.append(game[0:10])
            match_home_team = re.search(r'\d{2}-\d{2}-\d{4}\s+(\D+)', game)
            match_away_team = re.search(r'\s(\D+)$', game)
            match_home_goals = re.search(r'\s(\d+)\s', game)
            match_away_goals = re.search(r'(\d+)\s\D+$', game)

            if match_home_team and match_away_team and match_home_goals and match_away_goals:
                home_teams.append(match_home_team.group(1))
                away_teams.append(match_away_team.group(1))
                home_goals.append(match_home_goals.group(1))
                away_goals.append(match_away_goals.group(1))

                if int(match_home_goals.group(1)) > int(match_away_goals.group(1)):
                    home_result.append('W')
                    away_result.append('L')
                    home_points.append(3)
                    away_points.append(0)
                elif int(match_home_goals.group(1)) < int(match_away_goals.group(1)):
                    home_result.append('L')
                    away_result.append('W')
                    home_points.append(0)
                    away_points.append(3)
                else:
                    home_result.append('D')
                    away_result.append('D')
                    home_points.append(1)
                    away_points.append(1)

        self.df['Date'] = dates
        self.df['Home Team'] = home_teams
        self.df['Away Team'] = away_teams
        self.df['Home Team Goals'] = home_goals
        self.df['Away Team Goals'] = away_goals
        self.df['Home Team Result'] = home_result
        self.df['Away Team Result'] = away_result
        self.df['Home Team Points'] = home_points
        self.df['Away Team Points'] = away_points

    def transformToCSV(self, name):
        self.df.to_csv(name, index=False)



games_scrapping = WebScraping()
games_scrapping.initializeGetData()
games_scrapping.leagueData('Spain')
games_scrapping.seasonData('22/23')
games_scrapping_data = games_scrapping.getData()
games_scrapping.quitBrowser()

final_data = CleanningData(games_scrapping_data)
final_data.transformDataToDataFrame()
final_data.transformToCSV('allgameslaliga.csv')