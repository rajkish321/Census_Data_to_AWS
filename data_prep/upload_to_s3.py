#This uploads the csv files to your buckets in S3
import boto3
import os

base_dir = os.path.dirname(os.path.dirname(__file__))

bucketname_in = ''
bucketname_out = ''

# Make sure the names in inflow_bucket.txt and outflow_bucket.txt
# contain bucket names that are valid 
with open(base_dir + r'/inflow_bucket.txt','r') as file:
          bucketname_in = file.read().replace('\n','')

with open(base_dir + r'/outflow_bucket.txt','r') as file:
          bucketname_out = file.read().replace('\n','')

          
csv_in = base_dir + r"/flows/in"
csv_out = base_dir + r"/flows/out"



s3 = boto3.client('s3')

s3.create_bucket(Bucket = bucketname_in)

for file in os.listdir(csv_in): #for inflow CSVs
    if file.endswith(".csv"):
        filename = file[:-4]+' in'
        #print(filename)
        s3.upload_file(os.path.join(csv_in, file), bucketname_in,filename)



s3.create_bucket(Bucket = bucketname_out)

for file in os.listdir(csv_out): #for outflow CSVs
    if file.endswith(".csv"):
        filename = file[:-4]+' out'
        #print(filename)
        s3.upload_file(os.path.join(csv_out, file), bucketname_out,filename)

