from rest_framework import serializers
from leetcode.models.problem import Problem


class ProblemSerializer(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'
