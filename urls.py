from framework_wsgi.urls import Url
import views


# Pattern: front_controllers
urlpatterns = [
    Url("/contact/", views.contacts_view),
    Url("^/about/$", views.about),
    Url("^/$", views.Index),
]
