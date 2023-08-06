from contextlib import redirect_stdout

def startTree(c) -> None:
    if isinstance(c, dict):
        treeViewDict(c)
    elif isinstance(c, list):
        treeViewList(c)
    else:
        print(c)

def treeViewDict(d: dict, prefix='') -> None:
    prefix += '-'
    for k, v in d.items():
        suffix = f"[\"{k}\"]:"
        printValues(v, prefix, suffix)
    prefix = prefix[:-1]

def treeViewList(l: list, prefix='') -> None:
    prefix += '>'
    for i, v in enumerate(l):
        suffix = f"[{i}]:"
        printValues(v, prefix, suffix)
    prefix = prefix[:-1]

def printValues(c, prefix: str, id: str) -> None:
    spaces = (len(prefix)-1) * ' '
    if isinstance(c, dict):
        print(''.join([spaces, prefix[1:], id]))
        treeViewDict(c, prefix)
    elif isinstance(c, list):
        print(''.join([spaces, prefix[1:], id]))
        treeViewList(c, prefix)
    else:
        print(''.join([spaces, prefix[1:], id]), type(c).__name__)

def treeView(obj, output=None) -> None:
    if not output:
        startTree(obj)
    else:
        with open(output, 'w') as file:
            with redirect_stdout(file):
                startTree(obj)
