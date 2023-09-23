from framework_wsgi.template_view import render_from_line, render


def index_view(request):
    return "200 OK", render("index.html", context={"path": request.path})


def contact_form_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        print(email, subject, message)

        return "200 OK", render("contact.html")

    return "200 OK", render("contact.html")
