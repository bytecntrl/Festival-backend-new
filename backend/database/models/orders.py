from tortoise import fields
from tortoise.models import Model


class Orders(Model):
    """
    The Orders model
    """

    customer = fields.CharField(20)
    guests = fields.IntField(null=True)
    take_away = fields.BooleanField()
    table = fields.IntField(null=True)
    user = fields.ForeignKeyField("models.Users")
    created_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "orders"
