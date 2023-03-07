import logging


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def get_process_logger(name):
    logger = logging.getLogger(name)
    logging.getLogger().handlers.clear()
    # %(processName)s %(threadName)s
    formate = "%(asctime)s %(name)s (%(processName)s) | %(levelname)s - %(message)s"

    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomFormatter(formate))
    stream_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"Logs/logs/{name}.log")
    file_handler.setFormatter(logging.Formatter(formate, "%Y-%m-%d %H:%M:%S"))
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


def get_logger(name):
    logger = logging.getLogger(name)
    logging.getLogger().handlers.clear()

    formate = "%(asctime)s %(name)s | %(levelname)s - %(message)s"

    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomFormatter(formate))
    stream_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"Logs/logs/{name}.log")
    file_handler.setFormatter(logging.Formatter(formate, "%Y-%m-%d %H:%M:%S"))
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
