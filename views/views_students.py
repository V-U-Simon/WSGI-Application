# Pattern: page_controllers

from framework_wsgi import views
from framework_wsgi.http.response import Response

from framework_wsgi.design_patterns.connector import ConnectorDB
from framework_wsgi.design_patterns.unit_of_work import SQLiteUnitOfWork
from framework_wsgi.design_patterns.domain_users import Students


class StudentListView(views.ListView):
    model = Students
    template_name = "students/student_list.html"


class StudentDetailView(views.DetailView):
    model = Students
    template_name = "students/student_detail.html"


class StudentCreateView(views.CreateView):
    model = Students
    template_name = "students/student_form.html"
    success_url = "/students/"


class StudentUpdateView(views.UpdateView):
    model = Students
    template_name = "students/student_form.html"
    success_url = "/students/"


class StudentDeleteView(views.DeleteView):
    model = Students
    template_name = "students/student_delete.html"
    success_url = "/students/"
