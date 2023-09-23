from framework_wsgi.templator import render_from_line, render


# Pattern: page_controllers
def index_view(request):
    return "200 OK", render("index.html", context={"path": request.path})


def contacts_view(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        print(email, subject, message)

        return "200 OK", render("contact.html")

    return "200 OK", render("contact.html")
