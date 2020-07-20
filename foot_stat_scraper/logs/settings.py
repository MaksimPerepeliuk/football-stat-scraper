logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': ('# %(levelname)-8s %(filename)s'
                       '[LINE:%(lineno)d]'
                       '[%(asctime)s] %(message)s'),
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format'
        },
        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'std_format',
            'filename': 'foot_stat_scraper/logs/info.log',
            'encoding': 'utf8'
        },
        'debug_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
            'filename': 'foot_stat_scraper/logs/debug.log',
            'encoding': 'utf8'
        },
        'warn_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARN',
            'formatter': 'std_format',
            'filename': 'foot_stat_scraper/logs/warn.log',
            'encoding': 'utf8'
        },
        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'std_format',
            'filename': 'foot_stat_scraper/logs/error.log',
            'encoding': 'utf8'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['info_file_handler'],
        },
    },
}
