from pathlib import Path


def pytest_addoption(parser):
    parser.addoption(
        "--target",
        action="store",
        default=None,
        help="Specify a specific target to test (e.g., twoSum)",
    )


def pytest_generate_tests(metafunc):
    if "target" in metafunc.fixturenames:
        target_option = metafunc.config.getoption("target")
        if target_option:
            # If --target is specified, only test that target
            targets = [target_option]
        else:
            # Otherwise, test all targets
            targets = [name.stem for name in Path("test/data/").glob("*")]
        metafunc.parametrize("target", targets)
