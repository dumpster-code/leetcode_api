from django.db import models


class Problem(models.Model):
    titleSlug = models.CharField(max_length=128)
