from tortoise import fields
from tortoise.models import Model

from backend.utils import Permissions


class Roles(Model):
    """
    The Roles model
    """

    name = fields.CharField(20, unique=True)
    permissions = fields.CharEnumField(Permissions)

    class Meta:
        table = "roles"
