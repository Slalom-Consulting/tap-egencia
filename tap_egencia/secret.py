import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


def get_secret(secretKey: str):
    load_dotenv()
    secret_name = os.getenv('AWS_ACCOUNT')
    region_name = os.getenv('AWS_REGION')


    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        # Parse the JSON structure from the axios response
        parsedSecret = json.loads(get_secret_value_response['SecretString'])

        return parsedSecret[f"{secretKey}"]
    
    except ClientError as e:
        raise e
