import gc
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def debug_memory_usage():
    """
    Log memory usage information.
    """
    memory_info = gc.get_stats()
    logging.debug(f"Memory usage info: {memory_info}")

def error_handler(func):
    """
    Decorator to handle errors and log them.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error occurred in function {func.__name__}: {e}")
            return None
    return wrapper