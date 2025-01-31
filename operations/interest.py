import calendar
from datetime import datetime
import copy

from logger import logger
from messages import INTEREST, INTEREST_CAL
from utils import validate_time_format

class Interest:

    def __init__(self):
        self.interest_rules = []
        self.accounts = {}

    def validate_new_interest_rule(self, interest_rule):
        """
        Validate input interest rule
        :param interest_rule:
        :return:
        """
        interest_rule = interest_rule.strip().split()
        if len(interest_rule) != 3:
            raise Exception('Interest values are not in correct format.')
        date, rule_id, rate = interest_rule
        date = validate_time_format(date)
        rate = float(rate)
        if rate <= 0 or rate >= 100:
            raise Exception("Interest rate must be greater than 0 and less than 100.")
        return date, rate, rule_id

    def define_interest_rule(self, interest_rule: str):
        """
        Adds or updates an interest rule.
        :param interest_rule Input interest rule
        """
        date, rate, rule_id = self.validate_new_interest_rule(interest_rule)
        self.interest_rules = [rule for rule in self.interest_rules if rule["date"] != date]
        self.interest_rules.append({"date": date, "rule_id": rule_id, "rate": rate})
        self.interest_rules.sort(key=lambda x: x["date"])
        self.print_interest_rules()

    def print_interest_rules(self) -> None:
        """Console log interest rules"""
        find_space = lambda value: 20 - len(str(value))
        logger.info(INTEREST.format(
            'Date' + ' ' * find_space('Date'),
            'RuleId' + ' ' * find_space('RuleId'),
            'Rate (%)' + ' ' * find_space('Rate (%)'),
        ))
        for rule in self.interest_rules:
            date, rule_id, rate = str(rule['date']), str(rule['rule_id']), str(rule['rate'])
            logger.info(INTEREST.format(
                date + ' ' * find_space(date),
                rule_id + ' ' * find_space(rule_id),
                rate + ' ' * find_space(rate)
            ))

    def filter_current_month_transactions(self, year_month: datetime, account: str):
        """
        Return all transactions of provided month
        :param year_month:
        :param account:
        :return:
        """
        transaction_balances = []
        for index, txn in enumerate(self.accounts[account]['transactions'], start=1):
            if txn["date"].year > year_month.year:
                break
            if txn["date"].year == year_month.year and txn["date"].month == year_month.month:
                transaction_balances.append(copy.deepcopy(txn))
        return transaction_balances

    def calculate_monthly_interest(self, year_month):
        """
        Calculate interest of the provided month
        :param year_month:
        :return:
        """
        interest = 0.00
        last_date_txn_balance = {}  # This is to store days of the month with no transactions
        for daily_balance_date, balance in self.balance_by_day.items():
            filtered_rule = None
            # Gather interest rules that apply to each transaction and calculate interest
            if daily_balance_date.year == year_month.year and daily_balance_date.month == year_month.month:
                for rule in self.interest_rules:
                    if rule['date'].date() <= daily_balance_date:  # Get the most recent interest rule in the past
                        filtered_rule = rule
                        last_date_txn_balance.update(rule=filtered_rule, balance=balance, date=daily_balance_date)
            if filtered_rule:
                interest += balance * (filtered_rule['rate'] / 100 )
        # Calculate interest for days of no transactions
        if last_date_txn_balance.get('date') and last_date_txn_balance.get('rule'):
            last_month_day = calendar.monthrange(year_month.year, year_month.month)[1]
            remaining_days = (last_date_txn_balance['date'].replace(day=last_month_day) - last_date_txn_balance['date']).days
            if remaining_days > 0:
                for _ in range(remaining_days):
                    interest += last_date_txn_balance['balance'] * (last_date_txn_balance['rule']['rate'] / 100)
        interest = round(interest/365, 2) if interest else interest
        return interest

    def validate_input_acount_date(self, acount_date):
        """
        Validate input account and date for interest calculation
        :param acount_date:
        :return:
        """
        acount_date = acount_date.strip().split()
        if len(acount_date) != 2:
            raise Exception('Interest values are not in correct format.')
        account, year_month = acount_date
        year_month = datetime.strptime(year_month, "%Y%m")
        if self.accounts.get('account') and self.accounts['account']['transactions']:
            raise Exception('Provided account or its does not exist.')
        return account, year_month

    def handle_show_transaction_and_interest(self, acount_date: str) -> float:
        """
        Show all transactions along with interest of the month.
        :param acount_date: Input account number in string
        """
        account, year_month = self.validate_input_acount_date(acount_date)
        self.accounts[account]['transactions'].sort(key=lambda x: x['date'])
        transaction_balances = self.filter_current_month_transactions(year_month, account)
        interest = self.calculate_monthly_interest(year_month)
        if interest:
            transaction_balances.append({
                "date": datetime.now(), "id": '', "type": 'I', "amount": interest,
                "current_balance": self.accounts[account]['balance'] + interest
            })
        self.print_eom_interest_results(transaction_balances)
        return interest

    @staticmethod
    def print_eom_interest_results(transaction_balances: list) -> None:
        """
        Console log all transactions
        :param transaction_balances: All transactions of an account
        """
        find_space = lambda value: 20 - len(str(value))
        logger.info(INTEREST_CAL.format(
            'Date' + ' ' * find_space('Date'),
            'Txn Id' + ' ' * find_space('Txn Id'),
            'Type' + ' ' * find_space('Type'),
            'Amount' + ' ' * find_space('Amount'),
            'Balance' + ' ' * find_space('Balance'),
        ))
        for txn in transaction_balances:
            date, txn_id, txn_type, amount = txn['date'], str(txn['id']), str(txn['type']), str(txn['amount'])
            date = date.strftime("%Y%m%d")
            logger.info(INTEREST_CAL.format(
                date + ' ' * find_space(date),
                txn_id + ' ' * find_space(txn_id),
                txn_type + ' ' * find_space(txn_type),
                amount + ' ' * find_space(amount),
                str(txn['current_balance']) + ' ' * find_space(str(txn['current_balance']))
            ))
