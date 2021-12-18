from flask import render_template, url_for, flash, redirect, request, Blueprint, Response, jsonify, current_app
from salt import db
import logging, json, os, wave
from salt.models import User, TrackAsset
from salt.serializers import TrackAssetSchema
from salt.users.routes import token_required
import boto3
import audio_metadata
from botocore.exceptions import ClientError

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

@main.route('/api/get_track_assets/', methods=['GET'])
def api_get_all_track_assets():
    track_assets = TrackAsset.query.all()

    track_assets_serialized = track_assets_schema.dump(track_assets)
    response = Response(
        response=json.dumps(track_assets_serialized),
        status=200,
        mimetype='application/json'
    )
    return response

@main.route('/api/get_track_assets/<query>', methods=['GET'])
def api_get_track_assets(query):
    track_assets = TrackAsset.query.filter(TrackAsset.audio_metadata.contains(query))

    track_assets_serialized = track_assets_schema.dump(track_assets)
    response = Response(
        response=json.dumps(track_assets_serialized),
        status=200,
        mimetype='application/json'
    )
    return response

@main.route('/api/add_track_asset', methods=['POST'])
@token_required
def api_add_track_asset(current_user):
    audio_file = request.files['audio_file'].read()
    name = request.form['name']

    metadata = audio_metadata.loads(audio_file)
    metadata_tags = metadata['tags']
    metadata_genre = metadata_tags.genre[0]
    # logging.warning('#########################################################')
    # logging.warning(metadata_tags)

    
    track_asset = TrackAsset(name=name, audio_metadata=metadata_genre)
    db.session.add(track_asset)
    db.session.commit()

    track_asset_serialized = track_asset_schema.dump(track_asset)
    response = Response(
        response=json.dumps(track_asset_serialized),
        status=201,
        mimetype='application/json'
    )
    return response