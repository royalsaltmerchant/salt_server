from flask import request, Blueprint, Response
from salt import db
import logging, json, wave, math
from salt.models import User, TrackAsset
from salt.serializers import TrackAssetSchema
from salt.users.routes import token_required
from mutagen.wave import WAVE   
from sqlalchemy import desc, func, asc
from sqlalchemy.orm.attributes import flag_modified
import wave

tracks = Blueprint('tracks', __name__)

track_asset_schema = TrackAssetSchema()
track_assets_schema = TrackAssetSchema(many=True)

@tracks.route('/api/get_track_assets_by_username/<username>', methods=['POST'])
def api_get_paginated_track_assets_by_username(username):
    data = json.loads(request.data)
    offset = data["offset"]
    limit = data["limit"]
    if "query" in data:
        query = data["query"]
    else:
         query = None

    track_assets_by_username = db.session.query(TrackAsset).filter_by(author_username=username).all()

    track_assets_to_serialize = []
    
    if query:
        for asset in track_assets_by_username:
            metadata = asset.audio_metadata
            for item in metadata:
                if item == query:
                    track_assets_to_serialize.append(asset)
        track_assets_by_name = TrackAsset.query.filter_by(author_username=username).filter(func.lower(TrackAsset.name).contains(query))
        for asset in track_assets_by_name:
            if asset in track_assets_to_serialize:
                pass
            else:
                track_assets_to_serialize.append(asset)
        track_assets_count = len(track_assets_to_serialize)
    else:
        for asset in track_assets_by_username:
            track_assets_to_serialize.append(asset)
        track_assets_count = len(track_assets_to_serialize)
    
    remaining_amount = track_assets_count - (offset + limit)

    track_assets_offset_limit = track_assets_to_serialize[offset:(limit + offset)]
    track_assets_serialized = track_assets_schema.dump(track_assets_offset_limit)

    response_data = {
        "tracks": track_assets_serialized,
        "track_count": track_assets_count,
        "remaning_amount": remaining_amount,
        "offset": offset,
        "amount": limit
        }
    response = Response(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@tracks.route('/api/get_track_assets', methods=['POST'])
def api_get_track_assets():
    data = json.loads(request.data)
    offset = data["offset"]
    limit = data["limit"]
    if "query" in data:
        query = data["query"]
    else:
        query = None
    if "filter" in data:
        filter = data["filter"]
    else:
        filter = None

    all_track_assets = []
    track_assets_to_serialize = []

    if filter:
        if filter != 'popular':
            assets = TrackAsset.query.order_by(asc(TrackAsset.name)).all()
            for asset in assets:
                for item in asset.audio_metadata:
                    if item == filter:
                        all_track_assets.append(asset)
        if filter == 'popular':
            track_assets_by_popularity = TrackAsset.query.order_by(desc(TrackAsset.downloads)).limit(30)
            for asset in track_assets_by_popularity:
                if asset.downloads > 0:
                    all_track_assets.append(asset)
    else:
        assets = TrackAsset.query.order_by(asc(TrackAsset.name)).all()
        for asset in assets:
            all_track_assets.append(asset)

        
    if query:
        for asset in all_track_assets:
            metadata = asset.audio_metadata
            for item in metadata:
                if item == query:
                    track_assets_to_serialize.append(asset)
        for asset in all_track_assets:
            if query in asset.name.lower():
                if asset in track_assets_to_serialize:
                    pass
                else:
                    track_assets_to_serialize.append(asset)

    else:
        track_assets_to_serialize = all_track_assets

    track_assets_count = len(track_assets_to_serialize)    
    remaining_amount = track_assets_count - (offset + limit)
    track_assets_offset_limit = track_assets_to_serialize[offset:(limit + offset)]
    track_assets_serialized = track_assets_schema.dump(track_assets_offset_limit)

    response_data = {
        "tracks": track_assets_serialized,
        "track_count": track_assets_count,
        "remaning_amount": remaining_amount,
        "offset": offset,
        "amount": limit
        }

    response = Response(
        response=json.dumps(response_data),
        status=200,
        mimetype='application/json'
    )
    return response

@tracks.route('/api/add_track_asset', methods=['POST'])
@token_required
def api_add_track_asset(current_user):
    audio_file = request.files['audio_file']
    name = request.form['name']
    uuid = request.form['uuid']
    author_id = request.form['author_id']
    user_by_author_id = db.session.query(User).filter_by(id=author_id).first()
    user_by_author_id.upload_count = user_by_author_id.upload_count + 1
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
    
    track_asset = TrackAsset(name=name, uuid=uuid, author_id=author_id, author_username=author_username, audio_metadata=new_metadata_list, length=length, waveform=combined_results)
    db.session.add(track_asset)
    db.session.commit()

    track_asset_serialized = track_asset_schema.dump(track_asset)
    response = Response(
        response=json.dumps(track_asset_serialized),
        status=201,
        mimetype='application/json'
    )
    return response

@tracks.route('/api/edit_track_asset', methods=['POST'])
@token_required
def api_edit_track_asset(current_user):
    data = json.loads(request.data)
    track_id = data['track_id']
    track_to_edit = db.session.query(TrackAsset).filter_by(id=track_id).first()
    user_by_author_id = db.session.query(User).filter_by(id=track_to_edit.author_id).first()
    user_by_author_id.upload_count = user_by_author_id.upload_count - 1
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

@tracks.route('/api/remove_track_asset', methods=['POST'])
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