from typing import Any, Dict, Optional
import requests
import time

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

    def submit(self, problem: LeetCodeProblem) -> bool:
        self.header['Referer'] = problem.url

        payload = problem.payload()
        end_point = f'https://leetcode.com/problems/{problem.title_slug}/interpret_solution/'

        try:
            response = requests.post(end_point, json=payload, headers=self.header, cookies=self.cookies)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Error during POST request: {e}')

        response: Dict[str, str] = response.json()
        interpret_id: str = response.get('interpret_id')
        if interpret_id:
            print(f'Interpret ID: {interpret_id}')
        success = False
        retries = 5

        while not success and retries > 0:
            get_url = f'https://leetcode.com/submissions/detail/{interpret_id}/check/'
            try:
                response = requests.get(get_url, headers=self.header, cookies=self.cookies)
                response.raise_for_status()
                json = response.json()
                success = 'state' in json and json['state'] == 'SUCCESS'
                if success:
                    print('Submission successful!')
                else:
                    print('Waiting for submission to complete...')
            except requests.exceptions.RequestException as e:
                print(f'Error during GET request: {e}')

            retries -= 1
            time.sleep(1)

        print(json)

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
                    titleSlug
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

        try:
            response = requests.post(GRAPHQL_URL, headers=self.header, cookies=self.cookies, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Error during POST request: {e}')
            return {}

        result = response.json()

        # import json
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
p = l.problem('special-array-i')
time.sleep(1)
l.submit(p)
