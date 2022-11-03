import os.path
import logging


DEBUG = True


error_path = os.path.join('errors', 'log.txt')

if not os.path.exists(error_path):
    os.mkdir('errors')


# Create a logging instance
logger = logging.getLogger('my_application')
logger.setLevel(logging.INFO)  # you can set this to be DEBUG, INFO, ERROR

if not DEBUG:
# Assign a file-handler to that instance
    fh = logging.FileHandler(error_path)
    fh.setLevel(logging.INFO)  # again, you can set this differently
else:
    fh = logging.StreamHandler()
    fh.setLevel(logging.DEBUG)
# Format your logs (optional)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)  # This will set the format to the file handler

# Add the handler to your logging instance
logger.addHandler(fh)
