import json
import os
import boto3

dynamo = boto3.resource('dynamodb')


def copy_items(SOURCE_TABLE, DEST_TABLE):
    source_table = dynamo.Table(SOURCE_TABLE)

    response = source_table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = source_table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    dest_table = dynamo.Table(DEST_TABLE)
    with dest_table.batch_writer() as writer:
        for item in data:
            writer.put_item(Item=item)


def lambda_handler(event, context):
    SOURCE_TABLE = os.environ['SOURCE_TABLE']
    DEST_TABLE = os.environ['DEST_TABLE']
