import unittest
from io import BytesIO
import boto3
from moto import mock_aws
from managers.S3FileHandler import S3Handler

class TestS3Handler(unittest.TestCase):

    def setUp(self):
        self.region_name = 'us-east-1'
        self.bucket_name = 'cgiar-files'
        self.s3_handler = S3Handler(region_name=self.region_name, bucket_name=self.bucket_name)

    def test_upload_files(self):
        with mock_aws():
            # Initialize the S3 mock and create a bucket
            self.s3 = boto3.client('s3', region_name=self.region_name)
            self.s3.create_bucket(Bucket=self.bucket_name)

            # Mock file objects
            file1 = BytesIO(b"File content 1")
            file1.name = "file1.txt"
            file2 = BytesIO(b"File content 2")
            file2.name = "file2.txt"
            file_objects = [file1, file2]

            # Call the upload_files method
            result = self.s3_handler.upload_files(file_objects)

            # Verify the result
            expected_result = {
                "file1.txt": f"s3://{self.bucket_name}/file1.txt",
                "file2.txt": f"s3://{self.bucket_name}/file2.txt"
            }
            # self.assertEqual(result, expected_result)

            # Verify the files are uploaded
            for file_key in expected_result.keys():
                self.assertEqual(self.s3_handler.s3_client.head_object(Bucket='cgiar-files', Key=file_key)['ResponseMetadata']['HTTPStatusCode'],200)
            

if __name__ == '__main__':
    unittest.main()
