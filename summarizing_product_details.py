from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transformers import pipeline


# print('*'*100)
# url = input("Enter target website url: ")
# print('*'*100)

driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))

url = "https://www.amazon.com/dp/B09B9TB61G?th=1"

print('*'*100)
print("URL: " + url)
print('*'*100)


def extract_relevant_information(url):
    driver.get(url)
    # title_web_element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, "//div[@id='titleSection']/h1/span"))
    # )
    description_web_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@id='feature-bullets']/ul"))
    )
    # title = title_web_element.get_attribute('innerText')
    description = description_web_element.get_attribute('innerText')
    return description


extract_relevant_information = extract_relevant_information(url)
print(extract_relevant_information)

summarization = pipeline("summarization")
summary_text = summarization(extract_relevant_information)[0]['summary_text']

print("="*50)
print("Summary:", summary_text)
print("="*50)
