import re

from django.db import models
from django.contrib.auth.models import User


class Exercise(models.Model):
    exercise_text = models.TextField()
    original_code = models.TextField()
    solved_by = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return "Exercise {}".format(self.id)


class TestCase(models.Model):
    code = models.TextField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    matcher = re.compile(r'^TEST\([^\,\)]*\,[^\)]*\)')

    def __str__(self):
        case_name = TestCase.matcher.match(self.code).group(0)
        return "TestCase {} of exercise {}".format(case_name, self.exercise.id)
