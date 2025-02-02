from http import HTTPStatus
from typing import Optional

from api.serializers import TopicSerializer, ProblemSerializer
from api.core.leetcode import LeetCode
from api.core.problem import LeetCodeProblem


def create_problem(slug: str) -> HTTPStatus:
    lc = LeetCode()
    problem: Optional[LeetCodeProblem] = lc.get(slug)

    if not problem:
        return HTTPStatus.BAD_REQUEST

    data = {
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

    serializer = ProblemSerializer(data=data)
    if not serializer.is_valid():
        return HTTPStatus.BAD_REQUEST

    serializer.save()
    return HTTPStatus.OK


def _create_problem(problem: LeetCodeProblem) -> HTTPStatus:
    data = {
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
    }

    serializer = ProblemSerializer(data=data)
    if not serializer.is_valid():
        return HTTPStatus.BAD_REQUEST

    serializer.save()
    return HTTPStatus.OK


def create_topic(name: str, slug: str) -> HTTPStatus:
    data = {
        'name': name,
        'slug': slug,
    }

    serializer = TopicSerializer(data=data)
    if not serializer.is_valid():
        return HTTPStatus.BAD_REQUEST

    serializer.save()
    return HTTPStatus.OK
