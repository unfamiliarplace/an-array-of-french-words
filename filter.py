from pathlib import Path
from tools import make_folders, load_words, save_words
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
    words = set(load_words(PATH_ALPHA / f'{n}_alpha.json'))

    incl = set(load_words(PATH_DATA / f'{n}_incl.txt'))
    excl_nw = set(load_words(PATH_DATA / f'{n}_excl_nonword.txt'))
    excl_ns = set(load_words(PATH_DATA / f'{n}_excl_nsfw.txt'))
    excl_in = set(load_words(PATH_DATA / f'{n}_excl_inflection.txt'))

    words -= incl
    words = words - excl_nw - excl_ns - excl_in
    print(f'{len(words)} words | {len(incl)} confirmed | {len(excl_nw)} nonwords | {len(excl_ns)} NSFW words | {len(excl_in)} inflections')

    if not words:
        print('Already sorted this set')
        return

    words = sorted(words)
    commands = []

    print('\nEnter = Include | / = Nonword | I = Inflection | J = NSFW | P = Pass for now')
    print('U = Undo | S = Save | Q = Save and quit | X = Quit without saving\n')

    def _save() -> None:
        for command in commands:
            eval(command)
        commands.clear()

        print(f'{len(words)} words | {len(incl)} confirmed | {len(excl_nw)} nonwords | {len(excl_ns)} NSFW words | {len(excl_in)} inflections')

        save_words(PATH_DATA / f'{n}_incl.txt', list(incl))
        save_words(PATH_DATA / f'{n}_excl_nonword.txt', list(excl_nw))
        save_words(PATH_DATA / f'{n}_excl_nsfw.txt', list(excl_ns))
        save_words(PATH_DATA / f'{n}_excl_inflection.txt', list(excl_in))

    i = 0
    while 0 <= i < len(words):
        word = words[i]

        response = input(f'{word} : ').upper().strip()

        match response:
            case '':
                commands.append(f'incl.add("{word}")')
                i += 1
            
            case '/':
                commands.append(f'excl_nw.add("{word}")')
                i += 1
            
            case 'I':
                commands.append(f'excl_in.add("{word}")')
                i += 1
            
            case 'J':
                commands.append(f'excl_ns.add("{word}")')
                i += 1

            case 'P':
                i += 1
            
            case 'U':
                commands.pop()
                i -= 1
            
            case 'S':
                _save()
            
            case 'Q':
                break

            case 'X':
                commands.clear()
                break
    
    _save()

def run() -> None:
    make_folders([PATH_LISTS, PATH_DIVIDED, PATH_DATA])
    n = input('Enter word length to do: ')
    check(n)

if __name__ == '__main__':
    run()
