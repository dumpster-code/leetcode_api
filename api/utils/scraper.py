from typing import Dict, Any, Optional
import json
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from problem import LeetCodeProblem
from submitter import Submitter


class LeetCodeScraper:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
        except WebDriverException as e:
            print(f"WebDriver initialization failed: {e}")
            self.driver = None

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def __fetch_page_content(self, url: str) -> str:
        if not self.driver:
            return ''

        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        return self.driver.page_source

    def __get_json(self, html_content: str) -> Optional[Dict[str, Any]]:
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

        return json.loads(script_tag.string)

    def __save_json_to_file(self, json: Dict[str, any], filename='output.json'):
        try:
            with open(filename, 'w') as json_file:
                json.dump(json, json_file, indent=4)
            print(f'JSON data saved to {filename}')
        except IOError as e:
            print(f'Error saving JSON file: {e}')

    def scrape(self, url: str) -> LeetCodeProblem:
        html_content = self.__fetch_page_content(url)
        json = self.__get_json(html_content)
        # self.__save_json_to_file()

        self.driver.close()
        return LeetCodeProblem(json)


if __name__ == '__main__':
    url = 'https://leetcode.com/problems/two-sum/description'
    scraper = LeetCodeScraper()
    problem = scraper.scrape(url)

    # print(problem.url)
    # print(problem.question_id)
    # print(problem.title)
    # print(problem.difficulty)
    # print(problem.topics)
    # print(problem.language)
    # print(problem.typed_code)
    # print(problem.test_case)
    # print(''.join(problem.test_case))

    submitter = Submitter('')

    submitter.run(problem)
