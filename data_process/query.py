import boto3
import os


#base_dir = r'C:/Users/rajki/Documents/JP_Morgan_assignment/final_submit/' #user needs to change
base_dir = os.path.dirname(os.path.dirname(__file__))


ath = boto3.client('athena')
query_ = base_dir + r'/queries/query.ddl'

output_bucket = ''
with open(base_dir + r'/output_bucket.txt','r') as file:
          output_bucket = file.read().replace('\n','')

with open(query_) as ddl:
    ath.start_query_execution(
        QueryString=ddl.read(),
        ResultConfiguration={'OutputLocation': output_bucket})

