from salt.models import User
from salt import ma
import logging, json

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ("id", "username", "admin", "email", "password")