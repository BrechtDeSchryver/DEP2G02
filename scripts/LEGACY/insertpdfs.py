import os
import time
from numpy import convolve
from PDFReader import *
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from threading import BoundedSemaphore
from sqlfunctions import *
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

def upload(file_path,odm,nbbID):
    insertRawPDF(odm, GetDataPDF2(file_path))
    inertNBBID(odm, nbbID)

def main():
    path="D:/shared"
    pdfs= os.listdir(path)
    a=0
    for file in pdfs:
        a=a+1
        if a>10465:
            file_path=path+'/'+file
            odm=file.split('_')[1]
            nbbID=file.split('_')[2].split('.')[0]
            print(odm+" : " )
            upload(file_path,odm,nbbID)
        print(a)
if __name__ == '__main__':
    main()

    