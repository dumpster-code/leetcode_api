from typing import Dict, Any, List


class LeetCodeProblem:
    def __init__(self, json: Dict[str, Any]):
        self.json: Dict[str, Any] = json

        self.difficulty: str = ''
        self.question_id: str = ''
        self.topic_tags: List[str] = []
        self.test_case: List[str] = []
        self.title: str = ''
        self.title_slug: str = ''
        self.__get_question()

        self.url = f'https://leetcode.com/problems/{self.title_slug}'

        self.typed_code: str = ''
        self.language_slug: str = ''
        self.language: str = ''
        self.__get_code_snippet()

    def __get_question(self) -> None:
        question = self.json['props'] \
                            ['pageProps'] \
                            ['dehydratedState'] \
                            ['queries'] \
                            [1] \
                            ['state'] \
                            ['data'] \
                            ['question'] \

        self.difficulty = question['difficulty']
        self.question_id = question['questionId']
        self.topic_tags = [tag['name'] for tag in question['topicTags'] if 'name' in tag]
        self.test_case = question['exampleTestcaseList']
        self.title = question['title']
        self.title_slug = question['titleSlug']

    def __get_code_snippet(self):
        snippet = self.json['props'] \
                           ['pageProps'] \
                           ['dehydratedState'] \
                           ['queries'] \
                           [1] \
                           ['state'] \
                           ['data'] \
                           ['question'] \
                           ['codeSnippets'] \
                           [0]

        self.typed_code = snippet['code']
        self.language = snippet['lang']
        self.language_slug = snippet['langSlug']

    def payload(self) -> Dict[str, str]:
        return {
            'lang': self.language_slug,
            'question_id': self.question_id,
            'typed_code': self.typed_code,
            'data_input': '\n'.join(self.test_case),
        }
