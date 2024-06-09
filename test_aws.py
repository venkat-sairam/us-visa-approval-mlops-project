import boto3
import boto3.session
from pprint import pprint
aws_console = boto3.session.Session(profile_name="default", region_name="us-east-2")

iam_client = aws_console.client("iam")
iam_console = aws_console.resource("iam")
# for user in iam_console.users.all():
#     print(user.name)

# for user in iam_client.list_users()['Users']:
#     pprint(user['UserName'])

# ec2_client = aws_console.client("ec2")
# pprint(ec2_client.describe_instances())

s3_client = aws_console.client("s3")
response = s3_client.list_buckets()

pprint(response['Buckets'][0]['Name'])


s3 = boto3.resource("s3")


res = s3_client.list_objects_v2(Bucket="banking-data-analysis-project")
pprint(res)