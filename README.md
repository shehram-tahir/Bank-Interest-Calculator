# Bank Interest Calculator

### Setup project: 
    1. Install Python version 3.13.1

    2. Run Commands
        - pip3 install virtualenv
        - python3 -m venv test-env
        - pip install -r requirements.txt

### Run Project
    python run_prompt.py

## Run Tests
    pytest tests.py

## Commands:
    1. Add Transaction: t
    2. Add Interest Rule: i
    3. Print All Transactions: p
    4. Quit: q

## Sample Inputs:
    
    1. Transaction:
        20230626 AC001 d 1231
    
    2. Interest Rule: 
        20230615 RULE05 2.21
    
    3. Print All Transactions:
        AC001 202306

## Github Actions:
    1. Tests are run on every commit to main branch
    2. Tests are run on every PR for main branch
