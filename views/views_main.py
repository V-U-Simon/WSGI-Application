# Pattern: page_controllers

from framework_wsgi.templator import render
from framework_wsgi import views
from framework_wsgi.http.response import Response


class Index(views.TemplateView):
    template_name = "index.html"

    # def get(self, request) -> Response:
    #     context = {"date": request.GET.get("date", None)}
    #     return render(request, "index.html", context=context)


def contacts_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        print(email, subject, message)

        return "200 OK", render("contact.html")

    return render(request, "contact.html")
