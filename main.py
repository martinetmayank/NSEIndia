import requests
import json
from urllib.request import urlopen, urlretrieve

def fetch_oa():

    response = requests.get(url_1, timeout=10, headers=user_agent).json()
    filename = 'oa_data.json'
    file = open(filename, mode='w+')
    print(response)
    file.write(json.dumps(response, sort_keys=True, indent=4))
    file.close()


def main():
    fetch_oa()


if __name__ == '__main__':
    url_1 = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    user_agent = {'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    main()
