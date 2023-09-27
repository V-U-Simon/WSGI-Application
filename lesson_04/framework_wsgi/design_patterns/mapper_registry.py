from typing import TypeVar

from lesson_04.framework_wsgi.db.domain_users import Students, Teachers, Users

T = TypeVar("T")


class MapperRegistry:
    registry: list[T] = []

    @classmethod
    def register(cls, entity_type):
        """Регистрация нового маппера."""
        cls.registry.append(entity_type)


# Регистрация мапперов
MapperRegistry.register(Users)
MapperRegistry.register(Students)
MapperRegistry.register(Teachers)

if __name__ == "__main__":
    print(MapperRegistry._registry)
