import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Load environment variables from .env file
load_dotenv()
def test_connection():
    print("Loading AWS credentials from .env...")

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION")

    if not access_key or not secret_key:
        print("ERROR: Could not find AWS credentials in .env file.")
        return

    print(f"Region loaded: {region}")
    print("Attempting to connect to AWS using STS (Security Token Service)...")

    try:
        sts_client = boto3.client(
            "sts",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )
        identity = sts_client.get_caller_identity()

        print("\nSUCCESS! Connected to AWS.")
        print(f"Account ID: {identity['Account']}")
        print(f"User ARN:   {identity['Arn']}")
        print(f"User ID:    {identity['UserId']}")

    except NoCredentialsError:
        print("ERROR: No credentials found. Check your .env file.")
    except ClientError as e:
        print(f"ERROR: AWS rejected the credentials. Details: {e}")
    except Exception as e:
        print(f"ERROR: Unexpected error occurred: {e}")

if __name__ == "__main__":
    test_connection()