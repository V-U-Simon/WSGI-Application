from typing import List, Optional, Union
from abc import ABC, abstractmethod


ID = Optional[int]


# Категория курсов
class Categories:
    def __init__(self, name: str, parent: ID = None, id: ID = None):
        self.id = id
        self.name = name
        self.parent = parent

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


# Абстрактный базовый класс для курсов
class Courses:
    def __init__(
        self,
        name: str,
        category_id: ID,
        teacher_id: ID,
        location: str = None,
        url: str = None,
        id: ID = None,
    ):
        self.id = id
        self.name = name
        self.teacher_id = teacher_id
        self.category_id = category_id
        self.location = location
        self.url = url

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


class CoursesStudents:
    def __init__(self, course_id: ID, student_id: ID):
        self.course_id = course_id
        self.student_id = student_id


# Фабирчный метод
def course_factory(
    name: str,
    category_id: ID,
    teacher_id: ID,
    url: Optional[str] = None,
    location: Optional[str] = None,
    id: ID = None,
):
    if url and location:
        raise ValueError("A course cannot be both a WebCourse and a LiveCourse")

    if url:
        return Courses(name, category_id, teacher_id, url, id)

    if location:
        return Courses(name, category_id, teacher_id, location, id)

    raise ValueError("Either url or location must be provided")
