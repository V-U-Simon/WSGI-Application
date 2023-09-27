# Pattern: page_controllers

from framework_wsgi.templator import render
from framework_wsgi.views import View
from framework_wsgi.http.response import Response


class Index(View):
    def get(self, request) -> Response:
        context = {"date": request.GET.get("date", None)}
        return render(request, "index.html", context=context)


def about(request) -> Response:
    return render(request, "about.html")





class CourseDetailView:
    # select one
    def get(request, course_id) -> Response:
        


class CourseListView:
    # select all
    def get(request):
        pass


class CourseCreateView:
    def get(request):
        pass


class CourseUpdateView:
    def get(request):
        pass


class CourseDeleteView:
    def get(request):
        pass


class UserCreateView:
    def get(request):
        pass


def contacts_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        print(email, subject, message)

        return "200 OK", render("contact.html")

    return render(request, "contact.html")


# {'method': 'GET', 'request_params': {'id': '1', 'category': '10'}}
