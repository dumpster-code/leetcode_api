from http import HTTPStatus
from typing import Any, Dict

from rest_framework.response import Response
from rest_framework import status

from api.core.leetcode import LeetCode
from api.models import Topic, Problem
from api.serializers import TopicSerializer, ProblemSerializer


def create_problem(slug: str) -> Response:
    query = Problem.objects.filter(titleSlug=slug)
    if query.exists():
        return Response(
            data={'error': f'Problem: "{slug}" already exists.'},
            status=status.HTTP_409_CONFLICT
        )

    lc = LeetCode()
    problem: Dict[str, Any] = lc.get(slug)
    problem['url'] = f'https://leetcode.com/problems/{slug}/description/'

    serializer = ProblemSerializer(data=problem)

    if not serializer.is_valid():
        return Response(
            data={'error': f'Invalid data for problem: {serializer.errors}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer.save()
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
        status=HTTPStatus.OK
    )


def create_topic(name: str, slug: str) -> HTTPStatus:
    if Topic.objects.filter(name=name, slug=slug).exists():
        return HTTPStatus.BAD_REQUEST

    data = {
        'name': name,
        'slug': slug,
    }

    serializer = TopicSerializer(data=data)
    if not serializer.is_valid():
        return HTTPStatus.BAD_REQUEST

    serializer.save()
    return HTTPStatus.OK
