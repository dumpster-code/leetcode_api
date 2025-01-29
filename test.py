import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://leetcode.com/problems/two-sum/description')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')
script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

if script_tag:
    script_content = script_tag.string
    json_data = json.loads(script_content)
    pretty_json = json.dumps(json_data, indent=4)

    with open('output.json', 'w') as json_file:
        json_file.write(pretty_json)

    queries = json_data['props']['pageProps']['dehydratedState']['queries']
    question_data = queries[1]['state']['data']['question']
    code_snippets = question_data['codeSnippets']

    code_snippet = code_snippets[0]['code']

    print(code_snippet)

else:
    print('Error Loading...')

driver.quit()
