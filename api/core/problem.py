from typing import Dict, Any, Set
from urls import PROBLEM_URL


class LeetCodeProblem:
    def __init__(self, json: Dict[str, Any]):
        self.json: Dict[str, Any] = json

        self.content: str = json.get('content', '')
        self.difficulty: str = json.get('difficulty', '')
        self.dislikes: str = json.get('dislikes', '')
        self.example_testcase_list: str = json.get('exampleTestcaseList', '')
        self.is_paid_only: str = json.get('isPaidOnly', '')
        self.likes: str = json.get('likes', '')
        self.question_id: str = json.get('questionId', '')
        self.similar_questions: str = json.get('similarQuestions', '')
        self.stats: str = json.get('stats', '')
        self.title: str = json.get('title', '')
        self.title_slug: str = json.get('titleSlug', '')
        self.url: str = PROBLEM_URL.format(self.title_slug)

        self.code_lang: Dict[str, str] = {code['lang']: code['code'] for code in json.get('codeSnippets')}
        self.code_slug: Dict[str, str] = {code['langSlug']: code['code'] for code in json.get('codeSnippets')}

        self.topic_name: Set[str] = {topic['name'] for topic in json.get('topicTags')}
        self.topic_slug: Set[str] = {topic['slug'] for topic in json.get('topicTags')}

    # TODO: default to python for now
    def payload(self) -> Dict[str, str]:
        slug = 'python'
        return {
            'lang': slug,
            'question_id': self.question_id,
            'typed_code': self.code_slug[slug],
            'data_input': '\n'.join(self.example_testcase_list),
        }
