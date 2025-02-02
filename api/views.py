from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.core import database


@api_view(['GET'])
def get_problem(request, title_slug: str) -> Response:
    return database.get_problem(title_slug)


# TODO: Change to POST
@api_view(['GET'])
def create_problem(request, title_slug: str) -> Response:
    return database.create_problem(title_slug)
