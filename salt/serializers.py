from salt.models import TrackAsset, User, Project, Entry, Contribution, Pack, AssetType, ContributedAsset
from salt import ma
import logging, json

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "active", "first_name", "last_name", "username", "admin", "email", "address", "phone", "password", "approved_asset_count", "coins", "premium", "upload_count", "about", "contributor", "contributions")
    contributions = ma.Nested('ContributionSchema', many=True)
    track_assets = ma.Nested('TrackAssetSchema', many=True)

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
        fields = ("id", "date_created", "amount", "project_id", "entry_id", "user_id", "status", "contributed_assets")
    contributed_assets = ma.Nested('ContributedAssetSchema', many=True)

class ContributedAssetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ContributedAsset
        fields = ("id", "uuid", "contribution_id", "name", "status")
        
class PackSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pack
        fields = ("id", "title", "description", "image_file", "video_file", "downloads", "coin_cost", "active", "asset_types")
    asset_types = ma.Nested('AssetTypeSchema', many=True)

class AssetTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AssetType
        fields = ("id", "description", "pack_id")

class TrackAssetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TrackAsset
        fields = ("id", "name", "uuid", "author_id", "downloads", "length", "waveform", "audio_metadata", "active")

