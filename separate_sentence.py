from pathlib import Path
from janome.charfilter import *
from janome.analyzer import Analyzer
from janome.tokenizer import Tokenizer
from janome.tokenfilter import *
from gensim import *


def separate(path, review_type, noun=True, verb=True, adj=True, adv=True):
    '''
    pathの文章を分割し、./review_{review_type}_separated内に書き込む
    '''

    data_dir_path = Path('.')
    corpus_dir_path = Path('.')

    title = path[-14:-4]

    with open(data_dir_path.joinpath(path), 'r', encoding='utf-8') as file:
        texts = file.readlines()
    texts = [text_.replace('\n', '') for text_ in texts]


    # janomeのAnalyzerを使うことで、文の分割と単語の正規化をまとめて行うことができる
    # 文に対する処理のまとめ
    char_filters = [UnicodeNormalizeCharFilter(),         # UnicodeをNFKC(デフォルト)で正規化
                    RegexReplaceCharFilter('\(', ''),     
                    RegexReplaceCharFilter('\)', ''),     
                    RegexReplaceCharFilter('\!', ''),     
                    RegexReplaceCharFilter('\！', ''),     
                    RegexReplaceCharFilter('\?', ''),     
                    RegexReplaceCharFilter('\.', ''),     
                    RegexReplaceCharFilter('\^', ''),     
                    RegexReplaceCharFilter('\-', ''),     
                    RegexReplaceCharFilter('\.', ''),     
                    ]

    # 単語に分割
    tokenizer = Tokenizer()

    #
    # 名詞中の数(漢数字を含む)を全て0に置き換えるTokenFilterの実装
    #
    class NumericReplaceFilter(TokenFilter):

        def apply(self, tokens):
            for token in tokens:
                parts = token.part_of_speech.split(',')
                if parts[0] == '名詞' and parts[1] == '数':
                    token.surface = '0'
                    token.base_form = '0'
                    token.reading = 'ゼロ'
                    token.phonetic = 'ゼロ'
                yield token


    #
    #  ひらがな・カタガナ・英数字の一文字しか無い単語は削除
    #
    class OneCharacterReplaceFilter(TokenFilter):

        def apply(self, tokens):
            for token in tokens:
                # 上記のルールの一文字制限で引っかかった場合、その単語を無視
                if re.match('^[あ-んア-ンa-zA-Z0-9ー]$', token.surface):
                    continue

                yield token


    #引数で指定した品詞のみフィルターする
    filter_list = []
    if noun:
        filter_list.append('名詞')
    if verb:
        filter_list.append('動詞')
    if adj:
        filter_list.append('形容詞')
    if adv:
        filter_list.append('副詞')

    # 単語に対する処理のまとめ
    token_filters = [
                     #NumericReplaceFilter(),                        # 名詞中の漢数字を含む数字を0に置換
                     CompoundNounFilter(),                           # 名詞が連続する場合は複合名詞にする
                     POSKeepFilter(filter_list),                     # 名詞・動詞・形容詞・副詞のみを取得する
                     POSStopFilter('記号'),                          # 記号は取り除く 
                     LowerCaseFilter(),                              # 英字は小文字にする
                     OneCharacterReplaceFilter()                     # 一文字しか無いひらがなとカタガナと英数字は削除
                     ]

    analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)

    tokens_list = []
    raw_texts = []
    for text in texts:
        # 文を分割し、単語をそれぞれ正規化する
        text_ = [token.base_form for token in analyzer.analyze(text)]
        if len(text_) > 0:
            tokens_list.append([token.base_form for token in analyzer.analyze(text)])
            raw_texts.append(text)


    # 単語リストの作成
    words = []
    for text in tokens_list:
        words.extend([word+'\n' for word in text if word != ''])
    

    separated_path = f"./review_{review_type}_separated/{title}_separated.txt"
    with open(corpus_dir_path.joinpath(separated_path), 'w', encoding='utf-8') as file:
        file.writelines(words)
