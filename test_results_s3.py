import os
import unittest

import boto3
from moto import mock_s3

from results_s3 import ResultsS3


class TestResultsS3(unittest.TestCase):
    @mock_s3
    def test_upload(self):
        path = "__s3__test__path"
        bucket = "__s3__test__bucket"
        content = "__s3__test__content"

        connection = boto3.resource('s3', region_name='us-east-1')
        connection.create_bucket(Bucket=bucket)
        ResultsS3(bucket, path).upload(content)

        self.assertFalse(os.path.isfile(path))
        self.assertEqual(content,
                         connection.Object(bucket, path).get()['Body'].read().decode())


if __name__ == '__main__':
    unittest.main()
