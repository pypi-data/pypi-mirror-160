# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
*********************
Volos Python API
*********************
Documentation at: https://volosdataapi.docs.apiary.io/#
"""

__author__ = 'Saif Sultan'
__copyright__ = '2022 Volos Portfolio Solutions, Inc.. All rights reserved'
__version__ = '1.0'
__interpreter__ = 'Anaconda - Python 3.9.5 64 bit'
__maintainer__ = 'Francisco Pina'
__email__ = 'francisco.pina@volossoftware.com'
__status__ = 'In Progress'

import datetime
import io
import json
import os

import pandas as pd
import requests


class volosAPI(object):
    API_KEY = None
    API_STAGE = 'ci'
    API_ENDPOINT = 'https://api-data-ci-w1.volossoftware.com/'

    def __init__(self, api_key):
        self.API_KEY = api_key
        self.API_ENDPOINT = 'https://api-data-ci-w1.volossoftware.com/'

    def set_api_key(self, api_key):
        self.API_KEY = api_key

    def switch_stage_prod(self):
        self.API_STAGE = 'prod'

    def switch_stage_ci(self):
        self.API_STAGE = 'ci'

    def switch_stage_ir(self):
        self.API_STAGE = 'ir'

    def get_headers(self):
        if self.API_KEY is None:
            raise Exception("Please set API Key")
        return {'x-api-key': self.API_KEY}

    def get_url(self, uri, api_stage=None):
        if api_stage is None:
            return self.API_ENDPOINT + self.API_STAGE + uri
        else:
            return self.API_ENDPOINT + api_stage + uri

    def get_strategy_total_returns(self, strategy_id, output_format='csv', start_date='1990-01-01',
                                   end_date='2050-01-01'):
        uri = '/time-series/totalreturns'
        payload = {'strategy_id': strategy_id, 'output_format': output_format, 'start_date': start_date,
                   'end_date': end_date}

        res = requests.get(self.get_url(uri), params=payload, headers=self.get_headers())
        if output_format == 'json':
            return json.loads(res.content)
        elif output_format == 'csv':
            return pd.read_csv(io.StringIO(res.content.decode('utf-8')))
        else:
            raise NotImplementedError("Incorrect output format")

    def get_strategy_list_total_returns(self, strategy_id_list, start_date='1990-01-01', end_date='2050-01-01'):
        uri = '/time-series/total-returns-multi'
        payload = {'strategy_id_list': strategy_id_list, 'start_date': start_date, 'end_date': end_date}
        res = requests.post(self.get_url(uri), data=json.dumps(payload), headers=self.get_headers())
        return pd.read_csv(io.StringIO(res.content.decode('utf-8'))).rename(columns={'Unnamed: 0': 'date'})

    def get_custom_series(self, strategy_id, series_name, df_format='s3_file', start_date='1990-01-01',
                          end_date='2050-01-01'):
        if series_name not in ['EoD_Cash', 'EoD_Value', 'Draw_Down', 'Vol_30Day']:
            print("""Error: Please select one of custom series: 'EoD_Cash', 'EoD_Value', 'Draw_Down', 'Vol_30Day' """)
            return None
        else:
            uri = '/time-series/custom-time-series'
            payload = {'strategy_id': strategy_id, 'start_date': start_date,
                       'end_date': end_date, 'series_name': series_name, 'df_format': df_format}
            res = requests.post(self.get_url(uri), data=json.dumps(payload), headers=self.get_headers()).json()
            if list(res.keys())[0] == 'custom_series_csv_url':
                df = pd.read_csv(res['custom_series_csv_url'], index_col=[0])
            else:
                df = pd.json_normalize(res)
            return df

    def get_validation_data(self, strategy_id):
        uri = '/validation/get-validation-df'
        payload = {"strategy_id": strategy_id}
        res = requests.post(self.get_url(uri), data=json.dumps(payload), headers=self.get_headers()).json()

        if list(res.keys())[0] == 'validation_csv_url':
            df = pd.read_csv(res['validation_csv_url'])
        else:
            df = pd.json_normalize(res)
        return df

    def get_strategy_metrics(self, strategy_id, start_date='1990-01-01', end_date='2050-01-01'):
        uri = '/time-series/metrics'
        payload = {'strategy_id': strategy_id, 'start_date': start_date, 'end_date': end_date}
        res = requests.post(self.get_url(uri), data=json.dumps(payload), headers=self.get_headers())
        return pd.read_csv(io.StringIO(res.content.decode('utf-8'))).rename(columns={'Unnamed: 0': 'date'})

    def get_strategy_trade_logs(self, strategy_id, start_date='1990-01-01', end_date='2050-01-01'):
        uri = '/strategy/tradelogs'
        payload = {'strategy_id': strategy_id, 'start_date': start_date, 'end_date': end_date}
        res = requests.post(self.get_url(uri), data=json.dumps(payload), headers=self.get_headers())
        return pd.read_csv(json.loads(io.StringIO(res.content.decode('utf-8')).getvalue())['tradelogs_csv_url'],
                           index_col=[0])

    def get_strategy_positions(self, strategy_id, on_date, api_stage=None):
        uri = '/strategy/positions'
        payload = {'strategy_id': strategy_id, 'on_date': on_date}
        res = requests.post(self.get_url(uri, api_stage=api_stage), data=json.dumps(payload),
                            headers=self.get_headers())
        return pd.read_csv(
            json.loads(io.StringIO(res.content.decode('utf-8')).getvalue())['post_strategy_positions_csv_url'],
            index_col=[0])

    def get_strategy_list_meta_data(self, strategy_id_list):
        uri = '/strategy/meta-data'
        payload = {'strategy_id_list': strategy_id_list}
        res = requests.post(self.get_url(uri), data=json.dumps(payload), headers=self.get_headers())
        return json.loads(res.content.decode('utf-8'))

    def get_strategy_list_tags(self, strategy_id_list):
        uri = '/strategy/tags'
        payload = {'strategy_id_list': strategy_id_list}
        res = requests.post(self.get_url(uri), data=json.dumps(payload), headers=self.get_headers())
        return json.loads(res.content.decode('utf-8'))

    def search_by_ticker(self, ticker):
        uri = '/search/ticker'
        payload = {'ticker': ticker}
        res = requests.post(self.get_url(uri), data=json.dumps(payload), headers=self.get_headers())
        return pd.read_csv(io.StringIO(res.content.decode('utf-8')))

    def get_all_tags(self):
        uri = '/misc/all-tags'
        res = requests.get(self.get_url(uri), headers=self.get_headers())
        return json.loads(res.content)

    def get_timeseries_positions(self, strategy_id, start_date='1990-01-01', end_date='2050-01-01', api_stage=None):
        uri = '/time-series/positions'
        payload = {'strategy_id': strategy_id, 'start_date': start_date, 'end_date': end_date}
        res = requests.post(self.get_url(uri, api_stage=api_stage), data=json.dumps(payload),
                            headers=self.get_headers())
        return pd.read_csv(io.StringIO(res.content.decode('utf-8')), index_col=[0])

    def get_timeseries_positions_values(self, strategy_id, start_date='1990-01-01', end_date='2050-01-01',
                                        api_stage=None):
        uri = '/time-series/positions-values'
        payload = {'strategy_id': strategy_id, 'start_date': start_date, 'end_date': end_date}
        res = requests.post(self.get_url(uri, api_stage=api_stage), data=json.dumps(payload),
                            headers=self.get_headers())
        return pd.read_csv(io.StringIO(res.content.decode('utf-8')), index_col=[0])

    def get_strategy_positions_meta_data(self, strategy_id, api_stage=None):
        uri = '/strategy/positions/meta-data'
        payload = {'strategy_id': strategy_id}
        res = requests.post(self.get_url(uri, api_stage=api_stage), data=json.dumps(payload),
                            headers=self.get_headers())
        return pd.read_csv(io.StringIO(res.content.decode('utf-8')), index_col=[0])

    def save_positions_to_excel(self, strategy_id, path='.', api_stage=None):

        df_positions = self.get_timeseries_positions(strategy_id=strategy_id, api_stage=api_stage).pivot(index='date',
                                                                                                         columns='security_id',
                                                                                                         values='shares')
        df_values = self.get_timeseries_positions_values(strategy_id=strategy_id, api_stage=api_stage).pivot(
            index='date', columns='security_id', values='value')
        df_meta = self.get_strategy_positions_meta_data(strategy_id=strategy_id, api_stage=api_stage)

        sheet_name_list = ['holdings', 'values', 'meta_data']
        df_list = [df_positions, df_values, df_meta]

        timestamp = datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S-%f')
        fname = os.path.join(path, '{}-{}.xlsx'.format(strategy_id, timestamp))
        writer = pd.ExcelWriter(fname, engine='xlsxwriter')

        for sheet_name, df in zip(sheet_name_list, df_list):
            df.to_excel(writer, sheet_name=sheet_name)
        writer.save()
        print("saved to excel: {}".format(fname))

    def get_info_public_indexes(self):
        url = 'https://api-server-prod-e2.volossoftware.com/index/prod/index/all_index_data'
        headers = {"content-type": "json"}
        x = requests.post(url, headers=headers)
        index_df = pd.json_normalize(x.json())
        return index_df.loc[:, ['status', 'index_ticker', 'family_name', 'strategy_id',
                                'family_description', 'index_label', 'index_description',
                                'is_public', 'index_id', 'release_date']]


if __name__ == '__main__':
    vs = volosAPI(api_key="your_api_key")
    strategy_id = 'your_strategy_id'
    print('strategy returns', vs.get_strategy_total_returns(strategy_id))
    print('strategy list returns', vs.get_strategy_list_total_returns([strategy_id]))
    # 'EoD_Cash', 'EoD_Value', 'Draw_Down', 'Vol_30Day'
    print('custom series', vs.get_custom_series(strategy_id=strategy_id, series_name='Draw_Down'))
    print('validation data', vs.get_validation_data(strategy_id))
    print('strategy metrics', vs.get_strategy_metrics(strategy_id))
    print('trade_logs', vs.get_strategy_trade_logs(strategy_id))
    print('strategy positions', vs.get_strategy_positions(strategy_id, on_date='2022-01-03'))
    print('list meta data', vs.get_strategy_list_meta_data([strategy_id]))
    print('list tags', vs.get_strategy_list_tags(['strategy_id']))
    print('get all tags', vs.get_all_tags())
    print('get timeseries positions values', vs.get_timeseries_positions_values(strategy_id))
    print('get strategy positions metadata', vs.get_strategy_positions_meta_data(strategy_id))
    print('save positions to excel', vs.save_positions_to_excel(strategy_id))
    print('publicly available indexes',vs.get_info_public_indexes())
