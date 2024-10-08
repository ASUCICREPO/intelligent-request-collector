# intelligent-request-collector

**Prerequisites**

1) Make sure there is a valid internet gateway and VPC set up.
2) Ensure you have the Bedrock model Claude Sonnet available and activated.
3) Make there is a valid IAM Identity with the following permissions
- AmazonBedrockFullAccess
- AmazonEC2FullAccess
- AmazonS3FullAccess
- AmazonSESFullAccess

**AWS Console Setup**

1) Go to SES and verify the identity of the email address you will be sending to/from
2) You must enable Claude Sonnet Model Access on AWS Console for Amazon Bedrock.

**AWS CloudFormation**

```
aws configure sso
```
```
aws cloudformation create-stack --stack-name $Stackname --template-url $Template_object_url --parameters ParameterKey=S3Bucket,ParameterValue=$S3BucketName ParameterKey=SESEmail,ParameterValue=$Email —profile $Profile (Profile parameter is optional)
```
**Steps to launch an AWS EC2 Instance**

1) Click 'Launch Instance' in the EC2 Console
2) Provide a suitable name for the instance
3) Choose Amazon Linux 2023 AMI and Architecture - 64-bit
4) Instace type - t2.micro
5) Choose a valid key pair name or create a new key pair
6) Adjust network settings according to the setup vpc and subnet.
7) Make sure to enable Auto-assign public IP and IPv6 IP
8) Choose a suitable security group
9) In Advanced Details, choose the IAM instance profile that follow the instructions of the prequisites.
10) Add the following in the User data section:
```
Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0
 
--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment;
 filename="cloud-config.txt"
 
#cloud-config
cloud_final_modules:
- [scripts-user, always]
--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"
 
#!/bin/bash
# Update the instance and install screen
yum update -y
yum install -y screen
yum install -y python
yum install -y git
runuser -l ec2-user -c 'mkdir intelligent-request-collector'
git clone https://github.com/ASUCICREPO/intelligent-request-collector.git /home/ec2-user/intelligent-request-collector
yum install -y python-pip
cd /home/ec2-user/intelligent-request-collector
runuser -l ec2-user -c 'pip3 install --user -r /home/ec2-user/intelligent-request-collector/requirements.txt'
# Navigate to the project folder and start Streamlit in a detached screen session
runuser -l ec2-user -c 'cd /home/ec2-user/intelligent-request-collector'
runuser -l ec2-user -c 'screen -dmS my_streamlit_app bash -c "cd /home/ec2-user/intelligent-request-collector && streamlit run /home/ec2-user/intelligent-request-collector/main.py"'
# Output screen sessions list
echo "Streamlit app is running in a detached screen session named 'my_streamlit_app'."
echo "To view active screen sessions, run: screen -ls"
echo "To reattach to the Streamlit session, run: screen -r my_streamlit_app"
--//-- 
```
11) Launch Instance

**Connect to the EC2 Instance**

1) Choose the Launched EC2 Instance
2) Connect using EC2 Instance Connect tab
3) For connection type, choose 'Connect using EC2 Instance Connect'
4) Choose Public IPv4 address
5) Make sure the username is 'ec2-user'.
6) Click Connect

**In the EC2 Instance**

1) Traverse to the intelligent-resource-collector dir
   ```
   cd intelligent-resource-collector
   ```
2) create .env and edit the .env file
   ```nano .env```
3) _Edit the .env file with the appropriate values. BUCKET_NAME and FROM_EMAIL are the only required ones; the region name should default to us-east-1._
   ```
    REGION_NAME=""
    BUCKET_NAME=""
    FROM_EMAIL=""
    DYNAMODB_TABLE_NAME=""
    ```
4) Save and exit the .env file
   ```
   Ctrl + X
   y
   Enter
   ```
5) View the .env file
   ```
   cat .env
   ```

## Your setup is now complete

**Note:** The rest of the documentations provides commands to manage any Screen/Streamlit sessions

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

**Run it**

`streamlit run main.py`


**Architecture**

This prototype utilizes streamlit to provide the user a frontend experience.

_AWS Services that are utilized by this prototype:_
* Amazon Bedrock (Generative AI Functionality)
* Amazon SES (Email functionality)
* Amazon S3 (File attachment storage)
* Amazon EC2 (Frontend)
