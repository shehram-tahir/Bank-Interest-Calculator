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
        display_text = MAIN_OPERATIONS
        while True:
            try:
                choice = input(display_text).strip().lower()
                if choice == "t":
                    transaction_items = input(INPUT_TXN)
                    if transaction_items:
                        self.handle_transaction(transaction_items)
                elif choice == "i":
                    interest_rule = input(INPUT_INTEREST)
                    if interest_rule:
                        self.define_interest_rule(interest_rule)
                elif choice == "p":
                    account_no = input(INPUT_ACCOUNT)
                    if account_no:
                        self.print_transaction_and_interest(account_no)
                elif choice == "q":
                    logger.info(INPUT_QUIT)
                    break
                display_text = MORE_OPERATIONS
            except Exception as err:
                logger.error(str(err))
