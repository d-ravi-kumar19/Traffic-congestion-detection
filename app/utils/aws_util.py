import boto3
import os

def download_model_from_s3(bucket_name, model_file_name, local_model_path):
    """Download the model file from S3."""
    # Initialize a session using your AWS credentials
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Create a session using your credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Initialize S3 client
    s3 = session.client('s3')

    # Download the model file from S3
    s3.download_file(bucket_name, model_file_name, local_model_path)
    print(f"Model downloaded from S3 to {local_model_path}")
