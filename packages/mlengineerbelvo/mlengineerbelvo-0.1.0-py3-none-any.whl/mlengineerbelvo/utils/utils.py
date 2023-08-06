"""BaseLogger class"""
import logging
import sys
from io import StringIO

import boto3
import pandas as pd
from mlengineerbelvo.config.config import AWSConfig


class BaseLogger:
    def __init__(self):
        self.logger = self.__logger_settings()

    def __logger_settings(self):
        """configure logger instance

        Returns:
            _type_: _description_
        """

        logging.basicConfig(
            format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
            level=logging.INFO,
            datefmt="%H:%M:%S",
            stream=sys.stderr,
        )
        logger = logging.getLogger(__name__)

        return logger


class S3Manager:
    """S3 Bucket Manager Class"""

    def __init__(self, bucket: str, config: AWSConfig) -> None:
        """S3 Manager initization
        Args:
            bucket (str): S3 bucket name
            config (AWSConfig): AWS configuration
        """
        self._s3 = boto3.resource(
            "s3",
            aws_access_key_id=config.aws_key,
            aws_secret_access_key=config.aws_secret,
        )
        self._bucket = bucket

    def upload(self, file: str, path: str) -> None:
        """Upload files to S3 bucket
        Args:
            file (str): local file to upload
            path (str): S3 path
        """
        self._s3.Bucket(self._bucket).upload_file(file, path)

    def upload_pandas_dataframe(self, dataframe: pd.DataFrame, path: str) -> None:
        """Upload pandas dataframe in S3 Bucket Path
        Args:
            dataframe (pd.DataFrame): pandas dataframe
            path (str): S3 path
        """
        buffer = StringIO()
        dataframe.to_csv(buffer, index=False)
        self._s3.Object(self._bucket, path).put(Body=buffer.getvalue())

    def download(self, pathfile: str, localpath: str):
        """Download files form S3 brucket
        Args:
            pathfile (str): S3 file path
            localpath (str): local path
        """
        self._s3.Bucket(self._bucket).download_file(pathfile, localpath)
