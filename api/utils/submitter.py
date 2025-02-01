from typing import Dict
import requests
import time

from problem import LeetCodeProblem


class Submitter:
    def __init__(self, cookies: str):
        separator = '; '

        key_value = cookies.split(separator)
        self.cookies: Dict[str, str] = {key: value for pair in key_value for key, value in [pair.split('=', 1)]}
        self.header = {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.cookies['csrftoken'],
        }

    def run(self, problem: LeetCodeProblem):
        self.header['Referer'] = problem.url

        payload = problem.payload()
        end_point = f'https://leetcode.com/problems/{problem.title_slug}/interpret_solution/'

        try:
            response = requests.post(end_point, json=payload, headers=self.header, cookies=self.cookies)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error during POST request: {e}")

        response: Dict[str, str] = response.json()
        interpret_id = response.get('interpret_id')
        if interpret_id:
            print(f"Interpret ID: {interpret_id}")
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
                    print("Submission successful!")
                else:
                    print("Waiting for submission to complete...")
            except requests.exceptions.RequestException as e:
                print(f"Error during GET request: {e}")

            retries -= 1
            time.sleep(1)

        self.header.pop('Referer')

        print(json)
