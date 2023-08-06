import logging
import os
import datetime

def logger():
    class LoggerHandler:
        _logger_level = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING,
                         'error': logging.ERROR, 'critical': logging.CRITICAL}

        def __init__(self, log_name, file_name, logger_level, stream_level='info', file_level='warning'):
            self.log_name, self.file_name, self.logger_level, self.stream_level, self.file_level = log_name, file_name, self._logger_level.get(
                logger_level, 'debug'), self._logger_level.get(stream_level, 'info'), self._logger_level.get(file_level,
                                                                                                             'warning')
            self.logger = logging.getLogger(self.log_name)
            self.logger.setLevel(self.logger_level)
            if not self.logger.handlers:
                f_stream, f_file = logging.StreamHandler(), logging.FileHandler(self.file_name, encoding='utf-8')
                f_stream.setLevel(self.stream_level)
                f_file.setLevel(self.file_level)

                # set log output stream, or"%(asctime)s %(name)s %(levelname)s %(message)s", see more setting in "formater"
                formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
                f_stream.setFormatter(formatter)
                f_file.setFormatter(formatter)
                self.logger.addHandler(f_stream)
                self.logger.addHandler(f_file)

        @property
        def get_logger(self):
            return self.logger

    log_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    log_file_name = os.path.join(log_folder, datetime.datetime.now().strftime('%Y-%m-%d') + '.log')
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    return LoggerHandler(log_name="DEFAULT", logger_level='debug', file_name=log_file_name, stream_level='debug',
                         file_level='info').get_logger


log = logger()
