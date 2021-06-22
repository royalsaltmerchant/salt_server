from flask import request, Blueprint, Response, jsonify
from salt import db, bcrypt
from salt.models import Project, Entry
from salt.users.routes import token_required
from salt.serializers import ProjectSchema, EntrySchema
import logging, json

projects = Blueprint('projects', __name__)

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)

@projects.route("/api/projects", methods=['GET'])
def api_projects():
  try:
    all_projects = Project.query.all()

    projects_serialized = projects_schema.dump(all_projects)
    response = Response(
        response=json.dumps(projects_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@projects.route('/api/add_project', methods=['POST'])
@token_required
def api_add_project(current_user):
  try:
    data = json.loads(request.data)
    title = data['title']
    description = data['description']
    image_file = data['image_file']
    active = data['active']
    complete = data['complete']

    project = Project(title=title, description=description, image_file=image_file, active=active, complete=complete)
    db.session.add(project)
    db.session.commit()

    project_serialized = project_schema.dump(project)
    response = Response(
        response=json.dumps(project_serialized),
        status=201,
        mimetype='application/json'
    )

    return response
  except:
    raise

@projects.route('/api/edit_project', methods=['POST'])
@token_required
def api_edit_project(current_user):
  try:
    data = json.loads(request.data)
    project_id = data['project_id']
    project_to_edit = db.session.query(Project).filter_by(id=project_id).first()
    project_to_edit.title = data['title']
    project_to_edit.description = data['description']
    project_to_edit.image_file = data['image_file']
    project_to_edit.active = data['active']
    project_to_edit.complete = data['complete']

    db.session.commit()

    project_serialized = project_schema.dump(project_to_edit)
    response = Response(
        response=json.dumps(project_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@projects.route('/api/remove_project', methods=['POST'])
@token_required
def api_remove_project(current_user):
  try:
    data = json.loads(request.data)
    project_id = data['project_id']
    project_to_delete = db.session.query(Project).filter_by(id=project_id).first()

    db.session.delete(project_to_delete)
    db.session.commit()

    return Response(
        response='project has been removed',
        status=200
        )
  except:
    raise

@projects.route("/api/entries", methods=['GET'])
def api_entries():
  try:
    all_entries = Entry.query.all()

    entries_serialized = entries_schema.dump(all_entries)
    response = Response(
        response=json.dumps(entries_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@projects.route('/api/add_entry', methods=['POST'])
@token_required
def api_add_entry(current_user):
  try:
    data = json.loads(request.data)
    title = data['title']
    description = data['description']
    amount = data['amount']
    complete = data['complete']

    entry = Entry(title=title, description=description, amount=amount, complete=complete)
    db.session.add(entry)
    db.session.commit()

    entry_serialized = entry_schema.dump(entry)
    response = Response(
        response=json.dumps(entry_serialized),
        status=201,
        mimetype='application/json'
    )

    return response
  except:
    raise

@projects.route('/api/edit_entry', methods=['POST'])
@token_required
def api_edit_entry(current_user):
  try:
    data = json.loads(request.data)
    entry_id = data['entry_id']
    entry_to_edit = db.session.query(Entry).filter_by(id=entry_id).first()
    entry_to_edit.title = data['title']
    entry_to_edit.amount = data['amount']
    entry_to_edit.description = data['description']
    entry_to_edit.complete = data['complete']

    db.session.commit()

    entry_serialized = entry_schema.dump(entry_to_edit)
    response = Response(
        response=json.dumps(entry_serialized),
        status=200,
        mimetype='application/json'
    )
    return response
  except:
    raise

@projects.route('/api/remove_entry', methods=['POST'])
@token_required
def api_remove_entry(current_user):
  try:
    data = json.loads(request.data)
    entry_id = data['entry_id']
    entry_to_delete = db.session.query(Entry).filter_by(id=entry_id).first()

    db.session.delete(entry_to_delete)
    db.session.commit()

    return Response(
        response='entry has been removed',
        status=200
        )
  except:
    raise