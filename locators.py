import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class InstagramLocators:
    class LoginPageLocators:
        username_input_element = (By.NAME, "username")
        password_input_element = (By.NAME, "password")
        login_button_element = (By.XPATH, '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')

    class HomePageLocators:
        search_bar_element = (By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        giveaway_search_element = (By.XPATH, '// *[ @ id = "react-root"] / section / nav / div[2] / div / div / div[2] / div[2] / div[2] / div / a[1] / div')

    class SearchResultsPageLocators:
        pass


class GoogleChromeLocators:
    class SearchPageLocators:

        pass
    class SearchResultsLocators:
        pass
