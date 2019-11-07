import subprocess
import threading

__author__ = 'engine'

class LimiterThread(threading.Thread):

    def __init__(self, pid, peer_limit):
        threading.Thread.__init__(self)
        self.pid = pid
        self.peer_limit = peer_limit

    def run(self):
        p = subprocess.Popen("cpulimit -p "+self.pid+" -l "+str(self.peer_limit)+"", shell=True, stdout=subprocess.PIPE)
        p.communicate()