import threading
import xmlrpclib

__author__ = 'engine'

class CallWorkerThread(threading.Thread):

    def __init__(self, stressWorker, cpuStress, memStress, killTimeout):
        threading.Thread.__init__(self)
        self.stressWorker = stressWorker
        self.cpuStress = cpuStress
        self.memStress = memStress
        self.killTimeout = killTimeout

    def run(self):
        print("Starting On "+self.stressWorker)
        server = xmlrpclib.ServerProxy("http://"+self.stressWorker+":8000")
        multi = xmlrpclib.MultiCall(server)
        multi.do_run(self.cpuStress, self.memStress, self.killTimeout)
        multi.do_kill(self.killTimeout)
        for response in multi():
            print(str(response))