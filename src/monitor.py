import psutil
from os import path, system
import time
import subprocess
from log import info
from subprocess import DEVNULL

miner_path = '%s\\AppData\\Local\\Programs\\NiceHash Miner 2\\NiceHash Miner 2.exe' % (
    path.expanduser('~'))
print(miner_path)
miner_name = 'NiceHash Miner 2.exe'
retry_times = 0  # 重试次数

# 检查miner是否正在运行


def check_miner_isrunnig():
    for proc in psutil.process_iter():
        if proc.name() == miner_name:
            return True
        else:
            continue
    return False


def check_and_run():
    # retry_times = 0 # 重试次数
    global retry_times
    while True:
        if retry_times > 10:
            info('系统将在10秒钟后重启.....')
            time.sleep(10)
            system('reboot')
        status = check_miner_isrunnig()
        if status is True:
            info('程序正在运行')
            time.sleep(10)
        else:
            subprocess.Popen(miner_path, stdout=DEVNULL)
            retry_times += 1
            info('当前miner已重启%d次, 10次后将重启电脑' % retry_times)
            time.sleep(30)


if __name__ == '__main__':
    check_and_run()
