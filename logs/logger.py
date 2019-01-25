from datetime import datetime as dt


def log(text, error=False):
    log_file = 'logs/error.log' if error else 'logs/tagbox.log'
    with open(log_file, 'a') as l:
        l.write('{} {}'.format(dt.now(), text))

