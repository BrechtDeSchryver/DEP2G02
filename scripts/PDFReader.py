from re import X
from PyPDF2 import PdfFileReader , PdfFileWriter
import os
import time
from numpy import convolve


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
    
def GetinfoPDF(file_path,kieszelf=False):
    '''
    deze functie gaat de .txt van de inhoud van de pdf gaan lezen en de info die we willen er gaan uithalen

    :par_file_path : de locatie van de pdf dat we willen lezen
    :return (list(str)) : de informatie die we nodig hebben uit de inhoud van de pdf 
    '''
    try:
        informatie=['','','','null','B2B/B2C']
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
        frameworks=["GRI",'IIRC','ISO 26000']
        models=["B2B","B2C",'B2B2C']
        file = open(path,'r')
        flag=0
        sb=False
        werknemerstotaal=0
        for line in file:
            line=line.rstrip('\n')
            if (flag==3 and werknemerstotaal!=0)and string3=="100" and sb==True:
                    try:
                        line=line.replace(',','.')
                        line=float(line)
                        werknemerstotaal=werknemerstotaal+line
                        informatie[0]=werknemerstotaal
                        flag=0
                        continue
                    except ValueError:
                        flag=0
                        continue
            if flag==3:
                if informatie[0]=='' and string3=='1001' and sb==True:
                    try:
                        line=line.replace(',','.')
                        line=float(line)
                        werknemerstotaal=line
                        flag=0
                        continue
                    except ValueError:
                        flag=0
                        continue
                elif string3=='100'and werknemerstotaal==0 and sb==True:
                    try:
                        line=line.replace(',','.')
                        line=float(line)
                        werknemerstotaal=line
                        continue
                    except ValueError:
                        flag=0 
                        continue
            if flag==4 and sb==True:
                if informatie[0]=='':
                    try:
                        line=line.replace(',','.')
                        line=float(line)
                        werknemerstotaal+=line
                        informatie[0]=werknemerstotaal
                        flag=0
                        continue
                    except ValueError:
                        informatie[0]=werknemerstotaal
                        flag=0
                        continue
            if flag==1 and informatie[1]=='':
                informatie[1]=line
            if flag==2 and informatie[2]=='':
                informatie[2]=line
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
            for framework in frameworks:
                i=KMPSearch(str(" "+framework+" "),line)
                if i!=-1 or line==framework:
                    informatie[3]=framework
            for model in models:
                if model==line:
                    informatie[4]=model
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

def GetAllData(file_path):
    '''
    maakt .txt met alle data van de pdf in 

    :par_file_path : de locatie van de pdf
    :return (list) : list met alle data van de pdf 
    '''
    path = GetDataPDF(file_path)
    file = open(path,'r')
    x=[]
    for line in file:
        line=line.rstrip('\n')
        x.append(line)
    file.close()
    if os.path.exists(path):
        os.remove(path)
    return x
def zoekmachinePDF(file_path):
    '''
    deze functie gaat gaat de combinatie van Zoekterm1 en Zoekterm2 zoeken in de pdf binnen een range van 20 woorden

    :par_file_path: de locatie van de pdf 
    :return(list(int,int)): gaat het aantal keren dat Zoekterm1 en Zoekterm 2 binnen een range van 20 voorkomen geven
                          : en gaat de average afstand tussen Zoekterm 1 en 2 geven 
    '''
    ZOEKTERMEN={
        'Zoekterm1':['duurzaamheid','duurzame','duurzaamheidsstrategie','duurzaam'],
        'Zoekterm2':['strategie','strategisch','strategische','strategieën']
    }
    data=GetAllData(file_path)
    i=0
    combinatie=0
    averagewoorden=[]
    a=0
    zoekterm1=False
    for line in data:
        for zoekterm in ZOEKTERMEN['Zoekterm1']:
            if zoekterm in line:
                zoekterm1=True
        if zoekterm1==True:
            i+=1
            for zoekterm in ZOEKTERMEN['Zoekterm2']:
                if zoekterm in line:
                    averagewoorden.append(i)
                    combinatie+=1
                    zoekterm1=False
                    i=0
        if i==20:
            i=0
    if combinatie!=0:
        b=len(averagewoorden)
        for value in averagewoorden:
            a+=value/b
    return [combinatie,a]