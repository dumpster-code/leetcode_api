from http import HTTPStatus
from typing import Any, Dict

from api.core.leetcode import LeetCode
from api.core.problem import LeetCodeProblem
from api.models import Topic, Problem
from api.serializers import TopicSerializer, ProblemSerializer


def create_problem(slug: str) -> HTTPStatus:
    if Problem.objects.filter(title_slug=slug).exists():
        return HTTPStatus.BAD_REQUEST

    lc = LeetCode()
    problem: LeetCodeProblem = lc.get(slug)

    if not problem:
        return HTTPStatus.BAD_REQUEST

    data: Dict[str, Any] = _serialize_problem(problem)
    serializer = ProblemSerializer(data=data)

    if not serializer.is_valid():
        return HTTPStatus.BAD_REQUEST

    serializer.save()
    return HTTPStatus.OK


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
