from tortoise import fields
from tortoise.models import Model

from backend.utils import Roles


class RoleProduct(Model):
    """
    The RoleProduct model
    """

    role = fields.CharEnumField(Roles)
    product = fields.ForeignKeyField("models.Products")

    class Meta:
        table = "role_product"
