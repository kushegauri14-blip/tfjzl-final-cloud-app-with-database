from django.db import models


class Question(models.Model):
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_choices):
        correct_choices = set(
            self.choice_set.filter(is_correct=True).values_list(
                'id', flat=True
            )
        )
        selected_choices = set(selected_choices)

        return (
            self.grade
            if correct_choices and correct_choices == selected_choices
            else 0
        )


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        'Enrollment',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    choices = models.ManyToManyField(Choice, blank=True)

    def __str__(self):
        return (
            f"Submission {self.pk} - "
            f"{self.enrollment}"
        )
