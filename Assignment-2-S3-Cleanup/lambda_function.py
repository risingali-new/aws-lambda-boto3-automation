import boto3
import os
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME
    )

    deleted_files = []

    cutoff = datetime.now(timezone.utc) - timedelta(days=30)

    if 'Contents' in response:

        for obj in response['Contents']:

            if obj['LastModified'] < cutoff:

                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=obj['Key']
                )

                deleted_files.append(obj['Key'])

    print("Deleted Files:", deleted_files)

    return {
        "statusCode": 200,
        "deleted_files": deleted_files
    }
