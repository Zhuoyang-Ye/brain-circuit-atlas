#!/usr/bin/env python3
"""
Rewrite the data files in the compact, hand-editable layout used by this project:
one record per line inside arrays, long text fields (summary, finding, ...) on a
continuation line, everything else expanded only when it does not fit on a line.

    python3 tools/jsonfmt.py data/knowledge.json data/papers.json
"""
import json
import sys

LONG_TEXT = ('summary', 'finding', 'text', 'desc', 'note', 'manual')
WIDTH = 110


def _c(v):
    return json.dumps(v, ensure_ascii=False)


def fmt(v, ind=0):
    s = _c(v)
    if not isinstance(v, (dict, list)) or len(s) + ind <= WIDTH or not v:
        return s
    pad, inner = ' ' * ind, ' ' * (ind + 2)
    if isinstance(v, list):
        items = [record(x, ind + 2) if isinstance(x, dict) else fmt(x, ind + 2) for x in v]
        return '[\n' + ',\n'.join(inner + it for it in items) + '\n' + pad + ']'
    items = [f'{_c(k)}: {fmt(x, ind + 2)}' for k, x in v.items()]
    return '{\n' + ',\n'.join(inner + it for it in items) + '\n' + pad + '}'


def record(d, ind):
    """A dict inside an array: one line, breaking before long text fields."""
    if any(isinstance(x, (dict, list)) and len(_c(x)) > 160 for x in d.values()):
        return fmt(d, ind)  # big nested structure: expand it instead
    parts, line = [], []
    for k, x in d.items():
        if k in LONG_TEXT and len(_c(x)) > 60 and line:
            parts.append(', '.join(line))
            line = []
        line.append(f'{_c(k)}: {_c(x)}')
    parts.append(', '.join(line))
    return '{' + (',\n' + ' ' * (ind + 1)).join(parts) + '}'


def dumps(obj):
    return fmt(obj) + '\n'


if __name__ == '__main__':
    for path in sys.argv[1:]:
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
        text = dumps(data)
        assert json.loads(text) == data
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)
        print(f'formatted {path} ({text.count(chr(10))} lines)')
