# Logging configuration

import os
import logging
from logging.handlers import RotatingFileHandler

# Directory for logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Create logs directory if it doesn't exist

# Define log file paths
SERVER_LOG_FILE = os.path.join(LOG_DIR, "server.log")
MODEL_LOG_FILE = os.path.join(LOG_DIR, "model.log")

def setup_logging():
    """Sets up logging configuration for the application."""
    
    # Create a logger for the server
    server_logger = logging.getLogger("server")
    server_logger.setLevel(logging.INFO)
    
    # Create a file handler for the server logs
    server_handler = RotatingFileHandler(SERVER_LOG_FILE, maxBytes=5*1024*1024, backupCount=2)
    server_handler.setLevel(logging.INFO)
    
    # Create a formatter and set it for the handler
    server_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    server_handler.setFormatter(server_formatter)
    
    # Add the handler to the server logger
    server_logger.addHandler(server_handler)

    # Create a logger for the model
    model_logger = logging.getLogger("model")
    model_logger.setLevel(logging.INFO)
    
    # Create a file handler for the model logs
    model_handler = RotatingFileHandler(MODEL_LOG_FILE, maxBytes=5*1024*1024, backupCount=2)
    model_handler.setLevel(logging.INFO)
    
    # Create a formatter and set it for the handler
    model_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    model_handler.setFormatter(model_formatter)
    
    # Add the handler to the model logger
    model_logger.addHandler(model_handler)

    return server_logger, model_logger
