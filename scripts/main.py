from PDFReader import *
import os
def main():
    path="D:/shared"
    pdfs= os.listdir(path)
    for file in pdfs:
        file_path=path+'/'+file
        odm=file.split('_')[1]
        print(GetinfoPDF(file_path))

if __name__ == "__main__":
    main()