MAIN_OPERATIONS = """
Welcome to AwesomeGIC Bank! What would you like to do?
[T] Input transactions 
[I] Define interest rules
[P] Print statement
[Q] Quit
>   """
INPUT_TXN = """
Please enter transaction details in <Date> <Account> <Type> <Amount> format 
(or enter blank to go back to main menu):
>"""

INPUT_INTEREST = """
Please enter interest rules details in <Date> <RuleId> <Rate in %> format 
(or enter blank to go back to main menu):
>"""

INPUT_STATEMENT = """
Please enter account and month to generate the statement <Account> <Year><Month>
(or enter blank to go back to main menu):
>"""

TRANSACTION = '|{}|{}|{}|{}|'
INTEREST = '|{}|{}|{}|'
INTEREST_CAL = '|{}|{}|{}|{}|{}|'
