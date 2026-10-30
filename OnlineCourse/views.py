from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import Course, Enrollment, Question, Choice, Submission


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method != 'POST':
        return redirect('onlinecourse:course_details', course_id=course.id)

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    selected_ids = request.POST.getlist('choices')

    questions = Question.objects.filter(course=course)
    valid_choice_ids = Choice.objects.filter(
        question__in=questions,
        id__in=selected_ids
    ).values_list('id', flat=True)

    submission.choices.set(valid_choice_ids)

    return redirect(
        'onlinecourse:show_exam_result',
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        enrollment__course=course,
        enrollment__user=request.user
    )

    selected_ids = set(
        submission.choices.values_list('id', flat=True)
    )

    questions = Question.objects.filter(course=course)

    score = 0
    total = 0
    exam_results = []

    for question in questions:
        correct_ids = set(
            question.choice_set.filter(
                is_correct=True
            ).values_list('id', flat=True)
        )

        question_choice_ids = set(
            question.choice_set.values_list('id', flat=True)
        )

        selected_for_question = selected_ids.intersection(
            question_choice_ids
        )

        question_score = (
            question.grade
            if correct_ids and selected_for_question == correct_ids
            else 0
        )

        score += question_score
        total += question.grade

        exam_results.append({
            'question': question,
            'selected_choices': question.choice_set.filter(
                id__in=selected_for_question
            ),
            'correct_choices': question.choice_set.filter(
                is_correct=True
            ),
            'score': question_score,
            'grade': question.grade,
        })

    context = {
        'course': course,
        'submission': submission,
        'score': score,
        'total': total,
        'choices': submission.choices.all(),
        'exam_results': exam_results,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
