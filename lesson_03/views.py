# Pattern: page_controllers

from framework_wsgi.templator import render


class Index:
    def __call__(self, request):
        context = {"date": request.GET.get("date", None)}
        return "200 OK", render("index.html", context=context)


class About:
    # {'method': 'GET', 'request_params': {'id': '1', 'category': '10'}}
    def __call__(self, request):
        return "200 OK", "about"


def contacts_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        print(email, subject, message)

        return "200 OK", render("contact.html")

    return "200 OK", render("contact.html")
