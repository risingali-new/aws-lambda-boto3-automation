
# Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to automate the cleanup of old files stored in an Amazon S3 bucket using AWS Lambda and Boto3.

The Lambda function scans a specified S3 bucket, identifies files older than a defined retention period, and automatically deletes them.

---

## Architecture

```text
Amazon S3 Bucket
        |
        v
AWS Lambda Function
        |
        v
List Objects
        |
        v
Check Object Age
        |
        v
Delete Old Files
        |
        v
CloudWatch Logs
```

---

## AWS Services Used

* Amazon S3
* AWS Lambda
* AWS IAM
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

## Prerequisites

* AWS Account
* S3 Bucket
* IAM permissions to create Lambda functions and roles

---

## Step 1: Create S3 Bucket

An S3 bucket was created to store files for cleanup testing.

### Screenshot



---

## Step 2: Upload Test Files

Multiple files were uploaded to the S3 bucket for testing the cleanup process.

### Screenshot

![Uploaded Files](screenshots/s3-files-uploaded.png)


---

## Step 3: Create IAM Role

Created a Lambda execution role with the following permissions:

* AmazonS3FullAccess
* AWSLambdaBasicExecutionRole

Role Name:

```text
Lambda-S3-Cleanup-Role
```

### Screenshot

![IAM Role](screenshots/iam-role.png)

---

## Step 4: Create Lambda Function

Lambda Configuration:

| Property       | Value                  |
| -------------- | ---------------------- |
| Function Name  | s3-bucket-cleanup      |
| Runtime        | Python 3.13            |
| Execution Role | Lambda-S3-Cleanup-Role |

### Screenshot

![Lambda Function](screenshots/lambda-function.png)

---

## Step 5: Configure Environment Variable

Environment variable used:

| Key         | Value                        |
| ----------- | ---------------------------- |
| BUCKET_NAME | travelmemory-s3-cleanup-demo |

### Screenshot

![Environment Variable](screenshots/environment-variable.png)

---

## Step 6: Lambda Function Code

```python
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
```

---

## Step 7: Test the Lambda Function

A test event was created and the Lambda function was manually invoked.

Expected Result:

* Files older than the retention period are deleted.
* Remaining files stay intact.

### Screenshot

![Lambda Test Success](screenshots/lambda-success.png)

---

## Step 8: Verify Cleanup

The Lambda function successfully deleted the identified files from the S3 bucket.

### Screenshot

![Bucket After Cleanup](screenshots/bucket-after-cleanup.png)

---

## CloudWatch Logs Verification

CloudWatch logs were reviewed to verify successful execution.

### Screenshot

![CloudWatch Logs](screenshots/cloudwatch-logs.png)

---

## Outcome

Successfully automated S3 bucket cleanup using AWS Lambda and Boto3. The Lambda function scans the bucket, identifies files older than the retention period, deletes them automatically, and records execution details in CloudWatch Logs.

---

## Author

Ali Hussain
