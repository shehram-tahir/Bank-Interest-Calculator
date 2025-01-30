from operations.transaction import Transaction
from operations.interest import Interest


class BankOperationsMixins(Transaction, Interest):

    def __init__(self):
        Transaction.__init__(self)
        Interest.__init__(self)
