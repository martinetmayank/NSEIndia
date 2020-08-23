import requests
import json
import pandas as pd
import xlwings


pd.set_option('display.width', 1920)
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 1000)

excel_file = 'option_chain_analysis.xlsx'
workbook = xlwings.Book(excel_file)
sheet_name = 'OIData'
sheet_oi_single = workbook.sheets(sheet_name)


def read_oa(response):
    if expiry_data:
        ce_values = [data["CE"] for data in response['records']['data'] if "CE" in data and str(
            data['expiryDate']).lower() == str(expiry_data).lower()]
        pe_values = [data["PE"] for data in response['records']['data'] if "PE" in data and str(
            data['expiryDate']).lower() == str(expiry_data).lower()]

    else:
        ce_values = [data["CE"]
                     for data in response['filtered']['data'] if "CE" in data]
        pe_values = [data["PE"]
                     for data in response['filtered']['data'] if "PE" in data]

    ce_data = pd.DataFrame(ce_values)
    pe_data = pd.DataFrame(pe_values)

    ce_data = ce_data.sort_values(['strikePrice'])
    pe_data = pe_data.sort_values(['strikePrice'])

    ce_data = ce_data.drop([
        'askPrice', 'askQty', 'bidQty', 'bidprice',
        'expiryDate', 'identifier', 'totalBuyQuantity', 'totalSellQuantity',
        'totalTradedVolume', 'underlying', 'underlyingValue'
    ], axis=1)[
        ['change', 'changeinOpenInterest', 'impliedVolatility', 'lastPrice',
         'openInterest', 'pChange', 'pchangeinOpenInterest', 'strikePrice'
         ]
    ]
    pe_data = pe_data.drop([
        'askPrice', 'askQty', 'bidQty', 'bidprice',
        'expiryDate', 'identifier', 'totalBuyQuantity', 'totalSellQuantity',
        'totalTradedVolume', 'underlying', 'underlyingValue', 'strikePrice'
    ], axis=1)[
        ['change', 'changeinOpenInterest', 'impliedVolatility', 'lastPrice',
         'openInterest', 'pChange', 'pchangeinOpenInterest'
         ]
    ]

    sheet_oi_single.range('A2').options(
        index=False, header=False).value = ce_data
    sheet_oi_single.range('I2').options(
        index=False, header=False).value = pe_data


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
