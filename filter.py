from pathlib import Path
from tools import make_folders, read_words
from enum import Enum

PATH_LISTS = Path('lists')
PATH_DIVIDED = PATH_LISTS / 'divided'
PATH_ALPHA = PATH_DIVIDED / 'alpha'
PATH_DATA = PATH_LISTS / 'filtering_data'

class Response(Enum):
    INCLUDE: int=0
    EXCLUDE: int=1
    PASS: int=2

def check(n: str) -> None:
    path = PATH_ALPHA / f'{n}_alpha.json'
    words = set(read_words(path))

    incl = load_included(n)
    excl = load_excluded(n)

    words -= incl
    words -= excl
    words = sorted(words)

    print('\nEnter = Include | / = Exclude | P = Pass | U = Undo | S = Save | Q = Save and quit | X = Quit without saving\n')

    # lol
    commands = []

    i = 0
    while i < len(words):
        word = words[i]

        response = input(f'{word} : ').upper().strip()

        match response:
            case '':
                commands.append(f'incl.add("{word}")')
                i += 1
            
            case '/':
                commands.append(f'excl.add("{word}")')
                i += 1

            case 'P':
                i += 1
            
            case 'U':
                commands.pop()
            
            case 'S':
                for command in commands:
                    eval(command)
                commands = []
            
            case 'Q':
                break

            case 'X':
                commands = []
                break
    
    for command in commands:
        eval(command)
    commands = []

    save_included(n, incl)
    save_excluded(n, excl)

def load_included(n: str) -> set[str]:
    path = PATH_DATA / f'{n}_incl.txt'
    if not path.exists():
        return set()

    with open(path, 'r', encoding='utf-8') as f:
        return set(f.read().split(','))

def save_included(n: str, words: set[str]) -> None:
    if not words:
        return
    
    path = PATH_DATA / f'{n}_incl.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(','.join(words))

def load_excluded(n: str) -> set[str]:
    path = PATH_DATA / f'{n}_excl.txt'
    if not path.exists():
        return set()
    
    with open(path, 'r', encoding='utf-8') as f:
        return set(f.read().split(','))

def save_excluded(n: str, words: set[str]) -> None:
    if not words:
        return

    path = PATH_DATA / f'{n}_excl.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(','.join(words))

def run() -> None:
    make_folders([PATH_LISTS, PATH_DIVIDED, PATH_DATA])
    n = input('Enter word length to do: ')
    check(n)

if __name__ == '__main__':
    run()
