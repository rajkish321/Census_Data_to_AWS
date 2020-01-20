#This creates the CSV files from the inflow and outflow excel files
from xlsx2csv import Xlsx2csv
import os

base_dir = os.path.dirname(os.path.dirname(__file__))


inflow_path = base_dir + r"/flows/inflow.xlsx"
csv_in = base_dir + r"/flows/in"
outflow_path = base_dir + r"/flows/outflow.xlsx"
csv_out = base_dir + r"/flows/out"

print("start")

Xlsx2csv(inflow_path, escape_strings=True,outputencoding="utf-8").convert(csv_in, sheetid=0) #sheetid = 0 means convert all sheets
Xlsx2csv(outflow_path, escape_strings=True, outputencoding="utf-8").convert(csv_out, sheetid=0) #sheetid = 0 means convert all sheets
print("end")
