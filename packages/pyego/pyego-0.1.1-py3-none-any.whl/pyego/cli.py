# entry point for the cli

import requests
import ujson


def execute():
    response = ujson.loads(requests.get('https://sandbox.api.service.nhs.uk/hello-world/hello/world').text)['message']
    print(response + ' from an API endpoint.')
    return

if __name__ == '__main__':
    execute()
