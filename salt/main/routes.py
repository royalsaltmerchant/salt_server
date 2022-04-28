from flask import render_template, url_for, flash, redirect, request, Blueprint, Response, jsonify, current_app
from salt import db
import logging, json, os, wave, math
from salt.models import User, TrackAsset
from salt.serializers import TrackAssetSchema
from salt.users.routes import token_required
import boto3
from botocore.exceptions import ClientError
from mutagen.wave import WAVE   
from sqlalchemy import func, asc
from sqlalchemy.orm.attributes import flag_modified
import wave

main = Blueprint('main', __name__)

track_asset_schema = TrackAssetSchema()
track_assets_schema = TrackAssetSchema(many=True)

@main.route('/api/signed_URL_download', methods=['POST'])
def create_presigned_url():
    s3_client = boto3.client('s3')
    try:
        data = json.loads(request.data)
        bucket_name = data['bucket_name']
        object_name = data['object_name']
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=86400)
    except ClientError as e:
        logging.error(e)
        return None

    return response

@main.route('/api/signed_URL_upload', methods=['POST'])
def create_presigned_post():
    s3_client = boto3.client('s3')
    try:
        data = json.loads(request.data)
        bucket_name = data['bucket_name']
        object_name = data['object_name']
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=None,
                                                     Conditions=None,
                                                     ExpiresIn=3600)
    except ClientError as e:
        logging.error(e)
        return None

    return response

