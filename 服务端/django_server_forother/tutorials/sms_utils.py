import requests
import time

import redis

from tutorials.config import REDIS_HOST, REDIS_PORT, REDIS_DB_NUM, REDIS_PASSWORD, \
    XUE_OPENAPI_BASE_URL, XUE_OPENAPI_API_KEY, XUE_OPENAPI_SECRET_KEY
from tutorials.handle_log import HandleLog


logger = HandleLog()


def get_token():
    """
    获取xue平台 Access Token
    :return: access_token字符串 / None
    :rtype: str
    """
    try:
        pool = redis.ConnectionPool(
            host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB_NUM, decode_responses=True)
        redis_conn = redis.Redis(connection_pool=pool)
        key_name = 'xue_openapi:access_token'

        if redis_conn.exists(key_name):
            return redis_conn.get(key_name)

        # 请求新token
        url = XUE_OPENAPI_BASE_URL + 'access-token/'
        body = {
            'api_key': XUE_OPENAPI_API_KEY,
            'secret_key': XUE_OPENAPI_SECRET_KEY
        }
        res = requests.post(url=url, json=body)
        res_data = res.json()

        if res.status_code != 200 or res_data['errcode'] != 0:
            logger.error_log(res_data)
            return None
        access_token = res_data['data']['access_token']
        expired_time = time.strptime(res_data['data']['expiration_time'], '%Y-%m-%d %H:%M:%S')
        ttl = int(time.mktime(expired_time)) - int(time.time())
    except Exception as e:
        logger.exception_log('get_token', e)
        return None

    redis_conn.set(key_name, access_token, ex=ttl)
    return access_token


def send_sms(mobile_number):
    """
    调用接口发送短信验证码
    :param mobile_number: 手机号
    :rtype: bool
    :return:
        True / False
    """
    token = get_token()
    if token is None:
        return False, None

    url = XUE_OPENAPI_BASE_URL + 'sms/'
    body = {'mobile_number': mobile_number}
    headers = {'Authorization': 'bearer {}'.format(token)}
    res = requests.post(url=url, json=body, headers=headers)
    res_data = res.json()

    try:
        if res.status_code == 200 and res_data['errcode'] == 0:
            return True, res_data['data']

        logger.error_log(res_data)
        return False, res_data['errmsg']
    except Exception as e:
        logger.exception_log('send_sms', e)
        return False, None
