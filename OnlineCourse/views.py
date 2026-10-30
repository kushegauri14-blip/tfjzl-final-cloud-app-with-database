from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Course, Question, Choice, Submission, Enrollment


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

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    if request.method != "POST":
        return redirect("course_details", course_id=course.id)

    questions = Question.objects.filter(
        lesson__course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
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

            submission.choices.add(choice)

            if choice.is_correct:
                score += question.grade if question.grade > 0 else 1

    request.session["exam_score"] = score
    request.session["exam_total"] = questions.count()

    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        enrollment=enrollment
    )

    questions = Question.objects.filter(
        lesson__course=course
    )

    selected_choices = submission.choices.all()

    score = 0

    for question in questions:
        correct_choices = Choice.objects.filter(
            question=question,
            is_correct=True
        )

        if selected_choices.filter(
            id__in=correct_choices.values_list("id", flat=True)
        ).exists():
            score += question.grade if question.grade > 0 else 1

    total = sum(
        question.grade if question.grade > 0 else 1
        for question in questions
    )

    return render(
        request,
        "OnlineCourse/exam_result_bootstrap.html",
        {
            "course": course,
            "submission": submission,
            "score": score,
            "total": total,
            "choices": selected_choices,
        }
    )
