from rest_framework import serializers
from leetcode.models.topic import Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
