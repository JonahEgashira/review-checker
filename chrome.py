from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
import textwrap
 
# Amazonページ取得
def get_page_from_amazon(url):
     
    text = ""
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
     
    # ブラウザーを起動
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
     
    text = driver.page_source
         
    # ブラウザ停止
    driver.quit()
     
    return text

def get_all_reviews(url):
    review_list = []
    title = ""
    i = 1
    while True:
        print(i, 'searching')
        i += 1
        text = get_page_from_amazon(url)
        amazon_soup = BeautifulSoup(text, features='lxml')

        reviews = amazon_soup.select('.review-text')
        title = amazon_soup.find("title").text

        for review in reviews:
            review_list.append(review)

        next_page = amazon_soup.select('li.a-last a')
        if next_page != []:
            next_url = 'https://amazon.co.jp/' + next_page[0].attrs['href']
            url = next_url
            time.sleep(1)
        else:
            break
    
    #タイトルの整形
    title = title.split()
    title = title[1]
    return review_list, title

if __name__ == '__main__':

    

    new_url = url.replace('dp', 'product-reviews')
    review_list, title = get_all_reviews(new_url)

    with open(f"{title}.txt", 'w') as f:
        for i in range(len(review_list)):
            review_text = textwrap.fill(review_list[i].text, 80)
            print(f"\nNo.{i+1}")
            print(review_text, file = f)

