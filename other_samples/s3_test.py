from prefect.filesystems import S3

s3_block = S3.load("s3-prefect")

print(s3_block)