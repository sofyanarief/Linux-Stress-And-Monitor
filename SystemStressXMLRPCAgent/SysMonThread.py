from datetime import datetime
import threading
import time
import psutil
import logging
import re
import sqlite3

__author__ = 'engine'

class SysMonThread(threading.Thread):

    def __init__(self, killTimeout):
        threading.Thread.__init__(self)
        self.killTimeout = killTimeout

    def run(self):
        logging.debug('Log Monitor Mulai')
        while self.killTimeout > 0:
            if (self.killTimeout - 1) <= 0:
                logging.debug('Log Monitor Terakhir')
            curCPU = str(self.get_CPU_Load())
            curRAM = str(self.get_RAM_Used())
            curDate = time.strftime("%x %X")
            print(curDate+" "+curCPU+" "+curRAM)
            conn = sqlite3.connect('sysmon.sqlite')
            c = conn.cursor()
            c.execute("INSERT INTO sysmon VALUES('"+curDate+"','"+curCPU+"','"+curRAM+"')")
            if (self.killTimeout - 1) <= 0:
                c.execute("INSERT INTO sysmon VALUES('0000','0000','0000')")
            conn.commit()
            conn.close()
            print("hohoho")
            self.killTimeout -= 1

    def get_CPU_Load(self):
        cpuLoad = repr(psutil.cpu_percent(interval=1, percpu=False))
        # logging.debug('CPU Load = %s', cpuLoad)
        return cpuLoad

    def get_RAM_Used(self):
        mem_info = repr(psutil.virtual_memory())
        mem_info_arr = re.split(',', mem_info)
        used_mem_perc = re.split('=', mem_info_arr[2])
        used_mem_perc = used_mem_perc[1]
        # logging.debug('RAM Load = %s', used_mem_perc)
        return used_mem_perc