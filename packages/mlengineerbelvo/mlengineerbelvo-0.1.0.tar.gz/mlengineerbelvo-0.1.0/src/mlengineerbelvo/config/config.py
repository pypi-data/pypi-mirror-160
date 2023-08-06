from dataclasses import dataclass


@dataclass
class AWSConfig:
    aws_key: str
    aws_secret: str
