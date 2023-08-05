from unittest import result
import requests
import efinance as ef
import json
import pandas as pd
from .common import *

class ZhangTing:
    code_=[]
    top_price_=[]
    bottom_price_=[]
    yester_Close_price_=[]
    open_price_=[]
    code_map_ = {}
    eastmoney_request_headers_ = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    url_ = 'http://hsmarketwg.eastmoney.com/api/SHSZQuoteSnapshot'
    def __init__(self):
        self.session_ = requests.Session()
        self.zhangting_df_ = None
        self.stock_dict_ = {}
        self.stock_dict_['code_'] = []
        self.stock_dict_['top_price_'] = []
        self.stock_dict_['bottom_price_'] = []
        self.stock_dict_['yester_close_price_'] = []
        self.stock_dict_['open_price_'] = []
    def DownloadOneStock(self, code):
        params = (
            ('id', str(code)),
            ('callback', 'jQuery183026310160411569883_1646052793441'),
        )
        json_response = self.session_.get(self.url_,
                        headers=self.eastmoney_request_headers_,
                        params=params)
        if json_response.status_code != 200:
            return
        json_str=json_response.text.split('(')[1].split(')')[0]
        #print(json_response.text)
        tick_dict=json.loads(json_str)
        if tick_dict['fivequote']['openPrice'] == '-':
            print('not start')
            print(tick_dict)
            return
        self.code_map_['code']=tick_dict
        self.stock_dict_['top_price_'].append(tick_dict['topprice'])
        self.stock_dict_['bottom_price_'].append(tick_dict['bottomprice'])
        self.stock_dict_['code_'].append(tick_dict['code'])
        self.stock_dict_['yester_close_price_'].append(tick_dict['fivequote']['yesClosePrice'])
        self.stock_dict_['open_price_'].append(tick_dict['fivequote']['openPrice'])
        ##assert(False)
        #if len(tick_dict['data']['data']) == 0:
        #    break
        #self.last_page_index_[code] = page_index
        #page_list.append(tick_dict)#[page_index]=tick_dict
    def DownloadAllData(self):
        stock_id_list=GetAllStockIdList()
        count = 0
        for stock_id in stock_id_list:
            self.DownloadOneStock(stock_id)
            count = count + 1
            print(count, "/", len(stock_id_list))
        df=pd.DataFrame(self.stock_dict_)
        df.to_excel('D:/stock/20220720_zhangting.xlsx', index=False, encoding='utf_8_sig')

    def Get(self, date, code):
        if self.zhangting_df_ is None:
            file='D:/stock/'+str(date)+'_zhangting.xlsx'
            zhangting_data = pd.read_excel(file)
            if zhangting_data is None:
                assert(False)
            self.zhangting_df_ = zhangting_data.set_index("code_", inplace=True)
        return zhangting_data.loc[int(code)]
        #print(zhangting_data.loc[int(code)]['top_price_'])
ZhangTing().Get(20220720, '000017')