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
def upload(file_path,dest,odm):
    GetDataPDF(file_path,dest)
    pdftext=datatxt(dest)
    insertRawPDF(odm, pdftext)
def main():
    print("geef een pad naar een map met pdf's:")
    path=input()
    pdfs= os.listdir(path)
    with ProcessPoolExecutor(max_workers=8) as executer:
        for file in pdfs:
                ondernemingsnummer=file
                executer.submit(upload,path+file+".pdf",path+file+".txt",ondernemingsnummer)
if __name__ == '__main__':
    main()
    #print("Z:\PDFS\\"+file)
    #print("Z:\TXT\\"+file+".txt")
    #GetDataPDF("Z:\PDFS\\"+file,"Z:\TXT\\"+file+".txt")
    