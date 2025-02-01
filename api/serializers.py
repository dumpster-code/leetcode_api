from rest_framework import serializers
from .models import Problem, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug']


class ProblemSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = [
            'data',
            'content',
            'difficulty',
            'dislikes',
            'test_cases',
            'hints',
            'paid_only',
            'likes',
            'question_id',
            'stats',
            'title',
            'title_slug',
            'url',
            'code_lang',
            'code_slug',
            'personal_difficulty',
            'topics',
            'date_added',
            'last_solved',
            'solved_count',
        ]
