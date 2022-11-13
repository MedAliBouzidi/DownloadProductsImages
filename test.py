import threading
from time import sleep


class D:
    def fn(self):
        sleep(2)
        print(f'index {self.label}\n')

    def __init__(self, label):
        self.label = label
        t = threading.Thread(target=self.fn)
        t.start()


for i in range(1, 5):
    D(i)
