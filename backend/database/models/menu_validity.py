from tortoise import fields
from tortoise.models import Model


class MenuValidity(Model):
    """
    The MenuValidity model
    """

    menu = fields.ForeignKeyField("models.Menu")
    start_date = fields.DateField()
    end_date = fields.DateField()

    class Meta:
        table = "menu_validity"
