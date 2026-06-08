# Assignment 3: Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to improve AWS security posture by identifying S3 buckets that do not have server-side encryption enabled.

The Lambda function scans all S3 buckets in the AWS account and reports buckets without encryption configuration.

---

## Architecture

```text
Amazon S3 Buckets
        |
        v
AWS Lambda Function
        |
        v
List All Buckets
        |
        v
Check Encryption Configuration
        |
        v
Identify Non-Compliant Buckets
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
* Existing S3 Buckets
* IAM permissions to create Lambda functions and roles

---

## Step 1: Create IAM Role

Created a Lambda execution role with the following permissions:

* AmazonS3ReadOnlyAccess
* AWSLambdaBasicExecutionRole

Role Name:

```text
Lambda-S3-Encryption-Check-Role
```

### Screenshot

<img width="1883" height="746" alt="image" src="https://github.com/user-attachments/assets/de8eaa4f-b0b7-4202-9482-ee0065a4f6ce" />


---

## Step 2: Create Lambda Function

Lambda Configuration:

| Property       | Value                           |
| -------------- | ------------------------------- |
| Function Name  | s3-encryption-check             |
| Runtime        | Python 3.13                     |
| Execution Role | Lambda-S3-Encryption-Check-Role |
| Timeout        | 30 Seconds                      |

### Screenshot

<img width="2204" height="1336" alt="image" src="https://github.com/user-attachments/assets/2adb50f0-5f4e-4589-94ad-6d9076014e2d" />


---

## Step 3: Lambda Function Code

```python
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):

    unencrypted_buckets = []

    response = s3.list_buckets()

    for bucket in response['Buckets']:

        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(
                Bucket=bucket_name
            )

        except ClientError as e:

            error_code = e.response['Error']['Code']

            if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                unencrypted_buckets.append(bucket_name)

    print("Unencrypted Buckets:")
    print(unencrypted_buckets)

    return {
        'statusCode': 200,
        'unencrypted_buckets': unencrypted_buckets
    }
```

---

## Step 4: Execute Lambda Function

A test event was created and the Lambda function was executed manually.

### Screenshot

<img width="2226" height="1346" alt="image" src="https://github.com/user-attachments/assets/c1be3798-d17f-4873-9c1b-60b97408c9bc" />


---

## CloudWatch Logs Verification

CloudWatch logs confirmed successful execution of the Lambda function.

Example Output:

```text
Unencrypted Buckets:
[]
```

### Screenshot

<img width="2618" height="756" alt="image" src="https://github.com/user-attachments/assets/bd751f6c-2c82-4f25-97b8-1f0ec01758b0" />


---

## Results

The Lambda function successfully scanned all S3 buckets and verified their encryption configuration.

No buckets without server-side encryption were found.

```json
{
  "statusCode": 200,
  "unencrypted_buckets": []
}
```

---

## Outcome

Successfully implemented an automated security compliance check using AWS Lambda and Boto3 to monitor S3 bucket encryption settings.

The solution can be scheduled using Amazon EventBridge for continuous monitoring.

---

## Author

Ali Hussain
GitHub: https://github.com/risingali-new

