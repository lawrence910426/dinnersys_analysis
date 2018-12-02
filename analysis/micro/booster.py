import threading
import time
import queue


class booster:
    # input: neurons ,training parameters
    # output: neurons finished training
    threads = 300
    param = {
        "cycles": 1000,
        "precision": 0.00001,
        "alpha": 0.0001,
        "threads": 3
    }

    def __init__(self, param=None):
        self.task = queue.Queue()
        for i in range(self.param["threads"]):
            t = threading.Thread(target=self.run)
            t.start()

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
