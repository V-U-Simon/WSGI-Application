from framework_wsgi.urls import Url
import views_main


# Pattern: front_controllers
urlpatterns = [
    Url("/contact/", views_main.contacts_view),
    Url("^/about/$", views_main.about),
    Url("^/$", views_main.Index),
]
