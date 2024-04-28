from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple

def _get_date_time(datetime_string:str):
    ...
    ss = datetime_string.split(" ")
    print(ss)
    date_of_month = ss[1]
    month = ss[2]
    year = ss[3]
    time = ss[5]
    # return "d", "t"
    return f"{date_of_month}-{month}-{year}", time

def extractDatetimeFromString(date_text) -> Tuple[str, str]:
    # todo : expected h5 output as below
    # ข้อมูลเริ่มต้น :: [[ 2024040512 ]] - วันที่ 05 เมษายน 2567 เวลา 19:00 น.
    i = date_text.index("-")
    date_text = date_text[i + 1:].strip()
    # print(date_text)
    ret = xdate, xtime = _get_date_time(date_text)
    return ret

