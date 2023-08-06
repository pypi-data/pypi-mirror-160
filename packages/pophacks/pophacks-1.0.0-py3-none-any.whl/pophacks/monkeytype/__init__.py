"""pophacks. MonkeyType"""

from selenium import webdriver
from selenium.webdriver.common.by import By

import math
import time


class MonkeyType:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://monkeytype.com")

        self._prword: list = []
        self._timers: int = None

        self.driver.implicitly_wait(.1)

        # Cookie Popup
        (self.driver
            .find_element(By.ID, "cookiePopup")
            .find_element(By.CLASS_NAME, "acceptAll").click())

        self.driver.implicitly_wait(.15)

        # Words Element
        self._words = self.driver.find_element(By.ID, "words")

        self.driver.implicitly_wait(.2)

    def timerget(self) -> int:
        if self._timers is None:
            self._timers = (self.driver
                .find_element(By.CLASS_NAME, "desktopConfig")
                .find_element(By.CLASS_NAME, "time")
                .find_element(By.CLASS_NAME, "buttons")
                .find_elements(By.CLASS_NAME, "textButton"))

        for x in self._timers:
            if "active" in x.get_attribute("class").split():
                return int(x.text)

    def timerset(self, tm: int):
        if tm not in (1, 2, 3, 4):
            raise

        if self.timerget() == int([x.text for x in self._timers][tm-1]):
            return

        self._timers[tm-1].click()

    def next(self) -> str:
        """return the next letter to be typed everytime the function is called"""

        if not self._prword:
            try:
                self._prword = [
                    lr.text
                    for lr in (self._words
                        .find_element(By.CLASS_NAME, "active")
                        .find_elements(By.TAG_NAME, "letter"))
                ] + [" "]

            except Exception as e:
                print("next >None.", e); return None
        return self._prword.pop(0)

    def speedtype(self, wpm: int = 100):
        """speedtype function"""

        ct = math.ceil(wpm * 5 * self.timerget() / 60)  # req letter count
        pd = self.timerget() / ct

        print("wait delay: {}s".format(pd))

        while (ky := self.next()) is not None and ct > 0:
            try:
                tm = time.perf_counter()

                self._words.send_keys(ky)
                ct -= len(ky)

                sleeptime = pd - (time.perf_counter() - tm) - .015
                time.sleep(sleeptime if sleeptime > 0 else 0)

            except Exception as e:
                print("speedtype.", e)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kw):
        self.driver.close()
        self.driver.quit()
