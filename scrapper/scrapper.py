from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
from scrapper.datetimeExtractor import extractDatetimeFromString
from time import sleep
import pandas as pd


class Scrapper:
    def __init__(self):
        self.baseUrl = "https://hpc.tmd.go.th/pubData"

        self.driver = webdriver.Safari()

        self.driver.get(self.baseUrl)
        print("Copying data from " + self.driver.title)

        # df = self.getDateTimeCSVDataFrame()
        # # print(df)
        # print(df['csv url'])


    def release(self):
        self.driver.close()

    def getDateTimeCSVDataFrame(self):
        data = []

        try:
            p24d01_csv_a_tags = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'p24h.d01')]")
            for atag in p24d01_csv_a_tags:
                parenth5 = atag.find_element(By.XPATH, "../../../../h5")
                print(parenth5.text)
                # print(atag.text)
                date, time = extractDatetimeFromString(parenth5.text)
                csvUrl = atag.get_attribute("href")
                print(csvUrl)
                data.append([
                    date, time, csvUrl
                ])
                print()
            # print(data)
        except Exception as e:
            print(e)
            traceback.print_exc()
        if len(data) == 0:
            print("Error : Length of final dataframe should not be zero.")
            exit(0)
        
        df = pd.DataFrame(data, columns=["date", "time", "csv url"])
        return df

