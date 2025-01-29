from django.db import models
from django.utils.timezone import now


class Topic(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Problem(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

    DIFFICULTY = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard')
    ]

    problem_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=256)
    difficulty = models.CharField(
        max_length=6,
        choices=DIFFICULTY,
    )
    personal_difficulty = models.IntegerField(default=0)

    topics = models.ManyToManyField(Topic, related_name='problems')
    related_problems = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True
    )

    date_added = models.DateTimeField(default=now)
    last_solved = models.DateTimeField(null=True, blank=True)
    solved_count = models.IntegerField(default=0)

    url = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'{self.problem_id} {self.title}'

    class Meta:
        ordering = ['problem_id']
