import logging

# Module Level logger
logger = logging.getLogger("rfol")
logger.setLevel(logging.DEBUG)

# Set up formatter
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

# Set up FileHandler
file_handler = logging.FileHandler('module.log')
file_handler.setFormatter(formatter)

# console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Avoid duplicate handlers
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')
