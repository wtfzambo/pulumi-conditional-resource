import json

import pulumi
import pulumi_aws as aws
from pulumi_aws import s3, ssm

STACK_NAME = pulumi.get_stack()
AWS_ACCOUNT_ID = aws.get_caller_identity().id
PARAMETER_NAME = f'/pulumiExample/{STACK_NAME}/shouldCreateBucket'
BUCKET_NAME = f'pulumiexample-{STACK_NAME}-{AWS_ACCOUNT_ID}'

parameter = ssm.get_parameter(name=PARAMETER_NAME)
should_create_bucket = json.loads(parameter.value)

bucket = (
    # resource_name represents only the name of the resource managed by pulumi.
    # By default, pulumi appends a random string to the end of the name
    # of each resource created in order to prevent collisions.
    # If you want the bucket name to be the exact same, you need
    # to also specify the `bucket` arg.
    s3.Bucket(
        resource_name=BUCKET_NAME,
        bucket=BUCKET_NAME
    ) if should_create_bucket
    else s3.get_bucket(bucket=BUCKET_NAME)
)

# Export the resources value to be referenced in another stack
pulumi.export('Parameter value', parameter.value)
pulumi.export('Bucket Arn', bucket.arn)
