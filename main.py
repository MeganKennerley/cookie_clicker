from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time

chrome_driver_path = os.environ.get("chrome_driver_path")
service = Service(executable_path=chrome_driver_path)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(5)
consent = driver.find_element(by=By.CLASS_NAME, value="fc-primary-button")
consent.click()
time.sleep(2)

language = driver.find_element(by=By.ID, value="langSelect-EN")
language.click()
time.sleep(5)

cookie = driver.find_element(by=By.ID, value="bigCookie")

items = driver.find_elements(by=By.CSS_SELECTOR, value="#product0")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60*5
while True:
    cookie.click()

    if time.time() > timeout:

        prices = driver.find_elements(by=By.CLASS_NAME, value="price")
        item_prices = []

        for price in prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[0].strip().replace(",", ""))
                item_prices.append(cost)

        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = f"product{n}"

        money = driver.find_element(by=By.ID, value="cookies").text
        money_element = money.split()[0]
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        affordable_upgrades = {}
        for cost, num in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = num

        highest_price_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(by=By.ID, value=to_purchase_id).click()

        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cookiesPerSecond").text
        print(cookie_per_s)
        break
