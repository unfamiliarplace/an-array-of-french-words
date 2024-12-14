import json
from pathlib import Path

def load_words(path: Path) -> list[str]:
    if not path.exists():
        return []
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())
    
def save_words(path: Path, words: list[str]) -> None:
    if not words:
        return
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(words, ensure_ascii=False))

def make_folders(paths: list[Path]) -> None:
    for path in paths:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

def js_one(path_json: Path, path_destination: Path) -> None:

    with open(path_json, 'r', encoding='utf-8') as f:
        words = json.loads(f.read())

    with open(path_destination / f'{path_json.stem}.js', 'w', encoding='utf-8') as f:
        f.write(f'const {path_json.stem} = {json.dumps(words, ensure_ascii=False)};')
    
def js_many(path_origin: Path, path_destination: Path) -> None:
    for path in path_origin.rglob('*.json'):
        js_one(path, path_destination)
