from logger import logger
from operations import BankOperationsMixins
from messages import *


class BankSystem(BankOperationsMixins):

    def __init__(self):
        super().__init__()
        self.balance_by_day = {}

    def run_operations(self) -> None:
        """
        Listen to user commands
        """
        while True:
            try:
                choice = input(MAIN_OPERATIONS).strip().lower()
                if choice == "t":
                    transaction_items = input(INPUT_TXN)
                    if transaction_items:
                        self.handle_transaction(transaction_items)
                elif choice == "i":
                    interest_rule = input(INPUT_INTEREST)
                    if interest_rule:
                        self.define_interest_rule(interest_rule)
                elif choice == "p":
                    account_no = input(
                        'Please enter account and month to generate the statement <Account> <Year><Month>'
                        '(or enter blank to go back to main menu):>')
                    if account_no:
                        self.print_transaction_and_interest(account_no)
                elif choice == "q":
                    logger.info("Thank you for banking with AwesomeGIC Bank. Have a nice day!")
                    break
                else:
                    logger.info("Invalid option. Please try again.")
            except Exception as err:
                logger.error(str(err))
