#make sure you are connected to your aws account before running this
import boto3
import os

#base_dir = r'C:/Users/rajki/Documents/JP_Morgan_assignment/final_submit/' #user needs to change
base_dir = os.path.dirname(os.path.dirname(__file__))

bucketname_in = ''
bucketname_out = ''

#bucketname_in = 'census-data/census-inflow-data'
#bucketname_out = 'census-data/census-outflow-data'

with open(base_dir + r'/inflow_bucket.txt','r') as file:
          bucketname_in = file.read().replace('\n','')

with open(base_dir + r'/outflow_bucket.txt','r') as file:
          bucketname_out = file.read().replace('\n','')

          
csv_in = base_dir + r"/flows/in"
csv_out = base_dir + r"/flows/out"



s3 = boto3.client('s3')

s3.create_bucket(Bucket = bucketname_in)

for file in os.listdir(csv_in): #for inflow csvs
    if file.endswith(".csv"):
        filename = file[:-4]+' in'
        #print(filename)
        s3.upload_file(os.path.join(csv_in, file), bucketname_in,filename)



s3.create_bucket(Bucket = bucketname_out)

for file in os.listdir(csv_out): #for outflow csvs
    if file.endswith(".csv"):
        filename = file[:-4]+' out'
        #print(filename)
        s3.upload_file(os.path.join(csv_out, file), bucketname_out,filename)

