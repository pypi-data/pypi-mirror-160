"""
with open(f"{os.path.dirname(os.path.realpath(__file__))}/tests/test_actions.yml", 'r') as f:
    actions = yaml.safe_load(f)
action = actions[0]

#for Tuncel: crawler = GenericCrawler(endpoint=)
"""

from generic_crawler.core import GenericCrawler, ActionReader

reader = ActionReader(path_to_yaml="/Users/tcudikel/Dev/ace/generic-crawler-sdk/tests/actions/test_wait.yml")
crawler = GenericCrawler(endpoint=endpoint)

#reader.action["steps"][0]["duration"] = 20
data, _ = crawler.retrieve(reader.action)


print("ok")



