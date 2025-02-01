from typing import Any, Dict, Optional
import json
import requests

from cookies import cookies
from urls import GRAPHQL_URL
from problem import LeetCodeProblem


class LeetCode:
    def __init__(self):
        self.cookies: str = cookies

        separator = '; '

        key_value = cookies.split(separator)
        self.cookies: Dict[str, str] = {key: value for pair in key_value for key, value in [pair.split('=', 1)]}
        self.header = {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.cookies['csrftoken'],
        }

    def problem(self, slug: str) -> Optional[LeetCodeProblem]:
        data = self.__get_question_data(slug)
        if not data:
            print(f'Failed to get question data for: {slug}')
            return None

        return LeetCodeProblem(data)

    def __get_question_data(self, slug: str) -> Dict[str, Any]:
        payload = {
            'query': '''
            query questionData($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    content
                    difficulty
                    dislikes
                    exampleTestcaseList
                    isPaidOnly
                    likes
                    questionId
                    similarQuestions
                    stats
                    title
                    codeSnippets {
                        lang
                        langSlug
                        code
                    }
                    topicTags {
                        name
                        slug
                    }
                }
            }
            ''',
            'variables': {
                'titleSlug': slug,
            },
            'operationName': 'questionData'
        }

        response = requests.post(GRAPHQL_URL, headers=self.header, cookies=self.cookies, json=payload)

        result = response.json()
        # print(json.dumps(result, indent=4))
        return result['data']['question']

    def __get_synced_code(self, id: str) -> str:
        payload = {
            "query": """
                query syncedCode($questionId: Int!, $lang: Int!) {
                    syncedCode(questionId: $questionId, lang: $lang) {
                        timestamp
                        code
                    }
                }
            """,
            "variables": {
                "questionId": id,
                "lang": 0
            }
        }

        response = requests.post(GRAPHQL_URL, headers=self.header, cookies=self.cookies, json=payload)

        result = response.json()
        return result['data']['syncedCode']


l = LeetCode()
l.problem('special-array-i')
