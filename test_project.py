import pytest
from datetime import datetime
from project import validate_subscription, calculate_next_due, calculate_financial_analytics, remove_subscription

def test_validate_subscription_success():
    """Tests if valid data is cleanly formatted and accepted."""
    result = validate_subscription("  netflix premium  ", "2026-03-09", " 26.99 ", "$ (USD)", "monthly")
    assert result == {
        "name": "Netflix Premium", 
        "start_date": "2026-03-09",
        "price": 26.99, 
        "currency": "$ (USD)", 
        "cycle": "monthly"
    }

def test_validate_subscription_errors():
    """Tests if the validator catches bad data and stops the program from crashing."""
    with pytest.raises(ValueError):
        validate_subscription("   ", "2026-05-04", "19.99", "$ (USD)", "monthly")
    
    with pytest.raises(ValueError):
        validate_subscription("Spotify", "2026-02-30", "19.99", "$ (USD)", "monthly")
    
    with pytest.raises(ValueError):
        validate_subscription("Spotify", "2026-05-04", "-5.00", "$ (USD)", "monthly")

def test_calculate_next_due_monthly():
    """Tests if the calendar engine correctly jumps months."""
    mock_today = datetime(2026, 6, 16).date()
    next_due = calculate_next_due("2026-03-09", "monthly", mock_today)
    assert next_due == datetime(2026, 7, 9).date()

def test_calculate_next_due_yearly():
    """Tests if the calendar engine correctly jumps years."""
    mock_today = datetime(2026, 6, 16).date()
    next_due = calculate_next_due("2025-05-04", "yearly", mock_today)
    assert next_due == datetime(2027, 5, 4).date()

def test_calculate_financial_analytics():
    """Tests if the financial math calculates annual burn accurately by currency."""
    mock_subs = [
        {"name": "Netflix", "price": 26.99, "cycle": "monthly", "currency": "$ (USD)"},
        {"name": "Spotify", "price": 19.99, "cycle": "monthly", "currency": "$ (USD)"},
        {"name": "VPN", "price": 50.00, "cycle": "yearly", "currency": "€ (EUR)"}
    ]
    
    analytics = calculate_financial_analytics(mock_subs)
    
    assert analytics["$ (USD)"]["yearly"] == 563.76
    assert analytics["€ (EUR)"]["yearly"] == 50.00

def test_remove_subscription_success():
    """Tests if the cancellation filter properly removes an item from the list."""
    mock_subs = [
        {"name": "Netflix", "price": 15.99},
        {"name": "Hulu", "price": 9.99}
    ]
    result = remove_subscription(mock_subs, "Netflix")
    
    assert len(result) == 1
    assert result[0]["name"] == "Hulu"

def test_remove_subscription_error():
    """Tests if trying to delete an invisible/non-existent subscription throws an error."""
    mock_subs = [
        {"name": "Netflix", "price": 15.99}
    ]
    with pytest.raises(ValueError):
        remove_subscription(mock_subs, "Disney Plus")