import boto3
import os

#base_dir = r'C:/Users/rajki/Documents/JP_Morgan_assignment/final_submit/' #user needs to change
base_dir = os.path.dirname(os.path.dirname(__file__))
client = boto3.client('cloudformation')

stack_name = 'cfS3Athena'

path = base_dir + r'/cloudformation/cloudformation.txt'

#use your own path
template = ''


with open(path, 'r') as file:
    template = file.read().replace('\n', '')



print(template)

client.create_stack(StackName = stack_name,TemplateBody=template)


ath = boto3.client('athena')

#have output_bucket as common file in txt file

output_bucket = ''

with open(base_dir + r'/output_bucket.txt','r') as file:
          output_bucket = file.read().replace('\n','')

database_name = 'censusdb'

ath.start_query_execution(
    QueryString='create database '+ database_name,
    ResultConfiguration={'OutputLocation': output_bucket})
    
