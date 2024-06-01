import boto3

class S3Handler:
    def __init__(self, region_name='us-east-1', bucket_name='cgiar-files', dynamo_table_name = 'CGIAR-files'):
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name
        self.dynamo_table_name = dynamo_table_name
        
        #For future use
        # self.dynamodb = boto3.resource('dynamodb', region_name=region_name)

    def upload_files(self,file_objects):
        try:
            print(self.s3_client.head_bucket(Bucket = self.bucket_name))
        except self.s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                self.s3_client.create_bucket(
                    Bucket=self.bucket_name
                )

        uploaded_files = {}
        for file_object in file_objects:
            try:
                file_key = file_object.name
                self.s3_client.upload_fileobj(file_object, self.bucket_name, file_key)
                s3_path = f"s3://{self.bucket_name}/{file_key}"
                uploaded_files[file_key] = s3_path
            except Exception as e:
                print(f"An error occurred: {e}")