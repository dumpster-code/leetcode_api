from rest_framework import serializers
from .models import Problem, Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name', 'slug']


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
            'topic_tags',
            'date_added',
            'last_solved',
            'solved_count',
        ]
