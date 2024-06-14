import boto3

class S3Handler:
    def __init__(self,uuid, bucket_name, logger, region='us-east-1', dynamo_table_name=None):
        self.s3_client = boto3.client('s3', region_name=region)
        self.bucket_name = bucket_name
        self.dynamo_table_name = dynamo_table_name
        self.uploaded_files = {}
        self.uuid = uuid
        self.logger = logger
        
        #For future use
        # self.dynamodb = boto3.resource('dynamodb', region_name=region_name)

    def upload_files(self,file_objects):
        try:
            result = self.s3_client.head_bucket(Bucket = self.bucket_name)
            self.logger.debug("%s",result)
        except self.s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                self.logger.critical("An error occurred: The bucket does not exist!")

        for file_object in file_objects:
            try:
                file_key = self.uuid +'/'+ file_object.name
                self.s3_client.upload_fileobj(file_object, self.bucket_name, file_key)
                s3_path = f"s3://{self.bucket_name}/{self.uuid}/{file_key}"
                self.uploaded_files[file_key] = s3_path
            except Exception as e:
                self.logger.critical(f"An error occurred: {e}")