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

@main.route('/api/get_track_assets/', methods=['POST'])
def api_get_paginated_track_assets():
    data = json.loads(request.data)
    offset = data["offset"]
    amount = data["amount"]
    track_assets = TrackAsset.query.order_by(asc(TrackAsset.name)).offset(offset).limit(amount)
    track_assets_count = TrackAsset.query.all().count()
    remaining_amount = track_assets_count - (offset + amount)

    track_assets_serialized = track_assets_schema.dump(track_assets)

    response_data = {
        "tracks": track_assets_serialized,
        "track_count": track_assets_count,
        "remaning_amount": remaining_amount,
        "offset": offset,
        "amount": amount
        }
    response = Response(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@main.route('/api/get_track_assets_by_username/<username>', methods=['POST'])
def api_get_paginated_track_assets_by_username(username):
    data = json.loads(request.data)
    offset = data["offset"]
    amount = data["amount"]
    track_assets = db.session.query(TrackAsset).filter_by(author_username=username).order_by(asc(TrackAsset.name)).offset(offset).limit(amount)

    track_assets_count = TrackAsset.query.filter_by(author_username=username).all().count()
    remaining_amount = track_assets_count - (offset + amount)

    track_assets_serialized = track_assets_schema.dump(track_assets)

    response_data = {
        "tracks": track_assets_serialized,
        "track_count": track_assets_count,
        "remaning_amount": remaining_amount,
        "offset": offset,
        "amount": amount
        }
    response = Response(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@main.route('/api/get_track_assets/<query>', methods=['POST'])
def api_get_track_assets(query):
    data = json.loads(request.data)
    offset = data["offset"]
    amount = data["amount"]

    track_assets_to_serialize = []
    all_track_assets = TrackAsset.query.all()
    for asset in all_track_assets:
        metadata = asset.audio_metadata
        for item in metadata:
            if item == query:
                track_assets_to_serialize.append(asset)
    track_assets_by_name = TrackAsset.query.filter(func.lower(TrackAsset.name).contains(query))
    for asset in track_assets_by_name:
        if asset in track_assets_to_serialize:
            pass
        else:
            track_assets_to_serialize.append(asset)

    track_assets_serialized = track_assets_schema.dump(track_assets_to_serialize)

    response_data = {
        "tracks": track_assets_serialized,
        "track_count": len(track_assets_to_serialize),
        "remaning_amount": 0,
        "offset": offset,
        "amount": amount
        }

    response = Response(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@main.route('/api/add_track_asset', methods=['POST'])
@token_required
def api_add_track_asset(current_user):
    audio_file = request.files['audio_file']
    name = request.form['name']
    author_id = request.form['author_id']
    user_by_author_id = db.session.query(User).filter_by(id=author_id).first()
    author_username = user_by_author_id.username

    # get waveform
    waveform_samples_desired = 501
    keep_looping_through_frames = True
    volume_results = []
    with wave.open(audio_file, "rb") as wav_file:
        wave_frame_count = wav_file.getnframes()
        channels = wav_file.getnchannels()

        sample_frame_size = math.floor(wave_frame_count / waveform_samples_desired)
        frames_to_read_per_sample_frame = 1
        while keep_looping_through_frames:
            current_position = wav_file.tell()
            frames = wav_file.readframes(frames_to_read_per_sample_frame)

            left_channel = frames[:2]

            sixteen_bit_max_int: int = 32767 * 2

            left_int_from_bytes = int.from_bytes(left_channel, byteorder='big', signed=True)

            left_volume: float = left_int_from_bytes / sixteen_bit_max_int
            # logging.warning(left_volume)
            
            right_volume = 0
            if channels > 1:
                right_channel = frames[2:4]
                right_int_from_bytes = int.from_bytes(right_channel, byteorder='big', signed=True)
                right_volume = left_int_from_bytes / sixteen_bit_max_int
                # logging.warning(right_volume)
            

            next_position = current_position + sample_frame_size + 1
            if next_position > wave_frame_count:
                keep_looping_through_frames = False
                break
                
            wav_file.setpos(next_position)
            volume_results.append([left_volume, right_volume])
            # combine left and right channels
    combined_results = []
    for item in volume_results: 
        combined_results.append((item[0] + item[1]) / 2)
    # logging.warning(combined_results)

    # get metadata
    wave_meta = WAVE(audio_file)
    if 'TCON' in wave_meta:
        metadata = wave_meta['TCON'].text
        item_in_metadata = metadata[0]
        metadata_ready_for_list = item_in_metadata.replace(',', ' ',).lower()
        new_metadata_list = metadata_ready_for_list.split()
    else:
        new_metadata_list = []
    
    # get length
    audio_info = wave_meta.info
    length = round(audio_info.length, 2)
    track_asset = TrackAsset(name=name, author_id=author_id, author_username=author_username, audio_metadata=new_metadata_list, length=length, waveform=combined_results)
    db.session.add(track_asset)
    db.session.commit()

    track_asset_serialized = track_asset_schema.dump(track_asset)
    response = Response(
        response=json.dumps(track_asset_serialized),
        status=201,
        mimetype='application/json'
    )
    return response

@main.route('/api/edit_track_asset', methods=['POST'])
@token_required
def api_edit_track_asset(current_user):
    data = json.loads(request.data)
    track_id = data['track_id']
    track_to_edit = db.session.query(TrackAsset).filter_by(id=track_id).first()
    if 'downloads' in data:
        track_to_edit.downloads = data['downloads']
    if 'add_tag' in data:
        tag = data['add_tag']
        track_to_edit.audio_metadata.append(tag)
        flag_modified(track_to_edit, "audio_metadata")
        db.session.merge(track_to_edit)
    if 'remove_tag' in data:
        tag = data['remove_tag']
        track_to_edit.audio_metadata.remove(tag)
        flag_modified(track_to_edit, "audio_metadata")
        db.session.merge(track_to_edit)      

    db.session.commit()

    track_asset_serialized = track_asset_schema.dump(track_to_edit)
    response = Response(
        response=json.dumps(track_asset_serialized),
        status=200,
        mimetype='application/json'
    )
    return response

@main.route('/api/remove_track_asset', methods=['POST'])
@token_required
def api_remove_track_asset(current_user):
    data = json.loads(request.data)
    track_id = data['track_id']
    track_to_remove = db.session.query(TrackAsset).filter_by(id=track_id).first()
    
    db.session.delete(track_to_remove)
    db.session.commit()

    return Response(
        response='track has been removed',
        status=200
        )