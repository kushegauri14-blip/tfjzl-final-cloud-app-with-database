from django.urls import path
from . import views

urlpatterns = [
    path(
        "course/<int:course_id>/",
        views.course_details,
        name="course_details"
    ),
    path(
        "course/<int:course_id>/submit/",
        views.submit,
        name="submit"
    ),
    path(
        "course/<int:course_id>/result/",
        views.show_exam_result,
        name="show_exam_result"
    ),
]
