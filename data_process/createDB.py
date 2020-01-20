import boto3
import os

#base_dir = r'C:/Users/rajki/Documents/JP_Morgan_assignment/final_submit/' #user needs to change
base_dir = os.path.dirname(os.path.dirname(__file__))

inflow_table =base_dir + r'/tables/inflow_table.ddl'

outflow_table = base_dir + r'/tables/outflow_table.ddl'

ath = boto3.client('athena')


#output_bucket = 's3://'+tempBucket+'/athena'
output_bucket = ''
with open(base_dir + r'/output_bucket.txt','r') as file:
          output_bucket = file.read().replace('\n','')

with open(inflow_table) as ddl:
    ath.start_query_execution(
        QueryString=ddl.read(),
        ResultConfiguration={'OutputLocation': output_bucket})

with open(outflow_table) as ddl:
    ath.start_query_execution(
        QueryString=ddl.read(),
        ResultConfiguration={'OutputLocation': output_bucket})
