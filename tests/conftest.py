def pytest_addoption(parser):
    parser.addoption(
        "--no-AHM",
        action="store_true",
        help="Skip tests that require AHM"
    )