from django.db import models


class Attempt(models.Model):
    #problem = models.ForeignKey('problem.Problem', on_delete=models.CASCADE, related_name='attempts')

    date = models.DateField(auto_now_add=True)
    time_taken = models.IntegerField()
    failed_attempts = models.IntegerField()
    failed_test_cases = models.JSONField()
    failed_submissions = models.JSONField()
    solution = models.JSONField()
    personal_difficulty = models.FloatField()
    notes = models.TextField()
