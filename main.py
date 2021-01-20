import os
from separate_sentence import separate
from count_visualize import *
from scrape import *

def get_reviews():
    '''
    レビューを取得してファイルのパスをpath.txtに書き込む
    '''
    path_list = []
    with open('./url.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
        for url in urls:
            title = get_title(url)
            path = f"./review_original/{title}.txt"
            #もしすでにレビューを取得してたらcontinue
            if os.path.exists(path):
                continue

            #レビューを取得して、ファイルのパスを入れる
            path = create_review_file(url)
            path_list.append(path+'\n')
    
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
    #get_reviews()
    separate_and_count()
