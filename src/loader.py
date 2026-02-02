import json
from collections import deque
from collections.abc import Iterator
from pathlib import Path
from typing import (
    Any,
    Callable,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


T = TypeVar("T", bound=tuple[Any, ...])
U = TypeVar("U")


def build_tree(node: list[int]) -> TreeNode:
    root = TreeNode(val=node[0])
    q = deque([root])
    for i in range(1, len(node), 2):
        cur = q.popleft()
        cur.left = TreeNode(val=node[i])
        cur.right = TreeNode(val=node[i + 1])
        q.append(cur.left)
        q.append(cur.right)
    return root


def is_optional(t: Type[U]) -> bool:
    if get_origin(t) is Union:
        args = get_args(t)
        return len(args) == 2 and (
            (args[0] is type(None) and args[1] is TreeNode)
            or (args[0] is TreeNode and args[1] is type(None))
        )
    else:
        return False


def parse(txt: str, t: Type[U]) -> U:
    res = json.loads(txt)
    if is_optional(t):
        return build_tree(res)  # type: ignore
    return res  # type: ignore


def dynamical_loader(file: Path, t: Type[T]) -> Iterator[T]:
    txt = file.read_text().split("\n")
    hints = get_args(t)
    assert len(txt) % len(hints) == 0

    for i in range(0, len(txt), len(hints)):
        res: tuple[Any, ...] = ()
        for j, hint in enumerate(hints):
            res += (parse(txt[i + j], hint),)
        yield res  # type: ignore


def generate_loader_type_hint(f: Callable) -> type[tuple[Any, ...]]:
    type_hints = get_type_hints(f)
    return tuple[tuple([v for _k, v in type_hints.items()])]  # type: ignore
