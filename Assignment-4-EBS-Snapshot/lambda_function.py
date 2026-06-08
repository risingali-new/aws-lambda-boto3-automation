
import boto3
import os
from datetime import datetime, timezone, timedelta

ec2 = ec2 = boto3.client(
    'ec2',
    region_name='eu-north-1'
)

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
