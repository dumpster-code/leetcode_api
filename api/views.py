from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Topic, Problem
from .serializers import TopicSerializer, ProblemSerializer

from api.core.leetcode import LeetCode
import api.core.database as database


@api_view(['GET'])
def problem(request, title_slug: str) -> Response:
    if not Problem.objects.filter(title_slug=title_slug).exists():
        lc = LeetCode()
        lc_problem = lc.get(title_slug)

        if not lc_problem:
            return Response({'error': 'Could not find problem'}, status=status.HTTP_404_NOT_FOUND)

        if not database.store(lc_problem):
            return Response({'error': 'Could not store problem'}, status=status.HTTP_400_BAD_REQUEST)

    problem = Problem.objects.get(title_slug=title_slug)
    serializer = ProblemSerializer(problem)
    return Response(serializer.data, status=status.HTTP_200_OK)
