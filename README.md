# Uploading Census Data to AWS S3 and Athena

### Description
This is a project to upload census data to Amazon S3 and query it from Amazon Athena.   

## Exercise 1 Questions:


##### 1) Using Cloud Formation scripting; launch and configure a set of services to host, query, and aggregate the data:
######  a) Select from the following services: AWS EC2, AWS S3, AWS Athena, AWS Sagemaker, AWS EMR
######  b) Describe in detail why you chose your service and the design
Run 'create_stack.py' to create the cloudformation stack to set up the buckets in S3 and the database in Athena

Out of AWS EC2, AWS S3, AWS Athena, AWS Sagemaker, and AWS EMR, I chose to use AWS S3 and AWS Athena, because this is all we need in order to store and query the data. S3 is for storage, and Athena is for querying. Athena is also serverless, so there is no infrastructure that we need to manage, and we only pay for the queries. I create the cloudformation stack using boto3 and the template in "cloudformation.txt" to make buckets in S3 and a database in Athena.  


##### 2) Using a language of your choice, upload the Census datasets to your AWS services launched in step 1 (e.g., S3, EC2...)
Run 'excel_to_csv.py' to convert the xlsx to csv files.  
Run 'cleaning.py' to remove the headers and footnotes from the CSV files.  
Run 'upload_to_s3.py' to upload the CSV files to your buckets in S3.


Using python, I have uploaded the census datasets to S3. First, I convert the inflow and outflow excel sheets to csv files, because Athena cannot read xlsx, but it can read csv. Then, I remove the headers and footnotes from the csv files using RegEx. Finally, I upload the data to S3 using boto3.  
##### 3) Load the pre-processed data into the service of choice (e.g., AWS Athena, AWS Sagemaker, AWS EMR)
Run 'createDB.py' to create the tables in your Athena database.

Next, the data which was in S3 was loaded into the Athena database to create an inflow and outflow table. This was done with boto3 by uploading the query written in "inflow_table.ddl" and "outflow_table.ddl" (these are create table queries).
##### 4) Run a simple aggregation or query on the Census data and include the results in your submission.
```
SELECT curr_state, curr_county, SUM(curr_county_pop_est) AS pop
FROM (SELECT DISTINCT curr_state,curr_county,curr_county_pop_est
FROM censusdb.inflow
WHERE curr_state = 'California')
GROUP BY curr_state, curr_county
ORDER BY 3 DESC
```
This query will return all of California's counties sorted by population in descending order. The result of this query is located in query_result/query_ex.csv


##### 5) How much did this cost to run?
To find the cost of this query, we can check the "History" tab in Athena, and see how much data has been scanned for that specific query. The pricing for Athena is $5 per TB. In this case, I scanned about 55 MB (55.35 MB) of data. So my cost would be about ($5/1024/1024) * 55 = $0.000262.

---



### Setting up AWS
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

### Change inflow, outflow, and output bucket names in the following files. The bucket names need to be unique across all of S3:

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
### CloudFormation (make sure you are signed into aws)
Create a cloudformation stack to set up the buckets in S3 and the database in Athena
  - run 'create_stack.py'

### Data Prep
Create CSV files from the inflow and outflow excel files
  - run 'excel_to_csv.py'   

Clear the headers and footnotes from the CSV files
  - run 'cleaning.py'

Upload the CSV files to your buckets in S3
  - run 'upload_to_s3.py'


### Data Processing
Create tables in your database in Athena
  - run 'createDB.py'
---
### Query

  -You can query through Amazon Athena or query.py

  - Amazon Athena:
    - Go to the Query Editor for Athena and make sure you have selected "censusdb" as your database
    - Enter your query and click "Run query"
  - Query through python script:
    - In the queries folder, change the query.ddl file to the query you desire (using notepad again)
    - Run the python script and the output will be in your S3 output bucket

---
## Exercise 2 Questions:

##### 1) Would you propose using AWS Neptune or Neo4J for building a graph of the data?

I would propose using AWS Neptune because it is fully managed by AWS and we will only be charged for what we use.

However, if we want to have the flexibility of switching cloud providers, we should choose Neo4J, as it is also a good graph database software.

##### 2) How would you load data into your proposed graph database?

First we need to identify the nodes and edges after analyzing the data. We would then create the csv files for the nodes/edges and load the csv files to an S3 bucket. We will then use the Neptune loader to load the data into the Neptune instance.  



##### 3) How would you design the graph relationships of the data?

For this solution, we would have county nodes, US state nodes, and Foreign region nodes (Asia, Europe, etc.).
- County nodes would have a 'is part of' relationship with the US state nodes.
- We would have a 'flow' relationship between the county nodes. The 'flow' relationship would have a property 'flow count' to represent the county-to-county flow. We would have this relationship in both directions. If there are movers within the same county, there would be a self relationship.
- We would also have a 'flow' relationship from foreign region nodes to county nodes. This only goes in one direction: from foreign region node to county node.
