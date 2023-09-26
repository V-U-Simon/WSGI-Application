from typing import List, Optional, Union
from abc import ABC, abstractmethod


ID = Optional[int]


# все пользователи
class User:
    def __init__(self, name: str, id: ID = None):
        self.id = id
        self.name = name


class Teacher(User):
    def __init__(self, name: str, id: ID = None):
        super().__init__(name, id)


class Student(User):
    def __init__(self, name: str, id: ID = None):
        super().__init__(name, id)


# Категория курсов
class Category:
    def __init__(self, name: str, parent: ID = None, id: ID = None):
        self.id = id
        self.name = name
        self.parent = parent


# Абстрактный базовый класс для курсов
class Course(ABC):
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

    def add_student(self, student: Student):
        self.students.append(student)

    def remove_student(self, student: Student):
        self.students.remove(student)


# Веб-курс
class WebCourse(Course):
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
class LiveCourse(Course):
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
            return WebCourse(name, category_id, teacher_id, url, id)

        if location:
            return LiveCourse(name, category_id, teacher_id, location, id)

        raise ValueError("Either url or location must be provided")
