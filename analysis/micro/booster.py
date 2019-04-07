import threading
import time
import queue


class booster:
    # input: neurons ,training parameters
    # output: neurons finished training
    param = {
        "cycles": 3000,
        "precision": 0.00001,
        "alpha": 0.1,
        "threads": 30
    }

    def __init__(self, param=None):
        self.task = queue.Queue()
        t = {}
        for i in range(self.param["threads"]):
            t[i] = threading.Thread(target=self.run)
            t[i].start()
        self.threads = t

    def queue(self, task):
        self.task.put(task)

    def run(self):
        while True:
            if self.task.empty():
                time.sleep(3)
            task = self.task.get()

            task[0].build(self.param["alpha"],
                          self.param["cycles"],
                          self.param["precision"])
            nid = task[0].load()
            task[1](nid)
