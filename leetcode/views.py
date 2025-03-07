from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models.problem import Problem
from .serializers.problem import ProblemSerializer

from .api.leetcode import LeetCode

lc = LeetCode()


@api_view(['GET'])
def problem_daily(request: HttpRequest) -> Response:
    # TODO: handle errors
    slug = lc.daily_question()

    return problem_detail(request._request, slug)


@api_view(['GET'])
def problem_random(request) -> Response:
    problem = Problem.objects.order_by('?').first()
    if not problem:
        return Response({"error": "No problems found"}, status=404)

    serializer = ProblemSerializer(problem)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def problem_create(request: HttpRequest) -> Response:
    serializer = ProblemSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer.save()
    return Response(serializer.data, status=201)


@api_view(['POST'])
def problem_run(request) -> Response:
    # TODO: handle errors
    response = lc.run(request.data)
    return Response(response.data, status=200)


@api_view(['GET'])
def problem_detail(request: HttpRequest, slug: str) -> Response:
    try:
        problem = Problem.objects.get(titleSlug=slug)
    except Problem.DoesNotExist:
        raise NotFound(detail=f'Problem with slug: {slug} does not exist', code=404)

    serializer = ProblemSerializer(problem)
    return Response(serializer.data)


@api_view(['GET'])
def problem_query(request) -> Response:
    query_set = Problem.objects.all()

    valid_fields = {field.name for field in Problem._meta.get_fields()}

    filters = {key: value for key, value in request.GET.items() if key in valid_fields}
    query_set = query_set.filter(**filters)

    ordering = request.GET.get("ordering")
    if ordering:
        query_set = query_set.order_by(ordering)

    limit = request.GET.get("limit")
    if limit and limit.isdigit():
        query_set = query_set[:int(limit)]

    serializer = ProblemSerializer(query_set, many=True)

    return Response(serializer.data, status=200)


@api_view(['PUT', 'PATCH'])
def problem_update(request) -> Response:
    slug = request.data.get('titleSlug', '')

    try:
        problem = Problem.objects.get(titleSlug=slug)
    except Problem.DoesNotExist:
        raise NotFound(detail=f'Problem with slug: {slug} does not exist', code=404)

    serializer = ProblemSerializer(problem, data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    serializer.save()
    return Response(serializer.data, status=201)


@api_view(['DELETE'])
def problem_delete(request, slug: str) -> Response:
    try:
        problem = Problem.objects.get(titleSlug=slug)
    except Problem.DoesNotExist:
        raise NotFound(detail=f'Problem with slug: {slug} does not exist', code=404)

    problem.delete()
    return Response(status=204)


