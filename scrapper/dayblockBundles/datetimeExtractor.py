from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple

def _get_date_time(datetime_string):
    ...
    return "d", "t"

def extractDatetimeFromWebElement(h5Element) -> Tuple[str, str] | None:
    try:
        # todo : expected h5 output as below
        # ข้อมูลเริ่มต้น :: [[ 2024040512 ]] - วันที่ 05 เมษายน 2567 เวลา 19:00 น.
        date_text = h5Element.text
        i = date_text.index("-")
        date_text = date_text[i + 1:].strip()
        print(date_text)
        ret = xdate, xtime = _get_date_time(date_text)
        return ret

    except Exception as e:
        print(e)
        print("h5 something like\tข้อมูลเริ่มต้น :: [[ 2024040512 ]] - วันที่ 05 เมษายน 2567 เวลา 19:00 น.)\tNot found!")
    return None

