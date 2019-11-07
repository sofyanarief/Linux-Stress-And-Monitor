import logging
import socket
import subprocess
import time
from SimpleXMLRPCServer import SimpleXMLRPCServer
from LimiterThread import LimiterThread
from StressThread import StressThread
from SysMonThread import SysMonThread

__author__ = 'engine'

class SystemStressXMLRPCAgent:

    def __init__(self):
        self.cpuStress = 0
        self.memStress = 0
        self.killTimeout = 0

    def do_run(self, cpuStress, memStress, killTimeout):
        self.cpuStress = cpuStress
        self.memStress = memStress
        self.killTimeout = killTimeout
        self.do_stress()
        time.sleep(2)
        self.do_monitor(killTimeout)
        self.do_limitCPU()

    def do_stress(self):
        stressCPU_thr = StressThread(self.memStress)
        stressCPU_thr.start()

    def do_monitor(self, killTimeout):
        sysmon_thr = SysMonThread(killTimeout)
        sysmon_thr.start()

    def do_limitCPU(self):
        limiterThreadArr = []
        pid = ((self.do_searchPIDOfStress())[0]).split()
        print(len(pid))
        print(pid)
        if len(pid) > 0:
            idx = 0
            sum_pid = len(pid)-1
            peer_limit = float(self.cpuStress / sum_pid)
            print(peer_limit)
            for i in pid:
                if idx > 0:
                    limiterThreadArr.append(LimiterThread(i, peer_limit))
                idx += 1

        for j in range(0, len(limiterThreadArr)):
            limiterThreadArr[j].start()

    def do_searchPIDOfStress(self):
        p = subprocess.Popen("pgrep stress", shell=True, stdout=subprocess.PIPE)
        return p.communicate()

    def do_kill(self,killTimeout):
        time.sleep(killTimeout)
        p = subprocess.Popen("killall stress", shell=True, stdout=subprocess.PIPE)
        p.communicate()

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

logging.basicConfig(filename=IPAddr+'_run.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
server = SimpleXMLRPCServer((IPAddr, 8001), logRequests=True, allow_none=True);
server.register_multicall_functions()
server.register_instance(SystemStressXMLRPCAgent())

try:
    print('Use Control-C to exit')
    print('Your Computer IP Address is:' + IPAddr)
    logging.debug('Your Computer IP Address is:' + IPAddr)
    server.serve_forever()
except KeyboardInterrupt:
    print('Exiting')