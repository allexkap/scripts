from typing import Any


def pretty(obj: Any, nest: int = 0, indent: str = '  ', ignore: set = set()) -> str:
    prim_seq = (tuple, list, set, frozenset)
    brackets = ('()', '[]', '{}')

    if id(obj) in ignore:
        return '...'
    elif isinstance(obj, prim_seq):
        values, bracket_type = enumerate(obj), min(prim_seq.index(type(obj)), 2)
    elif isinstance(obj, dict):
        values, bracket_type = obj.items(), 2
    elif hasattr(obj, '__dict__'):
        attrs = {k: getattr(obj, k) for k in dir(obj)}
        attrs = {
            k: v
            for k, v in attrs.items()
            if not (
                k.startswith('__')
                or k.endswith('__')
                or callable(v)
                or type(v).__name__ == 'classmethod'
            )
        }
        values, bracket_type = attrs.items(), 2
    else:
        return repr(obj)

    text = '{} {}\n{}\n{}{}'.format(
        type(obj).__name__,
        brackets[bracket_type][0],
        ',\n'.join(
            f'{indent*(nest+1)}{k}: {type(v).__name__} = {pretty(v, nest+1, indent, ignore | {id(obj)})}'
            for k, v in values
        ),
        indent * nest,
        brackets[bracket_type][1],
    )

    return text
