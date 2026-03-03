# sample tests for project
import pytest

def test_sample_function():
    assert 1 + 1 == 2
def test_another_sample_function():
    assert "hello".upper() == "HELLO"
def test_list_length():
    assert len([1, 2, 3]) == 3
    
# run tests
if __name__ == "__main__":
    test_sample_function()
    test_another_sample_function()
    test_list_length()
    print("All tests passed!")