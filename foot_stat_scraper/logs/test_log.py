from loggers import debug_log, info_log, err_log


def main():
    debug_log('debug')
    info_log('info')
    try:
        'fdsfsd' - 10
    except Exception:
        err_log('error')


if __name__ == '__main__':
    main()
