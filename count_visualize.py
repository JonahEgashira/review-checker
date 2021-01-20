import collections
import matplotlib.pyplot as plt

def count_words(path):
    '''
    単語の数をカウントしたリストを返す
    '''

    with open(path) as f:
        words = [s.strip() for s in f.readlines()]

    counter = collections.Counter(words)
    counts = list(counter.values())
    return counts


def count_first_digits(data_list):
    '''
    それぞれのカウントの最上位桁の数字の割合を返す
    '''
    digit_count = [0]*9
    for val in data_list:
        s = str(val)
        begin = int(s[0])
        digit_count[begin-1] += 1

    total = sum(digit_count)
    data_pct = [(i / total) * 100 for i in digit_count]
    return data_pct


def bar_chart(data_pct):
    '''
    最上位桁の割合をベンフォードの法則と比較してプロットする
    '''
    BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]

    fig, ax = plt.subplots()

    index = [i + 1 for i in range(len(data_pct))]

    fig.canvas.set_window_title('Percentage First Digits')
    ax.set_title('Data vs. Benford Values', fontsize = 15)
    ax.set_ylabel('Frequency(%)', fontsize = 16)
    ax.set_xticks(index)
    ax.set_xticklabels(index, fontsize=14)

    rects = ax.bar(index, data_pct, width = 0.95, color='black', label='Data')

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height,
                '{:0.1f}'.format(height), ha = 'center', va = 'bottom')

    ax.scatter(index, BENFORD, s = 150, c = 'red', zorder=2, label = 'Benford')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(prop={'size': 15}, frameon=False)

    plt.show()

word_path = "./sentence/jagariko_word_list.txt"

def main():
    data = count_words(word_path)
    data_pct = count_first_digits(data)
    bar_chart(data_pct)


if __name__ == "__main__":
    main()