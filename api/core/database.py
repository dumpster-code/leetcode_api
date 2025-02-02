from typing import Any, Dict

from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from api.core.leetcode import LeetCode
from api.models import Topic, Problem
from api.serializers import TopicSerializer, ProblemSerializer


def create_problem(slug: str) -> Response:
    if Problem.objects.filter(titleSlug=slug).exists():
        return Response(
            data={'error': f'Problem: "{slug}" already exists.'},
            status=status.HTTP_409_CONFLICT
        )

    lc = LeetCode()
    problem_data: Dict[str, Any] = lc.get(slug)
    problem_data['url'] = f'https://leetcode.com/problems/{slug}/description/'

    serializer = ProblemSerializer(data=problem_data)
    if not serializer.is_valid():
        return Response(
            data={'error': f'Invalid data for problem: {serializer.errors}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        problem_instance = serializer.save()

        try:
            for topic_name, topic_slug in [t.values() for t in problem_data['topicTags']]:
                if not Topic.objects.filter(name=topic_name, slug=topic_slug).exists():
                    topic_create_response = create_topic(topic_name, topic_slug)
                    if topic_create_response.status_code != status.HTTP_201_CREATED:
                        raise ValueError(f'Invalid topic fields: {topic_name}, {topic_slug}')

                topic_instance = Topic.objects.get(name=topic_name, slug=topic_slug)
                topic_instance.problems.add(problem_instance)
                problem_instance.topics.add(topic_instance)

                topic_instance.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            transaction.set_rollback(True)
            return Response(
                data={'error': f'Failed to associate topics with the problem: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    return Response(
        data=serializer.data,
        status=status.HTTP_201_CREATED
    )


def get_problem(slug: str) -> Response:
    try:
        problem = Problem.objects.get(titleSlug=slug)
    except Problem.DoesNotExist:
        return Response(
            data={'error': f'Problem with slug {slug} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProblemSerializer(problem)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


def create_topic(name: str, slug: str) -> Response:
    if Topic.objects.filter(name=name, slug=slug).exists():
        return Response(
            data={'error': f'Topic: "{name}" already exists.'},
            status=status.HTTP_409_CONFLICT
        )

    data = {
        'name': name,
        'slug': slug,
    }

    serializer = TopicSerializer(data=data)
    if not serializer.is_valid():
        return Response(
            data={'error': f'Invalid data for topic: {serializer.errors}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer.save()
    return Response(
        data=serializer.data,
        status=status.HTTP_201_CREATED
    )


def get_topic(name: str, slug: str) -> Response:
    try:
        topic = Topic.objects.get(name=name, slug=slug)
    except Topic.DoesNotExist:
        return Response(
            data={'error': f'Topic with name: {name}, slug: {slug} not found'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = TopicSerializer(topic)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )
