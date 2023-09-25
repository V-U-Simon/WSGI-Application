from framework_wsgi.urls import Url
import views


# Pattern: front_controllers
urlpatterns = [
    Url("^/about/$", views.about),
    Url("^/$", views.Index),
    # Url("/index/", views.Index),
    # Url("/contact/", views.Index),
]
