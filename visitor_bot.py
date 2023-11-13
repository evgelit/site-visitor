import pyautogui as pg
from pyautogui import ImageNotFoundException
from time import sleep
from env import env
from random import randint, uniform


class VisitorBot:

    """
    Set target page
    """
    def __init__(self):
        pg.useImageNotFoundException()
        self.target_page = env['target_page'].rstrip('/')

    """
    Run general script
    """
    def run(self) -> None:
        pg.getWindowsWithTitle("Chrome")[0].activate()
        sleep(3)
        pg.moveTo(500, 500)
        pg.hotkey('ctrl', 't')
        search = set(env['search'])
        while len(search) > 0:
            self.search(search.pop())
            if self.is_loaded(30) is False:
                continue
            for i in range(0, randint(1, int(env['visits_limit']) + 1)):
                self.visit_random_page()
                sleep(uniform(0.8, 1.1))
            for i in range(0, 20):
                pg.keyDown('pgdn')
                sleep(uniform(0.3, 0.5))
            if self.visit_target_page() is True:
                return

    """
    visit random page from keywords search
    """
    def visit_random_page(self) -> None:
        pg.hotkey('ctrl', 'f')
        pg.write('http', 0.1)
        _iter = randint(1, 10)
        while _iter > 0:
            pg.press("enter")
            iter -= 1
        pg.hotkey('ctrl', 'enter')
        if self.is_loaded(30) is False:
            pg.hotkey('alt', 'left')
            return
        wait = self.wait(
            wait_from=int(env['visit_time_from']),
            wait_to=int(env['visit_time_to']),
            step_from=0.8,
            step_to=1.1
        )
        while next(wait) is False:
            pg.press("pgdn")
        pg.hotkey('alt', 'left')
        return

    """
    attempt to find target page
    """
    def visit_target_page(self) -> bool:
        pg.hotkey('ctrl', 'f')
        pg.write(self.target_page, 0.1)
        pg.hotkey('ctrl', 'enter')
        if self.is_loaded() is False:
            return False
        wait = self.wait(
            wait_from=int(env['target_page_visit_time_from']),
            wait_to=int(env['target_page_visit_time_to']),
            step_from=1,
            step_to=int(env['max_rand_scroll_delay'])
        )
        while next(wait) is False:
            pg.press(("pgdn", "pgup")[randint(0, 1)])
        pg.hotkey('alt', 'left')
        return True

    """
    focus of search bar and input keyword 
    """
    def search(self, search: str) -> None:
        pg.hotkey('ctrl', 'k')
        pg.write(search, uniform(0.1, 0.3))
        pg.hotkey('enter')

    """
    wait specified time
    """
    def wait(self, wait_from, wait_to, step_from, step_to) -> bool:
        counter = 0
        wait_until = randint(wait_from, wait_to)
        sleep_time = uniform(step_from, step_to)
        while counter < wait_until - sleep_time:
            sleep_time = uniform(step_from, step_to)
            sleep(sleep_time)
            counter += sleep_time
            yield False
        yield True

    """
    check is page loaded
    """
    def is_loaded(self, max_wait=5) -> bool:
        img = pg.screenshot(region=(100, 100, 300, 300))
        try:
            wait = 0
            while wait < max_wait:
                pg.locateOnScreen(img)
                sleep(uniform(0.8, 1.1))
                wait += 1
        except ImageNotFoundException:
            return True
        return False
