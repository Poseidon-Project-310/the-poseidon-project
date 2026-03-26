# backend/tests/repositories/test_order_repo.py
import json
import pytest
from unittest.mock import mock_open, patch
from backend.repositories.order_repo import OrderRepository

@patch("backend.repositories.order_repo.open", new_callable=mock_open)
@patch("os.path.exists")
def test_load_all_valid_data(mock_exists, mock_file):
    """
    Valid Equivalence Partitioning
    Load all of the order data from the JSON file
    """
    mock_exists.return_value = True
    fake_orders = [
        {"id": "abc123A", 
         "customer_id": "brady_b", 
         "status": "unpaid"}
    ]
    # Set the return value of the read operation
    mock_file.return_value.read.return_value = json.dumps(fake_orders)

    repo = OrderRepository()
    results = repo.load_all()
    
    assert len(results) == 1
    assert results[0]["id"] == "abc123A"
    assert results[0]["customer_id"] == "brady_b"


@patch("os.path.exists")
def test_load_all_missing_file(mock_exists):
    """
    Invalid Equivalence Partitioning
    Handles loading a file that doesn't exist by returning an empty list
    """
    mock_exists.return_value = False
    
    repo = OrderRepository()
    results = repo.load_all()
    
    # Should return empty list, not crash
    assert results == []


@patch("backend.repositories.order_repo.json.load")
@patch("os.path.exists")
def test_load_all_corrupted_data(mock_exists, mock_json_load):
    """
    Fault Injection/ Exception Handling
    Injects corrupted JSON to trigger a JSONDecodeError
    """
    mock_exists.return_value = True
    # Simulate a crash during json.load
    mock_json_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)

    repo = OrderRepository()
    results = repo.load_all()
    
    # Repo should catch the error and return []
    assert results == []


@patch("backend.repositories.order_repo.open", new_callable=mock_open)
def test_save_all_serialization(mock_file):
    """
    Mocking Functionality
    Verifies that the repository correctly writes data to the file
    """
    repo = OrderRepository()
    test_orders = [
        {"id": "xyz789B", 
         "customer_id": "test_user", 
         "status": "paid"}
    ]
    
    repo.save_all(test_orders)
    
    # Check that the file was opened for writing ('w')
    mock_file.assert_called_once_with('backend/data/orders.json', 'w')
    
    # Verify the content written to the file
    handle = mock_file()
    # Join all write calls to see the full string
    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    
    assert '"id": "xyz789B"' in written_content
    assert '"customer_id": "test_user"' in written_content