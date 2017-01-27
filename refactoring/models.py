from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings
from django.utils.timezone import localtime


class User(auth_models.AbstractUser):
    class Meta(auth_models.AbstractUser.Meta):
        pass


class Exercise(models.Model):
    exercise_text = models.TextField()
    original_code = models.TextField()
    original_tests = models.TextField()

    def __str__(self):
        return "Exercise {}".format(self.id)


class Session(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return "Session {}".format(self.id)

    def __eq__(self, other):
        return isinstance(other, Session) and self.id == other.id


class Solution(models.Model):
    code = models.TextField()
    tests = models.TextField()
    sub_date = models.DateTimeField('date submitted')
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Solution from {0:%Y-%m-%d}, {0:%-H:%M:%S}".format(localtime(self.sub_date))

    def __eq__(self, other):
        return isinstance(other, Solution) and self.id == other.id

    class Meta:
        unique_together = ('code', 'session')
