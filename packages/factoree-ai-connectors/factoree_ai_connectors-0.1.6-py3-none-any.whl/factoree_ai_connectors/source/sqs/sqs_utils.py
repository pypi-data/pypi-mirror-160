def get_sqs_url(aws_account_number: int, region_name: str, s3_bucket: str) -> str:
    return f'https://sqs.{region_name}.amazonaws.com/{str(aws_account_number)}/{s3_bucket}-notifications'
