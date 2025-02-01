from api.serializers import ProblemSerializer
from api.core.problem import LeetCodeProblem


def store(problem: LeetCodeProblem) -> bool:
    data = {
        'data': problem.json,
        'content': problem.content,
        'difficulty': problem.difficulty,
        'dislikes': problem.dislikes,
        'test_cases': problem.test_cases,
        'hints': problem.hints,
        'paid_only': problem.paid_only,
        'likes': problem.likes,
        'question_id': problem.question_id,
        'stats': problem.stats,
        'title': problem.title,
        'title_slug': problem.title_slug,
        'url': problem.url,
        'code_lang': problem.code_lang,
        'code_slug': problem.code_slug,
        'topics': problem.topic_name,
    }

    serializer = ProblemSerializer(data=data)
    if not serializer.is_valid():
        return False

    serializer.save()
    return True
