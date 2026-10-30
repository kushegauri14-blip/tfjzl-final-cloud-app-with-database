from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Question,
    Choice,
    Enrollment,
    Submission,
    Instructor,
    Learner,
)

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Enrollment)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)
