from tortoise import fields
from tortoise.models import Model


class Variant(Model):
    """
    The Variant model
    """

    name = fields.CharField(20)
    price = fields.FloatField()
    product = fields.ForeignKeyField("models.Products")

    class Meta:
        table = "variant"
