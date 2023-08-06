# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
from .api import quantim

class risk_data(quantim):
    def __init__(self, username, password, secretpool, env="qa"):
        super().__init__(username, password, secretpool, env)

    def load_ports_alm_co(self, file_name, overwrite=False):
        '''
        Load portfolio file to s3.
        '''
        payload = pd.read_csv(file_name, sep=';', dtype={'FECHA_EMISION':str, 'FECHA_VENCIMIENTO':str, 'FECHA_COMPRA':str}).to_dict(orient='records')
        data = {'bucket':'condor-sura-alm', 'file_name':'portfolios/co/'+file_name.split('/')[-1], 'payload':payload, 'sep':';', 'overwrite':overwrite}
        try:
            resp = self.api_call('load_data_s3', method="post", data=data, verify=False)
        except:
            resp = {'success':False, 'message':'Check permissions!'}
        return resp

    def get_limits(self, port_name):
        '''
        Get limits table.
        '''

        data = {'port_name':port_name}
        resp = self.api_call('co_limits', method="post", data=data, verify=False)
        port_date, summ, detail = resp['port_date'], pd.DataFrame(resp['summ']), pd.DataFrame(resp['detail'])

        return port_date, summ, detail
