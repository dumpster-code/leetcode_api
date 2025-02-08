import json

with open("db_clean.json", "r") as file:
    data = json.load(file)

json_str = json.dumps(data).replace("leetcode_problem_topics", "leetcode_topics")

with open("db_clean.json", "w") as file:
    file.write(json_str)
