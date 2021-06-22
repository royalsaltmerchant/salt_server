from salt.models import User, Project, Entry
from salt import ma
import logging, json

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "admin", "email", "password", "eligible", "approved_asset_count")

class ProjectSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Project
        fields = ("id", "title", "description", "image_file", "active", "complete")

class EntrySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Entry
        fields = ("id", "title", "description", "amount", "complete")