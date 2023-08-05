import re
import datetime
import sys
import os
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import mpl_finance as mpf
from matplotlib.ticker import Formatter
import numpy as np
import json
sys.path.append("..")
sys.path.append("../..")

class DrawTick:
    time_map_x_=None
    def __init__(self):
        self.time_map_x_= {\
915:0, 916:1, 917:2, 918:3, 919:4, 920:5, 921:6, 922:7, 923:8, 924:9, 925:10, 930:10,
931:11, 932:12, 933:13, 934:14, 935:15, 936:16, 937:17, 938:18, 939:19, 940:20,
941:21, 942:22, 943:23, 944:24, 945:25, 946:26, 947:27, 948:28, 949:29, 950:30,
951:31, 952:32, 953:33, 954:34, 955:35, 956:36, 957:37, 958:38, 959:39, 1000:40,
1001:41, 1002:42, 1003:43, 1004:44, 1005:45, 1006:46, 1007:47, 1008:48, 1009:49, 1010:50,
1011:51, 1012:52, 1013:53, 1014:54, 1015:55, 1016:56, 1017:57, 1018:58, 1019:59, 1020:60,
1021:61, 1022:62, 1023:63, 1024:64, 1025:65, 1026:66, 1027:67, 1028:68, 1029:69, 1030:70,
1031:71, 1032:72, 1033:73, 1034:74, 1035:75, 1036:76, 1037:77, 1038:78, 1039:79, 1040:80,
1041:81, 1042:82, 1043:83, 1044:84, 1045:85, 1046:86, 1047:87, 1048:88, 1049:89, 1050:90,
1051:91, 1052:92, 1053:93, 1054:94, 1055:95, 1056:96, 1057:97, 1058:98, 1059:99, 1100:100,
1101:101, 1102:102, 1103:103, 1104:104, 1105:105, 1106:106, 1107:107, 1108:108, 1109:109, 1110:110,
1111:111, 1112:112, 1113:113, 1114:114, 1115:115, 1116:116, 1117:117, 1118:118, 1119:119, 1120:120,
1121:121, 1122:122, 1123:123, 1124:124, 1125:125, 1126:126, 1127:127, 1128:128, 1129:129, 1300:130,
1301:131, 1302:132, 1303:133, 1304:134, 1305:135, 1306:136, 1307:137, 1308:138, 1309:139, 1310:140,
1311:141, 1312:142, 1313:143, 1314:144, 1315:145, 1316:146, 1317:147, 1318:148, 1319:149, 1320:150,
1321:151, 1322:152, 1323:153, 1324:154, 1325:155, 1326:156, 1327:157, 1328:158, 1329:159, 1330:160,
1331:161, 1332:162, 1333:163, 1334:164, 1335:165, 1336:166, 1337:167, 1338:168, 1339:169, 1340:170,
1341:171, 1342:172, 1343:173, 1344:174, 1345:175, 1346:176, 1347:177, 1348:178, 1349:179, 1350:180,
1351:181, 1352:182, 1353:183, 1354:184, 1355:185, 1356:186, 1357:187, 1358:188, 1359:189, 1400:190,
1401:191, 1402:192, 1403:193, 1404:194, 1405:195, 1406:196, 1407:197, 1408:198, 1409:199, 1410:200,
1411:201, 1412:202, 1413:203, 1414:204, 1415:205, 1416:206, 1417:207, 1418:208, 1419:209, 1420:210,
1421:211, 1422:212, 1423:213, 1424:214, 1425:215, 1426:216, 1427:217, 1428:218, 1429:219, 1430:220,
1431:221, 1432:222, 1433:223, 1434:224, 1435:225, 1436:226, 1437:227, 1438:228, 1439:229, 1440:230,
1441:231, 1442:232, 1443:233, 1444:234, 1445:235, 1446:236, 1447:237, 1448:238, 1449:239, 1450:240,
1451:241, 1452:242, 1453:243, 1454:244, 1455:245, 1456:246, 1457:247, 1500:248}
        self.xticks_times_=[0,10,20,30,40, 50,60,70,80,90, 100,110,120,130,140, 150,160,170,180,190, 200,210,220,230,240, 248]
        self.xticks_time_names_=[ '09:15', '09:30','09:40', '09:50', '10:00', '10:10','10:20', '10:30','10:40', '10:50', '11:00','11:10', '11:20', '13:00', '13:10', '13:20', '13:30','13:40', '13:50', '14:00', '14:10','14:20', '14:30','14:40', '14:50', '15:00' ]
        self.yticks_price_names_=['-10%','-9%','-8%','-7%','-6%','-5%','-4%','-3%','-2%','-1%','0','1%','2%','3%','4%','5%','6%','7%','8%','9%','10%']

    def LoadDataFromJson(self, path):
        path='tick_data'
        file=open(path,'r')
        jsondict=json.load(file)
        pricelist=jsondict.get('price')#价格
        amountlist=jsondict.get('amount')#金额
        timelist=jsondict.get('time')#时间
        print(type(timelist[0]))
        for index in range(0, len(pricelist)):
            #timelist[index]=float(timelist[index])
            pricelist[index]=float(pricelist[index])
            amountlist[index]=float(amountlist[index])
        self.pain_df_=pd.DataFrame(jsondict)
        self.draw('600848', '2022-05-11')

    #time->09:30:49 
    def ConvertTimeToX(self, time_str):
        time_list=time_str.split(":")
        time_int=int(time_list[0])*10000+int(time_list[1])*100+int(time_list[2])
        print("time_int:", time_int)
        return self.time_map_x_[time_int]

    def Set(self, code, trade_date, open_price, zhangting_price):
        self.code_=code
        self.trade_date_=trade_date
        self.y_limit_high_=zhangting_pric
        self.y_zero_price_ = open_price
        self.y_limit_low_=zhangting_price*0.8
        for i in range(0, len(self.yticks_price_names_)):
            weight=float(i-10)/100
            self.yticks_price_.append(open_price*(1+weight))
        self.yticks_price_names_=['-10%','-9%','-8%','-7%','-6%','-5%','-4%','-3%','-2%','-1%','0','1%','2%','3%','4%','5%','6%','7%','8%','9%','10%']

    def GenerateBigMoney(self):

    def DrawPoint(self, image, time_str, price, money):
        x=ConvertTimeToX(time_str)
        y=float(price)
        image.scatter(x, y, s=100)
        image.annotate(money, xy=(x, y), fontsize=20, xycoords="data")

    def draw(self, code, tradedate):
        self.pain_df_['time']=pd.to_datetime(self.pain_df_['time'], format="%H%M%S")
        #self.pain_df_['time']=tradedate + ' '+self.pain_df_['time']
        self.pain_df_ = self.pain_df_.set_index('time')

        price_df=self.pain_df_['price'].resample('1min').ohlc().dropna()

        amounts=self.pain_df_['amount'].resample('1min').sum().dropna()
        amount_df=pd.DataFrame(amounts, columns=['amount'])

        resample_df=price_df.merge(amount_df, left_index=True, right_index=True)
        resample_df=resample_df.reset_index()
        #resample_df.to_csv('./TickImg/'+str(code)+'.'+tradedate+'.min.csv')

        #matplotlib的date2num将日期转换为浮点数，整数部分区分日期，小数区分小时和分钟
        #因为小数太小了，需要将小时和分钟变成整数，需要乘以24（小时）×60（分钟）=1440，这样小时和分钟也能成为整数
        #这样就可以一分钟就占一个位置

        resample_df['time']=resample_df['time'].apply(lambda x:dates.date2num(x)*1440)
        #print(resample_df['time'])
        resample_df['MA5']=resample_df['close'].rolling(window=1).mean()

        plt.figure(figsize=(20,20))
        a1=plt.subplot(2,1,1)
        a1.grid(color='gray',linestyle='-')
        a1.plot( resample_df['close'].tolist(), c='r')
        a1.plot( resample_df['MA5'].tolist(), c='y')
        a1.set_ylim(self.y_limit_low_, self.y_limit_high_)
        plt.xticks(self.xticks_times_, self.xticks_time_names_, size=15, rotation=40)
        plt.yticks(self.yticks_price_, self.yticks_price_names_, size=15, rotation=40)

        plt.title(str(code)+"."+str(tradedate))
        plt.savefig('./TickImg/'+str(code)+'.'+tradedate+'.png')

draw=DrawTick()
draw.LoadDataFromJson('a')
