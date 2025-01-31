from datetime import datetime, timedelta

from logger import logger
from messages import TRANSACTION
from utils import validate_time_format


class Transaction:

    def __init__(self):
        self.balance_by_day = {}
        self.accounts = {}
        self.txn_no_id = {}

    def handle_transaction(self, transaction_items: str) -> float:
        """
        Validate and add transaction
        :param transaction_items
        """
        transaction_items = transaction_items.strip().split()
        if len(transaction_items) != 4:
            raise Exception('Transaction values are not in correct format.')
        date, account, txn_type, amount = transaction_items
        txn_type = txn_type.lower()
        amount = float(amount)
        date = validate_time_format(date)
        self.validate_transaction_type(txn_type)
        self.validate_transaction_amount(account, amount, txn_type)
        self.txn_no_id[date] = self.txn_no_id[date] + 1 if self.txn_no_id.get(date) else 1
        self.add_transaction(date, account, txn_type, amount)
        self.print_account_statement(account)
        return self.accounts[account]["balance"]

    @staticmethod
    def validate_transaction_type(txn_type: str) -> None:
        """
        Validate transaction type
        :param txn_type: Value can be either w or d case insensitive
        """
        if txn_type not in ['d', 'w']:
            raise Exception('Transaction type can only either be w or d.')

    def validate_transaction_amount(self, account: str, amount: float, txn_type: str) -> None:
        """
        Validate transaction amount against a few conditions
        :param account
        :param amount
        :param txn_type
        """
        if amount <= 0:
            raise Exception('Amount must be greater than 0.')
        if round(amount, 2) != amount:
            raise Exception('Amount must be at most 2 decimal places.')
        if txn_type == "w":
            if account not in self.accounts:
                raise Exception('Provided account does not exist.')
            if self.accounts.get(account, {}).get('balance') < amount:
                raise Exception('Insufficient balance.')
        if account not in self.accounts:
            self.accounts[account] = {"balance": 0.0, "transactions": []}

    def print_account_statement(self, account: str) -> None:
        """
        Print account statement
        :param account
        """
        find_space = lambda value: 20 - len(str(value))
        logger.info(TRANSACTION.format(
            'Date' + ' ' * find_space('Date'),
            'Txn Id' + ' ' * find_space('Txn Id'),
            'Type' + ' ' * find_space('Type'),
            'Amount' + ' ' * find_space('Amount'),
        ))
        for txn in self.accounts[account]["transactions"]:
            date, txn_id, txn_type, amount = txn['date'], str(txn['id']), str(txn['type']), str(txn['amount'])
            date = date.strftime("%Y%m%d")
            logger.info(TRANSACTION.format(
                date + ' ' * find_space(date),
                txn_id + ' ' * find_space(txn_id),
                txn_type + ' ' * find_space(txn_type),
                amount + ' ' * find_space(amount),
            ))

    def add_transaction(self, txn_date: datetime, account: str, txn_type: str, amount: float) -> None:
        """
        Adds a transaction for the specified account.
        :param txn_date
        :param account
        :param txn_type
        :param amount
        """
        transaction_id = self.generate_transaction_id(txn_date)
        if txn_type == "w":
            self.accounts[account]["balance"] -= amount
        else:
            self.accounts[account]["balance"] += amount
        self.update_missing_days_balance(txn_date, account)
        # Adding time to date to be able to sort transactions of a same day based on time
        current_time = datetime.now().time()
        txn_date= txn_date.replace(hour=current_time.hour, minute=current_time.minute, second=current_time.second,
                                   microsecond=current_time.microsecond)
        self.accounts[account]["transactions"].append({
            "date": txn_date,
            "id": transaction_id,
            "type": txn_type.upper(),
            "amount": amount,
            "current_balance": self.accounts[account]["balance"]
        })
        self.balance_by_day[txn_date.date()] = self.accounts[account]["balance"]

    def generate_transaction_id(self, date: datetime):
        """
        Generates a unique transaction ID based on the date.
        :param date
        """
        return f"{date.strftime('%Y%m%d')}-{self.txn_no_id[date]}"

    def update_missing_days_balance(self, txn_date: datetime, account: str):
        """
        Update balance of days that had no transaction with last day's balance
        :param txn_date:
        :param account:
        :return:
        """
        prev_txn = self.accounts[account]["transactions"][-1] if self.accounts[account]["transactions"] else {}
        if prev_txn and (txn_date.date() - prev_txn['date'].date()).days + 1 > 0:  # Updating balance of missed days
            prev_date = prev_txn['date'] + timedelta(days=1)
            while prev_date < txn_date:
                self.balance_by_day[prev_date.date()] = prev_txn['current_balance']
                prev_date += timedelta(days=1)
