from http import HTTPStatus
from typing import Any, Optional, Dict

from rest_framework.response import Response
from rest_framework import status

from api.core.leetcode import LeetCode
from api.core.problem import LeetCodeProblem
from api.models import Topic, Problem
from api.serializers import TopicSerializer, ProblemSerializer


def create_problem(slug: str) -> Response:
    query = Problem.objects.filter(title_slug=slug)
    if query.exists():
        return Response(
            data={'error': f'Problem: "{slug}" already exists.'},
            status=status.HTTP_409_CONFLICT
        )

    lc = LeetCode()
    problem: Optional[LeetCodeProblem] = lc.get(slug)
    # import json
    # print(json.dumps(problem, indent=4))

    # if not problem:
    #     return Response(
    #         data={'error': f'Error finding problem: "{slug}". The problem does not exist.'},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    data: Dict[str, Any] = _serialize_problem(problem)
    serializer = ProblemSerializer(data=data)

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
        problem = Problem.objects.get(title_slug=slug)
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


def _serialize_problem(problem) -> Dict[str, Any]:
    """Serializes a LeetCodeProblem instance into a dictionary."""
    return {
        'data': problem.json,
        'content': problem.content,
        'difficulty': problem.difficulty,
        'dislikes': problem.dislikes,
        'test_cases': problem.test_cases,
        'hints': problem.hints,
        'paid_only': problem.paid_only,
        'likes': problem.likes,
        'question_id': problem.question_id,
        'stats': problem.stats,
        'title': problem.title,
        'title_slug': problem.title_slug,
        'url': problem.url,
        'code_lang': problem.code_lang,
        'code_slug': problem.code_slug,
        'topic_tags': problem.topics,
    }
