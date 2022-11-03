
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from base_methods import BaseMethods
from bs4 import BeautifulSoup


class ChromeLeonBet(BaseMethods):
    ANCHOR = (By.CSS_SELECTOR,
              '#app > header > div > div > div > div > div.header-bar__right > div.header-registration > a.header-registration__button.header-registration__button--login.button.button--kind-transparent.button--height-small.button--uppercase.button--animation')
    COMPETITORS = 'sport-event-list-item-competitor__name'
    ENTIRE_TABLE = (By.XPATH, '//div[@class="group--shown"]')
    EVENT_BLOCK = 'sport-event-list-item__block'
    SCORE = 'live-progress__score-details'
    MORE_INFO = (By.XPATH, '//div[@class="sport-event-details-market-list sport-event-details-market-list--list-item"]')
    COEFFICIENT = 'sport-event-list-item-market__coefficient'
    TAB_STATS = 'sport-event-details-item sport-event-details-market-group__market'
    running: bool

    def __init__(self):
        super().__init__()
        self.all_games_ready = []

    def start_browser(self, driver):
        self.driver: webdriver.Chrome = driver
        self.driver.maximize_window()

    def run_script(self):
        self.driver.get('https://leon.bet/ru/live/soccer')
        if self.locate_visible(self.ANCHOR, 20):
            table = self.locate_element(self.ENTIRE_TABLE)
            games = self.collect_all_cards_info(table.get_attribute('innerHTML'))
            if games:
                self.all_games_ready = self.open_tab_for_each(games)

        else:
            raise TimeoutError

    def collect_all_cards_info(self, table: str) -> list:
        bf4 = BeautifulSoup(table, 'lxml')
        all_games_stats = []
        all_events = bf4.find_all('div', class_=self.EVENT_BLOCK)
        for event in all_events:
            href = event.find_next('a', href=True).get('href')

            if 'fifa-esports' not in href:
                team1, team2 = event.find_all('span', class_=self.COMPETITORS)
                score = event.find_next('span', class_=self.SCORE)
                coefficients = [coef.text for coef in event.find_all('span', class_=self.COEFFICIENT) if "+" not in coef.text]

                single_event = {'teams': [team1.text, team2.text],
                                'score': score.text if score is not None else 'Еще не начался',
                                'coef': coefficients,
                                'href': href}
                all_games_stats.append(single_event)

        return all_games_stats

    def open_tab_for_each(self, all_games: list) -> list:
        for game in all_games:
            if not self.running:
                self.driver.quit()
                self.driver.close()
            tab_button: WebElement
            try:
                _, tab_button = self.locate_elements((By.XPATH, f'//a[@href="{game["href"]}"]'))
                tab_button.click()
            except:
                continue
            if self.locate_visible(self.MORE_INFO, 15):
                time.sleep(1)
                html_extra = self.locate_element(self.MORE_INFO).get_attribute('innerHTML')
                parsed_html = BeautifulSoup(html_extra, 'lxml')
                all_tab_names = [name.text for name in parsed_html.find_all('span', 'sport-event-details-market-group__title')]
                stats_for_tab = [stats.text for stats in parsed_html.find_all('div', class_=self.TAB_STATS)]
                game['extra'] = list(zip(all_tab_names, stats_for_tab))

        return all_games





