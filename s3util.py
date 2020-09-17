import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file, bucket_name, s3_file):
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.upload_file(local_file, bucket_name, s3_file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


