# Uploading Census Data to AWS S3 and Athena

### Description
This is a project to upload census data to Amazon S3 and query it from Amazon Athena.   

Out of AWS EC2, AWS S3, AWS Athena, AWS Sagemaker, and AWS EMR, I chose to use AWS S3 and AWS Athena, because this is all we need in order to store and query the data. S3 is for storage, and Athena is for querying. I create the cloudformation stack using boto3 and the script in "cloudformation.txt" to make buckets in S3 and a database in Athena  

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

   Modules used (remove some of the pip installs)
---
  * csv:
  ```
  pip install csv - I think python has it built in
  ```  
  * boto3:
  ```
  pip install boto3
  ```
  * RegEx:
   ```
   python has it built in
   ```
  * os:
  ```
  pip install os - I think python has it built in
  ```
  * xlsx2csv:
  ```
  pip install xlsx2csv
  ```

---
## You need to change inflow, outflow, and output bucket names in the following files. The bucket names need to be unique across all of S3:

  - cloudformation/cloudformation.txt
  - inflow_bucket.txt
  - outflow_bucket.txt
  - output_bucket.txt
  - tables/inflow_table.ddl
  - tables/outflow_table.ddl

  ```diff
  - for ddl files, open with notepad and at the bottom, change __LOCATION 's3://census-inflow-data/'__ to __LOCATION 's3://\<YOUR_BUCKET_NAME>/'__
  ```

---
## CloudFormation (need to be signed into aws) done
  - run create_stack.py
  - this creates a cloudformation stack which sets up the bucket in S3 and the database in Athena

## Data Prep
  - run excel_to_csv.py
    - this creates CSVs from the inflow and outflow excel document
  - run cleaning.py
    - this clears the CSVs of headers and footnotes
  - run upload_to_s3.py
    - this uploads the CSV files to the bucket in S3

## Data Processing
  - run createDB
    - this creates tables in the database of Athena

---

# Query

  -Either on Amazon Athena or through query.py

  - Amazon Athena:
    - Go to the Query Editor for Athena and make sure you have selected "censusdb" as your database
    - Type any query
  - Query through python script:
    - In the queries folder, change the query.ddl file to the query you desire (using notepad again)
    - Run the python script and the output will be in your S3 bucket (It will go to your output bucket in S3)
