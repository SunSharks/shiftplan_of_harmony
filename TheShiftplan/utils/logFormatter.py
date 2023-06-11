"""Custom Formatter for logging.

logging.info("Test Info")
logging.warning("Test Warning")
logging.error("Test Error")
logging.critical("Test Critical")
try:
    raise Exception("Test Exception")
except Exception as exce:
    logging.exception(exce)
"""

import logging

try:
    from colorama import Fore, Back, Style
except ImportError:
    class Fore:
        """Dummy Fore class."""

        BLACK = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""
        RESET = ""

    class Back(Fore):
        """Dummy Back class."""

        pass

    class Style:
        """Dummy Style class."""

        RESET_ALL = ""
        DIM = ""
        NORMAL = ""
        BRIGHT = ""


class LogFormatter(logging.Formatter):
    """Custom Formatter class."""

    format_short = "%(asctime)s | %(threadName)10s | %(levelname)9s | "
    format_short = "%(asctime)s | %(levelname)9s | "
    format_mid = format_short + "%(module)s:%(funcName)s | "
    format_long = format_short + "%(filename)s: %(lineno)d | "
    format_long_end = "\n%(module)s:%(funcName)s @ %(pathname)s:%(lineno)d\n"

    message = "%(message)s"

    FORMATS = {
        logging.DEBUG:
            Fore.WHITE +
            Back.BLACK +
            Style.DIM +
            format_long +
            message +
            # format_long_end +
            Style.RESET_ALL,
        logging.INFO:
            Fore.GREEN +
            Back.BLACK +
            Style.NORMAL +
            format_short +
            message +
            Style.RESET_ALL,
        logging.WARNING:
            Fore.YELLOW +
            Back.BLACK +
            Style.NORMAL +
            format_mid +
            message +
            Style.RESET_ALL,
        logging.ERROR:
            Fore.RED +
            Back.BLACK +
            Style.NORMAL +
            format_mid +
            message +
            Style.RESET_ALL,
        logging.CRITICAL:
            Fore.RED +
            Back.YELLOW +
            Style.BRIGHT +
            format_mid +
            message +
            Style.RESET_ALL,
    }

    def format(self, record):
        """Actually format log messages."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
