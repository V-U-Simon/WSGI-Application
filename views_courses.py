# Pattern: page_controllers

from framework_wsgi.design_patterns.domain_courses import Courses
from framework_wsgi.templator import render
from framework_wsgi import views
from framework_wsgi.http.response import Response


class CourseListView(views.ListView):
    model = Courses
    template_name = "course_list.html"


# class CourseDetailView:
#     # select one
#     def get(request, course_id) -> Response:
#         pass


# class CourseCreateView:
#     def get(request):
#         pass


# class CourseUpdateView:
#     def get(request):
#         pass


# class CourseDeleteView:
#     def get(request):
#         pass
