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

    url = "https://www.amazon.co.jp/CosyInSofa-%E3%82%B9%E3%82%AD%E3%83%BC%E3%82%B4%E3%83%BC%E3%82%B0%E3%83%AB-%E3%82%B9%E3%83%8E%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89%E3%82%B4%E3%83%BC%E3%82%B0%E3%83%AB-99-UV%E3%82%AB%E3%83%83%E3%83%88-%E3%82%A2%E3%82%A6%E3%83%88%E3%83%89%E3%82%A2%E6%B4%BB%E5%8B%95%E9%81%A9%E7%94%A8/dp/B08MTTRK3J/ref=sr_1_21?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=%E3%82%B9%E3%83%8E%E3%83%9C&qid=1611145746&sr=8-21"
    #url = "https://www.amazon.co.jp/%E3%81%98%E3%82%83%E3%81%8C%E3%82%8A%E3%81%93-%E3%82%AB%E3%83%AB%E3%83%93%E3%83%BC/dp/B0184Z5CR8?ref_=Oct_s9_apbd_omwf_hd_bw_b3sAUV&pf_rd_r=A7B58TTX732RRTYTZ54F&pf_rd_p=39e4cabb-2072-5520-88ad-f69e8e96bed2&pf_rd_s=merchandised-search-10&pf_rd_t=BROWSE&pf_rd_i=57239051"

    new_url = url.replace('dp', 'product-reviews')
    review_list, title = get_all_reviews(new_url)

    with open(f"{title}.txt", 'w') as f:
        for i in range(len(review_list)):
            review_text = textwrap.fill(review_list[i].text, 80)
            print(f"\nNo.{i+1}")
            print(review_text, file = f)

