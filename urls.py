from framework_wsgi.urls import Url
import views_main
import views_categories
import views_courses
import views_students
import views_teachers
import views_courses_students


# <p>category: {{ next([c.name for c in categories if object.category_id == c.id]) }}</p>
# <p>teacher: {{ teachers[object.teacher_id].name }}-{{ object.teacher_id }}</p>


# {% for s in students %}{{ s.name }}{% endfor %}

# Pattern: front_controllers
urlpatterns = [
    # CoursesStudents
    Url("/courses/<id>/add_student/", views_courses_students.AddStudentView),
    Url("/courses/<id>/remove_student/", views_courses_students.RemoveStudentView),
    # Categories
    Url("/categories/create/", views_categories.CategoryCreateView),
    Url("/categories/<id>/update/", views_categories.CategoryUpdateView),
    Url("/categories/<id>/delete/", views_categories.CategoryDeleteView),
    Url("/categories/<id>/", views_categories.CategoryDetailView),
    Url("/categories/", views_categories.CategoryListView),
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
    # Teachers
    Url("/teachers/create/", views_teachers.TeacherCreateView),
    Url("/teachers/<id>/update/", views_teachers.TeacherUpdateView),
    Url("/teachers/<id>/delete/", views_teachers.TeacherDeleteView),
    Url("/teachers/<id>/", views_teachers.TeacherDetailView),
    Url("/teachers/", views_teachers.TeacherListView),
    # Other
    Url("/contact/", views_main.contacts_view),
    Url("/about/", views_main.about),
    Url("/", views_main.Index),
]
