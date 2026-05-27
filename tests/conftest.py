import pytest

def pytest_addoption(parser):
    """Add custom command line options to pytest."""
    parser.addoption(
        "--no-AHM",
        action="store_true",
        help="Skip tests that require AHM",
    )
    
def pytest_configure(config):
    # This registers the marker programmatically, skipping the need for an .ini or .toml file
    config.addinivalue_line(
        "markers", 
        "power: tests that enable high power output on hardware"
    )

def pytest_collection_modifyitems(config, items):
    # 1. Check if any of the collected tests have the 'power' marker
    has_power_tests = any(item.get_closest_marker("power") for item in items)
    # If user requested no AHM hardware tests, automatically skip power tests
    if config.getoption("no_AHM"):
        for item in items:
            if item.get_closest_marker("power"):
                item.add_marker(pytest.mark.skip(reason="Skipping power tests due to --no-AHM flag"))
        return
    
    # 2. If we found high-power tests, prompt the user for confirmation
    if has_power_tests:
        print("\n\n⚠️  WARNING: These tests involve setting power levels which is dangorous for equipment and hearing! ⚠️")
        print("\nEnsure that there is nothing connected to the preamp on the mixer")
        
        # We need to temporarily disable pytest's input capturing so the user can type
        capmanager = config.pluginmanager.getplugin("capturemanager")
        
        if capmanager:
            capmanager.suspend_global_capture(in_=True)
            
        try:
            response = input("Are you sure you want to proceed with hardware output? (yes/No): ").strip().lower()
        finally:
            if capmanager:
                capmanager.resume_global_capture()
                
        # 3. If they don't explicitly type 'yes', abort the entire session
        if response != 'yes':
            pytest.exit("Test session aborted by user safety check.", returncode=1)