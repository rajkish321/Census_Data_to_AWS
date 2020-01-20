# Uploading Census Data to AWS S3 and Athena

### Description
This is a project to upload census data to Amazon S3 and query it from Amazon Athena.   

Out of AWS EC2, AWS S3, AWS Athena, AWS Sagemaker, and AWS EMR, I chose to use AWS S3 and AWS Athena, because this is all we need in order to store and query the data. S3 is for storage, and Athena is for querying. Athena is also serverless, so there is no infrastructure that we need to manage, and we only pay for the queries. I create the cloudformation stack using boto3 and the template in "cloudformation.txt" to make buckets in S3 and a database in Athena.  

Using python, I have uploaded the census datasets to S3. First, I convert the inflow and outflow excel sheets to csv files, because Athena cannot read xlsx, but it can read csv. Then, I remove the headers and footnotes from the csv files using RegEx. Finally, I upload the data to S3 using boto3.  

Next, I loaded the data which was in S3 into the database in Athena to create an inflow and outflow table. This was done with boto3 by uploading the query written in "inflow_table.ddl" and "outflow_table.ddl" (these are create table queries).

#### Query Example:
```
SELECT curr_state, curr_county, SUM(curr_county_pop_est) AS pop
FROM (SELECT DISTINCT curr_state,curr_county,curr_county_pop_est
FROM censusdb.inflow
WHERE curr_state = 'California')
GROUP BY curr_state, curr_county
ORDER BY 3 DESC
```
This query will return all of California's counties sorted by population in descending order. The result of this is located in query_result/query_ex.csv



To find the cost of this query, we can check the "History" tab in Athena, and see how much data has been scanned for that specific query. The pricing for Athena is $5 per TB. In this case, I scanned about 55 MB (55.35 MB) of data. So my cost would be about ($5/1024/1024) * 55 = $0.000262.

---



## Setting up AWS
In your cmd:
```
pip install awscli
```
* In console  type: aws configure  
```
AWS Access Key ID [None]: <YOUR ACCESS KEY ID>
AWS Secret Access Key [None]: <YOUR SECRET ACCESS KEY ID>
Default region name [None]: <YOUR REGION NAME> (Northern VA is us-east-1)
Default output format [None]: <not needed, leave blank and click enter>
```
---
AWS Services used
---
  * S3
  * Athena
  * CloudFormation  


   Python Modules used (Use pip install if modules not installed)
---
  * csv
  * boto3
  * RegEx
  * os
  * xlsx2csv
  ```
  pip install boto3
  pip install xlsx2csv
  ```
---

## Change inflow, outflow, and output bucket names in the following files. The bucket names need to be unique across all of S3:

  - cloudformation/cloudformation.txt
  - inflow_bucket.txt
  - outflow_bucket.txt
  - output_bucket.txt
  - tables/inflow_table.ddl
  - tables/outflow_table.ddl

  ```diff
  - for ddl files, open with notepad and at the bottom of the file, change LOCATION 's3://census-inflow-data/' to LOCATION 's3://<YOUR_BUCKET_NAME>/'
  ```

---
## CloudFormation (need to be signed into aws) done
Create a cloudformation stack to set up the bucket in S3 and the database in Athena
  - run create_stack.py

## Data Prep
Create CSV files from the inflow and outflow excel files
  - run excel_to_csv.py  

Clear the headers and footnotes from the CSV
  - run cleaning.py

Upload the CSV files to your buckets in S3
  - run upload_to_s3.py


## Data Processing
Create tables in your database in Athena
  - run createDB.py
---
## Query

  -You can query through Amazon Athena or query.py

  - Amazon Athena:
    - Go to the Query Editor for Athena and make sure you have selected "censusdb" as your database
    - Enter your query and click "Run query"
  - Query through python script:
    - In the queries folder, change the query.ddl file to the query you desire (using notepad again)
    - Run the python script and the output will be in your S3 output bucket
