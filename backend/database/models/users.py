from tortoise import fields
from tortoise.models import Model


class Users(Model):
    """
    The User model
    """

    username = fields.CharField(30, unique=True)
    password = fields.TextField()
    role = fields.ForeignKeyField("models.Roles")

    class Meta:
        table = "users"

    async def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role_id": self.role_id,
        }
