import os
import boto3

from src.config.settings import (
    AWS_REGION,
    S3_BUCKET,
    S3_VECTOR_PREFIX
)


client = boto3.client(
    "s3",
    region_name=AWS_REGION
)

# 업로드
def upload_vector_store():

    files = [
        "index.faiss",
        "documents.json",
        "ids.json",
        "metadatas.json"
    ]

    for file in files:

        local_path = f"vector_store/{file}"

        s3_key = (
            f"{S3_VECTOR_PREFIX}/{file}"
        )

        client.upload_file(
            local_path,
            S3_BUCKET,
            s3_key
        )

# 존재여부 확인 함수
def exists_vector_store():

    try:
        client.head_object(
            Bucket=S3_BUCKET,
            Key=f"{S3_VECTOR_PREFIX}/index.faiss"
        )

        return True

    except:
        return False
    
# 다운로드
def download_vector_store():

    os.makedirs(
        "vector_store",
        exist_ok=True
    )

    files = [
        "index.faiss",
        "documents.json",
        "ids.json",
        "metadatas.json"
    ]

    for file in files:

        client.download_file(
            S3_BUCKET,
            f"{S3_VECTOR_PREFIX}/{file}",
            f"vector_store/{file}"
        )