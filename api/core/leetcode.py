from typing import Any, Dict, Optional
import requests
import time

from api.core.cookies import cookies
from api.core.urls import GRAPHQL_URL
from api.core.problem import LeetCodeProblem


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

    def get(self, slug: str) -> Optional[LeetCodeProblem]:
        data = self.__get_question_data(slug)
        if not data:
            print(f'Failed to get question data for: {slug}')
            return None

        return LeetCodeProblem(data)

    def daily_question(self) -> Optional[LeetCodeProblem]:
        payload = {
            'query': '''
            query questionOfToday {
                activeDailyCodingChallengeQuestion {
                    userStatus
                    question {
                        titleSlug
                    }
                }
            }
            ''',
        }

        try:
            response = requests.post(GRAPHQL_URL, headers=self.header, cookies=self.cookies, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Error during POST request: {e}')
            return None

        json = response.json()

        slug = json.get('data', {}) \
                     .get('activeDailyCodingChallengeQuestion', {}) \
                     .get('question', {}) \
                     .get('titleSlug')

        # import json
        # print(json.dumps(json, indent=4))

        if not slug:
            print('Could not retrieve problem of the day')
            return None

        return self.get(slug)

    def run(self, problem: LeetCodeProblem) -> bool:
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
        if not interpret_id:
            return False

        print(f'Interpret ID: {interpret_id}')
        url = f'https://leetcode.com/submissions/detail/{interpret_id}/check/'

        success = False
        retries = 5
        while not success and retries > 0:
            try:
                response = requests.get(url, headers=self.header, cookies=self.cookies)
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
                    hints
                    isPaidOnly
                    likes
                    questionId
                    stats
                    title
                    titleSlug
                    codeSnippets {
                        code
                        lang
                        langSlug
                    }
                    similarQuestionList {
                        difficulty
                        isPaidOnly
                        title
                        titleSlug
                    }
                    topicTags {
                        name
                        slug
                    }
                    isPaidOnly
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

        json = response.json()

        return json['data']['question']

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

        json = response.json()
        return json['data']['syncedCode']


# l = LeetCode()
# p = l.get('two-sum')
# p = l.daily_question()

# print(p)
# time.sleep(1)
# l.submit(p)
