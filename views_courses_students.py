# Pattern: page_controllers

from framework_wsgi.design_patterns.connector import ConnectorDB
from framework_wsgi.design_patterns.domain_courses import (
    Categories,
    Courses,
    CoursesStudents,
)
from framework_wsgi.design_patterns.domain_users import Students, Teachers
from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork
from framework_wsgi.templator import render
from framework_wsgi import views
from framework_wsgi.http.response import Response


class AddStudentView(views.View):
    def get_course_id(self, request):
        course_id = request.kwargs.get("id", None)
        return int(course_id)

    def get_student_id(self, request):
        student_id = self.request.POST.get("student_id", None)
        return int(student_id)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        course_id = self.get_course_id(request)
        student_id = self.get_student_id(request)

        uow = SQLiteUnitOfWork(ConnectorDB)
        with uow as repo:
            registration_on_course = CoursesStudents(course_id, student_id)
            repo.save(registration_on_course)
        return Response(request=request).redirect(f"/courses/{course_id}/")


class RemoveStudentView(views.View):
    def get_course_id(self, request):
        course_id = request.kwargs.get("id", None)
        return int(course_id)

    def get_registration_on_course_id(self, request):
        registration_on_course_id = self.request.POST.get(
            "registration_on_course_id", None
        )
        return int(registration_on_course_id)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        course_id = self.get_course_id(request)
        registration_on_course_id = self.get_registration_on_course_id(request)

        uow = SQLiteUnitOfWork(ConnectorDB)
        with uow as repo:
            registration = repo(CoursesStudents).find_by_id(registration_on_course_id)
            repo.delete(registration)
        return Response(request=request).redirect(f"/courses/{course_id}/")
