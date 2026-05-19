def pytest_addoption(parser):
    """Add custom command line options to pytest."""
    parser.addoption(
        "--no-AHM",
        action="store_true",
        help="Skip tests that require AHM",
    )
