import requests
import json


def read_oa(response):
    if expiry_data:
        ce_data = [data["CE"] for data in response['records']['data'] if "CE" in data and str(
            data['expiryDate']).lower() == str(expiry_data).lower()]
        pe_data = [data["PE"] for data in response['records']['data'] if "PE" in data and str(
            data['expiryDate']).lower() == str(expiry_data).lower()]
        print(pe_data)
    else:
        ce_data = [data["CE"]
                   for data in response['filtered']['data'] if "CE" in data]
        pe_data = [data["PE"]
                   for data in response['filtered']['data'] if "PE" in data]


def write_oa(response):
    filename = 'oa_data.json'
    file = open(filename, mode='w+')
    print('Data is being written to the file', filename, '...')
    file.write(json.dumps(response, sort_keys=True, indent=4))
    file.close()


def fetch_oa():
    response = requests.get(url, timeout=10, headers=user_agent).json()
    # write_oa(response)
    read_oa(response)


def main():
    fetch_oa()


if __name__ == '__main__':
    expiry_data = '31-Dec-2020'
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
    user_agent = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    main()
