"""Sample baseline tests."""
import pytest

def test_sample_function():
    """Test basic addition."""
    assert 1 + 1 == 2

def test_another_sample_function():
    """Test string uppercase conversion."""
    assert "hello".upper() == "HELLO"

def test_list_length():
    """Test list length."""
    assert len([1, 2, 3]) == 3
