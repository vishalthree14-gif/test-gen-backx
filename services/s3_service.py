import boto3
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


def upload_video(file_obj, key, content_type):
    s3.upload_fileobj(
        file_obj,
        BUCKET_NAME,
        key,
        ExtraArgs={"ContentType": content_type}
    )
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"



def generate_signed_url(key, expires_in=3600):
    
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": key
        },
        ExpiresIn=expires_in
    )


