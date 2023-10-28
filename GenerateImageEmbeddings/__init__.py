import logging
import azure.functions as func
import json
import io
import os
import base64
from . import embeddings as emb

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Generate Image Embeddings Custom Skill: Python HTTP trigger function processed a request.')

    try:
        # get request body
        body = req.get_json()
        # prep return shape
        records = { 'values': [] }
        recordId = ""
        # get key and endpoint from Environment variables
        aiVisionEndpoint = os.environ['COMPUTER_VISION_ENDPOINT']
        aiVisionApiKey = os.environ['COMPUTER_VISION_KEY']

        logging.info("##### value length: {}".format(len(body["values"])))
        for record in body["values"]:
            recordId = record["recordId"]
            # Get the base64 encoded image
            encoded_image = record["data"]["image"]["data"]
            base64Bytes = encoded_image.encode('utf-8')
            image = base64.b64decode(base64Bytes)
            image_bytes_io = io.BytesIO(image)

            ret_embeddings = emb.generate_embeddings(image_bytes_io, aiVisionEndpoint, aiVisionApiKey)

            if ret_embeddings is None:
                records['values'].append(makeErrRes(recordId, '500', 'Unable to generate embeddings', 'Python Error'))
            else:
                records['values'].append(makeRes(recordId, ret_embeddings))

    except Exception as error:
        logging.exception('Python Error')
        records['values'].append(makeErrRes(recordId, '500', f'{type(error).__name__}: {str(error)}', 'Python Error'))

    return func.HttpResponse(body=json.dumps(records), headers={ 'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*" })


def makeRes(recordId, embeddings):
    response = {
        'recordId': recordId,
        'data': {
            'embeddings': embeddings,
            'error': {}
        }
    }
    return response

def makeErrRes(recordId, code, message, type):
    response = {
        'recordId': recordId,
        'data': {
            'embeddings': "",
            'error': {
                'code': code,
                'message': message,
                'type': type
            }
        }
    }
    return response