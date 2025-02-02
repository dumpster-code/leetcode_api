# from http import HTTPStatus

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Topic, Problem

from api.core import database


@api_view(['GET'])
def get_problem(request, title_slug: str) -> Response:
    return database.get_problem(title_slug)


@api_view(['GET'])
def create_problem(request, title_slug: str) -> Response:
    return database.create_problem(title_slug)

    # server_response: HTTPStatus = database.create_problem(title_slug)
    # if server_response != HTTPStatus.OK:
    #     return Response({'error': status.description}, status=server_response.value)

    # return Response({'error': ''}, status=status.HTTP_201_CREATED)


def _get_or_create_problem(title_slug: str) -> Problem:
    """Fetches an existing problem or creates it if it does not exist."""
    if not Problem.objects.filter(title_slug=title_slug).exists():
        if database.create_problem(title_slug) != HTTPStatus.OK:
            return None

    return Problem.objects.get(title_slug=title_slug)


def _associate_topics(problem: Problem):
    """Associates topics with the problem."""
    for name, slug in [t.values() for t in problem.topic_tags]:
        topic = _get_or_create_topic(name, slug)
        if topic:
            problem.topics.add(topic)
            topic.problems.add(problem)
            topic.save()


def _get_or_create_topic(name: str, slug: str) -> Topic:
    """Fetches an existing topic or creates it if it does not exist."""
    if not Topic.objects.filter(name=name, slug=slug).exists():
        if database.create_topic(name, slug) != HTTPStatus.OK:
            return None

    return Topic.objects.get(name=name, slug=slug)
