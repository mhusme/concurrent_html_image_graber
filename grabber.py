from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Firefox()
browser.get("https://www.daraz.com.bd/shop/badminton-planet")
html_source = browser.page_source
soup = BeautifulSoup(html_source,'lxml')
# if ".webp" in html_source:
#     # do something
#     print('yey')
# else:
#     # do something else
#     print('no')

img = soup.select_one('#pi-component-container > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div:nth-child(1) > div > div > div > div:nth-child(1) > img[src]')

print(img['src'])
browser.quit()