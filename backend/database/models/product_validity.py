from tortoise import fields
from tortoise.models import Model


class ProductValidity(Model):
    """
    The ProductValidity model
    """

    product = fields.ForeignKeyField("models.Products")
    start_date = fields.DateField()
    end_date = fields.DateField()

    class Meta:
        table = "product_validity"
