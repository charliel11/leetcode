from pathlib import Path

from leetcode import Solution
from loader import TreeNode, dynamical_loader, generate_loader_type_hint


def test_target(target):
    test_case_path = f"test/data/{target}.txt"
    f = Solution(target).__getattribute__(target)

    print()
    for *args, answer in dynamical_loader(
        Path(test_case_path), generate_loader_type_hint(f)
    ):
        print(args, answer)
        if isinstance(answer, float):
            assert abs(f(*args) - answer) <= 1e-5
        elif isinstance(answer, TreeNode):
            assert 1  # TODO: Compare TreeNode
        else:
            assert f(*args) == answer
