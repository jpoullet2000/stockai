# Create a logger object
import logging

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a stream handler to output to the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Create a formatter and set it for the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(stream_handler)
