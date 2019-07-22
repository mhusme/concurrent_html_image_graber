import multiprocessing
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def calc_square(number):
    print('Square:', number * number)
    result = number * number
    print(result)
    return result
def calc_quad(number):
    print('Quad:' , number * number * number * number)
    return number * number * number * number

def grab_image_src(process_id, head, rows):
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

    # browser = webdriver.Firefox()

    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)

    for target in targets:
        browser.get(target["shop_url"])
        html_source = browser.page_source
        soup = BeautifulSoup(html_source,'lxml')

        img = soup.select_one('#pi-component-container > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div:nth-child(1) > div > div > div > div:nth-child(1) > img[src]')

        img_src = img['src']

        if "http" in img_src:
            # browser.get(img_src)
            print("hi")
        else:
            img_src = "Logo not found!"

        target['logo_url'] = img_src

    browser.quit()
        
    filename = str(process_id) + "_child_process_output.csv"
    with open(filename, 'w') as csvfile:
        fieldnames = ['seller_id', 'seller_short_code', 'seller_name', 'shop_url', 'logo_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for target in targets:
            writer.writerow(target)
    return 0
if __name__ == "__main__":
    start = time.time()
    number = 7
    result = None

    parallelism = 4
    processes = []

    for i in range(0,parallelism):
        print("haha")
        processes.append(multiprocessing.Process(target=grab_image_src, args=(i,0,0)))
        processes[i].start()
        # p2 = multiprocessing.Process(target=calc_quad, args=(number,))

    for process in processes:
        process.join()

    # Wont print because processes run using their own memory location                     
    print(result)
    end = time.time()
    print(end - start)