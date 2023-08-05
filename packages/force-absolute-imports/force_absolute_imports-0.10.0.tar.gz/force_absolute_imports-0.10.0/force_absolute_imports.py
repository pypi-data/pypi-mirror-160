__version__ = '0.10.0'

import io
import re
import sys
from pathlib import Path
from typing import Optional


def parse(line: str):
    """here s means spaces"""
    return re.match(r'(?P<s0>\s*)from(?P<s1>\s*)(?P<dots>\.+)(?P<s2>\s*)(?P<rest>.*)', line, re.DOTALL).groupdict()


def fix(file: Path, line: str) -> str:
    p = parse(line)
    if not p['s1']:
        p['s1'] = ' '
    module = '.'.join(file.parents[len(p['dots']) - 1].parts)
    out = f'{p["s0"]}from{p["s1"]}'
    if p['rest'].startswith('import '):
        if not p['s2']:
            p['s2'] = ' '
        out += f'{module}'
    else:
        out += f'{module}.'
    out += f'{p["s2"]}{p["rest"]}'
    return out


def only_absolute_line(line: str) -> bool:
    return not re.match(r'\s*from\s*\.', line)


def only_absolute_file(file, root_dir: Optional[Path] = None, in_place: bool = False) -> bool:
    file = Path(file)
    if file.suffix != '.py':
        print(f'{file} not a python file')
        raise SystemExit(2)

    if in_place:
        fixed_str = io.StringIO()

    only_absolute = True

    with open(file) as f:
        for linenumber, line in enumerate(f, start=1):
            if not only_absolute_line(line):
                line_fixed = fix(file, line)
                print(f'relative import | {file}:{linenumber} {line.rstrip()} | fix -> | {line_fixed.rstrip()} | {root_dir} |')
                only_absolute = False
                if in_place:
                    line = line_fixed
            if in_place:
                fixed_str.write(line)

    if in_place:
        with open(file, 'w') as f:
            f.write(fixed_str.getvalue())

    if in_place:
        return True
    return only_absolute


def only_absolute_folder(folder: Path, in_place: bool = False) -> bool:
    only_absolute = True
    for file in Path(folder).rglob('*.py'):
        if not only_absolute_file(file, root_dir=folder, in_place=in_place):
            only_absolute = False
    return only_absolute


def main() -> int:
    """
    return codes
    0 - success, all imports are absolute
    1 - some imports are relative
    2 - non existed files, non .py extensions, files are not passed
    """
    if len(sys.argv) == 1:
        print('pass files and/or folders to check')
        return 2

    options = set()
    paths = []
    for a in sys.argv[1:]:
        if a.startswith('-'):
            options.add(a.lstrip('-'))
        else:
            paths.append(Path(a))

    in_place = 'in-place' in options

    only_absolute = 1
    for p in paths:
        if p.is_file():
            only_absolute *= only_absolute_file(p, in_place=in_place)
        elif p.is_dir():
            only_absolute *= only_absolute_folder(p, in_place=in_place)
        else:
            print(f'{p}: is not exists or not a file or folder')
            raise SystemExit(2)

    return 0 if only_absolute else 1


if __name__ == '__main__':
    raise SystemExit(main())
