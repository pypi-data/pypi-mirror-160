import logging


def get_logger(name: str):
    ''' basic log'''
    _log = logging.getLogger(name)
    _log.propagate = False
    _log.setLevel(logging.DEBUG)
    if len(_log.handlers) == 0:
        stream_handler = logging.StreamHandler()
        format_str = '%(levelname)-7s | %(message)s'
        formatter = logging.Formatter(format_str)
        stream_handler.setFormatter(formatter)
        _log.addHandler(stream_handler)

    return _log
