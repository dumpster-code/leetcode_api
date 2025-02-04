from django.db import models
from django.utils.timezone import now


class Topic(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Problem(models.Model):
    content = models.TextField()
    difficulty = models.CharField(max_length=6)
    dislikes = models.IntegerField()
    exampleTestcaseList = models.JSONField()
    hints = models.JSONField()
    isPaidOnly = models.BooleanField()
    likes = models.IntegerField()
    questionId = models.IntegerField(unique=True)
    stats = models.JSONField()
    title = models.CharField(max_length=128)
    titleSlug = models.CharField(max_length=128)
    topicTags = models.JSONField()

    codeSnippets = models.JSONField()
    similarQuestionList = models.JSONField()
    topicTags = models.JSONField()

    url = models.CharField(max_length=256)

    personal_difficulty = models.FloatField(default=5.0)
    topics = models.ManyToManyField(Topic, related_name='problems', blank=True)
    related_problems = models.ManyToManyField('self', symmetrical=True, blank=True)

    date_added = models.DateTimeField(default=now)
    last_solved = models.DateTimeField(null=True, blank=True)
    solved_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['questionId']

    def __str__(self):
        return self.titleSlug
