import json
from pathlib import Path
from tools import make_folders, js_many

PATH_LISTS = Path('lists')
PATH_MASTER = PATH_LISTS / 'master.json'

PATH_PROCESSED = PATH_LISTS / 'processed'
PATH_JS = PATH_PROCESSED / 'js'

def len_alpha_range(words: list[str]) -> None:

    path_alpha = PATH_PROCESSED / 'alpha'
    path_alpha_range = PATH_PROCESSED / 'alpha_range'
    make_folders([path_alpha, path_alpha_range])

    longest = len(max(words, key=len))

    words_of_len = {}
    words_of_len_alpha = {}

    for n in range(1, longest + 1):
        
        words_of_len[n] = list(filter(lambda w: len(w) == n, words))
        words_of_len_alpha[n] = list(filter(lambda w: w.isalpha(), words_of_len[n]))

        with open(PATH_PROCESSED / f'{n}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(words_of_len[n], ensure_ascii=False))

        words_of_len_alpha[n] = list(filter(lambda w: w.isalpha(), words_of_len[n]))
        with open(path_alpha / f'{n}_alpha.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(words_of_len_alpha[n], ensure_ascii=False))

    # 1-N incl.

    for upper in range(2, longest + 1):

        _1_to_ = {}

        for n in range(1, upper):
            _1_to_[n] = words_of_len_alpha[n]

        with open(PATH_PROCESSED / 'alpha_range' / f'1_{n}_alpha.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(_1_to_, ensure_ascii=False))

def run() -> None:
    make_folders([PATH_LISTS, PATH_PROCESSED, PATH_JS])
    with open(PATH_MASTER, 'r', encoding='utf-8') as f:
        words = json.loads(f.read())
        len_alpha_range(words)
        js_many(PATH_PROCESSED, PATH_JS)

if __name__ == '__main__':
    run()