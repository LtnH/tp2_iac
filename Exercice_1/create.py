import boto3
import json
import sys

input_filename = sys.argv[1]
with open(input_filename,"r", encoding="utf-8") as input_file:
    env = json.load(input_file)
print(env)

session = boto3.Session()
s3 = session.client("s3", region_name=env['Localisation'])
Lambda = session.client('lambda', region_name=env['Localisation'])

try:
    s3.head_bucket(
        Bucket=env['BucketName']
    )
except :
    response = s3.create_bucket(
        Bucket=env['BucketName'],
        CreateBucketConfiguration={
           'LocationConstraint': env['Localisation']
        }
    )
    print(response)

response = s3.put_bucket_tagging(
    Bucket=env['BucketName'],
    Tagging={
        'TagSet': [
            {
                'Key': 'school',
                'Value': 'esgi',
            },
            {
                'Key': 'promotion',
                'Value': 'al-m2',
            },
            {
                'Key': 'user',
                'Value': 'vincentfabiano'
            }
        ]
    },
)
print(response)

response = s3.upload_file(
    "external/" + env['Filename'],
    env['BucketName'],
    env['Filename']
)
print(response)

response = Lambda.create_function(
    FunctionName=env['LambdaName'],
    Runtime='python3.10',
    Role=env['RoleName'],
    Handler='lambda_function.lambda_handler',
    Code={
        'S3Bucket': env['BucketName'],
        'S3Key': env['Filename']
    },
    Tags={
        'school': 'esgi',
        'promotion': 'al-m2',
        'user': 'VincentFabiano'
    }
)
print(response)
