import numpy as np
import pandas as pd
from pathlib import Path
import datetime
import time
import asyncio
import os

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

ROOT_PATH = Path("../stock_data/project2/data")
# core_cols = ['date_fundamentals','cusip_company_part_fundamentals', 'siccode_fundamentals', 'ticker_fundamentals', 'company_name_fundamentals',   'assets', 'liabilities', 'marketcap', 'ncf',
#        'currentratio', 'receivables', 'payables', 'payoutratio',  'grossmargin', 'ebitdamargin', 'netmargin', 'revenueusd', 'ebitdausd', 'ebitusd', 'debtusd', 'deferredrev', 'pe', 'price', 'inventory',
#        'fcf', 'investments', 'workingcapital', 'capex', 'cashnequsd']

core_cols = ['date_fundamentals','cusip_company_part_fundamentals', 'siccode_fundamentals', 'ticker_fundamentals', 'company_name_fundamentals', 'revenueusd','ebitdausd','ebitdamargin','netinccmnusd',
             'netmargin','cashnequsd','workingcapital','debtusd','liabilities','equityusd','marketcap','ev','fcf','ncfdebt','currentratio','de','divyield','epsusd','payoutratio','evebitda','pb','pe']

core_cols2 = ['date_fundamentals', 'cusip_company_part_fundamentals', 'assets', 'marketcap', 'payables']

# edi_cols = ['date_edi', 'YearMonth_edi', 'mktclosedate', 'maturity_date', 'foreign_key_edi','cusip_company_part_edi', 'uscode', 'isin', 'currency', 'close_edi', 'issuername','coupon', 'security_type']
edi_cols = ['mktclosedate', 'maturity_date', 'cusip_company_part_edi', 'isin', 'uscode', 'secid', 'currency', 'close_edi', 'issuername','coupon', 'sectycd', 'security_type', 'bond_attribute' , 'minimum_denomination' ]
edi_cols2 = ['isin', 'close_edi', 'coupon', 'maturity_date', 'mktclosedate', 'cusip_company_part']

def dateDiff(d1, d2):
       tdelta = (d1 - d2).days
       return tdelta

async def combine_core_edi(core_df, edi_df):
       start_time = time.time()
       combine_df = pd.DataFrame()
       comp_cusips = core_df['cusip_company_part'].unique().tolist()
       comp_cusips = comp_cusips[0:50]
       count = 0

       await asyncio.sleep(0.1)

       print('Strated processing to join Core US cusips with EDI bond price... ')
       for cusip in comp_cusips:
              if count % 10 == 0:
                     print(f'{count} Issuer cusips processed... ')

              cusip_df = core_df.loc[core_df['cusip_company_part'] == cusip].sort_values(by = 'date_fundamentals')
              fund_dates = cusip_df['date_fundamentals'].unique().tolist()
              edi_cusip_df = edi_df.loc[edi_df['cusip_company_part'] == cusip]

              isins = edi_cusip_df['isin'].unique().tolist()

              for isin in isins:
                     edi_cusip_df = edi_df.loc[edi_df['isin'] == isin]
                     edi_dates = edi_cusip_df['mktclosedate'].unique().tolist()
                     min_edi_date = min(edi_dates)

                     for date in fund_dates:
                            # if date == datetime.date(2013, 6, 10):
                            #        print(date)
                            if  min_edi_date > date:
                                   continue

                            cusip_df1 = cusip_df.loc[cusip_df['date_fundamentals'] == date]
                            df1 = cusip_df1.merge(edi_cusip_df, how='inner', on='cusip_company_part')
                            df1 = df1.loc[df1['date_fundamentals'] <= df1['maturity_date']]

                            if df1.empty:
                                   continue

                            df1['timedelta'] = df1.apply(lambda x: dateDiff(x.date_fundamentals, x.mktclosedate),axis=1)
                            df1 = df1.loc[df1['timedelta'] >= 0]
                            df2 = df1.loc[df1['timedelta'] == df1['timedelta'].min()]

                            if not combine_df.empty:
                                   combine_df = combine_df.append(df2)
                            else:
                                   combine_df = df2
              count += 1

       end_time = time.time()
       print("--- %s seconds ---" % (end_time - start_time))

       # end_time = time.time()
       # print(f'Total time in seconds: {start_time - end_time}')

       return combine_df

async def main():
       core_us_file = 'core_us_fundamentals.csv'
       core_path = Path.joinpath(ROOT_PATH, core_us_file)

       # Load Core US Fundamental table
       df = pd.read_csv(core_path, usecols=core_cols, infer_datetime_format=True, parse_dates=True, )

       # Subset of Core US df
       core_df = df[core_cols]
       core_df['date_fundamentals'] = pd.to_datetime(df['date_fundamentals']).dt.date
       core_df_test = core_df[core_cols].copy()
       core_df_test = core_df_test.rename(columns={'cusip_company_part_fundamentals': 'cusip_company_part'})

       # EDI Bond Price Table
       edi_bond_file = 'edi_bond_price_NT_4.csv'
       edi_path = Path.joinpath(ROOT_PATH, edi_bond_file)
       df_edi_bond_price = pd.read_csv(edi_path, infer_datetime_format=True, parse_dates=True)
       # df_edi_bond_price = df_edi_bond_price.loc[df_edi_bond_price['bond_attribute'] == 'REDEEM']
       df_edi_bond_price = df_edi_bond_price.rename(columns={'cusip_company_part_edi': 'cusip_company_part'})

       # Convert string into Datetime.Date
       edi_dates = ['mktclosedate', 'maturity_date']
       for date in edi_dates:
              df_edi_bond_price[date] = pd.to_datetime(df_edi_bond_price[date], errors='coerce').dt.date

       bond_cusip = df_edi_bond_price['cusip_company_part'].unique().tolist()

       # df_edi_test = df_edi_bond_price[edi_cols].sort_values(by=['cusip_company_part', 'mktclosedate'])
       # df_edi_test_1 = df_edi_test.loc[df_edi_test['cusip_company_part'] == '95709T']

       core_bond_df = core_df_test.loc[core_df_test['cusip_company_part'].isin(bond_cusip)].sort_values(by=['cusip_company_part', 'date_fundamentals'])
       # core_bond_df_1 = core_df_test.loc[core_df_test['cusip_company_part'] == '95709T']

       # Issuer Cusips avilable in EDI Bond Price table
       comp_cusips = core_bond_df['cusip_company_part'].unique().tolist()

       # Bond price Dataframe from EDI bond price only for the Cusip available in Core US Fundamental
       edi_cusip_df = df_edi_bond_price.loc[df_edi_bond_price['cusip_company_part'].isin(comp_cusips)]

       # df_merge = combine_core_edi(core_bond_df, edi_cusip_df)

       comp_cusips = comp_cusips[0:5]

       chunk_size = 10
       chunks = [comp_cusips[x: x + chunk_size] for x in range(0, len(comp_cusips), chunk_size)]

       tasks = []
       final_core_df = []

       for chunk in chunks:
              print(chunk)
              chunk_core_df = core_bond_df.loc[core_bond_df['cusip_company_part'].isin(chunk)]
              chunk_edi_df = edi_cusip_df.loc[edi_cusip_df['cusip_company_part'].isin(chunk)]

              tasks.append(asyncio.create_task(combine_core_edi(chunk_core_df,chunk_edi_df)))
              # tasks.append(asyncio.ensure_future(get_macd(ticker)))

       await asyncio.gather(*tasks)


       for task in tasks:
              if len(task.result()) == 0:
                     continue
              final_core_df.append(task.result())

       return final_core_df

if __name__ == '__main__':

       start_time = time.time()
       res = asyncio.run(main())

       df = res[0]

       end_time = time.time()
       print("--- %s seconds ---" % (end_time - start_time))
