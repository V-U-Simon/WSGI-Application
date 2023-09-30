# Pattern: page_controllers

from framework_wsgi import views
from framework_wsgi.http.response import Response

from framework_wsgi.design_patterns.connector import ConnectorDB
from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork
from framework_wsgi.design_patterns.domain_users import Teachers


class TeacherListView(views.ListView):
    model = Teachers
    template_name = "teachers/teacher_list.html"


class TeacherDetailView(views.DetailView):
    model = Teachers
    template_name = "teachers/teacher_detail.html"


class TeacherCreateView(views.CreateView):
    model = Teachers
    template_name = "teachers/teacher_form.html"
    success_url = "/teachers/"


class TeacherUpdateView(views.UpdateView):
    model = Teachers
    template_name = "teachers/teacher_form.html"
    success_url = "/teachers/"


class TeacherDeleteView(views.DeleteView):
    model = Teachers
    template_name = "teachers/teacher_delete.html"
    success_url = "/teachers/"
