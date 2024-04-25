from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
import traceback
from time import sleep



# NOTE need driver for watings
def extractIndualvidualCsv(day_block: WebElement, driver):
    try:
        # sleep(1)
        clickable_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            day_block
        ))
        clickable_element.click()
    except Exception as ee:
        print("can not click this element")
        print(ee)
        traceback.print_exc()

    return "file"