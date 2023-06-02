from tortoise import fields
from tortoise.models import Model


class Menu(Model):
    """
    The Menu model
    """

    name = fields.CharField(30, unique=True)

    class Meta:
        table = "menu"
