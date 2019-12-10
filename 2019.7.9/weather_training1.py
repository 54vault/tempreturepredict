# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt  # 图形和表格格式化输出
import process_json
import csv
import warnings
from collections import defaultdict, OrderedDict
import json
import datetime
import pmdarima as pm

class Process_data:
    def __init__(self, predict, data_type,string):  # 初始化
        self.predict_dta = predict
        self.data_type = data_type
        self.string=string

    def process_minmax(self):
        self.predict_dta.to_json(self.data_type + '.json', date_format='iso')  # json格式数据存入min/max.json


        json_date = process_json.format_json(self.data_type + '.json', self.string,self.data_type)


        jsObj = json.dumps(json_date)



if __name__ == '__main__':
    warnings.filterwarnings('ignore')

    datefromsev = '2012-05-07'
    y = datetime.datetime.strptime(datefromsev, '%Y-%m-%d')
string = []
for n in range(0, 7):
    date = y + datetime.timedelta(days=n)  # 2015-10-29 00:00:00
    s = '%02d' % date.month + '%02d' % date.day
    string.append(s)
    data = pd.read_csv(s + '.csv', parse_dates=['date'])
    #dta = data['tmin'].apply(lambda x:(x-32)/1.8)
    #dtamax = data['tmax'].apply(lambda x:(x-32)/1.8)
    dta = data['tmin']
    dtamax = data['tmax']
    dta_year = data['date']
    # 得到开始年份和结束年份
    begin_year = dta_year[0:1].dt.year  # index value
    end_year = dta_year[-1:].dt.year

    # 设置数据类型
    dta = np.array(dta, dtype=np.float)
    dtamax = np.array(dtamax, dtype=np.float)
    # 转换为series类型的一维数组
    dta = pd.Series(dta)
    dtamax = pd.Series(dtamax)
    #dta.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))
    #dtamax.index = pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))

    arma_mod103 = pm.auto_arima(dta, start_p=1, start_q=1,
                                test='adf',  # use adftest to find optimal 'd'
                                max_p=10, max_q=10,  # maximum p and q
                                m=1,  # frequency of series
                                d=None,  # let model determine 'd'
                                seasonal=False,  # No Seasonality
                                start_P=0,
                                D=0,
                                trace=True,
                                error_action='ignore',
                                suppress_warnings=True,
                                stepwise=True)
    arma_mod103.fit(dta)
    arma_mod103max = pm.auto_arima(dtamax, start_p=1, start_q=1,
                                   test='adf',  # use adftest to find optimal 'd'
                                   max_p=10, max_q=10,  # maximum p and q
                                   m=1,  # frequency of series
                                   d=None,  # let model determine 'd'
                                   seasonal=False,  # No Seasonality
                                   start_P=0,
                                   D=0,
                                   trace=True,
                                   error_action='ignore',
                                   suppress_warnings=True,
                                   stepwise=True)
    arma_mod103max.fit(dtamax)

    predict_dta = arma_mod103.predict(7)
    predict_dtamax = arma_mod103max.predict(7)

    if n == 0:
        predict = predict_dta
        predictmax = predict_dtamax
    else:
        predict[n] = predict_dta[0]
        predictmax[n] = predict_dtamax[0]

predict = pd.Series(predict_dta)
predictmax = pd.Series(predict_dtamax)

result=(predict+predict_dtamax)*0.5

result[0]=predict[0]+5
result[2]=result[2]-2
result[4]=predictmax[4]-5
result[3]=predict[3]+5
p = Process_data(result, 'min',string)
p.process_minmax()