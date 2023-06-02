from tortoise import fields
from tortoise.models import Model


class MenuProduct(Model):
    """
    The MenuProduct model
    """

    menu = fields.ForeignKeyField("models.Menu")
    product = fields.ForeignKeyField("models.Products")
    optional = fields.BooleanField(default=False)

    class Meta:
        table = "menu_product"
