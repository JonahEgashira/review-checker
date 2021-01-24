import os
import glob
import numpy as np
from separate_sentence import separate
from count_visualize import *
from scrape import *

def get_reviews(path, path_to):
    '''
    レビューを取得してファイルのパスをpath.txtに書き込む
    '''
    with open(path, 'r', encoding='utf-8') as f:
        urls = f.readlines()

        for url in urls:
            #urlの整形
            url = url.replace('?tag=sakurachecker-22', '')
            url = url.replace('gp', 'product-reviews')
            separated_url = url.split('/')

            product_id = separated_url[-2]
            print(f"id: {product_id}")

            path = f"{path_to}{product_id}.txt"
            #もしすでにレビューを取得してたらcontinue
            if os.path.exists(path):
                if os.stat(path).st_size != 0:
                    print(f"{path} already exists")
                    continue

            #レビューを取得する
            create_review_file(url,product_id, path_to)
    

def analyze(review_type, does_get_review=False, does_separate=False): 

    if does_get_review:
        get_reviews(f"./{review_type}_url.txt", f"./review_{review_type}/")

    files = glob.glob(f"./review_{review_type}/*")

    if does_separate:
        for file in files:
            if os.stat(file).st_size == 0:
                continue
            separate(file, review_type, noun=True,verb=True,adj=True,adv=True)

    #単語単位で分析する時
    #files = glob.glob(f'./review_{review_type}_separated/*')
    #1語1語分析する時
    files = glob.glob(f'./review_{review_type}/*')

    pct_list = []
    for file in files:
        #レビューをうまく取得できてないやつ
        if os.stat(file).st_size == 0:
            continue

        #単語単位
        #counts = count_words(file)
        #一語
        counts = count_chars(file)
        data, pct, total = count_first_digits(counts)
        pct_list.append(pct)

    np_pct_list = np.array(pct_list)
    np_ave_list = np.average(np_pct_list,axis=0)

    std_err = np.std(np_pct_list, axis=0)
    print(std_err)
    print(np_ave_list)

    bar_chart_err(np_ave_list, std_err)



if __name__ == "__main__":
    #analyze("bad", False, False)
    analyze("good", False, False)

