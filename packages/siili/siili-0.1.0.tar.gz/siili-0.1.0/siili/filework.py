# -*- coding: utf-8 -*-
import datetime
import logging
import os
from typing import Any

import boto3
import colorlog
from botocore.exceptions import ClientError
from environs import Env
from yaspin import yaspin
from yaspin.spinners import Spinners

logger = logging.getLogger(__name__)
logger.setLevel(colorlog.ERROR)

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter())
logger.addHandler(handler)


def upload(file_name: str, object_name: Any = None) -> bool:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=env("AWS_ACCESS_KEY"),
        aws_secret_access_key=env("AWS_ACCESS_SECRET_KEY"),
    )
    bucket = env("AWS_BUCKET")

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        logger.debug("No object name specified, using yyyy-mm-dd_hh-mm-ss__file-name")
        logger.debug(f"attempting to path: {object_name}")
        object_name = os.path.basename(str(current_time) + "__" + str(file_name))

    logger.debug(f"object_name: {object_name}")

    # Upload the file

    with yaspin(
        Spinners.circle, text=f"Uploading {file_name}...", color="yellow"
    ) as spinner:
        try:
            response = s3.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            spinner.ok(f"❌ Failed to upload {file_name} to {bucket}.")
            logging.error(e)
            return False
        finally:
            spinner.ok(f"✅ Uploaded {file_name} to {bucket}.\n")
            logger.debug(f"response type: {type(response)}")
            logger.info(f"response: {response}")

    print(
        "https://s3.console.aws.amazon.com/s3/buckets/{}/{}".format(bucket, object_name)
    )
    return True


env = Env()
env.read_env()  # read .env file, if it exists
# required variables
aws_key: str = env("AWS_ACCESS_KEY")
aws_secret_key: str = env("AWS_ACCESS_SECRET_KEY")
aws_bucket: str = env("AWS_BUCKET")


if __name__ == "__main__":
    logger.debug("This is what DEBUG looks like.")
    logger.info("This is what INFO looks like.")
    logger.warning("This is what WARNING looks like.")
    logger.error("This is what ERROR looks like.")
    logger.critical("This is what CRITICAL looks like.")
