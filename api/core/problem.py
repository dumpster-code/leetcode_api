from typing import List, Dict, Any, Set
import json

from api.core.urls import PROBLEM_URL


class LeetCodeProblem:
    def __init__(self, json: Dict[str, Any]):
        self.json: Dict[str, Any] = json

        self.content: str = json.get('content', '')
        self.difficulty: str = json.get('difficulty', '').lower()
        self.dislikes: str = json.get('dislikes', '')
        self.test_cases: str = json.get('exampleTestcaseList', '')
        self.hints: List[str] = json.get('hints', [])
        self.paid_only: str = json.get('isPaidOnly', '')
        self.likes: str = json.get('likes', '')
        self.question_id: str = json.get('questionId', '')
        self.stats: str = json.get('stats', '')
        self.title: str = json.get('title', '')
        self.title_slug: str = json.get('titleSlug', '')
        self.url: str = PROBLEM_URL.format(self.title_slug)

        self.code_lang: Dict[str, str] = {code['lang']: code['code'] for code in json.get('codeSnippets')}
        self.code_slug: Dict[str, str] = {code['langSlug']: code['code'] for code in json.get('codeSnippets')}

        self.similar_questions: str = json.get('similarQuestionList', '')

        self.topic_name: Set[str] = {topic['name'] for topic in json.get('topicTags')}
        self.topic_slug: Set[str] = {topic['slug'] for topic in json.get('topicTags')}

    def __str__(self):
        return json.dumps(self.json, indent=4)

    # TODO: default to python for now
    def payload(self) -> Dict[str, str]:
        slug = 'python'
        return {
            'lang': slug,
            'question_id': self.question_id,
            'typed_code': self.code_slug[slug],
            'data_input': '\n'.join(self.example_testcase_list),
        }
