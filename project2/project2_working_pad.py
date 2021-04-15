import numpy as np
import pandas as pd
from pathlib import Path
import datetime
import time

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

ROOT_PATH = Path("../stock_data/project2/data")

core_cols = ['date_fundamentals', 'cusip_company_part_fundamentals', 'assets', 'marketcap', 'payables']
edi_cols = ['cusip_company_part', 'isin', 'uscode', 'close_edi', 'coupon', 'maturity_date', 'mktclosedate',]


def getCusip(isin):
    if isin == "":
        return isin
    cusip = isin[2:len(isin) - 1]
    return cusip

def find_cusip_in_core(core_df, edi_bond_df):
    core_cusips = core_df['cusip_company_part'].unique().tolist()
    edi_bond_cusips = edi_bond_df['cusip_company_part'].unique().tolist()
    common_cusips = list(set(core_cusips) & set(edi_bond_cusips))

    print(common_cusips)
    edi_common_bond_df = None
    if common_cusips:
        edi_common_bond_df = edi_bond_df.loc[edi_bond_df['cusip_company_part'].isin(common_cusips)]

    return edi_common_bond_df

if __name__ == '__main__':

    data_files = ['edi_bond_price_NT_2.csv', 'edi_bond_price_NT_3.csv', 'edi_bond_price_NT_4.csv', 'edi_bond_price_DB.csv', 'edi_bond_price_MTN.csv', 'edi_bond_price_reduced.csv']
    dfs = []

    # Load Core US Fundamental table
    # core_us_file = 'core_us_fundamentals.csv'
    # core_path = Path.joinpath(ROOT_PATH, core_us_file)
    # core_df = pd.read_csv(core_path, usecols=core_cols, infer_datetime_format=True, parse_dates=True, )
    # core_df['date_fundamentals'] = pd.to_datetime(core_df['date_fundamentals']).dt.date
    # core_test_df = core_df[core_cols].copy()
    # core_test_df = core_test_df.rename(columns={'cusip_company_part_fundamentals': 'cusip_company_part'})

    final_edi_bonds_df = []
    for file in data_files:
        file_path = Path.joinpath(ROOT_PATH, file)
        print(file_path)
        # Load the edi bond files
        edi_bond_df = pd.read_csv(file_path, infer_datetime_format=True, parse_dates=True,)
        edi_bond_df = edi_bond_df.rename(columns={'cusip_company_part_edi': 'cusip_company_part'})
        edi_bond_df = edi_bond_df[edi_cols]
        # edi_bond_df['cusip_number'] = edi_bond_df.apply(lambda x: getCusip(x['isin']), axis=1)

        # Convert string into Datetime.Date
        edi_dates = ['mktclosedate', 'maturity_date']
        for date in edi_dates:
            edi_bond_df[date] = pd.to_datetime(edi_bond_df[date], errors='coerce').dt.date

        dfs.append(edi_bond_df)

        # df = find_cusip_in_core(core_test_df, edi_bond_df)
        # dfs.append(df)

    final_edi_bonds_df = pd.concat(dfs)
    # core_us_df = pd.concat(dfs)
    # core_us_df.to_csv("C:\stock_data\project2\data\\all_cusips_core_rating_df.csv", index=False)
    print('Done')
