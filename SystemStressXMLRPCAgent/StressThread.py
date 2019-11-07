import threading
import subprocess
import psutil
import re

__author__ = 'engine'

class StressThread(threading.Thread):

    def __init__(self, memStress):
        threading.Thread.__init__(self)
        self.memStress = memStress

    def run(self):
        mem_info = repr(psutil.virtual_memory())
        mem_info_arr = re.split(',', mem_info)
        used_mem_perc = re.split('=', mem_info_arr[2])
        used_mem_perc = float(used_mem_perc[1])
        tot_mem_byte = re.split('=', mem_info_arr[0])
        tot_mem_byte = str(tot_mem_byte[1])
        tot_mem_byte = re.split('L', tot_mem_byte)
        tot_mem_byte = float(tot_mem_byte[0])
        if self.memStress >= used_mem_perc:
            mem_to_stress = int(tot_mem_byte * (self.memStress - used_mem_perc)/100)
            print(str(mem_to_stress))
            p = subprocess.Popen("stress --cpu 1 --vm-bytes "+str(mem_to_stress)+" --vm-keep -m 1 &", shell=True, stdout=subprocess.PIPE)
        else:
            p = subprocess.Popen("stress --cpu 1", shell=True, stdout=subprocess.PIPE)
        p.communicate()