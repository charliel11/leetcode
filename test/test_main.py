from pathlib import Path

from leetcode import Solution
from loader import ListNode, TreeNode, dynamical_loader, generate_loader_type_hint


def list_equal(a: ListNode | None, b: ListNode | None) -> bool:
    while a is not None and b is not None:
        if a.val != b.val:
            return False
        a, b = a.next, b.next
    return a is None and b is None


def tree_equal(a: TreeNode | None, b: TreeNode | None) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return (
        a.val == b.val and tree_equal(a.left, b.left) and tree_equal(a.right, b.right)
    )


def test_target(target):
    test_case_path = f"test/data/{target}"
    f = Solution(target).__getattribute__(target)

    print()
    for i, (*args, answer) in enumerate(
        dynamical_loader(Path(test_case_path), generate_loader_type_hint(f)), 1
    ):
        print(f"[{i}]", args, answer)
        result = f(*args)
        if isinstance(answer, float):
            assert abs(result - answer) <= 1e-5
        elif isinstance(answer, TreeNode):
            assert tree_equal(result, answer)
        elif isinstance(answer, ListNode):
            assert list_equal(result, answer)
        else:
            assert result == answer
