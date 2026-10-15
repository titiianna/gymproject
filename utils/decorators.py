import functools
from datetime import datetime
from utils.constants import data_path
from utils.file_handler import FileHandler


def log_action(action_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                if isinstance(result, tuple) and len(result) >= 2:
                    detail = f"{result[0]} | {result[1]}"
                else:
                    detail = str(result)
                line = f"{datetime.now():%Y-%m-%d %H:%M:%S} | {action_name} | {detail}\n"
                FileHandler.txt_append(data_path("actions.log"), line)
            except Exception:
                pass
            return result
        return wrapper
    return decorator