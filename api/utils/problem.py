from typing import Dict, Any, List


class LeetCodeProblem:
    def __init__(self, json: Dict[str, Any]):
        self.id: str = self.__get_id(json)
        self.title: str = self.__get_title(json)
        self.code_snippet: str = self.__get_code_snippet(json)
        self.difficulty: str = self.__get_difficulty(json)
        self.topics: List[str] = self.__get_topics(json)
        self.url = f'https://leetcode.com/problems/{self.__to_slug(self.title)}'

    def __to_slug(self, entry: str) -> str:
        return entry.replace(' ', '-').lower()

    def __get_id(self, json: Dict[str, Any]) -> str:
        return json['props'] \
                   ['pageProps'] \
                   ['dehydratedState'] \
                   ['queries'] \
                   [1] \
                   ['state'] \
                   ['data'] \
                   ['question'] \
                   ['questionId']

    def __get_title(self, json: Dict[str, Any]) -> str:
        return json['props'] \
                   ['pageProps'] \
                   ['dehydratedState'] \
                   ['queries'] \
                   [1] \
                   ['state'] \
                   ['data'] \
                   ['question'] \
                   ['title']

    def __get_code_snippet(self, json: Dict[str, Any]) -> str:
        return json['props'] \
                   ['pageProps'] \
                   ['dehydratedState'] \
                   ['queries'] \
                   [1] \
                   ['state'] \
                   ['data'] \
                   ['question'] \
                   ['codeSnippets'] \
                   [0] \
                   ['code']

    def __get_difficulty(self, json: Dict[str, Any]) -> str:
        return json['props'] \
                   ['pageProps'] \
                   ['dehydratedState'] \
                   ['queries'] \
                   [1] \
                   ['state'] \
                   ['data'] \
                   ['question'] \
                   ['difficulty']

    def __get_topics(self, json: Dict[str, Any]) -> List[str]:
        topic_tags = json['props'] \
                         ['pageProps'] \
                         ['dehydratedState'] \
                         ['queries'] \
                         [1] \
                         ['state'] \
                         ['data'] \
                         ['question'] \
                         ['topicTags']

        return [tag['name'] for tag in topic_tags if 'name' in tag]
