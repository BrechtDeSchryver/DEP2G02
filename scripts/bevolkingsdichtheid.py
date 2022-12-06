from sqlfunctions import insert_bevolkingsdichtheid
import csv
def main():
    # reading csv file
    with open('./data/bevolkingsdichtheid.csv', 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        
        # extracting field names through first row
        fields = next(csvreader)
    
        # extracting each data row one by one
        for row in csvreader:
            print(f"insterting: {row[0]},{row[1]}")
            insert_bevolkingsdichtheid(row[0],row[1])
            #print(row)
            
        
        

if __name__ == "__main__":
    main()