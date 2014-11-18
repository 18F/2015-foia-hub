import json


def json_from(response):
    return json.loads(response.content.decode(encoding='UTF-8'))
