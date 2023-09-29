from framework_wsgi.urls import Url
import views_main
import views_courses


# Pattern: front_controllers
urlpatterns = [
    Url("/courses/create/", views_courses.CourseCreateView),
    Url("/courses/<id>/update/", views_courses.CourseUpdateView),
    Url("/courses/<id>/", views_courses.CourseDetailView),
    Url("/courses/", views_courses.CourseListView),
    Url("/contact/", views_main.contacts_view),
    Url("/about/", views_main.about),
    Url("/", views_main.Index),
]
