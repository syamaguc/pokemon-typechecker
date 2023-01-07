import itertools
import random
import shutil
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

POKEMON = [
    "マスカーニャ",
    "カイリュー",
    "ジバコイル",
    "サザンドラ[ふゆう]",
    "サーフゴー",
    "ドラパルト",
]


def setup_driver():
    user_agent = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    ]

    options = Options()
    options.add_argument("--headless")
    UA = user_agent[random.randrange(0, len(user_agent), 1)]
    options.add_argument("--user-agent=" + UA)
    options.binary_location = shutil.which("google-chrome-stable")
    driver = webdriver.Chrome(
        service=Service(executable_path=ChromeDriverManager().install()),
        options=options,
    )
    driver.implicitly_wait(15)
    # wait = WebDriverWait(driver, 10)
    return driver


if __name__ == "__main__":
    cmbs = list(itertools.combinations(POKEMON, 3))
    print(f"{len(cmbs)}種類の組み合わせを検索します。")
    driver = setup_driver()
    driver.get("https://yakkun.com/tool/type_checker.htm")
    for cmb in cmbs:
        driver.find_element(By.NAME, "p1").send_keys(cmb[0])
        driver.find_element(By.NAME, "p2").send_keys(cmb[1])
        driver.find_element(By.NAME, "p3").send_keys(cmb[2])
        driver.find_element(By.ID, "check_submit").click()
        time.sleep(0.5)
        elm = driver.find_element(By.XPATH, "//*[@id='check_result']/div[2]/table")
        resistance = elm.text.count("×")
        msg = f"{cmb}, {resistance}"
        if resistance < 1:
            print(msg)
        driver.find_element(By.NAME, "p1").clear()
        driver.find_element(By.NAME, "p2").clear()
        driver.find_element(By.NAME, "p3").clear()
