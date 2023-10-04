# Pattern: page_controllers

from framework_wsgi.design_patterns.connector import ConnectorDB
from framework_wsgi.design_patterns.domain_courses import (
    Categories,
    Courses,
    CoursesStudents,
)
from framework_wsgi.design_patterns.domain_users import Students, Teachers
from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork
from framework_wsgi.templator import TemplateEngineJSON, render
from framework_wsgi import views
from framework_wsgi.http.response import Response


class CourseListView(views.ListView):
    model = Courses
    template_name = "courses/course_list.html"


class JsonCourseListView(views.ListView):
    model = Courses
    template_engine = TemplateEngineJSON


class CourseDetailView(views.DetailView):
    model = Courses
    template_name = "courses/course_detail.html"

    def get_context_data(self) -> dict:
        obj = self.get_object()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: obj}
        uow = SQLiteUnitOfWork(ConnectorDB)
        with uow as repo:
            categories = repo(Categories).all()
            teachers = repo(Teachers).all()
            course_students = repo(CoursesStudents).all() or []
            students = repo(Students).all()

            course_students = [
                c_s for c_s in course_students if c_s.course_id == obj.id
            ]
            id_students_on_course = [c.student_id for c in course_students]
            students_on_course = list(
                filter(lambda student: student.id in id_students_on_course, students)
            )
            students_not_on_course = list(
                filter(
                    lambda student: student.id not in id_students_on_course, students
                )
            )

        context.update(
            {
                "categories": categories,
                "teachers": teachers,
                "course_students": course_students,
                "students_on_course": students_on_course,
                "students_not_on_course": students_not_on_course,
            }
        )
        return context


class CourseCreateView(views.CreateView):
    model = Courses
    template_name = "courses/course_form.html"
    success_url = "/courses/"

    def prepare_form_data(self, request) -> dict:
        data = super().prepare_form_data(request)
        location_or_url = data.pop("location_or_url")
        if location_or_url.startswith("http://"):
            data["url"] = location_or_url
        else:
            data["location"] = location_or_url
        return data

    def get_context_data(self) -> dict:
        context = super().get_context_data()
        uow = SQLiteUnitOfWork(ConnectorDB)
        with uow as repo:
            categories = repo(Categories).all()
            teachers = repo(Teachers).all()
        context.update({"categories": categories, "teachers": teachers})
        return context


class CourseUpdateView(views.UpdateView):
    model = Courses
    template_name = "courses/course_form.html"
    success_url = "/courses/"

    def prepare_form_data(self, request) -> dict:
        data = super().prepare_form_data(request)
        location_or_url = data.pop("location_or_url")
        if location_or_url.startswith("http://"):
            data["url"] = location_or_url
        else:
            data["location"] = location_or_url
        return data

    def get_context_data(self) -> dict:
        context = super().get_context_data()
        uow = SQLiteUnitOfWork(ConnectorDB)
        with uow as repo:
            categories = repo(Categories).all()
            teachers = repo(Teachers).all()

        context.update(
            {
                "categories": categories,
                "teachers": teachers,
            }
        )
        return context


class CourseDeleteView(views.DeleteView):
    model = Courses
    template_name = "courses/course_delete.html"
    success_url = "/courses/"
