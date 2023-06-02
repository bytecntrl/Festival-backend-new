from tortoise import fields
from tortoise.models import Model


class ProductOrder(Model):
    """
    The ProductOrder model
    """

    menu = fields.ForeignKeyField("models.MenuOrder", null=True)
    product = fields.ForeignKeyField("models.Products")
    variant = fields.ForeignKeyField("models.Variant", null=True)
    order = fields.ForeignKeyField("models.Orders")

    class Meta:
        table = "product_order"
