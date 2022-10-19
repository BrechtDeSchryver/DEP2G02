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
    path="C:/testpdf"
    pdfs= os.listdir(path)
    for file in pdfs:
        file_path=path+'/'+file
        odm=file.split('_')[1]
        nbbID=file.split('_')[2].split('.')[0]
        print(odm)
        print(nbbID)
        upload(file_path,odm,nbbID)
if __name__ == '__main__':
    main()

    