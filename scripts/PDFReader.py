from re import X
from PyPDF2 import PdfFileReader , PdfFileWriter
import os
import time
from numpy import convolve
from dotenv import load_dotenv
from tika import parser
load_dotenv()

USER=os.getenv("DBUSER")
PASSWORD=os.getenv("DBPASSWD")

def datatxt(file_path):
    '''
    deze functie upload de inhoud van de pdf naar de database
    :par_file_path: de locatie van de pdf
    '''
    with open(file_path,'r') as file:
        data=file.read()
    file.close()
    if os.path.exists(file_path):
        os.remove(file_path)
    return data
def GetDataPDF(file_path,dest):



    '''
    deze functie maakt een .txt van de inhoud van de pdf zodat het mooi leesbaar is
    :par_file_path = de exacte locatie van de pdf
    '''
    path = dest
    pdf = PdfFileReader(file_path)
    with open(path, 'w') as x:
        for page in range(pdf.numPages):
            pageObj=pdf.getPage(page)
            try:
                txt = pageObj.extractText()
            except:
                pass
            else:
                try:
                    x.write(txt)
                except:
                    pass
        x.close()
    return path
def GetDataPDF2(file_path):
    raw = parser.from_file(file_path)
    content=raw['content']
    content=content.replace("\n",' ')
    return content
