# Pattern: page_controllers

from framework_wsgi.design_patterns.connector import ConnectorDB
from framework_wsgi.design_patterns.domain_courses import Categories, Courses
from framework_wsgi.design_patterns.domain_users import Teachers
from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork
from framework_wsgi.templator import render
from framework_wsgi import views
from framework_wsgi.http.response import Response


class CourseListView(views.ListView):
    model = Courses
    template_name = "course_list.html"


class CourseDetailView(views.DetailView):
    model = Courses
    template_name = "course_detail.html"


class CourseCreateView(views.CreateView):
    model = Courses
    template_name = "course_form.html"
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
    template_name = "course_form.html"
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
    template_name = "course_delete.html"
    success_url = "/courses/"
