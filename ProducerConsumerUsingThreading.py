import concurrent.futures
import logging
import queue
import random
import threading
import time

def JobInputQueue(queue, event):
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("new job got added: %s", message)
        queue.put(message)
        time.sleep(1)

    logging.info("JobInputQueue received event. Exiting")

def JobOutputQueue(queue, event):
    while not event.is_set() or not queue.empty():
        message = queue.get()
        logging.info( "jobs submitted for execution: %s (size=%d)", message, queue.qsize())
        time.sleep(2)
    logging.info("JobOutputQueue received event. Exiting")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    pipeline = queue.Queue(0)
    event = threading.Event()
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(JobInputQueue, pipeline, event)
            executor.submit(JobOutputQueue, pipeline, event)
            time.sleep(1)

    logging.info("Main: about to set event")
    event.set()
