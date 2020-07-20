import logging
import logging.config
from settings import logger_config


logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')
logging.basicConfig(level=logging.INFO)


def main():
    logger.info('Hello world')


if __name__ == '__main__':
    main()
