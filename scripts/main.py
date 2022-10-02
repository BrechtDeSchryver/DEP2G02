import os
import time
from numpy import convolve
from PDFReader import GetDataPDF
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from threading import BoundedSemaphore

class BoundedExecutor:
    def __init__(self, bound, max_workers):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.semaphore = BoundedSemaphore(bound + max_workers)

    def submit(self, fn, *args, **kwargs):
        self.semaphore.acquire()
        try:
            future = self.executor.submit(fn, *args, **kwargs)
        except:
            self.semaphore.release()
            raise
        else:
            future.add_done_callback(lambda x: self.semaphore.release())
            return future

    def shutdown(self, wait=True):
        self.executor.shutdown(wait)
def main():
    pdfs= os.listdir("Z:\PDFS")
    with ProcessPoolExecutor(max_workers=8) as executer:
        for file in pdfs:
                executer.submit(GetDataPDF,"Z:\PDFS\\"+file,"Z:\TXT\\"+file+".txt")
if __name__ == '__main__':
    main()
    #print("Z:\PDFS\\"+file)
    #print("Z:\TXT\\"+file+".txt")
    #GetDataPDF("Z:\PDFS\\"+file,"Z:\TXT\\"+file+".txt")
    