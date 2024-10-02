# intelligent-request-collector

**Prerequisites**

- Make sure there is a valid internet gateway and VPC set up.
- Ensure you have the Bedrock model Claude Sonnet available and activated.

**AWS Console Setup**
1) Create a bucket with default policies, make note of the name
2) Go to SES and verify the identity of the email address you will be sending to/from
3) You must enable Claude Sonnet Model Access on AWS Console for Amazon Bedrock.

**AWS CloudFormation**

```
aws configure sso
```
```
aws cloudformation create-stack --stack-name $Stackname --template-url $Template_object_url --parameters ParameterKey=S3Bucket,ParameterValue=$S3BucketName ParameterKey=SESEmail,ParameterValue=$Email —profile $Profile (Profile parameter is optional)
```

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
5) create .env and edit in the root folder of the repo
   ```nano .env```
6) _Edit the .env file with the appropriate values. BUCKET_NAME and FROM_EMAIL are the only required ones; the region name should default to us-east-1._
   ```
    REGION_NAME=""
    BUCKET_NAME=""
    FROM_EMAIL=""
    DYNAMODB_TABLE_NAME=""
    ```
7) Install Screen to run streamlit event even after closing Instance
   ```
   sudo yum install screen -y
   ```

**Run Streamlit with Screen**

1) Create a Screen Session
   ```
   screen -S my_streamlit_app
   ```
2) After entering the Session, Traverse to root folder
   ```
   cd intelligent-request-collector
   ```
3) Run streamlit
   ```
   streamlit run main.py
   ```
4) Detach from the session:
   ```
    Ctrl + A, then D
    ```
5) You can now run the session after exiting the Instance

**Shutdown Streamlit app**

1) After entering the instance, you can view the screen sessions using:
    ```
    screen -ls
    ```
2) Reattach to the intended session.
   ```
   screen -r my_streamlit_app
   ```
3) Stop the session
   ```
   Ctrl + C
   ```
4) Exit Screen Session
   ```
   exit
   ```


**Set your access information**
_You can obtain this from your AWS Apps Portal._
```
export AWS_ACCESS_KEY_ID={REDACT}
export AWS_SECRET_ACCESS_KEY={REDACT}
export AWS_SESSION_TOKEN={REDACT}
```

**Run it**

`streamlit run main.py`


**Architecture**

This prototype utilizes streamlit to provide the user a frontend experience.

_AWS Services that are utilized by this prototype:_
* Amazon Bedrock (Generative AI Functionality)
* Amazon SES (Email functionality)
* Amazon S3 (File attachment storage)
