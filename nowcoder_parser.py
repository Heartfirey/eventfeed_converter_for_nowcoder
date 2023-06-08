import time
from selenium import webdriver
from selenium.webdriver.common.by import By

CONTEST_URL= "https://ac.nowcoder.com/acm/contest/59040"

def nowcoder_url_cfg(page: str = "desc"):
    post_attr_dict = {
        "desc": r"#description",
        "problem": r"#question",
        "submission": r"#submit",
        "rank": r"#rank",
    }
    result_url = f"{CONTEST_URL}{post_attr_dict[page]}"
    return result_url

def crawl_contest_info(driver):
    contest_desc = nowcoder_url_cfg('desc')
    contest_rank = nowcoder_url_cfg('rank')
    driver.get(contest_desc)
    # Parase contest title
    contest_name = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/h1/span[1]')
    # Parase contest start time and end time
    contest_time_info = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/p[1]/span[1]').text
    assert type(contest_time_info) is str
    contest_time_split_position = contest_time_info.find('至')
    assert contest_time_split_position != -1
    contest_start_time = contest_time_info[:contest_time_split_position - 1]
    contest_ended_time = contest_time_info[contest_time_split_position + 2:]

    print(contest_time_info) # '2023-06-04 09:00:00 至 2023-06-04 14:00:00'

    exit(0)

if __name__ == "__main__":
    driver = webdriver.Edge()
    driver.get(r'https://www.nowcoder.com/')
    res = driver.find_element(By.XPATH, "//*[@id='jsApp']/header/header/nav/div[3]/button/span/a[1]")
    res.click()
    time.sleep(5)
    try:
        while(True):
            tmp = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/img')
    except:
        try:
            time.sleep(20)
            tmp = driver.find_element(
            By.XPATH, '//*[@id="jsApp"]/header/header/nav/div[2]/div/div/span/img')
        except:
            print("Timeout! Please run this script again to login.")
            time.sleep(10)
            driver.close()
            exit(1)
        print("Login successful!")
    driver.minimize_window()
    time.sleep(5)
    crawl_contest_info(driver=driver)
    