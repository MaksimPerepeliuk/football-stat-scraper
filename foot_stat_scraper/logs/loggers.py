import logging
import logging.config
from settings import logger_config


logging.config.dictConfig(logger_config)
debug_log = logging.getLogger('debug_logger').debug
info_log = logging.getLogger('info_logger').info
err_log = logging.getLogger('error_logger').exception
