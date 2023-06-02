from tortoise import fields
from tortoise.models import Model


class Subcategories(Model):
    """
    The Subcategories model
    """

    name = fields.CharField(20, unique=True)
    order = fields.IntField(unique=True)

    class Meta:
        table = "subcategories"
