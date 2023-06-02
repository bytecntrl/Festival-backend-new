from tortoise import fields
from tortoise.models import Model

from backend.utils import Roles


class RoleMenu(Model):
    """
    The RoleMenu model
    """

    role = fields.CharEnumField(Roles)
    menu = fields.ForeignKeyField("models.Menu")

    class Meta:
        table = "role_menu"
