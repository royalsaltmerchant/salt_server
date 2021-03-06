from flask import request, Blueprint, Response, jsonify
from salt import db, bcrypt
from salt.models import Project, Entry, Contribution, ContributedAsset
from salt.users.routes import token_required
from salt.serializers import ProjectSchema, EntrySchema, ContributionSchema, ContributedAssetSchema
import logging, json

projects = Blueprint('projects', __name__)

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)

contribution_schema = ContributionSchema()
contributions_schema = ContributionSchema(many=True)

contributed_asset_schema = ContributedAssetSchema()
contributed_assets_schema = ContributedAssetSchema(many=True)

@projects.route("/api/get_project", methods=['POST'])
def api_get_project():
  data = json.loads(request.data)
  project_id = data['project_id']
  project = db.session.query(Project).filter_by(id=project_id).first()

  project_serialized = project_schema.dump(project)
  response = Response(
      response=json.dumps(project_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

@projects.route("/api/projects", methods=['GET'])
def api_projects():
  all_projects = Project.query.all()

  projects_serialized = projects_schema.dump(all_projects)
  response = Response(
      response=json.dumps(projects_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

@projects.route('/api/add_project', methods=['POST'])
@token_required
def api_add_project(current_user):
  data = json.loads(request.data)
  title = data['title']
  description = data['description']
  image_file = data['image_file']

  project = Project(title=title, description=description, image_file=image_file)
  db.session.add(project)
  db.session.commit()

  project_serialized = project_schema.dump(project)
  response = Response(
      response=json.dumps(project_serialized),
      status=201,
      mimetype='application/json'
  )

  return response

@projects.route('/api/edit_project', methods=['POST'])
@token_required
def api_edit_project(current_user):
  data = json.loads(request.data)
  project_id = data['project_id']
  project_to_edit = db.session.query(Project).filter_by(id=project_id).first()
  if 'title' in data:
    project_to_edit.title = data['title']
  if 'description' in data:
    project_to_edit.description = data['description']
  if 'image_file' in data:
    project_to_edit.image_file = data['image_file']
  if 'active' in data:
    project_to_edit.active = data['active']
  if 'complete' in data:
    project_to_edit.complete = data['complete']

  db.session.commit()

  project_serialized = project_schema.dump(project_to_edit)
  response = Response(
      response=json.dumps(project_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

@projects.route('/api/remove_project', methods=['POST'])
@token_required
def api_remove_project(current_user):
  data = json.loads(request.data)
  project_id = data['project_id']
  project_to_delete = db.session.query(Project).filter_by(id=project_id).first()

  db.session.delete(project_to_delete)
  db.session.commit()

  return Response(
      response='project has been removed',
      status=200
      )

@projects.route("/api/entries", methods=['GET'])
def api_entries():
  all_entries = Entry.query.all()

  entries_serialized = entries_schema.dump(all_entries)
  response = Response(
      response=json.dumps(entries_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

@projects.route("/api/get_entry", methods=['POST'])
def api_get_entry():
  data = json.loads(request.data)
  entry_id = data['entry_id']
  entry = db.session.query(Entry).filter_by(id=entry_id).first()

  entry_serialized = entry_schema.dump(entry)
  response = Response(
      response=json.dumps(entry_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

@projects.route('/api/add_entry', methods=['POST'])
@token_required
def api_add_entry(current_user):
  data = json.loads(request.data)
  project_id = data['project_id']
  title = data['title']
  description = data['description']
  amount = data['amount']

  entry = Entry(project_id=project_id, title=title, description=description, amount=amount)
  db.session.add(entry)
  db.session.commit()

  entry_serialized = entry_schema.dump(entry)
  response = Response(
      response=json.dumps(entry_serialized),
      status=201,
      mimetype='application/json'
  )

  return response

@projects.route('/api/edit_entry', methods=['POST'])
@token_required
def api_edit_entry(current_user):
  data = json.loads(request.data)
  entry_id = data['entry_id']
  entry_to_edit = db.session.query(Entry).filter_by(id=entry_id).first()
  if 'title' in data:
    entry_to_edit.title = data['title']
  if 'amount' in data:
    entry_to_edit.amount = data['amount']
  if 'description' in data:
    entry_to_edit.description = data['description']
  if 'complete' in data:
    entry_to_edit.complete = data['complete']

  db.session.commit()

  entry_serialized = entry_schema.dump(entry_to_edit)
  response = Response(
      response=json.dumps(entry_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

@projects.route('/api/remove_entry', methods=['POST'])
@token_required
def api_remove_entry(current_user):
  data = json.loads(request.data)
  entry_id = data['entry_id']
  entry_to_delete = db.session.query(Entry).filter_by(id=entry_id).first()

  db.session.delete(entry_to_delete)
  db.session.commit()

  return Response(
      response='entry has been removed',
      status=200
      )

@projects.route("/api/get_contribution", methods=['POST'])
@token_required
def api_get_contribution(current_user):
  data = json.loads(request.data)
  contribution_id = data['contribution_id']
  contribution = db.session.query(Contribution).filter_by(id=contribution_id).first()

  contribution_serialized = contribution_schema.dump(contribution)
  response = Response(
      response=json.dumps(contribution_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

@projects.route('/api/add_contribution', methods=['POST'])
@token_required
def api_add_contribution(current_user):
  data = json.loads(request.data)
  entry_id = data['entry_id']
  project_id = data['project_id']
  user_id = current_user.id
  amount = data['amount']

  contribution = Contribution(entry_id=entry_id, project_id=project_id, user_id=user_id, amount=amount)
  db.session.add(contribution)
  db.session.commit()

  contribution_serialized = contribution_schema.dump(contribution)
  response = Response(
      response=json.dumps(contribution_serialized),
      status=201,
      mimetype='application/json'
  )

  return response

@projects.route('/api/edit_contribution', methods=['POST'])
@token_required
def api_edit_contribution(current_user):
  data = json.loads(request.data)
  contribution_id = data['contribution_id']
  contribution_to_edit = db.session.query(Contribution).filter_by(id=contribution_id).first()
  if 'amount' in data:
    contribution_to_edit.amount = data['amount']
  if 'status' in data:
    contribution_to_edit.status = data['status']
  db.session.commit()

  contribution_serialized = contribution_schema.dump(contribution_to_edit)
  response = Response(
      response=json.dumps(contribution_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

@projects.route('/api/remove_contribution', methods=['POST'])
@token_required
def api_remove_contribution(current_user):
  data = json.loads(request.data)
  contribution_id = data['contribution_id']
  contribution_to_delete = db.session.query(Contribution).filter_by(id=contribution_id).first()

  db.session.delete(contribution_to_delete)
  db.session.commit()

  return Response(
      response='contribution has been removed',
      status=200
      )

@projects.route('/api/add_contributed_asset', methods=['POST'])
@token_required
def api_add_contributed_asset(current_user):
  data = json.loads(request.data)
  contribution_id = data['contribution_id']
  name = data['name']
  uuid = data['uuid']

  contributed_asset = ContributedAsset(contribution_id=contribution_id, name=name, uuid=uuid)
  db.session.add(contributed_asset)
  db.session.commit()

  contributed_asset_serialized = contributed_asset_schema.dump(contributed_asset)
  response = Response(
      response=json.dumps(contributed_asset_serialized),
      status=201,
      mimetype='application/json'
  )

  return response

@projects.route('/api/edit_contributed_asset', methods=['POST'])
@token_required
def api_edit_contributed_asset(current_user):
  data = json.loads(request.data)
  contributed_asset_id = data['contributed_asset_id']
  contributed_asset_to_edit = db.session.query(ContributedAsset).filter_by(id=contributed_asset_id).first()
  if 'status' in data:
    contributed_asset_to_edit.status = data['status']
  db.session.commit()

  contributed_asset_serialized = contributed_asset_schema.dump(contributed_asset_to_edit)
  response = Response(
      response=json.dumps(contributed_asset_serialized),
      status=200,
      mimetype='application/json'
  )
  return response

