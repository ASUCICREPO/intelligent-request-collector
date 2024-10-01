# intelligent-request-collector

**Prerequisites**
```
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

**AWS Console Setup**
1) Create a bucket with default policies, make note of the name
2) Go to SES and verify the identity of the email address you will be sending to/from
3) You must enable Claude Sonnet Model Access on AWS Console for Amazon Bedrock.

**AWS CDK Setup**

```
aws configure sso
```
```
aws cloudformation create-stack --stack-name {$StackName} --template-url {$S3URL of the Template JSON} —profile (profile info)
```

*To set a different email and/or s3_bucket location to store attachment files:*

1) download the template JSON and edit ("EmailIdentity": {$new_email} ; "aws:cdk:path": "PotatoStack/cgiar-files-v2/Resource”)
2) Save the template JSON and upload it to s3.
3) copy S3 URL path of the template JSON.
4) Follow the AWS CDK Setup above replacing the {$S3URL of the Template JSON} value with the copied s3 URL.

**Steps to setup intelligent-request-collector on AWS EC2 instance:**

1) Install python3.9
```
    sudo yum install python
```

2) Clone repo : 
```
    sudo yum update -y
    sudo yum install git -y
    git clone https://github.com/ASUCICREPO/intelligent-request-collector.git
```

3) Install pip: ``` sudo yum install python-pip -y ```
4) Install requirements 
   ```pip install -r requirements.txt```
5) create .env following the instructions below

**Set your access information**
_You can obtain this from your AWS Apps Portal._
```
export AWS_ACCESS_KEY_ID={REDACT}
export AWS_SECRET_ACCESS_KEY={REDACT}
export AWS_SESSION_TOKEN={REDACT}
```

**Create a .env file**

_Create a .env file with the appropriate values. BUCKET_NAME and FROM_EMAIL are the only required ones; region name should default to us-east-1._
```
REGION_NAME=""
BUCKET_NAME=""
FROM_EMAIL=""
DYNAMODB_TABLE_NAME=""
```

**Run it**

`streamlit run main.py`


**Architecture**

This prototype utilizes streamlit to provide the user a frontend experience.

_AWS Services that are utilized by this prototype:_
* Amazon Bedrock (Generative AI Functionality)
* Amazon SES (Email functionality)
* Amazon S3 (File attachment storage)
