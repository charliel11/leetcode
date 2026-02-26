class Solution:
    def __init__(self, name: str) -> None:
        import importlib

        module = importlib.import_module(f"leetcode.{name}")

        import inspect

        for attr_name, attr_value in inspect.getmembers(
            module.__getattribute__("Solution"), predicate=inspect.isfunction
        ):
            setattr(self.__class__, attr_name, attr_value)
