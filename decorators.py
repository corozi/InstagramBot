import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import os
import time


class Decorators:
    def time_lapsed_decorator(function):
        def wrapper():
            start = time.time()
            function()
            end = time.time()
            duration = end - start

            minutes = str(int(duration) // 60)
            second_list = str(duration).split('.')

            front_part_seconds = second_list[0]
            back_part_seconds = second_list[1]

            seconds = int(front_part_seconds) % 60

            print(f'{minutes} minutes {seconds}.{back_part_seconds} seconds')
        return wrapper






