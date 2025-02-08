from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from problem.models.problem import Problem
from problem.serializers.problem import ProblemSerializer


@api_view(['GET'])
def problem_detail(request: HttpRequest, slug: str) -> Response:
    try:
        problem = Problem.objects.get(titleSlug=slug)
    except Problem.DoesNotExist:
        raise NotFound(detail=f'Problem with slug: {slug} does not exist', code=404)

    serializer = ProblemSerializer(problem)
    return Response(serializer.data)


# TODO: change to POST
@api_view(['GET'])
def problem_create(request: HttpRequest) -> Response:
    serializer = ProblemSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer.save()
    return Response(serializer.data, status=201)


@api_view(['PUT', 'PATCH'])
def problem_update(request, slug: str):
    try:
        problem = Problem.objects.get(titleSlug=slug)
    except Problem.DoesNotExist:
        raise NotFound(detail=f'Problem with slug: {slug} does not exist', code=404)

    serializer = ProblemSerializer(problem)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer.save()
    return Response(serializer.data, status=201)


@api_view(['DELETE'])
def problem_delete(request, slug: str):
    try:
        problem = Problem.objects.get(titleSlug=slug)
    except Problem.DoesNotExist:
        raise NotFound(detail=f'Problem with slug: {slug} does not exist', code=404)

    problem.delete()
    return Response(status=204)
