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

@main.route('/', methods=['GET'])
def health_check():
    # TODO: check health of system with a few things here
    # datbase connection is still solid, etc
    result = {
        "healthy": True,
        "environment": os.environ.get('FLASK_ENV'),
        "version": "0.0.1"
    }
    response = Response(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response

@main.route('/home')
def home():
  return render_template('home.html')

@main.route('/api/signed_URL', methods=['POST'])
@token_required
def create_presigned_url(current_user):
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

