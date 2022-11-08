from re import X
from PyPDF2 import PdfFileReader , PdfFileWriter
import os
import time
from numpy import convolve
from dotenv import load_dotenv
from tika import parser
from sqlfunctions import *
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
def getString(paginas,kieszelf):
    '''
    
    :par_paginas: het aantal paginas van de pdf
    '''
    strings=[]
    if kieszelf==False:
        if paginas>25:
            strings.append('70/76A')#omzetcijfer
            strings.append('20/58')#balanstotaal
            strings.append('1001')
            strings.append('1002')
        else:
            strings.append('9900')#omzetcijfer
            strings.append('20/58')#balanstotaal
            strings.append('100')
            strings.append('Bababoey')#niet in gebruik
    else:
        if paginas>25:
            strings.append('9900')#omzetcijfer
            strings.append('20/58')#balanstotaal
            strings.append('100')
            strings.append('Bababoey')#niet in gebruik
        else:
            strings.append('70/76A')#omzetcijfer
            strings.append('20/58')#balanstotaal
            strings.append('1001')
            strings.append('1002')
    return strings
    
def GetinfoPDF(file_path,kieszelf=False):
#
# GetinfoPDF neemt een file_path naar een pdf bestand van een jaarrekening 
# en retourneerd gevraagde info in een array 
# [0]=Omzetcijfer
# [1]=Balanstotaal
# [2]=Aantal werknemers fulltime
# [3]=Aantal werknemers parttime
    '''
    deze functie gaat de .txt van de inhoud van de pdf gaan lezen en de info die we willen er gaan uithalen

    :par_file_path : de locatie van de pdf dat we willen lezen
    :return (list(str)) : de informatie die we nodig hebben uit de inhoud van de pdf 
    '''
    try:
        informatie=['','','','','']
        path = f"{file_path}.txt"
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
                        x.write('Page {0}'.format(page+1))
                        x.write(''.center(100,'-')+'\n')
                        x.write(txt)
                    except:
                        pass
            x.close()
        Strings=getString(int(pdf.getNumPages()),kieszelf)
        string1=Strings[0]
        string2=Strings[1]
        string3=Strings[2]
        string4=Strings[3]
        socialbalans="SOCIALE BALANS"
        #frameworks=["GRI",'IIRC','ISO 26000']
        #models=["B2B","B2C",'B2B2C']
        file = open(path, 'r')
        flag=0
        Flag2=False
        sb=False
        for line in file:
            line=line.rstrip('\n')
            if Flag2==True:
                try:
                    line=line.replace(',','.')
                    line=float(line)
                    informatie[3]=line
                    flag=0
                    Flag2=False
                    continue
                except ValueError:
                    flag=0
                    continue
            if flag==3 and string3=="100" and sb==True and informatie[3]=='':
                try:
                    line=line.replace(',','.')
                    line=float(line)
                    informatie[2]=line
                    Flag2=True
                    continue
                except ValueError:
                    flag=0 
                    continue
            if flag==3:
                if informatie[2]=='' and string3=='1001' and sb==True:
                    try:
                        line=line.replace(',','.')
                        line=float(line)
                        informatie[2]=line
                        flag=0
                        continue
                    except ValueError:
                        flag=0
                        continue
            if flag==4 and sb==True:
                if informatie[3]=='':
                    try:
                        line=line.replace(',','.')
                        line=float(line)
                        informatie[3]=line
                        flag=0
                        continue
                    except ValueError:
                        flag=0
                        continue
            if flag==1 and informatie[0]=='':
                informatie[0]=line
            if flag==2 and informatie[1]=='':
                informatie[1]=line
            flag=0
            if string1==line:
                flag= 1
            if string2==line: 
                flag= 2
            if string3==line:
                flag= 3
            if string4==line:
                flag= 4
            if socialbalans==line:
                sb=True
        file.close()
    except ValueError as err:
        file.close()
        print(err)
        print(file_path)
        print(flag)
        print(line)
        return informatie
    except:
        try:
            file.close()
            print(flag)
            print(line)
            return informatie
        except:
            return informatie
    if os.path.exists(path):
       os.remove(path)
    if informatie[0]=="" and informatie[1]=="" and informatie[2]!="" and kieszelf==False:
        return GetinfoPDF(file_path,True)
    return informatie
