from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from api.core import database


@api_view(['GET'])
def get_problem(request: Request, title_slug: str) -> Response:
    return database.get_problem(title_slug)


@api_view(['GET'])
def get_daily_problem(request: Request) -> Response:
    return database.get_daily_problem()


@api_view(['GET'])
def get_query(request: Request) -> Response:
    return database.get_query(request)


# TODO: Change to POST
@api_view(['GET'])
def create_problem(request: Request, title_slug: str) -> Response:
    return database.create_problem(title_slug)
