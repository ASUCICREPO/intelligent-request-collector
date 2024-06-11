import boto3
from dotenv import load_dotenv
import os

load_dotenv()

class S3Handler:
    def __init__(self,uuid, region_name=os.getenv('REGION_NAME'), bucket_name=os.getenv('BUCKET_NAME'), dynamo_table_name = os.getenv('DYNAMO_TABLE_NAME')):
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name
        self.dynamo_table_name = dynamo_table_name
        self.uploaded_files = {}
        self.uuid = uuid
        
        #For future use
        # self.dynamodb = boto3.resource('dynamodb', region_name=region_name)

    def upload_files(self,file_objects):
        try:
            print(self.s3_client.head_bucket(Bucket = self.bucket_name))
        except self.s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print("An error occurred: The bucket does not exist!")

        for file_object in file_objects:
            try:
                file_key = self.uuid +'/'+ file_object.name
                self.s3_client.upload_fileobj(file_object, self.bucket_name, file_key)
                s3_path = f"s3://{self.bucket_name}/{self.uuid}/{file_key}"
                self.uploaded_files[file_key] = s3_path
            except Exception as e:
                print(f"An error occurred: {e}")