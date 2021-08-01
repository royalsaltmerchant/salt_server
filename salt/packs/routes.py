from flask import request, Blueprint, Response, jsonify
from salt import db, bcrypt
from salt.models import Pack, AssetType
from salt.users.routes import token_required
from salt.serializers import PackSchema, AssetTypeSchema
import logging, json

packs = Blueprint('packs', __name__)

pack_schema = PackSchema()
packs_schema = PackSchema(many=True)

asset_type_schema = AssetTypeSchema()
asset_types_schema = AssetTypeSchema(many=True)

@packs.route("/api/packs", methods=['GET'])
def api_packs():
  try:
    all_packs = Pack.query.all()

    packs_serialized = packs_schema.dump(all_packs)
    response = Response(
        response=json.dumps(packs_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@packs.route("/api/get_pack_by_title", methods=['POST'])
def api_get_pack_by_title():
  try:
    data = json.loads(request.data)
    pack_title = data['pack_title']
    pack = db.session.query(Pack).filter_by(title=pack_title).first()

    pack_serialized = pack_schema.dump(pack)
    response = Response(
        response=json.dumps(pack_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@packs.route('/api/add_pack', methods=['POST'])
@token_required
def api_add_pack(current_user):
  try:
    data = json.loads(request.data)
    title = data['title']
    description = data['description']
    image_file = data['image_file']
    video_file = data['video_file']
    coin_cost = data['coin_cost']

    pack = Pack(title=title, description=description, image_file=image_file, video_file=video_file, coin_cost=coin_cost)
    db.session.add(pack)
    db.session.commit()

    pack_serialized = pack_schema.dump(pack)
    response = Response(
        response=json.dumps(pack_serialized),
        status=201,
        mimetype='application/json'
    )

    return response
  except:
    raise

@packs.route('/api/edit_pack', methods=['POST'])
@token_required
def api_edit_pack(current_user):
  try:
    data = json.loads(request.data)
    pack_id = data['pack_id']
    pack_to_edit = db.session.query(Pack).filter_by(id=pack_id).first()
    if 'title' in data:
      pack_to_edit.title = data['title']
    if 'description' in data:
      pack_to_edit.description = data['description']
    if 'image_file' in data:
      pack_to_edit.image_file = data['image_file']
    if 'video_file' in data:
      pack_to_edit.video_file = data['video_file']
    if 'coin_cost' in data:
      pack_to_edit.coin_cost = data['coin_cost']
    if 'active' in data:
      pack_to_edit.active = data['active']
    if 'downloads' in data:
      pack_to_edit.downloads = data['downloads']

    db.session.commit()

    pack_serialized = pack_schema.dump(pack_to_edit)
    response = Response(
        response=json.dumps(pack_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@packs.route('/api/remove_pack', methods=['POST'])
@token_required
def api_remove_pack(current_user):
  try:
    data = json.loads(request.data)
    pack_id = data['pack_id']
    pack_to_delete = db.session.query(Pack).filter_by(id=pack_id).first()

    db.session.delete(pack_to_delete)
    db.session.commit()

    return Response(
        response='pack has been removed',
        status=200
        )
  except:
    raise

@packs.route("/api/asset_types", methods=['GET'])
def api_asset_types():
  try:
    all_asset_types = AssetType.query.all()

    asset_types_serialized = asset_types_schema.dump(all_asset_types)
    response = Response(
        response=json.dumps(asset_types_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@packs.route("/api/get_asset_type", methods=['POST'])
def api_get_asset_type():
  try:
    data = json.loads(request.data)
    asset_type_id = data['asset_type_id']
    asset_type = db.session.query(AssetType).filter_by(id=asset_type_id).first()

    asset_type_serialized = asset_type_schema.dump(asset_type)
    response = Response(
        response=json.dumps(asset_type_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@packs.route('/api/add_asset_type', methods=['POST'])
@token_required
def api_add_asset_type(current_user):
  try:
    data = json.loads(request.data)
    description = data['description']
    pack_id = data['pack_id']

    asset_type = AssetType(description=description, pack_id=pack_id)
    db.session.add(asset_type)
    db.session.commit()

    asset_type_serialized = asset_type_schema.dump(asset_type)
    response = Response(
        response=json.dumps(asset_type_serialized),
        status=201,
        mimetype='application/json'
    )

    return response
  except:
    raise

@packs.route('/api/edit_asset_type', methods=['POST'])
@token_required
def api_edit_asset_type(current_user):
  try:
    data = json.loads(request.data)
    asset_type_id = data['asset_type_id']
    asset_type_to_edit = db.session.query(AssetType).filter_by(id=asset_type_id).first()
    if 'description' in data:
      asset_type_to_edit.description = data['description']

    db.session.commit()

    asset_type_serialized = asset_type_schema.dump(asset_type_to_edit)
    response = Response(
        response=json.dumps(asset_type_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@packs.route('/api/remove_asset_type', methods=['POST'])
@token_required
def api_remove_asset_type(current_user):
  try:
    data = json.loads(request.data)
    asset_type_id = data['asset_type_id']
    asset_type_to_delete = db.session.query(AssetType).filter_by(id=asset_type_id).first()

    db.session.delete(asset_type_to_delete)
    db.session.commit()

    return Response(
        response='asset_type has been removed',
        status=200
        )
  except:
    raise