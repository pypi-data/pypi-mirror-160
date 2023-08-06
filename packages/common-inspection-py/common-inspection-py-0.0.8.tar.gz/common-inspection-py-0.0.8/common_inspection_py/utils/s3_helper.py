import asyncio

import boto3
import pandas as pd
from boto3.s3.transfer import TransferConfig


async def getS3Data(params: any):
    s3 = boto3.resource("s3")

    try:
        obj = s3.Object(params['Bucket'], params['Key'])
        data_content = obj.get()['Body'].read()

        print({"data": params['Key'], "success": True})

        return {
            "file_key": obj.key,
            "file_body": data_content.decode('utf-8'),
            "file_length": obj.content_length}

    except OSError as e:
        print(e)
        return e


async def putS3Data(params: any):
    s3 = boto3.resource('s3')
    try:
        s3object = s3.Object(params['Bucket'], params['Key'])
        s3object.put(
            Body=params["Body"]
        )
        print({"data": params['Key'], "success": True})
        return {"data": params['Key'], "success": True}
    except OSError as e:
        print(e)
        return e


async def convertToCSV(params: any):
    with open(params, encoding='utf-8') as inputfile:
        df = pd.read_json(inputfile)

    return await df
