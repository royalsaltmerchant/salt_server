from salt import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from sqlalchemy.types import (
    ARRAY
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    approved_asset_count = db.Column(db.Integer, nullable=True, default=0)
    coins = db.Column(db.Integer, nullable=True, default=30)
    active = db.Column(db.Boolean, default=True)
    premium = db.Column(db.Boolean, default=False)
    contributor = db.Column(db.Boolean, default=False)
    upload_count = db.Column(db.Integer, default=0)
    about = db.Column(db.String(), nullable=True)
    contributions = db.relationship('Contribution', backref='user', lazy=True)
    track_assets = db.relationship('TrackAsset', backref="user", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(), nullable=False)
    image_file = db.Column(db.String(120), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    entries = db.relationship('Entry', backref='project', lazy=True)
    contributions = db.relationship('Contribution', backref='project', lazy=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=1)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    contributions = db.relationship('Contribution', backref='entry', lazy=True)

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(60), nullable=False, default='Pending')
    amount = db.Column(db.Integer, nullable=False, default=1)
    contributed_assets = db.relationship('ContributedAsset', backref='contribution', lazy=True)

class ContributedAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(), default='pending')
    contribution_id = db.Column(db.Integer, db.ForeignKey('contribution.id'))

class TrackAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    audio_metadata = db.Column('metadata', ARRAY(db.String()))
    length = db.Column(db.Float())
    waveform = db.Column('waveform', ARRAY(db.Float))
    active = db.Column(db.Boolean, nullable=False, default=True)
    downloads = db.Column(db.Integer, nullable=False, default=0)

class Pack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(), nullable=False)
    image_file = db.Column(db.String(120), nullable=False)
    video_file = db.Column(db.String(120), nullable=False)
    downloads = db.Column(db.Integer, nullable=False, default=0)
    coin_cost = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False, default=False)
    asset_types = db.relationship('AssetType', backref='pack', lazy=True)

class AssetType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    pack_id = db.Column(db.Integer, db.ForeignKey('pack.id'))