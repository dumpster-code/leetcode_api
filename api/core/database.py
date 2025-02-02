from typing import Any, Dict
import time
import random

from rest_framework.response import Response
from rest_framework import status

from api.core.leetcode import LeetCode
from api.models import Topic, Problem
from api.serializers import TopicSerializer, ProblemSerializer


def create_problem(slug: str) -> Response:
    problem = Problem.objects.filter(titleSlug='two-sum').first()
    if problem:
        related_problems = problem.related_problems.all()
        print([p.titleSlug for p in related_problems])
    else:
        print("Problem with slug 'two-sum' not found.")

    if Problem.objects.filter(titleSlug=slug).exists():
        return Response(
            data={'error': f'Problem: "{slug}" already exists.'},
            status=status.HTTP_409_CONFLICT
        )

    time.sleep(random.uniform(1.0, 3.0))

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
    link_problem_to_topic(problem_instance)

    for similar_question in problem_data.get('similarQuestionList', []):
        similar_question_slug = similar_question['titleSlug']

        related_problem = Problem.objects.filter(titleSlug=similar_question_slug).first()
        if related_problem is None:
            response = create_problem(similar_question_slug)
            if response.status_code == status.HTTP_201_CREATED:
                related_problem = Problem.objects.get(titleSlug=similar_question_slug)

        if related_problem:
            problem_instance.related_problems.add(related_problem)

    return Response(
        data=serializer.data,
        status=status.HTTP_201_CREATED
    )


def link_problem_to_topic(problem: Problem):
    for topic_name, topic_slug in [t.values() for t in problem.topicTags]:
        if not Topic.objects.filter(name=topic_name, slug=topic_slug).exists():
            create_topic(topic_name, topic_slug)

        topic = Topic.objects.get(name=topic_name, slug=topic_slug)
        problem.topics.add(topic)

        topic.save()


def get_problem(slug: str) -> Response:
    try:
        problem = Problem.objects.get(titleSlug=slug)
    except Problem.DoesNotExist:
        return Response(
            data={'error': f'Problem with slug {slug} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProblemSerializer(problem)
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
