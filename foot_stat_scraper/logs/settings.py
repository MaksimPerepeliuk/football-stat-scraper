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
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'std_format',
            'filename': 'foot_stat_scraper/logs/info.log',
            'encoding': 'utf8',
            'mode': 'w'
        },
        'debug_file_handler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
            'filename': 'foot_stat_scraper/logs/debug.log',
            'encoding': 'utf8',
            'mode': 'w'
        },
        'error_file_handler': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'std_format',
            'filename': 'foot_stat_scraper/logs/error.log',
            'encoding': 'utf8',
            'mode': 'w'
        }
    },
    'loggers': {
        'debug_logger': {
            'level': 'DEBUG',
            'propagate': 'no',
            'handlers': ['debug_file_handler', 'error_file_handler'],
        },
        'info_logger': {
            'level': 'INFO',
            'handlers': ['info_file_handler'],
        },
        'error_logger': {
            'level': 'ERROR',
            'handlers': ['error_file_handler'],
        },
    },
}
