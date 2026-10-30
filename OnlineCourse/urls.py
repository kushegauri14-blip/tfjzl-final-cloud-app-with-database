from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Keep your existing course and other URL patterns here.

    path(
        'course/<int:course_id>/submit/',
        views.submit,
        name='submit'
    ),

    path(
        'course/<int:course_id>/exam_result/<int:submission_id>/',
        views.show_exam_result,
        name='show_exam_result'
    ),
]
