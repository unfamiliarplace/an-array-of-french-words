import json
from pathlib import Path

PATH_LISTS = Path('lists')
PATH_JS = PATH_LISTS / 'js'
PATH_MASTER = PATH_LISTS / 'master.json'

if not PATH_LISTS.exists():
    PATH_LISTS.mkdir(parents=True)

if not PATH_JS.exists():
    PATH_JS.mkdir(parents=True)

with open(PATH_MASTER, 'r', encoding='utf-8') as f:
    master = json.loads(f.read())

longest = len(max(master, key=len))

for n in range(1, longest + 1):
    
    words_n = list(filter(lambda w: len(w) == n, master))
    with open(PATH_LISTS / f'{n}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(words_n, ensure_ascii=False))
    with open(PATH_JS / f'{n}.js', 'w', encoding='utf-8') as f:
        f.write(f'const fr_{n} = {json.dumps(words_n, ensure_ascii=False)};')

    words_n_alpha = list(filter(lambda w: w.isalpha(), words_n))
    with open(PATH_JS / f'{n}_alpha.js', 'w', encoding='utf-8') as f:
        f.write(f'const fr_{n}_alpha = {json.dumps(words_n_alpha, ensure_ascii=False)};')
