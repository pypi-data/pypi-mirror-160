from wencaipy.stock import stock_prs

import streamlit as st

from wencaipy.common.dataToExcel import read_data_from_excel
from wencaipy.common.tradeDate import get_real_trade_date
from wencaipy.stock.stock_prs import stock_prs_oh_ol_volchg_inc_forecast_concept

def save_stock_prs_to_excel():
    #stock_prs.stock_prs_oh_ol_volchg_inc()
    #stock_prs.stock_prs_oh_ol_volchg_inc_concept()
    stock_prs_oh_ol_volchg_inc_forecast_concept()
    
def stock_streamlit():
    df = read_data_from_excel(f'stock_prs_oh_volchg_inc_forecast_concept_{get_real_trade_date()}')
    st.write(df)
    
if __name__ == "__main__":
    #save_stock_prs_to_excel()
    stock_streamlit()