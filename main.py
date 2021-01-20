from separate_sentence import separate
from count_visualize import *

def main():
    path = "./jagariko.txt"
    separated_path = separate(path)

    counts = count_words(separated_path)
    data_pct = count_first_digits(counts)
    bar_chart(data_pct)


if __name__ == "__main__":
    main()
    
