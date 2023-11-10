import pyautogui as pg
from time import sleep
from env import env
from random import randint
from validators import ValidationError, url
from pathlib import Path


class VisitorBot:

    """
    Set time counters
    """

    def __init__(self):
        self.counter = 0
        self.wait_until = 0

    def get_file(self, file_name: str) -> str:
        path = Path(__file__).with_name(file_name)
        return str(path.absolute())

    """
    Run general script
    """

    def run(self) -> None:
        if self.open_browser() is False:
            return
        sleep(3)
        pg.hotkey('ctrl', 't')
        search = set(env['search'])
        while len(search) > 0:
            is_website = self.search(search.pop())
            sleep(3)
            if is_website is True:
                self.visit_page(is_website=True)
                return
            for i in range(0, randint(1, int(env['visits_limit']) + 1)):
                self.visit_page()

    """
    find next link on search page, visit site, scroll and go back
    """

    def visit_page(self, is_website=False):
        pg.hotkey('ctrl', 'f')
        pg.write('http')
        if is_website is True:
            pg.hotkey('enter')
        pg.hotkey('ctrl', 'enter')
        # checking do we left search page
        while pg.locateCenterOnScreen(self.get_file(env['search_page_marker'])) is not None:
            sleep(1)
        if is_website is False:
            self.wait(init=True)
            while self.wait() is False:
                pg.scroll(randint(-20, -1))
        else:
            self.rand_wait(init=True)
            while self.rand_wait() is False:
                pg.scroll(randint(-30, 30))
        pg.hotkey('alt', 'left')

    """
    Open browser based on icon
    """

    def open_browser(self) -> bool:
        start = pg.locateCenterOnScreen(
            self.get_file(env['browser_icon'])
        )
        if start is None:
            return False
        pg.moveTo(start)
        pg.click()
        return True

    """
    focus of search bar and input keyword 
    """

    def search(self, search: str) -> bool:
        is_website = not isinstance(url(search), ValidationError)
        pg.hotkey('ctrl', 'k')
        if is_website:
            search = "find " + search
        pg.write(search)
        pg.hotkey('enter')
        return is_website

    """
    wait specified time
    """

    def wait(self, init=False):
        if init is True:
            self.counter = 0
            self.wait_until = randint(
                int(env['visit_time_from']),
                int(env['visit_time_to'])
            )
            return False
        sleep(1)
        self.counter += 1
        if self.counter == self.wait_until:
            return True
        return False

    def rand_wait(self, init=False):
        if init is True:
            self.counter = 0
            self.wait_until = randint(
                int(env['specific_page_visit_time_from']),
                int(env['specific_page_visit_time_to'])
            )
            return False
        sleep_time = randint(1, env['max_rand_scroll_delay'])
        sleep(sleep_time)
        self.counter += sleep_time
        if self.counter >= self.wait_until - env['max_rand_scroll_delay']:
            return True
        return False
