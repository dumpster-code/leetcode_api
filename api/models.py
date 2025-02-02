from django.db import models
from django.utils.timezone import now


class Topic(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Problem(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

    DIFFICULTY = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard')
    ]

    data = models.JSONField()

    content = models.TextField()
    difficulty = models.CharField(
        max_length=6,
        choices=DIFFICULTY,
    )
    dislikes = models.IntegerField()
    test_cases = models.JSONField()
    hints = models.JSONField()
    paid_only = models.BooleanField()
    likes = models.IntegerField()
    question_id = models.IntegerField(unique=True)
    stats = models.JSONField()
    title = models.CharField(max_length=128)
    title_slug = models.CharField(max_length=128)
    url = models.CharField(max_length=256)

    code_lang = models.JSONField()
    code_slug = models.JSONField()

    # similar_questions: str = json.get('similarQuestionList', '')

    personal_difficulty = models.FloatField(default=5.0)

    topics = models.ManyToManyField(Topic, related_name='problems', blank=True)
    topic_tags = models.JSONField()

    similar_questions = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True
    )

    date_added = models.DateTimeField(default=now)
    last_solved = models.DateTimeField(null=True, blank=True)
    solved_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['question_id']
