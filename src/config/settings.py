import os
from dotenv import load_dotenv


load_dotenv()


AWS_REGION = os.getenv("AWS_REGION")

SUMMARY_LAMBDA_NAME = os.getenv("SUMMARY_LAMBDA_NAME")
ROUTER_LAMBDA_NAME = os.getenv("ROUTER_LAMBDA_NAME")
GENERATE_LAMBDA_NAME = os.getenv("GENERATE_LAMBDA_NAME")


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

S3_BUCKET = os.getenv("S3_BUCKET")
S3_VECTOR_PREFIX = os.getenv("S3_VECTOR_PREFIX")