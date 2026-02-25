from app.domain.interfaces import S3Client
import boto3
import os
import logging
from botocore.exceptions import ClientError

class S3ClientImpl(S3Client):
    def __init__(self, bucket_name: str = None):
         self.bucket_name = bucket_name or os.getenv("S3_BUCKET_NAME")
         self.s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )

    def upload(self, bundle_path: str, bucket: str = None, key: str = "bundle.zip") -> str:
        target_bucket = bucket or self.bucket_name
        if not target_bucket:
            return "Error: No S3 bucket specified"
            
        try:
            self.s3_client.upload_file(bundle_path, target_bucket, key)
            
            # Generate presigned URL
            url = self.s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': target_bucket,
                                                            'Key': key},
                                                    ExpiresIn=3600)
            return url
        except ClientError as e:
            logging.error(f"S3 Upload Error: {e}")
            return f"Error uploading to S3: {e}"
