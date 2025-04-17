#!/home/xfel/xfelopr/local/anaconda3/bin/python3

import multiprocessing
import random
import time

def produce(queue):
  for i in range(10):
    queue.put(i)
    time.sleep(random.randint(1, 5))

def consume(queue):
  for i in range(10):
    n = queue.get()
    print(n)
    time.sleep(random.randint(1, 5))

if __name__ == '__main__':
  queue = multiprocessing.Queue()
  
  p0 = multiprocessing.Process(target=produce, args=(queue,))
  p1 = multiprocessing.Process(target=produce, args=(queue,))
  c0 = multiprocessing.Process(target=consume, args=(queue,))
  c1 = multiprocessing.Process(target=consume, args=(queue,))
  
  p0.start()
  p1.start()
  c0.start()
  c1.start()
  
  p0.join()
  p1.join()
  c0.join()
  c1.join()
