from tortoise import fields
from tortoise.models import Model

from backend.utils import Roles


class Users(Model):
    """
    The User model
    """

    username = fields.CharField(30, unique=True)
    password = fields.TextField()
    role = fields.CharEnumField(Roles)

    class Meta:
        table = "users"

    async def to_dict(self):
        return {"id": self.id, "username": self.username, "role": self.role}
