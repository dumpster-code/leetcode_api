import pytest
from problem.models import Problem


@pytest.mark.django_db
def test_first_model():
    model = Problem.objects.create()
