from http import HTTPStatus

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Topic, Problem
from .serializers import TopicSerializer, ProblemSerializer

from api.core.leetcode import LeetCode
import api.core.database as database


# TODO: temporarily combine GET and POST while I scrape problems
@api_view(['GET'])
def problem(request, title_slug: str) -> Response:
    if not Problem.objects.filter(title_slug=title_slug).exists():
        if database.create_problem(title_slug) != HTTPStatus.OK:
            return Response({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

        problem = Problem.objects.get(title_slug=title_slug)

        for name, slug in [t.values() for t in problem.topic_tags]:
            if not Topic.objects.filter(name=name, slug=slug).exists():
                if database.create_topic(name, slug) == HTTPStatus.BAD_REQUEST:
                    return Response({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

            topic = Topic.objects.get(name=name, slug=slug)

            topic.save()

            problem.topics.add(topic)
            topic.problems.add(problem)

    problem = Problem.objects.get(title_slug=title_slug)
    serializer = ProblemSerializer(problem)
    return Response(serializer.data, status=status.HTTP_200_OK)
