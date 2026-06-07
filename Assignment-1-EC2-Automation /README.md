
# Assignment 1: Automated EC2 Instance Management Using AWS Lambda and Boto3

## Objective

The objective of this assignment is to automate the starting and stopping of EC2 instances based on instance tags using AWS Lambda and Boto3.

---

## Architecture

```text
AWS Lambda
     |
     v
Describe EC2 Instances
     |
     +----------------------+
     |                      |
     v                      v
Action=Auto-Stop      Action=Auto-Start
     |                      |
     v                      v
Stop Instance         Start Instance
```

---

## AWS Services Used

* AWS EC2
* AWS Lambda
* AWS IAM
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

## Prerequisites

* AWS Account
* Two EC2 Instances
* IAM permissions to create Lambda functions and roles

---

## Step 1: Create EC2 Instances

Two EC2 instances were created.

| Instance Name         | Purpose    |
| --------------------- | ---------- |
| TravelMemory-Server-1 | Auto Stop  |
| TravelMemory-Server-2 | Auto Start |

The following tags were added:

| Key    | Value      |
| ------ | ---------- |
| Action | Auto-Stop  |
| Action | Auto-Start |

### Screenshot

<img width="940" height="507" alt="image" src="https://github.com/user-attachments/assets/84197d5e-67da-4743-9b7c-6f5264a93301" />
<img width="940" height="542" alt="image" src="https://github.com/user-attachments/assets/e79e3a0b-cb48-4c4e-af4b-b8c0b8e87223" />



---

## Step 2: Create IAM Role

Created an IAM role for Lambda execution.

Role Name:

```text
Lambda-EC2-Automation-Role
```

Attached Policy:

```text
AmazonEC2FullAccess
```

### Screenshot

<img width="940" height="476" alt="image" src="https://github.com/user-attachments/assets/3b632c61-3de4-4ca3-a043-988c17a3fe0a" />


---

## Step 3: Create Lambda Function

Lambda Configuration:

| Property       | Value                      |
| -------------- | -------------------------- |
| Function Name  | ec2-start-stop             |
| Runtime        | Python 3.14               |
| Execution Role | Lambda-EC2-Automation-Role |

### Screenshot

<img width="2620" height="1594" alt="image" src="https://github.com/user-attachments/assets/b14e0a05-4417-433e-a02f-fa0872e51529" />


---

## Step 4: Lambda Function Code

```python
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    stop_instances = []
    start_instances = []

    response = ec2.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:

            instance_id = instance['InstanceId']

            tags = instance.get('Tags', [])

            for tag in tags:

                if tag['Key'] == 'Action':

                    if tag['Value'] == 'Auto-Stop':
                        stop_instances.append(instance_id)

                    elif tag['Value'] == 'Auto-Start':
                        start_instances.append(instance_id)

    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print(f"Stopped Instances: {stop_instances}")

    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print(f"Started Instances: {start_instances}")

    return {
        "statusCode": 200,
        "message": "EC2 automation completed"
    }
```

---

## Step 5: Test the Lambda Function

A test event was created and the Lambda function was invoked manually.

Expected Result:

* Instances tagged with Auto-Stop should stop.
* Instances tagged with Auto-Start should start.

### Screenshot

<img width="2896" height="1086" alt="image" src="https://github.com/user-attachments/assets/84a3e200-2023-4592-b02a-d3cce42aa281" />


---

## Step 6: Verification

The Lambda function successfully performed the required actions.

| Instance              | Expected State | Result  |
| --------------------- | -------------- | ------- |
| TravelMemory-Server-1 | Stopped        | Success |
| TravelMemory-Server-2 | Running        | Success |

### Screenshot

<img width="2360" height="318" alt="image" src="https://github.com/user-attachments/assets/0c4793f4-cb80-4954-ac1f-1232aa6825da" />



---

## CloudWatch Logs Verification

The execution logs were reviewed in Amazon CloudWatch to confirm successful execution of the Lambda function.

### Screenshot

<img width="3808" height="929" alt="image" src="https://github.com/user-attachments/assets/bffe5339-5413-4e2c-91de-9b5921b3bec6" />


---

## Outcome

Successfully automated EC2 instance management using AWS Lambda and Boto3. The Lambda function detects EC2 instances based on tags and performs start/stop actions automatically.

---

## Author

Ali Hussain

GitHub Repository:

```text
https://github.com/risingali-new/aws-lambda-boto3-automation
```
