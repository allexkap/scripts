import argparse
from hashlib import sha256
from pathlib import Path
from typing import List


def walker(dir: Path) -> bytes:
    content: List[bytes] = []
    for path in dir.glob('*'):
        if path.name == '.checksumignore':
            continue
        elif path.is_file():
            with open(path, 'rb') as file:
                content.append(path.name.encode() + sha256(file.read()).digest())
        elif path.is_dir():
            content.append(path.name.encode() + walker(path))
    return sha256(b''.join(sorted(content))).digest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs=1, type=Path)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    root = args.path[0]
    if root.exists():
        print(''.join(f'{b:0>2x}' for b in walker(root)))
