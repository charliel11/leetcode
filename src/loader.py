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


class ListNode:
    def __init__(self, val=0, next=None):
        self.val: int = val
        self.next: ListNode | None = next

    def __lt__(self, other: "ListNode"):
        """for heapq"""
        return self.val <= other.val


T = TypeVar("T", bound=tuple[Any, ...])
U = TypeVar("U")


def build_list(node: list[int]) -> ListNode:
    dummy = ListNode()
    cur = dummy
    for val in node:
        cur.next = ListNode(val=val)
        cur = cur.next
    return dummy.next  # type: ignore


def build_tree(node: list[int | None]) -> TreeNode | None:
    if not node or node[0] is None:
        return None
    root = TreeNode(val=node[0])
    q = deque([root])
    i = 1
    while q and i < len(node):
        cur = q.popleft()
        if i < len(node) and (lval := node[i]) is not None:
            cur.left = TreeNode(val=lval)
            q.append(cur.left)
        i += 1
        if i < len(node) and (rval := node[i]) is not None:
            cur.right = TreeNode(val=rval)
            q.append(cur.right)
        i += 1
    return root


def is_optional_of(t: Type[U], node_type: type) -> bool:
    if get_origin(t) is Union:
        args = get_args(t)
        return len(args) == 2 and (
            (args[0] is type(None) and args[1] is node_type)
            or (args[0] is node_type and args[1] is type(None))
        )
    else:
        return False


def parse(txt: str, t: Type[U]) -> U:
    res = json.loads(txt)
    if t is ListNode or is_optional_of(t, ListNode):
        return build_list(res)  # type: ignore
    if t is TreeNode or is_optional_of(t, TreeNode):
        return build_tree(res)  # type: ignore
    if get_origin(t) is list:
        args = get_args(t)
        if len(args) == 1 and (
            args[0] is ListNode or is_optional_of(args[0], ListNode)
        ):
            return [build_list(item) if item is not None else None for item in res]  # type: ignore
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
