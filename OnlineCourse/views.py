from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Course, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        "OnlineCourse/course_details_bootstrap.html",
        {"course": course}
    )


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    questions = Question.objects.filter(
        lesson__course=course
    )

    score = 0

    for question in questions:
        answer = request.POST.get(f"question_{question.id}")

        if answer:
            choice = get_object_or_404(
                Choice,
                id=answer,
                question=question
            )

            Submission.objects.create(
                user=request.user,
                question=question,
                selected_choice=choice
            )

            if choice.is_correct:
                score += 1

    request.session["exam_score"] = score
    request.session["exam_total"] = questions.count()

    return render(
        request,
        "OnlineCourse/course_details_bootstrap.html",
        {
            "course": course,
            "score": score,
            "total": questions.count(),
            "submitted": True
        }
    )


@login_required
def show_exam_result(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    score = request.session.get("exam_score", 0)
    total = request.session.get("exam_total", 0)

    return render(
        request,
        "OnlineCourse/course_details_bootstrap.html",
        {
            "course": course,
            "score": score,
            "total": total,
            "show_result": True
        }
    )
