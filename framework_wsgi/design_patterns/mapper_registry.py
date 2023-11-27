from typing import TypeVar

from framework_wsgi.design_patterns.domain_courses import (
    Courses,
    Categories,
    CoursesStudents,
)

from framework_wsgi.design_patterns.domain_users import (
    Students,
    Teachers,
    Users,
)

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
MapperRegistry.register(Courses)
MapperRegistry.register(Categories)
MapperRegistry.register(CoursesStudents)

if __name__ == "__main__":
    print(MapperRegistry._registry)
