import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time

start = time.time()

targets = []
limit = 10

with open('seller.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    i = 0
    for row in reader:
        i += 1
        if i == limit:
            break
        profile = {

            "seller_id" : "initialized",
            "seller_short_code" : "initialized",
            "seller_name" : "initialized",
            "shop_url" : "initialized",
            "logo_url" : "0 tries"
        }
                
        profile['seller_id'] = row['seller_id']
        profile['seller_short_code'] = row['seller_short_code']
        profile['seller_name'] = row['seller_name']
        profile['shop_url'] = row['shop_url']

        print(profile['seller_name'], profile['seller_name'], profile['shop_url'])
        targets.append(profile)

browser = webdriver.Firefox()
for target in targets:
    browser.get(target["shop_url"])
    html_source = browser.page_source
    soup = BeautifulSoup(html_source,'lxml')

    img = soup.select_one('#pi-component-container > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div:nth-child(1) > div > div > div > div:nth-child(1) > img[src]')

    img_src = img['src']

    if "http" in img_src:
        browser.get(img_src)
    else:
        img_src = "Logo not found!"

    target['logo_url'] = img_src

browser.quit()
    

with open('new_seller.csv', 'w') as csvfile:
    fieldnames = ['seller_id', 'seller_short_code', 'seller_name', 'shop_url', 'logo_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for target in targets:
        writer.writerow(target)

end = time.time()
print(end - start)