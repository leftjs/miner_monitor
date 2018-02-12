#-*- coding:utf-8 -*-
import subprocess
import xmltodict
import json
import psutil
from log import info
import time

NVSMI_path = 'C:\\Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe'


class GPU_INFO():
    def __init__(self, d):
        self.bus_id = int(d['pci']['pci_bus'])
        self.name = d['product_name']
        self.fan_speed = int(d['fan_speed'].replace('%', ''))  # %
        self.usage = int(d['utilization']['gpu_util'].replace('%', ''))  # %
        self.current_temp = int(
            d['temperature']['gpu_temp'].replace('C', ''))  # C
        self.current_graphics_clock = int(
            d['clocks']['graphics_clock'].replace('MHz', ''))  # Mhz
        self.max_graphics_clock = int(
            d['max_clocks']['graphics_clock'].replace('MHz', ''))  # Mhz
        self.current_mem_clock = int(
            d['clocks']['mem_clock'].replace('MHz', ''))  # Mhz
        self.max_mem_clock = int(
            d['max_clocks']['mem_clock'].replace('MHz', ''))  # Mhz

    def __str__(self):
        return "bus_id is %d, %s's fan speed is %d%%, current usage is %d%%, current temperature is %dC current and max graphics_clock is %dMHz / %dMHz, current and max mem_clock is %dMHz / %dMHz" % (self.bus_id, self.name, self.fan_speed,
                                                                                                                                                                                                        self.usage, self.current_temp, self.current_graphics_clock, self.max_graphics_clock,
                                                                                                                                                                                                        self.current_mem_clock, self.max_mem_clock)

    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# print("miner path is '%s'" %miner_path)

info_dict = xmltodict.parse(subprocess.check_output([NVSMI_path, '-q', '-x']))
info_str = json.dumps(info_dict, indent=4)
info_json = json.loads(info_str)

# with open('./stat.json', 'w') as outfile:
#     outfile.write(info_str)


def get_gpu_report():
    gpu_count = int(info_json['nvidia_smi_log']['attached_gpus'])
    gpu_infos = info_json['nvidia_smi_log']['gpu']
    gpus = []
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for g in gpu_infos:
        gpu = GPU_INFO(g)
        gpus.append(gpu)
        # print(gpu)
    return (gpu_count, current_time, gpus)


if __name__ == '__main__':
    gpu_count, current_time, gpus = get_gpu_report()

    gpu_strings = []
    for gpu in gpus:

        gpu_string = ','.join([str(value)
                               for key, value in gpu.__dict__.items()])
        gpu_strings.append(gpu_string)
    gpus_string = ','.join(gpu_strings)
    data = ','.join(map(str, [gpu_count, current_time, gpu_strings]))

    print(data)
