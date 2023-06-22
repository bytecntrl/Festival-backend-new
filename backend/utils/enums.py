import enum


class Category(enum.StrEnum):
    FOODS = "foods"
    DRINKS = "drinks"


class Permissions(enum.StrEnum):
    ALL = "all"
    ORDER = "order"
    STATISTICS_PRIORITY = "statistics_priority"
    STATISTICS_ALL = "statistics_all"
