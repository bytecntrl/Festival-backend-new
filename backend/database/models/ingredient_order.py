from tortoise import fields
from tortoise.models import Model


class IngredientOrder(Model):
    """
    The IngredientOrder model
    """

    ingredient = fields.ForeignKeyField("models.Ingredients")
    product = fields.ForeignKeyField("models.ProductOrder")
    order = fields.ForeignKeyField("models.Orders")
    price = fields.FloatField()

    class Meta:
        table = "ingredient_order"
