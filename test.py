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


class LeetCodeScraper:
    def __init__(self):
        self.json_data = None

        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options())
        except WebDriverException as e:
            print(f"WebDriver initialization failed: {e}")
            self.driver = None

    def __del__(self):
        if self.driver:
            self.driver.quit()

    def _fetch_page_content(self, url: str):
        if not self.driver:
            return None

        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        return self.driver.page_source

    def _extract_json_data(self, html_content):
        if not html_content:
            return

        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        if script_tag:
            self.json_data = json.loads(script_tag.string)

    def _save_json_to_file(self, filename='output.json'):
        if self.json_data:
            with open(filename, 'w') as json_file:
                json.dump(self.json_data, json_file, indent=4)

    def _extract_code_snippet(self):
        return self.json_data['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['question']['codeSnippets'][0]['code']

    def scrape(self, url: str):
        html_content = self._fetch_page_content(url)
        self._extract_json_data(html_content)
        self._save_json_to_file()
        code_snippet = self._extract_code_snippet()

        if code_snippet:
            print("Extracted Code Snippet:\n", code_snippet)
        else:
            print("No code snippet found.")


if __name__ == '__main__':
    url = 'https://leetcode.com/problems/two-sum/description'
    scraper = LeetCodeScraper()
    scraper.scrape(url)
