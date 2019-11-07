import thread
from CallWorkerThread import CallWorkerThread

__author__ = 'engine'

class SystemStressXMLRPCCaller:

    def __init__(self):
        self.stress_worker = ['10.0.0.11']
        self.cpuStress = [50.0]
        self.memStress = [80.0]
        self.killTimeout = 10

    def do_run(self):
        callWorkerThreadArr = []
        for i in range(0, len(self.stress_worker)):
            callWorkerThreadArr.append(CallWorkerThread(self.stress_worker[i], self.cpuStress[i], self.memStress[i],self.killTimeout))
        for j in range(0, len(callWorkerThreadArr)):
            callWorkerThreadArr[j].start()

try:
    print 'Use Control-C to exit'
    MyClass = SystemStressXMLRPCCaller()
    MyClass.do_run()
except KeyboardInterrupt:
    print 'Exiting'