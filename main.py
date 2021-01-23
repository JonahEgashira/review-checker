import os
import glob
import numpy as np
from separate_sentence import separate
from count_visualize import *
from scrape import *

def get_reviews(path):
    '''
    レビューを取得してファイルのパスをpath.txtに書き込む
    '''
    path_list = []
    with open(path, 'r', encoding='utf-8') as f:
        urls = f.readlines()
        for url in urls:

            #urlの整形
            url = url.replace('?tag=sakurachecker-22', '')
            url = url.replace('gp', 'product-reviews')
            separated_url = url.split('/')

            product_id = separated_url[-2]
            print(f"id: {product_id}")

            path = f"./review_original/{product_id}.txt"
            #もしすでにレビューを取得してたらcontinue
            if os.path.exists(path):
                print(f"{path} already exists")
                continue

            #レビューを取得して、ファイルのパスを入れる
            new_path = create_review_file(url,product_id)
            path_list.append(new_path+'\n')
    
    with open('./path.txt', 'w', encoding='utf-8') as f:
        f.writelines(path_list)


def separate_and_count():
    '''
    ファイルのレビューを単語に分解して分析する
    '''
    with open('./path.txt', 'r', encoding='utf-8') as f:
        paths = f.read().splitlines()
        for path in paths:
            #取得したレビューを単語に分解する
            separated_path = separate(path, noun=False, verb=False, adj=True, adv=False)
    
            #単語ごとのカウントを数え、最上位桁の割合をプロットする
            counts = count_words(separated_path)
            data_pct = count_first_digits(counts)
            bar_chart(data_pct)


        
if __name__ == "__main__":
    get_reviews('./good_url.txt')

    '''
    #レビューをまとめて標準偏差のエラーバーを表示
    files = glob.glob('./review_bad/*')
    pct_list = []
    for file in files:
        counts = count_chars(file)
        data, pct, total = count_first_digits(counts)
        pct_list.append(pct)
        #bar_chart(pct)

    np_pct_list = np.array(pct_list)
    np_ave_list = np.average(np_pct_list,axis=0)

    std_err = np.std(np_pct_list, axis=0)
    print(std_err)
    print(np_ave_list)

    bar_chart_err(np_ave_list, std_err)
    '''

