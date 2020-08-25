import requests
import json
import pandas as pd
import xlwings
from time import sleep
from datetime import datetime
import os
from pprint import pprint

pd.set_option('display.width', 1920)
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 1000)

excel_file = 'option_chain_analysis.xlsx'
workbook = xlwings.Book(excel_file)
sheet_name = 'OIData'
sheet_oi_single = workbook.sheets(sheet_name)
df_list = []

oi_filenmame = os.path.join(os.getcwd(), 'oi_data_records_{0}.json'.format(
    datetime.now().strftime('%m%d%Y')))


def read_oa(response, dataframe):
    global df_list
    tries = 0
    max_tries = 5
    while tries <= max_tries:
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
        # pe_data = pe_data.drop([
        #     'askPrice', 'askQty', 'bidQty', 'bidprice',
        #     'expiryDate', 'identifier', 'totalBuyQuantity', 'totalSellQuantity',
        #     'totalTradedVolume', 'underlying', 'underlyingValue', 'strikePrice'
        # ], axis=1)[
        #     ['change', 'changeinOpenInterest', 'impliedVolatility', 'lastPrice',
        #      'openInterest', 'pChange', 'pchangeinOpenInterest'
        #      ]
        # ]
        pe_data = pe_data.drop([
            'askPrice', 'askQty', 'bidQty', 'bidprice',
            'expiryDate', 'identifier', 'totalBuyQuantity', 'totalSellQuantity',
            'totalTradedVolume', 'underlying', 'underlyingValue'
        ], axis=1)[
            ['change', 'changeinOpenInterest', 'impliedVolatility', 'lastPrice',
             'openInterest', 'pChange', 'pchangeinOpenInterest', 'strikePrice'
             ]
        ]

        sheet_oi_single.range('A2').options(
            index=False, header=False).value = ce_data
        sheet_oi_single.range('I2').options(
            index=False, header=False).value = pe_data

        ce_data['type'] = 'CE'
        pe_data['type'] = 'PE'
        df1 = pd.concat([ce_data, pe_data], sort=True)
        if len(df_list) > 0:
            df1['Time'] = df_list[-1][0]['Time']


        if len(df_list) > 0 and df1.to_dict('records') == df_list[-1]:
            print('Dplicate data, not recording...')
            sleep(10)
            tries += 1
            continue

        df1['Time'] = datetime.now().strftime('%H:%M')
        df_list.append(df1.to_dict('records'))

        dataframe = pd.concat([dataframe, df1], sort=True)

        with open(oi_filenmame, 'w') as file:
            file.write(json.dumps(df_list, indent=4, sort_keys=False))
        return df1


def fetch_oi(dataframe):
    user_agent = {
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    response = requests.get(url, timeout=10, headers=user_agent).json()
    output = read_oa(response, dataframe)
    return output


def main():
    global df_list
    try:
        df_list = json.loads(open(oi_filenmame).read())
    except Exception as e:
        print('Error reading file.... error', e)
        df_list = []

    if df_list:
        dataframe = pd.DataFrame()
        for item in df_list:
            dataframe = pd.concat([dataframe, pd.DataFrame(item)], sort=False)
    else:
        dataframe = pd.DataFrame()
    fetch_oi(dataframe)


if __name__ == '__main__':
    expiry_data = '31-Dec-2020'
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

    main()
