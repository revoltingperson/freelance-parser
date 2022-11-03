import os.path
import time
from sys import platform

from PySide6.QtCore import QThread, Signal, Slot, QObject, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (QHBoxLayout, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget, QLabel, QMessageBox, QFrame)
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from script_instance import ChromeLeonBet
from settings import DEBUG, logger
from team_element import TeamElement
from ui_main_frame_sports_event import Ui_Form

if platform == "win32":
    from subprocess import CREATE_NO_WINDOW


class MainWidget(QWidget, Ui_Form):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.setupUi(self)
        ic = os.path.join('ico', 'favicon-228.ico')
        self.setWindowIcon(QIcon(ic))
        self.setWindowTitle('Инфоборд')
        self.start.clicked.connect(self.start_script)
        self.stop.clicked.connect(self.stop_browser)
        self.stop.setDisabled(True)
        self.status_label = QLabel()
        self.horizontalLayout.addWidget(self.status_label)

    def start_script(self):
        self.thread = QThread()
        self.browser_thread = BrowserThread()
        self.stop.setDisabled(False)
        self.start.setDisabled(True)
        self.browser_thread.br.running = True
        self.browser_thread.moveToThread(self.thread)
        self.thread.started.connect(self.browser_thread.run)
        self.browser_thread.finished.connect(self.process_result_from_thread)
        self.browser_thread.finished.connect(self.thread.quit)
        self.browser_thread.finished.connect(self.browser_thread.deleteLater)
        self.browser_thread.driver_loading.connect(self.notify)

        self.thread.start()

    def stop_browser(self):
        self.stop.setDisabled(True)
        self.start.setDisabled(False)
        self.browser_thread.br.running = False
        self.status_label.setText('Бот остановлен')

    @Slot(str)
    def notify(self, message):
        self.status_label.setText(message)

    @Slot(list)
    def process_result_from_thread(self, events):
        for item in range(self.main_layout.count()):
            item = self.main_layout.itemAt(0)
            item.widget().setVisible(False)
            self.main_layout.removeItem(item)

        for event in events:
            stats_for_category: str
            event_window = TeamElement()

            event_window.score.setText(event['score'])
            event_window.teams.setText(" vs ".join(event['teams']))
            try:
                extra = event['extra']
            except KeyError:
                continue

            for category, stats_for_category in extra:
                font = QFont()
                font.setPointSize(10)
                font.setItalic(True)

                layout_vertical_categories = QVBoxLayout()
                horizontal_category = QHBoxLayout()
                spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
                category_label = QLabel()
                category_label.setFont(font)
                font.setItalic(False)
                category_label.setAlignment(Qt.AlignmentFlag.AlignTop)
                numbers_label = QLabel()
                numbers_label.setFont(font)
                numbers_label.setMaximumWidth(700)
                category_label.setText(category + ":")

                if category != 'Фора':
                    numbers_label.setText(stats_for_category.replace(' Б', '\nБ'))
                else:
                    numbers_label.setText(stats_for_category.replace(' 1 ', '\n1 '))

                horizontal_category.addWidget(category_label)
                horizontal_category.addWidget(numbers_label)
                layout_vertical_categories.addLayout(horizontal_category)
                horizontal_category.addItem(spacer)
                event_window.verticalLayout_2.addLayout(layout_vertical_categories)

            event_window.setStyleSheet('QFrame#Form {border: 1px solid pink; box-shadow: 10px 5px 5px red; background-color: white} QFrame { font-family: Sans-serif }')


            self.main_layout.addWidget(event_window)


class BrowserThread(QObject):
    finished = Signal(list)
    br = ChromeLeonBet()
    driver_loading = Signal(str)

    def run(self):
        # for testing
        # self.finished.emit([{'coef': ['2.40', '1.90', '7.20'], 'extra': [('Победитель', '1 2.40 X 1.90 2 7.20 '), ('Тотал', 'Больше (0.5) 1.71 Меньше (0.5) 2.03 Больше (1.5) 4.41 Меньше (1.5) 1.17 '), ('Тотал гостей', 'Больше (0.5) 3.97 Меньше (0.5) 1.21 '), ('Двойной исход', '1X 1.06 12 1.80 Х2 1.50 '), ('Тотал хозяев', 'Больше (0.5) 2.06 Меньше (0.5) 1.68 Больше (1.5) 6.30 Меньше (1.5) 1.08 ')], 'href': '/ru/bets/soccer/russia/pfl-group-3/1970324840969068-ska-khabarovsk-2-zenit-penza', 'score': ' (0:0; 0:0) ', 'teams': [' СКА-Хабаровск 2 ', ' Зенит Пенза ']}, {'coef': ['1.22', '6.20', '8.50'], 'extra': [('Победитель', '1 1.22 X 6.20 2 8.50 '), ('Двойной исход', '1X 1.02 12 1.07 Х2 3.77 '), ('Азиатская фора', '1 (-2.25) 1.88 2 (+2.25) 1.79 '), ('Кто забьет 1-й гол', '1 1.22 X 18.00 2 4.42 '), ('Результат не включая ничью', '1 1.06 2 7.30 '), ('Тотал', 'Больше (1.5) 1.11 Меньше (1.5) 5.30 Больше (2.5) 1.33 Меньше (2.5) 2.96 Больше (3.5) 1.73 Меньше (3.5) 1.95 Больше (5.5) 4.67 Меньше (5.5) 1.14 ')], 'href': '/ru/bets/soccer/india/delhi-senior-division/1970324840970927-central-industrial-security-force-bom-ahbab', 'score': ' (0:0) ', 'teams': [' Central Industrial Security Force ', ' Ахбаб ']}, {'coef': ['2.10', '5.90', '2.25'], 'extra': [('Победитель', '1 2.10 X 5.90 2 2.25 '), ('Фора', '1 (-1) 2.74 2 (+1) 1.42 1 (0) 1.81 2 (0) 1.93 1 (+1) 1.36 2 (-1) 3.00 '), ('Тотал хозяев', 'Больше (3.5) 1.96 Меньше (3.5) 1.75 '), ('Двойной исход', '1X 1.53 12 1.08 Х2 1.61 '), ('Тотал', 'Больше (5.5) 1.34 Меньше (5.5) 3.09 Больше (6) 1.45 Меньше (6) 2.63 Больше (6.5) 1.71 Меньше (6.5) 2.07 Больше (7) 2.00 Меньше (7) 1.75 Больше (7.5) 2.35 Меньше (7.5) 1.55 Больше (8) 3.05 Меньше (8) 1.35 '), ('Тотал гостей', 'Больше (3.5) 2.05 Меньше (3.5) 1.69 ')], 'href': '/ru/bets/soccer/egypt/cairo-development-league/1970324840969818-al-abtal-el-madina', 'score': 'Еще не начался', 'teams': [' Аль-Абталь ', ' Аль-Мадина ']}, {'coef': ['2.21', '3.50', '2.84'], 'extra': [('Победитель', '1 2.21 X 3.50 2 2.84 '), ('Фора', '1 (-1.5) 3.95 2 (+1.5) 1.22 1 (-1) 3.33 2 (+1) 1.30 1 (0) 1.68 2 (0) 2.11 1 (+1) 1.17 2 (-1) 4.64 1 (+1.5) 1.13 2 (-1.5) 5.40 '), ('Тотал', 'Больше (0.5) 1.03 Меньше (0.5) 9.90 Больше (1.5) 1.22 Меньше (1.5) 3.95 Больше (2) 1.35 Меньше (2) 3.03 Больше (2.5) 1.68 Меньше (2.5) 2.10 Больше (3) 2.17 Меньше (3) 1.64 Больше (3.5) 2.77 Меньше (3.5) 1.41 Больше (4.5) 4.47 Меньше (4.5) 1.18 Больше (5.5) 8.00 Меньше (5.5) 1.06 '), ('Двойной исход', '1X 1.35 12 1.23 Х2 1.54 '), ('Азиатская фора', '1 (-0.25) 1.94 2 (+0.25) 1.81 '), ('Обе команды забьют', 'Да 1.59 Нет 2.26 ')], 'href': '/ru/bets/soccer/india/manipur-state-league/1970324840970760-young-physiques-union-nesu-fc', 'score': 'Еще не начался', 'teams': [' Янг Физикс Юнион ', ' НЕСУ ']}, {'coef': ['16.00', '7.60', '1.12'], 'extra': [('Победитель', '1 16.00 X 7.60 2 1.12 '), ('Двойной исход', '1X 4.90 12 1.01 -- -- '), ('Азиатская фора', '1 (+2.25) 1.99 2 (-2.25) 1.76 '), ('Победитель противостояния', '1 8.70 2 1.06 '), ('Фора', '1 (0) 9.00 2 (0) 1.04 1 (+1) 4.26 2 (-1) 1.20 1 (+1.5) 2.72 2 (-1.5) 1.42 1 (+2) 2.13 2 (-2) 1.67 1 (+2.5) 1.69 2 (-2.5) 2.09 1 (+3) 1.41 2 (-3) 2.77 1 (+3.5) 1.30 2 (-3.5) 3.34 1 (+4) 1.18 2 (-4) 4.45 '), ('Тотал', '-- -- Меньше (0.5) 18.70 Больше (1.5) 1.11 Меньше (1.5) 6.00 Больше (2.5) 1.38 Меньше (2.5) 2.88 Больше (3) 1.56 Меньше (3) 2.32 Больше (3.5) 1.90 Меньше (3.5) 1.83 Больше (4) 2.43 Меньше (4) 1.52 Больше (4.5) 2.88 Меньше (4.5) 1.38 Больше (5) 3.81 Меньше (5) 1.24 Больше (5.5) 4.45 Меньше (5.5) 1.18 ')], 'href': '/ru/bets/soccer/thailand/thailand-fa-cup/1970324840969135-chanthaburi-fc-chiangrai-united', 'score': 'Еще не начался', 'teams': [' Chanthaburi FC ', ' Чианграй Юнайтед ']}, {'coef': ['1.80', '3.74', '3.76'], 'extra': [('Победитель', '1 1.80 X 3.74 2 3.76 '), ('Двойной исход', '1X 1.17 12 1.21 Х2 1.93 '), ('Азиатская фора', '1 (-0.75) 1.97 2 (+0.75) 1.78 '), ('Победитель противостояния', '1 1.41 2 2.84 '), ('Фора', '1 (-3.5) 9.20 2 (+3.5) 1.04 1 (-2.5) 5.20 2 (+2.5) 1.14 1 (-2) 4.34 2 (+2) 1.19 1 (-1.5) 2.77 2 (+1.5) 1.41 1 (-1) 2.34 2 (+1) 1.56 1 (0) 1.45 2 (0) 2.61 1 (+1.5) 1.08 2 (-1.5) 6.90 '), ('Тотал', 'Больше (1.5) 1.22 Меньше (1.5) 3.95 Больше (2) 1.33 Меньше (2) 3.14 Больше (2.5) 1.72 Меньше (2.5) 2.05 Больше (3) 2.12 Меньше (3) 1.67 Больше (3.5) 2.59 Меньше (3.5) 1.46 Больше (4) 3.75 Меньше (4) 1.25 Больше (4.5) 4.45 Меньше (4.5) 1.18 ')], 'href': '/ru/bets/soccer/thailand/thailand-fa-cup/1970324840970857-khonkaen-province-banbueng-f-c', 'score': 'Еще не начался', 'teams': [' Кхонкэн ', ' Банбуенг ']}, {'coef': ['2.05', '3.29', '3.35'], 'extra': [('Победитель', '1 2.05 X 3.29 2 3.35 '), ('Двойной исход', '1X 1.25 12 1.25 Х2 1.66 '), ('Азиатская фора', '1 (-0.25) 1.88 2 (+0.25) 1.85 '), ('Победитель противостояния', '1 1.58 2 2.35 '), ('Фора', '1 (-3.5) 10.70 2 (+3.5) 1.02 1 (-2.5) 6.10 2 (+2.5) 1.10 1 (-2) 5.20 2 (+2) 1.14 1 (-1.5) 3.12 2 (+1.5) 1.33 1 (-1) 2.52 2 (+1) 1.48 1 (0) 1.51 2 (0) 2.45 1 (+1.5) 1.08 2 (-1.5) 6.90 '), ('Тотал', 'Больше (0.5) 1.06 Меньше (0.5) 8.10 Больше (1.5) 1.33 Меньше (1.5) 3.13 Больше (2) 1.52 Меньше (2) 2.43 Больше (2.5) 1.97 Меньше (2.5) 1.78 Больше (3) 2.63 Меньше (3) 1.45 Больше (3.5) 3.24 Меньше (3.5) 1.31 Больше (4) 4.61 Меньше (4) 1.17 Больше (4.5) 5.90 Меньше (4.5) 1.11 ')], 'href': '/ru/bets/soccer/thailand/thailand-fa-cup/1970324840969136-kabin-united-fc-nakhon-ratchasima-united', 'score': 'Еще не начался', 'teams': [' Саймит Кабин ', ' Накхон Ратчасима ']}])
        try:
            options = webdriver.ChromeOptions()
            if not os.path.exists('browser'):
                self.driver_loading.emit('Подождите, загружаю драйвер')
                ChromeDriverManager(path='browser').install()
            if not DEBUG:
                options.add_argument('--headless')
                options.add_argument("window-size=1920,1080")

            chrome_paths = ""
            for root, dirs, files in os.walk("browser", topdown=False):
                for name in files:
                    chrome_path = os.path.join(root, name)
                    if 'chromedriver.exe' in chrome_path:
                        chrome_paths = chrome_path
                for name in dirs:
                    chrome_path = os.path.join(root, name)
                    if 'chromedriver.exe' in chrome_path:
                        chrome_paths = chrome_path

            service = ChromeService(executable_path=chrome_paths)
            service.HideCommandPromptWindow = True
            service.service_args = ["hide_console", ]
            if platform == "win32":
                service.creationflags = CREATE_NO_WINDOW

            self.br.start_browser(
                webdriver.Chrome(service=service, options=options))
            while self.br.running:
                self.driver_loading.emit('Работаю. Записываю данные из браузера')
                self.br.run_script()
                self.finished.emit(self.br.all_games_ready)
                time.sleep(10)
            else:
                self.br.driver.quit()
        except Exception as e:
            if self.br.running:
                self.driver_loading.emit('Ошибка, проверьте логи')
                logger.exception(e)
                self.br.driver.save_screenshot(os.path.join('errors', 'screenshot.png'))
            self.br.running = False
