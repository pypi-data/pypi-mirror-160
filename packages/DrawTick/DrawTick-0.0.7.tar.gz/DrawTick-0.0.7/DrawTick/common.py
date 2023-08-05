import tushare as ts
def GetAllStockIdList():
    #import kdata
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    basic_datas = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    codes = basic_datas['symbol'].values.tolist()
    return codes