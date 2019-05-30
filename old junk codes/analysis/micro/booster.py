import threading
import time
import queue


class booster:
    # input: neurons ,training parameters
    # output: neurons finished training
    param = {
        "cycles": 20,
        "limit": 20,
        "threads": 10
    }

    def __init__(self, param=None):
        if not (param is None):
            booster.param = param

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

            task[0].build(self.param["limit"],
                          self.param["cycles"])
            nid = task[0].load()
            task[1](nid)
