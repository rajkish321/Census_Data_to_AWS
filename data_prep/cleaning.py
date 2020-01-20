import re
import csv
import os

#base_dir = r'C:/Users/rajki/Documents/JP_Morgan_assignment/final_submit/' #user needs to change
base_dir = os.path.dirname(os.path.dirname(__file__))



csv_in = base_dir + r"/flows/in"
csv_out = base_dir + r"/flows/out"

#this is to clean the data of headers and footnotes


print("start cleaning csv files")
for file in os.listdir(csv_in):     #this is cleaning the inflow files
    if file.endswith(".csv"):
        input_ = open(os.path.join(csv_in, file),'rt')
        output = open(os.path.join(csv_in, 'temp.csv'),'w',newline='')

        writer = csv.writer(output)
        reader = csv.reader(input_)

        for row in reader:

            if len(row) > 0 and re.search('\D',row[0]) is None and row[0] is not '':
                #print(row)
                writer.writerow(row)


        input_.close()
        os.remove(os.path.join(csv_in, file))

        output.close()
        os.rename(os.path.join(csv_in, 'temp.csv'),os.path.join(csv_in, file))




for file in os.listdir(csv_out):    #this is cleaning the outflow files
    if file.endswith(".csv"):

        input_ = open(os.path.join(csv_out, file),'rt')
        output = open(os.path.join(csv_out, 'temp.csv'),'w',newline='')

        writer = csv.writer(output)
        reader = csv.reader(input_)

        for row in reader:

            if len(row) > 0 and re.search('\D',row[0]) is None and row[0] is not '':
                #print(row)
                writer.writerow(row)


        input_.close()
        os.remove(os.path.join(csv_out, file))

        output.close()
        os.rename(os.path.join(csv_out, 'temp.csv'),os.path.join(csv_out, file))


print("done cleaning csv files")
