# Assignment 4: Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to automate EBS volume backups using AWS Lambda and Boto3.

The Lambda function creates snapshots of a specified EBS volume and removes snapshots older than the retention period to optimize storage costs.

---

## Architecture

```text
Amazon EBS Volume
        |
        v
AWS Lambda Function
        |
        +-------------------+
        |                   |
        v                   v
Create Snapshot     Delete Old Snapshots
        |
        v
CloudWatch Logs
```

---

## AWS Services Used

- Amazon EC2
- Amazon EBS
- AWS Lambda
- AWS IAM
- Amazon CloudWatch
- Boto3 (AWS SDK for Python)

---

## Prerequisites

- AWS Account
- Existing EBS Volume
- IAM permissions to create Lambda functions and roles

---

## Step 1: Identify EBS Volume

An existing EBS volume was selected for automated backup.

Volume ID:

```text
vol-01b00f32704499c12
```

### Screenshot

<img width="3204" height="615" alt="image" src="https://github.com/user-attachments/assets/d56c5625-fdb9-47a2-8c6f-33d193ba5a54" />


---

## Step 2: Create IAM Role

Created a Lambda execution role with:

- AmazonEC2FullAccess
- AWSLambdaBasicExecutionRole

Role Name:

```text
Lambda-EBS-Snapshot-Role
```

### Screenshot

<img width="2540" height="1186" alt="image" src="https://github.com/user-attachments/assets/b7a8aa96-bd9c-461c-ba73-34407fd39568" />


---

## Step 3: Create Lambda Function

Lambda Configuration:

| Property | Value |
|-----------|---------|
| Function Name | ebs-snapshot-cleanup |
| Runtime | Python 3.13 |
| Execution Role | Lambda-EBS-Snapshot-Role |
| Timeout | 30 Seconds |

### Screenshot

<img width="2709" height="1426" alt="image" src="https://github.com/user-attachments/assets/8f937b28-b83a-4a1c-a3a3-896972fea2c8" />


---

## Step 4: Configure Environment Variable

Environment variable used:

| Key | Value |
|------|--------|
| VOLUME_ID | vol-01b00f32704499c12 |

### Screenshot

<img width="2507" height="1021" alt="image" src="https://github.com/user-attachments/assets/a8808a35-cece-4c20-aa9b-eea993b2e37c" />


---

## Step 5: Lambda Function Code

```python
import boto3
import os
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = os.environ['VOLUME_ID']

def lambda_handler(event, context):

    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description='Automated Lambda Snapshot'
    )

    snapshot_id = snapshot['SnapshotId']

    print(f"Created Snapshot: {snapshot_id}")

    deleted_snapshots = []

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)

    snapshots = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    for snap in snapshots['Snapshots']:

        if (
            snap['Description'] == 'Automated Lambda Snapshot'
            and snap['StartTime'] < cutoff_date
        ):

            ec2.delete_snapshot(
                SnapshotId=snap['SnapshotId']
            )

            deleted_snapshots.append(
                snap['SnapshotId']
            )

    print(
        f"Deleted Snapshots: {deleted_snapshots}"
    )

    return {
        "statusCode": 200,
        "snapshot_created": snapshot_id,
        "deleted_snapshots": deleted_snapshots
    }
```

---

## Step 6: Execute Lambda Function

A test event was created and the Lambda function was executed manually.

### Screenshot

<img width="2618" height="1681" alt="image" src="https://github.com/user-attachments/assets/8656cf5f-4718-4d4b-bcc1-bafe4ce37882" />


---

## Step 7: Verify Snapshot Creation

A new EBS snapshot was successfully created.

Example:

```text
snap-079b9487051b72d9d
```

### Screenshot

<img width="2757" height="677" alt="image" src="https://github.com/user-attachments/assets/c24f0519-5b42-467a-94bf-c18e91d9260b" />


---

## CloudWatch Logs Verification

CloudWatch logs confirmed successful execution.

Example Output:

```text
Created Snapshot: snap-079b9487051b72d9d
Deleted Snapshots: []
```

### Screenshot

<img width="2957" height="956" alt="image" src="https://github.com/user-attachments/assets/53e131a1-1e44-48e9-9ab9-9b97ea2e58cd" />


---

## Results

Lambda successfully:

- Created an EBS snapshot
- Checked for old snapshots
- Deleted snapshots older than retention period (if found)
- Logged execution details to CloudWatch

---

## Bonus Enhancement

This solution can be integrated with Amazon EventBridge to automatically create snapshots on a daily or weekly schedule.

---

## Outcome

Successfully implemented automated EBS backup and retention management using AWS Lambda and Boto3.

---

## Author

Ali Hussain

GitHub: https://github.com/risingali-new
