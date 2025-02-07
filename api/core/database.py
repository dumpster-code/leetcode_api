import os
import json
from typing import Any, Dict
import time
import random

from rest_framework.response import Response
from rest_framework import status

from api.core.leetcode import LeetCode
from api.models import Topic, Problem
from api.serializers import TopicSerializer, ProblemSerializer


def create_problem(slug: str) -> Response:
    if Problem.objects.filter(titleSlug=slug).exists():
        return Response(
            data={'error': f'Problem: "{slug}" already exists.'},
            status=status.HTTP_409_CONFLICT
        )

    # need to update to throw correct Response when
    # fetching a problem that is paid only
    lc = LeetCode()
    problem_data: Dict[str, Any] = lc.get(slug)
    problem_data['url'] = f'https://leetcode.com/problems/{slug}/description/'

    serializer = ProblemSerializer(data=problem_data)
    if not serializer.is_valid():
        return Response(
            data={'error': f'Invalid data for problem: {serializer.errors}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    problem_instance = serializer.save()

    if not link_problem_to_topic(problem_instance):
        return Response(
            data={'error': 'Could not link problem with its topics'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        data=serializer.data,
        status=status.HTTP_201_CREATED
    )


def link_problem_to_topic(problem: Problem) -> bool:
    for topic_name, topic_slug in [t.values() for t in problem.topicTags]:
        if not topic_name or not topic_slug:
            return False

        if not Topic.objects.filter(name=topic_name, slug=topic_slug).exists():
            create_topic(topic_name, topic_slug)

        topic = Topic.objects.get(name=topic_name, slug=topic_slug)
        problem.topics.add(topic)

        topic.save()

    return True


def get_problem(slug: str) -> Response:
    problem = Problem.objects.filter(titleSlug=slug).first()

    if problem is None:
        return Response(
            data={'error': f'Problem with slug {slug} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProblemSerializer(problem)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


def get_daily_problem() -> Response:
    link_related_problems()

    lc = LeetCode()
    data = lc.daily_question()
    slug = data['titleSlug']

    response = get_problem(slug)
    if response.status_code == status.HTTP_200_OK:
        return response

    return create_problem(slug)


def delete_problem(slug: str) -> Response:
    problem = Problem.objects.filter(titleSlug=slug).first()

    if not problem:
        return Response(
            data={'error': f'Problem with slug: {slug} does not exist'},
            status=status.HTTP_400_BAD_REQUEST
        )

    problem.delete()

    return Response(
        data={'message': f'Problem: {slug} deleted'},
        status=status.HTTP_200_OK
    )


def get_query(request) -> Response:
    queryset = Problem.objects.all()

    for key, value in request.GET.items():
        if hasattr(Problem, key):
            queryset = queryset.filter(**{key: value})

    serializer = ProblemSerializer(queryset, many=True)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


def create_topic(name: str, slug: str) -> Response:
    if Topic.objects.filter(name=name, slug=slug).exists():
        return Response(
            data={'error': f'Topic: "{name}" already exists.'},
            status=status.HTTP_409_CONFLICT
        )

    data = {
        'name': name,
        'slug': slug,
    }

    serializer = TopicSerializer(data=data)
    if not serializer.is_valid():
        return Response(
            data={'error': f'Invalid data for topic: {serializer.errors}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer.save()
    return Response(
        data=serializer.data,
        status=status.HTTP_201_CREATED
    )


def get_topic(name: str, slug: str) -> Response:
    try:
        topic = Topic.objects.get(name=name, slug=slug)
    except Topic.DoesNotExist:
        return Response(
            data={'error': f'Topic with name: {name}, slug: {slug} not found'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = TopicSerializer(topic)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


# ---------------------------------------------------------------------------------------------------


def get_all_problems():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '../all_problems.json')

    with open(file_path, 'r') as f:
        data = json.load(f)

    errors = []

    for problem in data['data']['problemsetQuestionList']['questions']:
        if (id := problem.get('frontendQuestionId')) and (slug := problem.get('titleSlug')):
            if get_problem(slug).status_code == 200:
                continue

            time.sleep(random.uniform(3.0, 5.0))

            if create_problem(slug).status_code != 201:
                print(f'error: {id} {slug}')
                errors.append({id, slug})
                continue

            print(f'success: {id} {slug}')


def link_related_problems():
    for idx, problem in enumerate(Problem.objects.all(), start=1):
        print(f'{idx}: {problem}')
        for similar_problem in problem.similarQuestionList:
            if not similar_problem:
                continue

            similar_problem_slug = similar_problem.get('titleSlug')
            if not similar_problem_slug:
                continue

            model = Problem.objects.filter(titleSlug=similar_problem_slug).first()
            if not model:
                continue

            if problem.related_problems.filter(id=model.id).exists():
                continue

            print(f'    added: {model.titleSlug}')
            problem.related_problems.add(model)

        problem.save()
