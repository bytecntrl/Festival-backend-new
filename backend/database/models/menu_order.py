from tortoise import fields
from tortoise.models import Model


class MenuOrder(Model):
    """
    The MenuOrder model
    """

    menu = fields.ForeignKeyField("models.Menu")
    order = fields.ForeignKeyField("models.Orders")

    class Meta:
        table = "menu_order"
