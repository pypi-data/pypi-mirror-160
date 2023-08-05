from unittest import result
import requests
import efinance as ef
import json
import pandas as pd

class DownloadTick:
    last_page_index_={}
    page_list_={}
    code_map_stock_={}
    eastmoney_request_headers_ = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    url_ = 'http://push2ex.eastmoney.com/getStockFenShi'
    def __init__(self):
        self.session_ = requests.Session()
    def GetMarket(self, code):
        if int(code) >= 300000 and int(code) <= 399999: 
            market='0'
        elif int(code) < 100000: 
            market='0'
        else:
            market='1'
        return market
    def Download(self, code):
        if self.page_list_.get(code) is None:
            self.page_list_[code] = []
        page_list=self.page_list_[code]
        already_deal_page_index=len(page_list)
        #old_page_flag=json.dump(page_list)
        start_page_index=0
        if self.last_page_index_.get(code) is None:
            self.last_page_index_[code] = 0
            start_page_index=0
        else:
            start_page_index=self.last_page_index_[code]
        for page_index in range(start_page_index, 161):
            params = (
                ('pagesize', '161'),
                ('ut', '7eea3edcaed734bea9cbfc24409ed989'),
                ('dpt', 'wzfscj'),
                ('cb', 'jQuery1123006424997167590785_1580710971173'),
                ('pageindex', str(page_index)),
                ('id', str(code)),
                ('sort', '1'),
                ('ft', '1'),
                ('code', str(code)),
                ('market', self.GetMarket(code)),
                ('_', '1580710971260')
            )
            json_response = self.session_.get(self.url_,
                            headers=self.eastmoney_request_headers_,
                            params=params)
            if json_response.status_code != 200:
                break
            json_str=json_response.text.split('(')[1].split(')')[0]
            tick_dict=json.loads(json_str)
            #print(tick_dict)
            #assert(False)
            if len(tick_dict['data']['data']) == 0:
                break
            self.last_page_index_[code] = page_index
            page_list.append(tick_dict)#[page_index]=tick_dict
        if len(page_list) == 0:
            return
        #if old_page_flag == json.dump(page_list):
        #    return
        return self.DealDownload(code)

    def DealDownload(self, code):
        if self.code_map_stock_.get(code) is None:
            self.code_map_stock_[code]={'type':[],'time':[],'price':[]}
        stock_data=self.code_map_stock_[code]
        page_list=self.page_list_[code]
        if len(page_list) == 0:
            return
        for one_page in page_list:
            #print(one_page)
            one_pagedata=one_page['data']
            for one_page_item in one_pagedata['data']:
                if int(one_page_item['bs']) == 2: 
                    stock_data['type'].append('买盘')
                elif int(one_page_item['bs']) == 1: 
                    stock_data['type'].append('卖盘')
                elif int(one_page_item['bs']) == 4: 
                    stock_data['type'].append('盘前')
                #else:
                #    assert(False, stock_data['type'])
                stock_data['time'].append(one_page_item['t'])
                price = float(one_page_item['p']/1000)
                stock_data['price'].append(str(price))
        #print(self.page_list_[code])

    def GetTickData(self, code):
        self.code_map_stock_[code]={'type':[],'time':[],'price':[]}
        self.Download(code)
        return self.code_map_stock_.get(code)

#def Test():
#    dowanload_tool = DownloadTick()
#    dowanload_tool.Download('603629')

#http://push2ex.eastmoney.com/getStockFenShi?pagesize=143&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj&cb=jQuery1123006424997167590785_1580710971173&pageindex='+str(pageindex)+'&id='+str(code)+'&sort=1&ft=1&code='+str(code)+'&market='+str(market)+'&_=1580710971260
#import requests
#import json
#import pandas as pd
#session = requests.Session()
##columns = { **EASTMONEY_QUOTE_FIELDS, **kwargs.get(MagicConfig.EXTRA_FIELDS, {}) }
#columns = {}
#fields = ",".join(columns.keys())
##params=()
##url = 'http://push2ex.eastmoney.com/getStockFenShi?pagesize=144&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj&cb=jQuery1123006424997167590785_1580710971173&pageindex=2&id=603629&sort=1&ft=1&code=603629&market=1&&_=1580863887639'
#url = 'http://push2ex.eastmoney.com/getStockFenShi'
#EASTMONEY_REQUEST_HEADERS = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
#    'Accept': '*/*',
#    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#    # 'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
#}
##pagesize=144&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj&cb=jQuery1123006424997167590785_1580710971173&pageindex=12&id=603629&sort=1&ft=1&code=603629&market=1&&_=1580863887639
#json_response = session.get(url,
#                            headers=EASTMONEY_REQUEST_HEADERS,
#                            params=params)
#jsonstr=json_response.text.split('(')[1].split(')')[0]
#print(json.loads(jsonstr), type(json.loads(jsonstr)))
#for k in json_response:
#    print(k, json_response.get(k))
#df = pd.DataFrame(json_response['data']['diff'])
#df = df.rename(columns=columns)
#df: pd.DataFrame = df[columns.values()]
#df['行情ID'] = df['市场编号'].astype(str)+'.'+df['代码'].astype(str)
#df['市场类型'] = df['市场编号'].astype(str).apply(
#    lambda x: MARKET_NUMBER_DICT.get(x))
#df['更新时间'] = df['更新时间戳'].apply(lambda x: str(datetime.fromtimestamp(x)))
#df['最新交易日'] = pd.to_datetime(df['最新交易日'], format='%Y%m%d').astype(str)
#tmp = df['最新交易日']
#del df['最新交易日']
#df['最新交易日'] = tmp
#del df['更新时间戳']
#return 
