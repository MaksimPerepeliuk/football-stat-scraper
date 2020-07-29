from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chromedriver_path = './chromedriver'
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=chromedriver_path)
    return driver
