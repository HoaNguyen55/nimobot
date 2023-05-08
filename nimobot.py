# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

import time
import os
import random
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--waitlongtime', type=int, default=10, help='Wait long time. Default is 10')
parser.add_argument('--waitshorttime', type=int, default=5, help='Wait short time. Default is 5')
parser.add_argument('--opentabnum', type=int, default=10, help='Number of tabs to open. Default is 10')
parser.add_argument('--username', type=str, required='true', help='User input. This parameter is required')
parser.add_argument('--password', type=str, required='true', help='Password input. This parameter is required')
parser.add_argument('--headless', type=str, default='true', help='Run Chrome in headless mode. Default is true')
parser.add_argument('--nonlogin', type=str, default='false', help='Choose NOT to login account. Default is false')
parser.add_argument('--url', type=str, default='https://www.nimo.tv/lives', help='Website URL. Default is https://www.nimo.tv/lives')
parser.add_argument('--urlonlyset', type=str, default='false', help='Use specific URL. Default is false')
parser.add_argument('--specificurl', type=str, default='', help='Specific URL. Default is empty string')
parser.add_argument('--egg', type=str, default='false', help='Collect eggs. Default is false')

args = parser.parse_args()


class NimoTVBot:
    def __init__(self, username, password, open_tab_num,
                 wait_short_time, wait_long_time,
                 url, headless, nonlogin, urlonlyset, specificurl, egg):
        self.username = username
        self.password = password
        self.open_tab_num = open_tab_num
        self.wait_short_time = wait_short_time
        self.wait_long_time = wait_long_time
        self.url = url
        self.headless = headless
        self.nonlogin = nonlogin
        self.urlonlyset = urlonlyset
        self.specificurl = specificurl
        self.egg = egg
        self.driver = None
        self.main_window = None

    def setup_driver(self):
        options = Options()
        if self.headless.lower() == 'true':
            options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.url)
        self.main_window = self.driver.current_window_handle

    def login(self):
        wait = WebDriverWait(self.driver, self.wait_short_time)
        login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(.,"Login")]')))
        login_button.click()
        phone_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="c3-pl c2 bc10 phone-number-input n-as-of-hidden"]')))
        phone_input.send_keys(self.username)
        pass_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="c3-pl c2 bc10"]')))
        pass_input.send_keys(self.password)
        pass_input.send_keys(Keys.ENTER)
        time.sleep(self.wait_short_time)
        try:
            phone_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@class="c3-pl c2 bc10 phone-number-input n-as-of-hidden"]')))
        except TimeoutException:
            print("Đăng nhập thành công")
        else:
            print("Đăng nhập không thành công, vui lòng kiểm tra lại tài khoản hoặc do Nimo phát hiện bạn đã đăng nhập quá nhiều lần")

    def scrape(self):
        temp_link_list = []
        temp_name_list = []
        random.seed(int(time.time()))

        time.sleep(self.wait_long_time)

        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        with open("file_soup.html", 'w', encoding="utf-8") as f:
            f.write(soup.prettify())

        os.system('clear')

        url_divs = soup.find_all('div', class_='nimo-card-body')
        print(f"Tổng số lượng đường dẫn: {len(url_divs)}")
        random.shuffle(url_divs)
        new_url_divs = random.sample(url_divs, len(url_divs))

        for url_div in new_url_divs:
            a_tag = url_div.find('a')
            b_tag = url_div.find('h4')

            if a_tag or b_tag:
                url_extract = a_tag['href']
                name_extract = b_tag.text

                if url_extract == '/live/35270277':
                    print('Không vào room của Vẹt')
                    continue

                temp_link_list.append(url_extract)
                temp_name_list.append(name_extract)

            if self.urlonlyset.lower() == 'true' and url_extract == self.specificurl:
                temp_link_list = [url_extract]
                temp_name_list = [name_extract]
                break

        windows = []
        element = 0

        print(f"<=== Open {len(temp_link_list)} tabs ===>")
        print(f"Index".ljust(10) + "URL".ljust(27) + "Name".ljust(20))

        for idx in range(len(temp_link_list)):
            print(f"{str(idx+1).ljust(10)}nimo.tv{temp_link_list[idx].ljust(20)}{temp_name_list[idx].ljust(20)}")
            self.driver.execute_script("window.open('" + temp_link_list[idx] + "', '_blank');")
            time.sleep(self.wait_long_time)
            windows = self.driver.window_handles
            idx = 0 if len(windows) == 0 else len(windows) - 1
            self.driver.switch_to.window(windows[idx])

            if self.egg.lower() == 'true':
                # Lấy nội dung HTML của trang web
                html_per_tab = self.driver.page_source
                soup_per_tab = BeautifulSoup(html_per_tab, 'html.parser')

                with open("file_soup_per_tab.html", 'w', encoding="utf-8") as f:
                    f.write(soup_per_tab.prettify())

                egg_collect = soup_per_tab.find_all('div', class_='nimo-box-gift__box n-fx-col n-fx-sc')

                if len(egg_collect) > 0:
                    egg_gift = egg_collect[0].find('nimo-box-gift__box__cd n-as-fs12')
                    if egg_gift != 0:
                        print("====== Yehhh - Room này có trứng nè ======")
                        while True:
                            if not element:
                                value = self.driver.find_element(By.XPATH, '//sup[@class="nimo-scroll-number nimo-badge-count"]')
                                if not value:
                                    break
                                print(f"Remaining eggs: {value.text}")  # Output: 3

                            if int(value.text) >= 1:
                                # Click on the image element using Selenium
                                egg_collect.click()
                                time.sleep(0.3)
                            else:
                                break

            if len(windows) > self.open_tab_num:
                for window in windows:
                    if window != self.main_window:
                        self.driver.switch_to.window(window)
                        # Đóng các tab đang mở
                        # current_url = self.driver.current_url
                        # print(f"Close {current_url}")
                        self.driver.close()
                self.driver.switch_to.window(self.main_window)

        # Chuyển về tab ban đầu
        self.driver.switch_to.window(self.main_window)

        time.sleep(self.wait_short_time)
        self.driver.refresh()

    def app_login(self):
        self.login()

    def run(self):
        self.scrape()


if __name__ == '__main__':
    bot = NimoTVBot(args.username,
                    args.password,
                    args.opentabnum,
                    args.waitshorttime,
                    args.waitlongtime,
                    args.url,
                    args.headless,
                    args.nonlogin,
                    args.urlonlyset,
                    args.specificurl,
                    args.egg)

    try:
        bot.setup_driver()

        if args.nonlogin == 'false':
            bot.app_login()
        while True:
            bot.run()
    except:
        print("Có lỗi rồi bạn ơi !!!")
