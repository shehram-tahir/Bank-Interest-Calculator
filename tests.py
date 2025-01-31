import logging

import pytest
from main import BankSystem


@pytest.fixture
def bank_system():
    return BankSystem()


def test_add_transaction(bank_system):
    assert bank_system.handle_transaction("20240101 AC001 d 1000") == 1000.0
    assert "AC001" in bank_system.accounts
    assert bank_system.accounts["AC001"]["balance"] == 1000.0
    assert len(bank_system.accounts["AC001"]["transactions"]) == 1
    assert bank_system.handle_transaction("20240101 AC001 d 1000") == 2000.0
    assert bank_system.accounts["AC001"]["balance"] == 2000.0
    with pytest.raises(Exception, match='Provided account does not exist.'):
        bank_system.handle_transaction("20240101 AC002 w 500")  # Should fail


def test_define_interest_rule(bank_system):
    assert bank_system.define_interest_rule("20240101 RULE01 2.0") is None
    assert len(bank_system.interest_rules) == 1
    assert bank_system.interest_rules[0]["rate"] == 2.0
    with pytest.raises(Exception, match="Interest rate must be greater than 0 and less than 100"):
        bank_system.define_interest_rule("20240101 RULE02 -1.0")  # Invalid rate
    with pytest.raises(Exception, match="Incorrect format of time"):
        bank_system.define_interest_rule("INVALID RULE03 3.0")  # Invalid date


def test_calculate_interest(bank_system):
    bank_system.define_interest_rule("20240101 RULE01 2.0")
    bank_system.handle_transaction("20240101 AC001 d 1000")
    interest = bank_system.handle_show_transaction_and_interest("AC001 202401")
    assert interest > 0
    assert round(bank_system.accounts["AC001"]["balance"]) == 1000


def test_invalid_transactions(bank_system):
    with pytest.raises(Exception, match="Incorrect format of time"):
        bank_system.handle_transaction("INVALID AC001 d 100.00")  # Invalid date
    with pytest.raises(Exception, match="Amount must be greater than 0"):
        bank_system.handle_transaction("20240101 AC001 d -50.00")  # Negative amount
    with pytest.raises(Exception, match="Amount must be at most 2 decimal places"):
        bank_system.handle_transaction("20240101 AC001 d 50.123")  # More than 2 decimals
    with pytest.raises(Exception, match='Transaction type can only either be w or d.'):
        bank_system.handle_transaction("20240101 AC002 INVALID 500")  # Should fail


def test_invalid_interest_rules(bank_system):
    with pytest.raises(Exception, match="Incorrect format of time"):
        bank_system.define_interest_rule("INVALID RULE01 2.0")  # Invalid date
    with pytest.raises(Exception, match="Interest rate must be greater than 0 and less than 100"):
        bank_system.define_interest_rule("20240101 RULE02 -5.0")  # Invalid rate
    with pytest.raises(Exception, match="Interest rate must be greater than 0 and less than 100"):
        bank_system.define_interest_rule("20240101 RULE03 105.0")  # Rate > 100


def test_complete_flow_one(bank_system):
    for txn in ['20240101 AC001 d 1000.00', '20240110 AC001 w 200.00', '20240120 AC001 d 500.00']:
        bank_system.handle_transaction(txn)
    for rule in ['20240105 RULE01 2.00', '20240115 RULE02 3.00']:
        bank_system.define_interest_rule(rule)
    interest = bank_system.handle_show_transaction_and_interest('AC001 202401')
    assert round(interest, 2) == 2.1


def test_complete_flow_two(bank_system):
    for txn in ['20240101 AC001 d 1000.00', '20240110 AC001 w 200.00', '20240120 AC001 d 500.00']:
        bank_system.handle_transaction(txn)
    for rule in ['20240101 RULE01 2.00', '20240103 RULE01 4.00', '20240115 RULE02 3.00']:
        bank_system.define_interest_rule(rule)
    interest = bank_system.handle_show_transaction_and_interest('AC001 202401')
    assert round(interest, 2) == 2.93
