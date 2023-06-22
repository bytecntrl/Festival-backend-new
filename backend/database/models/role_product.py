from tortoise import fields
from tortoise.models import Model


class RoleProduct(Model):
    """
    The RoleProduct model
    """

    role = fields.ForeignKeyField("models.Roles")
    product = fields.ForeignKeyField("models.Products")

    class Meta:
        table = "role_product"
