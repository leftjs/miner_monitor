import time


def log(log_type, msg):
    print('%s [%s] --->> %s' %
          (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), log_type, msg))


def info(msg):
    log('INFO', msg)


def error(msg):
    log('ERROR', msg)
