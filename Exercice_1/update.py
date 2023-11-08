import boto3
import json
import sys

input_filename = sys.argv[1]
with open(input_filename,"r", encoding="utf-8") as input_file:
    env = json.load(input_file)
print(env)

session = boto3.Session()
Lambda = session.client('lambda', region_name=env['Localisation'])

response = Lambda.update_function_configuration(
    FunctionName=env['LambdaName'],
    Timeout=10,
    Runtime='python3.11'
)
print(response)
