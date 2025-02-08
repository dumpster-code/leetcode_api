from dotenv import load_dotenv
from typing import Any, Dict
import os
import requests
import time

GRAPHQL_URL = 'https://leetcode.com/graphql/'
PROBLEM_URL = 'https://leetcode.com/problems/{}/description/'

load_dotenv()


class LeetCode:
    def __init__(self):
        cookies: str = os.getenv('cookies')
        separator = '; '
        key_value = cookies.split(separator)
        self.cookies: Dict[str, str] = {key: value for pair in key_value for key, value in [pair.split('=', 1)]}

        self.header = {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.cookies['csrftoken'],
        }

    def get(self, slug: str) -> Dict[str, Any]:
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

        return response.json()

    def daily_question(self) -> str:
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
            return response.json()

        json = response.json()

        slug = json.get('data', {}) \
                   .get('activeDailyCodingChallengeQuestion', {}) \
                   .get('question', {}) \
                   .get('titleSlug')

        if not slug:
            print('Could not retrieve problem of the day')
            return {}

        return slug

        # query = """
        #     query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
        #         problemsetQuestionList: questionList(
        #             categorySlug: $categorySlug
        #             limit: $limit
        #             skip: $skip
        #             filters: $filters
        #         ) {
        #             total: totalNum
        #             questions: data {
        #                 acRate
        #                 difficulty
        #                 freqBar
        #                 frontendQuestionId: questionFrontendId
        #                 isFavor
        #                 paidOnly: isPaidOnly
        #                 status
        #                 title
        #                 titleSlug
        #                 topicTags {
        #                     name
        #                     id
        #                     slug
        #                 }
        #                 hasSolution
        #                 hasVideoSolution
        #             }
        #         }
        #     }
        # """
    def get_problem_list(self) -> Dict[str, Any]:
        query = """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
                ) {
                    total: totalNum
                    questions: data {
                        frontendQuestionId: questionFrontendId
                        titleSlug
                    }
                }
            }
        """

        variables = {
            "categorySlug": "all-code-essentials",
            "skip": 0,
            "limit": 4000,
            "filters": {}
        }

        response = requests.post(GRAPHQL_URL, headers=self.header, cookies=self.cookies, json={"query": query, "variables": variables})
        return response.json()

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self.header['Referer'] = data.get('url', '')
        title_slug = data.get('titleSlug', '')

        payload = {
            # TODO: defaulting to python for now
            'lang': data.get('lang', ''),
            'question_id': data.get('questionId', ''),
            'typed_code': data.get('codeSlug', ''),
            'data_input': data.get('exampleTestcaseList', ''),
        }

        end_point = f'https://leetcode.com/problems/{title_slug}/interpret_solution/'

        try:
            response = requests.post(end_point, json=payload, headers=self.header, cookies=self.cookies)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'HTTP Error: {e.response.status_code} - {e.response.reason}')
            print(f'Response Content: {e.response.text}')
        except requests.exceptions.ConnectionError as e:
            print(f'Connection Error: {e}')
        except requests.exceptions.Timeout as e:
            print(f'Timeout Error: {e}')
        except requests.exceptions.RequestException as e:
            print(f'General Request Error: {e}')

        response: Dict[str, str] = response.json()
        interpret_id: str = response.get('interpret_id')

        if not interpret_id:
            return {}

        print('Waiting', end='', flush=True)
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
                    print(' Done', flush=True)
                else:
                    print('.', end='', flush=True)
            except requests.exceptions.RequestException as e:
                print(f'Error during GET request: {e}')

            retries -= 1
            time.sleep(1)

        return json

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
