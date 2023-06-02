import enum


class Roles(enum.StrEnum):
    ADMIN = "admin"
    BAR = "bar"
    PUNTO_GIOVANI = "punto giovani"
    SAGRA = "sagra"

    @classmethod
    def is_in_roles(cls, data: str):
        return data in cls.roles()

    @classmethod
    def roles(cls):
        return [x for x in cls._value2member_map_ if x != "admin"]
