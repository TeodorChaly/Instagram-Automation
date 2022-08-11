from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from LogIn.auth_data import username, password, gmail
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import requests
import random
import time
import os


def accept_cookies(browser):
    accept_button = browser.find_element(By.XPATH, "/html/body/div[4]/div/div/button[2]")
    accept_button.click()


def login(browser, username, password, url):
    browser.get(url)
    browser.implicitly_wait(5)
    accept_cookies(browser)
    try:
        time.sleep(2)
        username_input = browser.find_element(By.NAME, "username")
        username_input.send_keys(username)
        time.sleep(1)
        password_input = browser.find_element(By.NAME, "password")
        password_input.send_keys(password)
        time.sleep(1)
        password_input.send_keys(Keys.ENTER)
        if xpath_exists(browser, "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[2]/p"):
            print(112)
            username_input = browser.find_element(By.NAME, "username")
            username_input.send_keys(Keys.CONTROL + "A")
            username_input.send_keys(gmail[:3])
            username_input.send_keys(gmail[3:])
            time.sleep(1)
            password_input.send_keys(Keys.ENTER)
            time.sleep(3)
            time.sleep(3)
    except:
        print(11)


def hashtag_search(browser, hashtag):
    try:
        browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(2)

        hrefs = browser.find_elements(By.TAG_NAME, "a")
        urls_dict = []
        for item in hrefs:
            href = item.get_attribute("href")
            if "/p/" in href:
                urls_dict.append(href)
        print(urls_dict)


    except Exception:
        print("ec")


def get_all_followers(browser, page_url):
    time.sleep(3)
    browser.get(page_url)
    time.sleep(3)

    followers_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a")
    followers_count = browser.find_element(By.XPATH,
                                           "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span").get_attribute(
        "title")
    following_button = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a")
    followers_loop = int(int(followers_count.replace(",", "")) / 12)
    time.sleep(3)
    followers_button.click()
    time.sleep(3)

    followers_ul = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]")

    try:
        followers_urls = []
        for i in range(1, followers_loop + 1):
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
            time.sleep(random.randint(2, 4))
            print(f"Iteration:{i}")
            if i == 4:
                break
            all_urls_div = followers_ul.find_elements(By.TAG_NAME, "a")
            for url in all_urls_div:
                followers_urls.append(url.get_attribute("href"))
                print(url.text.strip())
        count = 0
        for user_url in followers_urls:
            print(user_url)
            if count == 4:
                break
            try:
                page_info(browser, user_url)
            except:
                print("Page Error")
            count += 1
    except:
        pass


def read_post(browser, name_of_file):
    if os.path.exists(f"{name_of_file}"):
        print("Directory exists")
    else:
        print(name_of_file)
        os.mkdir(name_of_file)

    with open(f"{name_of_file}.txt")as file:
        urls_list = file.readlines()
        img_and_video = []
        for post_url in urls_list:
            try:
                print(post_url.replace("\n", ""))
                browser.get(post_url.replace("\n", ""))
                time.sleep(4)
                post_id = post_url.split("/")[-2]

                try:
                    likes = browser.find_element(By.XPATH,
                                                 "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span").text
                except:
                    likes = "No info"
                try:
                    post_date = browser.find_element(By.XPATH,
                                                     "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[2]/div/div/a/div/time").text
                except:
                    post_date = "No info"
                try:
                    first_comment = browser.find_element(By.XPATH,
                                                         "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                except:
                    first_comment = "No comment"

                img_xpath = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/div[1]/img"
                video_xpath = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div/div/video"
                if xpath_exists(browser, img_xpath):
                    img_src_url = browser.find_element(By.XPATH, img_xpath).get_attribute("src")
                    img_and_video.append(img_src_url)

                    get_img = requests.get(img_src_url)
                    print(name_of_file)
                    with open(f"{name_of_file}/{post_id}_img.jpg", "wb") as image_file:
                        image_file.write(get_img.content)

                elif xpath_exists(browser, video_xpath):
                    video_url = browser.find_element(By.XPATH, video_xpath).get_attribute("src")
                    img_and_video.append(video_url)

                    get_video = requests.get(img_src_url, stream=True)
                    with open(f"{name_of_file}/{post_id}_video.mp4", "wb") as video_file:
                        for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                video_file.write(chunk)

                else:
                    print("Something went wrong!")
                    img_and_video.append(f"{name_of_file}/{post_url} - Something went wrong!")

                print("Likes: ", likes, "Post date: ", post_date, "First comment: ", first_comment, "Post link: ", browser.current_url)
                time.sleep(15)
            except:
                print("Error")


def page_info(browser, page_url):
    time.sleep(3)
    browser.get(page_url)
    time.sleep(3)

    name = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/h2").text
    publications = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[1]/div/span").text
    subscribers_count = browser.find_element(By.XPATH,
                                             "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span").text
    following_count = browser.find_element(By.XPATH,
                                           "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div/span").text

    scroll_down = int(int(publications) / 12)
    list_post_url = []
    for item in range(0, scroll_down):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        hrefs = browser.find_elements(By.TAG_NAME, "a")
        for href in hrefs:
            if "/p" in href.get_attribute("href") and href.get_attribute("href") not in list_post_url:
                list_post_url.append(href.get_attribute("href"))

    with open(f"{name}.txt", "w"):
        pass

    with open(f"{name}.txt", "a") as file:
        for url in list_post_url:
            file.write(url + "\n")

    print("Name:" + name, "Posts count:" + publications, "Followers count:" + subscribers_count, "Following count:" + following_count)


def xpath_exists(browser, url):
    try:
        browser.find_element(By.XPATH, url)
        exist = True
    except NoSuchElementException:
        exist = False
    return exist


def main():
    PATH = "C:\WEBDRIVER\chromedriver.exe"
    option = webdriver.ChromeOptions()
    option.headless = False
    option.add_argument(
        "user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
    option.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(PATH, chrome_options=option)
    try:

        login(browser, username, password, "https://www.instagram.com/")
        get_all_followers(browser, "https://www.instagram.com/toni.starr")

        # page_info(browser, "https://www.instagram.com/toni.starr/")
        # read_post(browser, "toni.starr" )
        # hashtag_search(browser, "surfing")

    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()

    finally:
        browser.close()
        browser.quit()


if __name__ == '__main__':
    main()
