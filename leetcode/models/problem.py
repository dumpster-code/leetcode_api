from django.db import models


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

    url = models.CharField(max_length=256)

    topics = models.ManyToManyField('leetcode.Topic', related_name='problems', blank=True)
    relatedProblems = models.ManyToManyField('self', symmetrical=True, blank=True)

    class Meta:
        ordering = ['questionId']

    def __str__(self):
        return self.titleSlug
