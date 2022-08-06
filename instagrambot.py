from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from LogIn.auth_data import username, password
from selenium import webdriver
import random
import time

def accept_cookies(browser):
    accept_button = browser.find_element(By.XPATH, "/html/body/div[4]/div/div/button[2]")
    accept_button.click()

def login(username, password):
    try:
        PATH = "C:\WEBDRIVER\chromedriver.exe"
        browser = webdriver.Chrome(PATH)
        browser.get("https://www.instagram.com")
        time.sleep(random.randint(3,5))
        accept_cookies(browser)
        time.sleep(1)
        username_input =  browser.find_element(By.NAME, "username")
        username_input.send_keys(username)

        time.sleep(2)
        password_input = browser.find_element(By.NAME, "password")
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

        hashtag_search(browser, "surfing")

    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()

    finally:
        browser.close()
        browser.quit()

def hashtag_search(browser, hashtag):
    try:
        browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(2)

        hrefs = browser.find_elements(By.TAG_NAME, "a")
        urls_dict = []
        for item in hrefs:
            href = item.get_attribute("href")
            if "/p" in href:
                urls_dict.append(href)
        print(urls_dict)

        for i in range(1, 4):
            browser.execute_script("window.scrollTO(0, document.body.scrollHeight);")
            time.sleep(3)
    except Exception:
        print("ec")

def main():
    login(username, password)


if __name__ == '__main__':
    main()

