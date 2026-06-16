import boto3
import json

from src.config.settings import AWS_REGION


client = boto3.client(
    "lambda",
    region_name=AWS_REGION
)


def invoke_lambda(payload, function_name):

    
    response = client.invoke(
        FunctionName=function_name,
        Payload=json.dumps(payload)
    )

    result = json.loads(
        response["Payload"].read()
    )
  
    print(result)

    if "body" not in result:
        raise Exception(
            f"Lambda Error: {result}"
        )

    body = json.loads(
        result["body"]
    )

    return body["result"]

