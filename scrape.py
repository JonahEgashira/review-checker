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
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
     
    text = driver.page_source
         
    # ブラウザ停止
    driver.quit()
     
    return text

#商品名を日本語で得たい場合
def get_title(url):
    #普通
    #new_url = url.replace('dp', 'product-reviews')
    #サクラチェッカー用
    new_url = url.replace('gp', 'product-reviews')
    text = get_page_from_amazon(new_url)
    amazon_soup = BeautifulSoup(text, features='lxml')

    title = amazon_soup.find("title").get_text()
    #タイトルの整形
    title = title.split()
    title = title[1]

    return title


def get_all_reviews(url):
    '''
    レビューを取得する
    '''

    review_list = []
    title = ""
    i = 1
    while True:
        print(i, 'searching')
        i += 1
        text = get_page_from_amazon(url)
        amazon_soup = BeautifulSoup(text, features='lxml')

        reviews = amazon_soup.select('.review-text')

        for review in reviews:
            review_list.append(review)

        #次のページに行く
        next_page = amazon_soup.select('li.a-last a')
        if next_page != []:
            next_url = 'https://amazon.co.jp/' + next_page[0].attrs['href']
            url = next_url
            time.sleep(1)
        else:
            break
    
    return review_list

def create_review_file(url, product_id):
    '''
    引数のurlからレビューを取得、新しくファイルに書き込む
    新しく書かれたファイルのパスを返す(ファイル名はproduct_id)
    '''
    review_list = get_all_reviews(url)
    #title = get_title(new_url)

    path = f"./review_original/{product_id}.txt"
    with open(path, 'w') as f:
        for i in range(len(review_list)):
            review_text = textwrap.fill(review_list[i].text, 80)
            print(f"\nNo.{i+1}")
            print(review_text, file = f)
    return path

