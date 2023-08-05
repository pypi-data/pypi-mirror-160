import pandas as pd
from wencaipy.common.wcParameter import SQLITE_PATH_RR_PC 


def data_to_excel(data=None,file_name=None):
    try:
        data.to_excel(f"{SQLITE_PATH_RR_PC }/{file_name}.xlsx")
        print(f"Save data to excel <{file_name}.xlsx> finish !")
    except Exception as e:
        print(e)


def read_data_from_excel(file_name=None):
    try:
        return pd.read_excel(f"{SQLITE_PATH_RR_PC }/{file_name}.xlsx",index_col=0)
        print(f"Read data from excel <{file_name}.xlsx> finish !")
    except Exception as e:
        print(e)
        

if __name__ == "__main__":
    print(read_data_from_excel("trade_date_sse"))
    print(read_data_from_excel("stock_ma"))
    