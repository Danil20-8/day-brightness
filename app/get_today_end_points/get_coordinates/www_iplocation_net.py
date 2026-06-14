import re
import requests

def get_with_www_iplocation_net():
    contents = requests.get("https://www.iplocation.net/ip-lookup").text

    for line in re.findall(r'source\s*:\s*(\S+?),', contents):
        service = line.lstrip("'").rstrip("'")
        result = requests.post("https://www.iplocation.net/get-ipdata", data={ "source": service }).json()

        if "res" in result:
            return [result['res']['latitude'], result['res']['longitude']]

    return ["56.8575", "60.6125"]