from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
# from dayblockBundles.datetimeExtractor import extractDatetimeFromWebElement
# from dayblockBundles.csvExtractor import extractIndualvidualCsv
from datetimeExtractor import extractDatetimeFromWebElement
from csvExtractor import extractIndualvidualCsv
import traceback

class DayblockManager:
    def __init__(self, driver:webdriver):
        self.driver = driver

        dayblocks = self.find_day_blocks()
        self.iterate_open_each_day_blocks(dayblocks)
    

    def iterate_open_each_day_blocks(self, day_blocks: List[WebElement]):

        for b in day_blocks:
            # ---------------------------------------------------------------------------- #
            #                             GET date time string                             #
            # ---------------------------------------------------------------------------- #
            
            h5 = b.find_element(By.TAG_NAME, "h5")
            # xdate, xtime = extractDatetimeFromWebElement(h5)
            out = extractDatetimeFromWebElement(h5)
            if out is not None:
                xdate, xtime = out
                print(out)
            # ---------------------------------------------------------------------------- #
            #                                 GET csv file                                 #
            # ---------------------------------------------------------------------------- #
            csv = extractIndualvidualCsv(b, self.driver)


    def find_day_blocks(self) -> List[WebElement] | None:
        blocks = None
        try:
            # class_name_to_find = "w3-container w3-white w3-card w3-margin"
            blocks = self.driver.find_elements(By.XPATH,
                f"//div[contains(@class, 'w3-container') and contains(@class, 'w3-white') and contains(@class, 'w3-card') and contains(@class, 'w3-margin')]"
            )
            blocks.reverse()

        except Exception as e:
            print(e)
            print("not found day-blocks -> exiting program")
            exit(1)
        return blocks