import logging as log


class Logger:
    """Class Config For Logger"""

    def __init__(
        self,
        log_level: int = log.INFO,
    ):
        self.logger = log.getLogger("")
        self.logger.setLevel(log_level)

        # Console handler
        self.console_handler = log.StreamHandler()
        self.console_handler.setFormatter(
            log.Formatter(
                "%(levelname)s - %(asctime)s - %(message)s  [%(lineno)d]"
            )
        )
        self.logger.addHandler(self.console_handler)

    def get_logger(self):
        return self.logger


logging = Logger().get_logger()
