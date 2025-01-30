import logging

# Create a logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler("logs.txt")
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter that only includes the message
formatter = logging.Formatter('%(message)s')

# Set the formatter for both handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
