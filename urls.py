from framework_wsgi.urls import Url
import views_main
import views_courses
import views_students


# Pattern: front_controllers
urlpatterns = [
    # Courses
    Url("/courses/create/", views_courses.CourseCreateView),
    Url("/courses/<id>/update/", views_courses.CourseUpdateView),
    Url("/courses/<id>/delete/", views_courses.CourseDeleteView),
    Url("/courses/<id>/", views_courses.CourseDetailView),
    Url("/courses/", views_courses.CourseListView),
    # Students
    Url("/students/create/", views_students.StudentCreateView),
    Url("/students/<id>/update/", views_students.StudentUpdateView),
    Url("/students/<id>/delete/", views_students.StudentDeleteView),
    Url("/students/<id>/", views_students.StudentDetailView),
    Url("/students/", views_students.StudentListView),
    # Other
    Url("/contact/", views_main.contacts_view),
    Url("/about/", views_main.about),
    Url("/", views_main.Index),
]
