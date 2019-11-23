import os

import boto3

SOURCE_FILENAME = 'index.html'


class ResultsS3():
    def __init__(self, bucket, path=SOURCE_FILENAME):
        self.bucket = bucket
        self.path = path

    def upload(self, content):
        index = open(self.path, "w")
        index.write(content)
        index.close()

        s3 = boto3.client('s3')
        s3.upload_file(self.path, self.bucket, self.path, ExtraArgs={'ContentType': 'text/html'})

        os.remove(self.path)
