from typing import Dict, Any, List


class LeetCodeProblem:
    def __init__(self, json: Dict[str, Any]):
        self.json: Dict[str, Any] = json

        self.question_id: str = ''
        self.title: str = ''
        self.title_slug: str = ''
        self.test_case: List[str] = []
        self.__get_question()

        self.difficulty: str = self.__get_difficulty()
        self.topics: List[str] = self.__get_topics()
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

        self.title = question['title']
        self.title_slug = question['titleSlug']
        self.question_id = question['questionId']
        self.test_case = question['exampleTestcaseList']

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

    def __get_difficulty(self) -> str:
        return self.json['props'] \
                        ['pageProps'] \
                        ['dehydratedState'] \
                        ['queries'] \
                        [1] \
                        ['state'] \
                        ['data'] \
                        ['question'] \
                        ['difficulty']

    def __get_topics(self) -> List[str]:
        topic_tags = self.json['props'] \
                              ['pageProps'] \
                              ['dehydratedState'] \
                              ['queries'] \
                              [1] \
                              ['state'] \
                              ['data'] \
                              ['question'] \
                              ['topicTags']

        return [tag['name'] for tag in topic_tags if 'name' in tag]

    def payload(self) -> Dict[str, str]:
        return {
            'lang': self.language_slug,
            'question_id': self.question_id,
            'typed_code': self.typed_code,
            'data_input': '\n'.join(self.test_case),
        }
