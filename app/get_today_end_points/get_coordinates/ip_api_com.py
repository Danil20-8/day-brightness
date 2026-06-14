import requests

def get_with_ip_api_com():
    contents = requests.get("https://demo.ip-api.com/json", headers={"Origin":"https://ip-api.com"}).json()

    return [contents['lat'],  contents['lon']]