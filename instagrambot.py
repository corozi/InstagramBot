import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from decorators import *

import os

import time

import openpyxl


# global lists
sneakers = []
lifestyle_items = []
electronics = []
cars = []
others = []
post_link_list = []


# keyword matches
sneakers_matches = ['sneaker', 'nike', 'adidas']
lifestyle_items_matches = ['perfume', 'watch', 'clothe']
electronics_matches = ['iphone', 'ipad', 'phone', 'samsung', 'huawei', 'mobile']
cars_matches = ['car', 'sedan']


# global variables
likes_count = 0
views_count = 0
post_link_list_index = 0


# error_matches
error_matches = ['Sorry, something went wrong' ]
temporary_ban_string = 'Please wait a few minutes before you try again'


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


class Authentication:
    def __init__(self, username , password):
        self.username = username
        self.password = password

    def login(self):
        driver.get('https://www.instagram.com/accounts/login/')
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        login_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button'))
        )
        username.send_keys(self.username)
        password.send_keys(self.password)
        login_btn.click()

    @Decorators.time_lapsed_decorator
    def search_giveaway(self):
        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
        )
        search.send_keys("#giveaway")
        search.send_keys(Keys.RETURN)


class Extraction:

    def __init__(self):
        self.hashtag_link_list = []

    def search_giveaway(self):
        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
        )
        search.send_keys("#giveaway")
        search.send_keys(Keys.RETURN)

    def get_hashtags(self):
        hashtags_search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "yCE8d  "))
        )

        for hashtag in hashtags_search_results:
            hashtag_link = hashtag.get_attribute('href')
            self.hashtag_link_list.append(hashtag_link)

    def get_post_links(self):
        post_board = WebDriverWait(driver, 10).until(
             EC.presence_of_element_located((By.CLASS_NAME, "KC1QD"))
         )
        posts_a = post_board.find_elements_by_tag_name("a")

        for post_a in posts_a:
            post_link = post_a.get_attribute("href")
            post_link_list.append(post_link)

    def extract_and_sort_link_body_text(self):

        global likes_count
        global views_count
        global post_link_list_index

        def sort_post_types(post_text, post_link):

            # calling global lists
            global sneakers
            global lifestyle_items
            global electronics
            global cars
            global others

            # calling global matching keyword lists
            global sneakers_matches
            global lifestyle_items_matches
            global electronics_matches
            global cars_matches

            all_matches = sneakers_matches + lifestyle_items_matches + electronics_matches + cars_matches

            for match in all_matches:

                if match in post_text:

                    if match in sneakers_matches:
                        sneakers.append(post_link)

                    elif match in lifestyle_items_matches:
                        lifestyle_items.append(post_link)

                    elif match in electronics_matches:
                        electronics.append(post_link)

                    elif match in cars_matches:
                        cars.append(post_link)

                else:
                    others.append(post_link)

        def check_likes_and_views():

            global likes_count
            global views_count

            likes_or_views = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div'))
            )

            likes_or_views_text = likes_or_views.text

            if 'like' in likes_or_views_text:   # classify as like post
                likes_text = likes_or_views_text

                if 'Be the first to' in likes_text:                          # if not no likes on post
                    likes_count = 0

                elif likes_text == '1 like':
                    likes_count = 1

                else:
                    likes_count = likes_text[:-6]

                    if likes_count != '' and likes_count != ' ':

                        if ',' in likes_count:

                            likes_count = likes_count.replace(',', '')        # there are commas

                        likes_count = int(float(likes_count))

                    else:
                        print('raised likes_count error')
                        likes_count = 0

                print(f'{post_link_list_index + 1}. {likes_count} likes')

            elif 'view' in likes_or_views_text:        # classify as a video
                views_text = likes_or_views_text

                if 'views' in views_text:                         # more than 1 view on video

                    global views_count
                    views_count = views_text[:-6]

                    if views_count != '' and views_count != ' ':

                        if ',' in views_count:
                            views_count = views_count.replace(',', '')

                        views_count = int(float(views_count))

                elif views_text == '1 view':                      # only 1 view
                    views_count = 1

                else:
                    views_count = 0

                print(f'{post_link_list_index + 1}. {views_count} views')

        while post_link_list_index != (len(post_link_list)):                   # while not end of list
            post_link = post_link_list[post_link_list_index]
            driver.get(post_link)

            page_source = driver.page_source

            if "this page isn't available" in page_source:

                print("this page isn't available")

            elif 'Please wait a few minutes before you try again' in page_source:

                print('temporary ban by Instagram')
                driver.stop_client()

            elif 'C4VMK' not in page_source:

                print('post has no text / garbage post')

            elif 'Sorry, something went wrong' in page_source:

                print('unknown error has occurred')

            else:
                check_likes_and_views()

                if likes_count >= 100 or views_count >= 100:

                    post_body_div = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "C4VMK"))
                    )
                    post_text1 = post_body_div.text

                    sort_post_types(post_text1, post_link)

            post_link_list_index += 1

class Spreadsheets:
    def load_workbook(self):
        wb = openpyxl.load_workbook('post_links_database.xlsx')



@Decorators.time_lapsed_decorator
def main():
    ig_bot = Authentication('allgiveawayrn', 'WEDJUN_24')
    ig_bot.login()
    extraction = Extraction()
    extraction.search_giveaway()
    extraction.get_hashtags()

    for hashtag_link in extraction.hashtag_link_list:
        driver.get(hashtag_link)
        extraction.get_post_links()

    print(post_link_list)
    print(f'there are : {len(post_link_list)} post links')

    extraction.extract_and_sort_link_body_text()

    print(f'sneakers = {sneakers}')
    print(f'lifestyle_items = {lifestyle_items} ')
    print(f'electronics = {electronics}')
    print(f'cars = {cars}')
    print(f'others = {others}')

    useful_posts = sneakers + lifestyle_items + electronics + cars + others
    print(f'{len(useful_posts)} useful posts')


if __name__ == '__main__':
    main()


