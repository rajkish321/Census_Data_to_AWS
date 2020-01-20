#This creates a cloudformation stack to set up the buckets in S3 and the database in Athena
import boto3
import os


base_dir = os.path.dirname(os.path.dirname(__file__))
client = boto3.client('cloudformation')

stack_name = 'cfS3Athena'

path = base_dir + r'/cloudformation/cloudformation.txt'


template = ''


with open(path, 'r') as file:
    template = file.read().replace('\n', '')





client.create_stack(StackName = stack_name,TemplateBody=template)   #creating cloudformation stack


ath = boto3.client('athena')

#have to change output_bucket in output_bucket.txt

output_bucket = ''

with open(base_dir + r'/output_bucket.txt','r') as file:
          output_bucket = file.read().replace('\n','')

database_name = 'censusdb'

ath.start_query_execution(      #creating database
    QueryString='create database '+ database_name,
    ResultConfiguration={'OutputLocation': output_bucket})
    
