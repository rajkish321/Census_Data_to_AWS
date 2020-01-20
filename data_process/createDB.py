#This creates the tables in your Athena database
import boto3
import os

base_dir = os.path.dirname(os.path.dirname(__file__))

inflow_table =base_dir + r'/tables/inflow_table.ddl'

outflow_table = base_dir + r'/tables/outflow_table.ddl'

ath = boto3.client('athena')

#make sure you changed your output bucket name in output_bucket.txt
output_bucket = ''
with open(base_dir + r'/output_bucket.txt','r') as file:
          output_bucket = file.read().replace('\n','')


# Make sure to edit the inflow_table.ddl and outflow_table.ddl
# so that the location is pointing to your inflow and outflow buckets
# (Can be seen at the bottom of the files)

with open(inflow_table) as ddl: #this creates the inflow table
    ath.start_query_execution(
        QueryString=ddl.read(),
        ResultConfiguration={'OutputLocation': output_bucket})

with open(outflow_table) as ddl: #this creates the outflow table
    ath.start_query_execution(
        QueryString=ddl.read(),
        ResultConfiguration={'OutputLocation': output_bucket})
