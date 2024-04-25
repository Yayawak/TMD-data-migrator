from selenium import webdriver
from scrapper.dayblockBundles.dayblockManager import DayblockManager
from selenium.webdriver.common.by import By
import traceback


class Scrapper:
    def __init__(self):
        self.baseUrl = "https://hpc.tmd.go.th/pubData"

        self.driver = webdriver.Safari()

        self.driver.get(self.baseUrl)

        print("Copying data from " + self.driver.title)

        # self.find_day_blocks()
        # self.dayBlockManager = DayblockManager(self.driver)

        try:
            p24d01_csv_a_tags = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'p24h.d01')]")
            for atag in p24d01_csv_a_tags:
                print(atag.text)
        except Exception as e:
            print(e)
            traceback.print_exc()
            


        self.driver.close()
    
