# -*- coding:utf-8 -*-
from rainiee_engine.base import client, login, upass
import pandas as pd

def auth(username=None, password=None):
    upass.set_token(login.LoginApi(username, password).login())

def get_client():
    return client.DataApi(upass.get_token())

def execute_bt_sha_strat(start_index, end_index, instance_name,buying_strategy_name,selling_strategy_name,type):
    return get_client().query(api_name='execute_bt_sha_strat',method_type='POST', req_param={
        'start_index': start_index,
        'end_index': end_index,
        'instance_name': instance_name,
        'buying_strategy_name': buying_strategy_name,
        'selling_strategy_name': selling_strategy_name,
        'type':type
    })


def get_bt_benchmark_result(start_index, end_index, index_code):
    response_dict = get_client().query(api_name='get_bt_benchmark_result',method_type='POST', req_param={
        'start_index': start_index,
        'end_index': end_index,
        'index_code': index_code
    })
    result = {}
    for code in index_code.split(','):
        result[code] = pd.DataFrame(response_dict[code])

    return result

def get_bt_sha_result_ind(top, order_by,type=None,instance_bs_id=None):
    return pd.DataFrame(get_client().query(api_name='get_bt_sha_result_ind',method_type='POST', req_param={
        'instance_bs_id': instance_bs_id,
        'top': top,
        'order_by': order_by,
        'type': type
    }))

def get_bt_sha_result_perform(instance_bs_id,type):
    return get_client().query(api_name='get_bt_sha_result_perform',method_type='POST', req_param={
        'instance_bs_id': instance_bs_id,
        'type': type
    })

def get_bt_sha_result(instance_bs_id,type,start_index=None, end_index=None):
    return pd.DataFrame(get_client().query(api_name='get_bt_sha_result',method_type='POST', req_param={
        'instance_bs_id': instance_bs_id,
        'start_index': start_index,
        'end_index': end_index,
        'type': type
    }))

def train_sha_strat_model(tr_idx,strategy_name):
    return get_client().query(api_name='train_sha_strat_model',method_type='POST', req_param={
        'tr_idx': tr_idx,
        'strategy_name': strategy_name
    })

def batch_train_sha_strat_model(start_index,end_index,strategy_name):
    return get_client().query(api_name='batch_train_sha_strat_model',method_type='POST', req_param={
        'start_index': start_index,
        'end_index': end_index,
        'strategy_name': strategy_name
    })
def evaluate_sha_strat_model(testing_index,strategy_name):
    return get_client().query(api_name='evaluate_sha_strat_model',method_type='POST', req_param={
        'testing_index': testing_index,
        'strategy_name': strategy_name
    })
def simulate_sha_strat_signal(buy_index,strategy_name):
    return get_client().query(api_name='simulate_sha_strat_signal',method_type='POST', req_param={
        'buy_index': buy_index,
        'strategy_name': strategy_name
    })

def get_sha_strat_instance():
    return pd.DataFrame(get_client().query(api_name='get_sha_strat_instance',method_type='POST', req_param={}))

def get_sha_exp_strat_instance():
    return pd.DataFrame(get_client().query(api_name='get_sha_exp_strat_instance',method_type='POST', req_param={}))

def get_trading_instance():
    return pd.DataFrame(get_client().query(api_name='get_trading_instance',method_type='POST', req_param={}))

def get_strategy_instance():
    return pd.DataFrame(get_client().query(api_name='get_strategy_instance',method_type='POST', req_param={}))

def get_selling_instance():
    return pd.DataFrame(get_client().query(api_name='get_selling_instance',method_type='POST', req_param={}))

def get_funnel_instance():
    return pd.DataFrame(get_client().query(api_name='get_funnel_instance',method_type='POST', req_param={}))

def get_launch_instance():
    return pd.DataFrame(get_client().query(api_name='get_launch_instance',method_type='POST', req_param={}))

def get_sha_strat_seed():
    return get_client().query(api_name='get_sha_strat_seed',method_type='POST', req_param={})

def get_strat_dict():
    return pd.DataFrame(get_client().query(api_name='get_strat_dict',method_type='POST', req_param={}))


def get_pred_features(feat_idx,strategy_name):
    return pd.read_json(get_client().query(api_name='get_pred_features',method_type='POST', req_param={'feat_idx':feat_idx,'strategy_name':strategy_name}), orient='records')

def get_pred_base_features(feat_idx,strategy_name):
    return pd.read_json(get_client().query(api_name='get_pred_base_features',method_type='POST', req_param={'feat_idx':feat_idx,'strategy_name':strategy_name}), orient='records')

def get_pred_base_bcmkprice(feat_idx,strategy_name):
    return pd.read_json(get_client().query(api_name='get_pred_base_bcmkprice',method_type='POST', req_param={'feat_idx':feat_idx,'strategy_name':strategy_name}), orient='records')

def get_predict_result(feat_idx,strategy_name):
    return pd.read_json(get_client().query(api_name='get_predict_result',method_type='POST', req_param={'feat_idx':feat_idx,'strategy_name':strategy_name}), orient='records')

def get_training_data(tr_idx,strategy_name):
    return pd.read_json(get_client().query(api_name='get_training_data',method_type='POST', req_param={'tr_idx':tr_idx,'strategy_name':strategy_name}), orient='records')

def get_training_scaler(tr_idx,strategy_name):
    response_list = get_client().query(api_name='get_training_scaler',method_type='POST', req_param={'tr_idx':tr_idx,'strategy_name':strategy_name})
    return pd.read_json(response_list[0], orient='records'),pd.read_json(response_list[1], orient='records')


