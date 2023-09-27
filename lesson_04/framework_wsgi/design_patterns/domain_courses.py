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
class Courses(ABC):
    def __init__(
        self,
        name: str,
        category_id: ID,
        teacher_id: ID,
        id: ID = None,
    ):
        self.id = id
        self.name = name
        self.teacher_id = teacher_id
        self.category_id = category_id
        self.students: List[int] = []

    def add_student(self, student: Students):
        self.students.append(student)

    def remove_student(self, student: Students):
        self.students.remove(student)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


# Веб-курс
class WebCourses(Courses):
    def __init__(
        self,
        name: str,
        category_id: ID,
        teacher_id: ID,
        url: str,
        id: ID = None,
    ):
        super().__init__(name, category_id, teacher_id, id)
        self.url = url


# Очный курс
class LiveCourses(Courses):
    def __init__(
        self,
        name: str,
        category_id: ID,
        teacher_id: ID,
        location: str,
        id: ID = None,
    ):
        super().__init__(name, category_id, teacher_id, id)
        self.location = location


# Фабрика курсов
class CourseFactory:
    @staticmethod
    def create_course(
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
            return WebCourses(name, category_id, teacher_id, url, id)

        if location:
            return LiveCourses(name, category_id, teacher_id, location, id)

        raise ValueError("Either url or location must be provided")
