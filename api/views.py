import random

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Topic, Problem
from .serializers import TopicSerializer, ProblemSerializer


@api_view(['GET'])
def get_problem(request) -> Response:
    fake_problem = {
        'problem_id': 1,
        'title': 'Two Sum',
        'difficulty': 'easy',
        'personal_difficulty': 5,
        'topics': [
            {'id': 1, 'name': 'Array'},
            {'id': 2, 'name': 'Hash Table'}
        ],
        'related_problems': [],
        'date_added': '2025-01-01T00:00:00Z',
        'last_solved': None,
        'solved_count': 1000,
        'url': 'https://leetcode.com/problems/two-sum',
    }

    serializer = ProblemSerializer(data=fake_problem)
    serializer.is_valid()
    return Response(serializer.data, status=status.HTTP_200_OK)


# TODO: returning a random problem for now
@api_view(['GET'])
def solve_problem(request) -> Response:
    count = Problem.objects.count()
    if count == 0:
        return Response({"error": "No problems stored in database"}, status=status.HTTP_404_NOT_FOUND)

    random_index = random.randint(0, count - 1)
    problem = Problem.objects.all()[random_index]

    serializer = ProblemSerializer(problem)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_problem(request) -> Response:
    serializer = ProblemSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
