import inspect
import logging
import sys
from datetime import date, datetime


class StdoutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.INFO


def init_logging():
    root_logger = logging.getLogger()
    root_logger.handlers = []
    root_logger.filters = []
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.addFilter(StdoutFilter())
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)
    root_logger.addHandler(stderr_handler)


def get_params_log_generator(func, args, kwargs, param_ignore=None):
    log_config = {
        int: lambda x: str(x),
        float: lambda x: str(x),
        date: lambda x: str(x),
        datetime: lambda x: str(x),
        bool: lambda x: str(x),
        str: lambda x: x if len(x) <= 20960 else None
    }

    args_name = inspect.getfullargspec(func)[0][1:len(args) + 1]

    if len(args_name) == len(args):
        original_args_dict = dict(zip(args_name, args))
    else:
        original_args_dict = {f'arg_{i + 1}': args[i] for i in range(len(args))}

    args_dict = dict()
    param_i = 0
    for k, v in {**original_args_dict, **kwargs}.items():
        if type(v) not in log_config:
            continue
        str_v = log_config[type(v)](v)
        if str_v is None:
            continue
        if param_ignore is not None and param_i == param_ignore:
            continue
        args_dict[k] = str_v
        param_i += 1

    return lambda status: f'op={func.__name__} | status={status} | params={args_dict}'


def logger(func):
    def wrapper(*args, **kwargs):
        params_log_generator = get_params_log_generator(func, args, kwargs)
        logging.info(params_log_generator('start'))
        try:
            res = func(*args, **kwargs)
            logging.info(params_log_generator('success'))
            return res
        except Exception as e:
            logging.info(params_log_generator('fail'))
            raise e

    return wrapper


init_logging()
