from salt.models import User, Project, Entry, Contribution
from salt import ma
import logging, json

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "admin", "email", "password", "eligible", "approved_asset_count", "coins", "contributions")
    contributions = ma.Nested('ContributionSchema', many=True)

class ProjectSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Project
        fields = ("id", "title", "description", "image_file", "active", "complete", "entries", "contributions")
    entries = ma.Nested('EntrySchema', many=True)
    contributions = ma.Nested('ContributionSchema', many=True)

class EntrySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Entry
        fields = ("id", "project_id", "title", "description", "amount", "complete", "contributions")
    contributions = ma.Nested('ContributionSchema', many=True)

class ContributionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Contribution
        fields = ("id", "date_create", "amount", "project_id", "entry_id", "user_id", "status")