from typing import Optional, List

from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork
from framework_wsgi.design_patterns.domain_courses import (
    Categories,
    CourseFactory,
    Courses,
)
from framework_wsgi.design_patterns.domain_users import (
    Students,
    Teachers,
    Users,
)


class ServiceLayer:
    def __init__(self, unit_of_work: SQLiteUnitOfWork):
        self.uow = unit_of_work

    def add_user(self, name: str, user_type: str = "Users") -> None:
        with self.uow as repo:
            if user_type == "Teachers":
                user = Teachers(name)
            elif user_type == "Students":
                user = Students(name)
            else:
                user = Users(name)
            repo(user.__class__).save(user)

    def add_category(self, name: str, parent_id: Optional[int] = None) -> None:
        with self.uow as repo:
            category = Categories(name, parent_id)
            repo(Categories).save(category)

    def update_category(self, id: int, name: str, parent_id: Optional[int]) -> None:
        with self.uow as repo:
            category = repo(Categories).find_by_id(id)
            if category:
                category.name = name
                category.parent = parent_id
                repo(Categories).save(category)

    def delete_category(self, id: int) -> None:
        with self.uow as repo:
            category = repo(Categories).find_by_id(id)
            if category:
                repo(Categories).delete(category)

    def add_course(
        self,
        name: str,
        category_id: int,
        teacher_id: int,
        course_type: str,
        url: Optional[str] = None,
        location: Optional[str] = None,
    ) -> None:
        with self.uow as repo:
            course = CourseFactory.create_course(
                name, category_id, teacher_id, url, location
            )
            repo(course.__class__).save(course)

    def update_course(
        self, id: int, name: str, category_id: int, teacher_id: int
    ) -> None:
        with self.uow as repo:
            course = repo(Courses).find_by_id(id)
            if course:
                course.name = name
                course.category_id = category_id
                course.teacher_id = teacher_id
                repo(Courses).save(course)

    def delete_course(self, id: int) -> None:
        with self.uow as repo:
            course = repo(Courses).find_by_id(id)
            if course:
                repo(Courses).delete(course)

    def add_teacher_to_course(self, course_id: int, teacher_id: int) -> None:
        with self.uow as repo:
            course = repo(Courses).find_by_id(course_id)
            if course:
                course.teacher_id = teacher_id
                repo(Courses).save(course)

    def add_student_to_course(self, course_id: int, student_id: int) -> None:
        with self.uow as repo:
            course = repo(Courses).find_by_id(course_id)
            student = repo(Students).find_by_id(student_id)
            if course and student:
                course.add_student(student)
                repo(Courses).save(course)
