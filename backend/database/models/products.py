from tortoise import fields
from tortoise.models import Model

from backend.utils import Category


class Products(Model):
    """
    The Products model
    """

    name = fields.CharField(30, unique=True)
    price = fields.FloatField()
    category = fields.CharEnumField(Category)
    subcategory = fields.ForeignKeyField("models.Subcategories")

    class Meta:
        table = "products"
