from logging import LogRecord, Handler
import logging

from loralogger.utils import separate_log_data


class LogToESHandler(Handler):
    def __init__(self, label: str) -> None:
        super().__init__()

        self.label = label

    def write_log(self, level: str, log_content: dict, extra_data: dict) -> None:
        from loralogger.producer import worker

        try:
            worker.send_task(
                "logger.tasks.write_log",
                queue="logger",
                args=(
                    self.label,
                    level,
                    log_content,
                    extra_data,
                ),
            )
        except Exception:
            logging.critical("Cannot write log")

    def emit(self, record: LogRecord) -> None:
        # get main and extra data from the log record
        main_data, extra_data = separate_log_data(record.__dict__)

        self.write_log(record.levelname, main_data, extra_data)
