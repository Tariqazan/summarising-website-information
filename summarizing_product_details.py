import heapq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import nltk
from nltk.corpus import stopwords

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
print("Description", extract_relevant_information)


sentence_list = nltk.sent_tokenize(extract_relevant_information)

stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(extract_relevant_information):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)

print("="*50)
print("Summary:", summary)
print("="*50)
