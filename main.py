#! -*- coding:utf-8 -*-
from multiprocessing import Process, Queue

def f(q, msg):
    q.put([42, None, 'hello', msg])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q, "test"))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()