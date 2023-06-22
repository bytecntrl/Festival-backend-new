from tortoise import fields
from tortoise.models import Model


class RoleMenu(Model):
    """
    The RoleMenu model
    """

    role = fields.ForeignKeyField("models.Roles")
    menu = fields.ForeignKeyField("models.Menu")

    class Meta:
        table = "role_menu"
