from rest_framework import serializers
from .models import Problem, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class ProblemSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    related_problems = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Problem.objects.all()
    )

    class Meta:
        model = Problem
        fields = [
            'problem_id',
            'title',
            'difficulty',
            'personal_difficulty',
            'topics',
            'related_problems',
            'date_added',
            'last_solved',
            'solved_count',
            'url',
        ]
