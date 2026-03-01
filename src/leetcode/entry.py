class Solution:
    def __init__(self, name: str) -> None:
        import importlib

        module = importlib.import_module(f"leetcode.{name}")

        import inspect

        for attr_name, attr_value in inspect.getmembers(
            module.__getattribute__("Solution")
        ):
            if not attr_name.startswith("__"):
                setattr(self.__class__, attr_name, attr_value)
