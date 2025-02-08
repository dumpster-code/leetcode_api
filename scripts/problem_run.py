import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from leetcode.api import leetcode

data = {
    'url': 'https://leetcode.com/problems/{}/'.format('two-sum'),
    'titleSlug': 'two-sum',
    'lang': 'python3',
    'questionId': '1',
    "codeSlug": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        ",
    "exampleTestcaseList": "[2,7,11,15]\n9\n[3,2,4]\n6\n[3,3]\n6",
}

response = leetcode.LeetCode().run(data)

print(f"Submission ID: {response['submission_id']}")
print(f"Language: {response['pretty_lang']}")
print(f"Status: {response['status_msg']}")
print(f"Run Successful: {response['run_success']}")
print(f"Total Test Cases: {response['total_testcases']}")
print(f"Total Correct: {response['total_correct']}")
print(f"Error Message: {response['runtime_error']}")
print(f"Full Error Details:\n{response['full_runtime_error']}")

template = {
    'status_code': 15,
    'lang': 'python3',
    'run_success': False,
    'runtime_error': 'Line 4: IndentationError: expected an indented block after function definition on line 60',
    'full_runtime_error': 'IndentationError: expected an indented block after function definition on line 60\n    import sys\nLine 4  (Solution.py)',
    'status_runtime': 'N/A',
    'memory': 8608000,
    'code_answer': [],
    'code_output': [],
    'std_output_list': [''],
    'elapsed_time': 17,
    'task_finish_time': 1739027513779,
    'status_msg': 'Runtime Error',
    'total_correct': 0,
    'total_testcases': 3,
    'correct_answer': False,
    'pretty_lang': 'Python3',
    'submission_id': 'runcode_1739027511.6554987_ashXtUQxb9',
    'state': 'SUCCESS'
}
