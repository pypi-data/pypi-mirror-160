''' get cookies
javascript:(function(){prompt(document.domain,document.cookie)})();
'''

from bs4 import BeautifulSoup as bs
import random, hashlib, requests, json, time

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
bbs_ys_url = 'https://bbs.mihoyo.com/ys/'

header = {
	'origin': bbs_ys_url,
	'referer': bbs_ys_url,
	'user-agent': ua
}
mhyVersion = '2.11.1'

mid = '252335886'
uid = '150471589'
ck = 'UM_distinctid=17e2921aec10-0ea82985a49946-36657407-1ea000-17e2921aec25a7; _ga=GA1.2.2047390022.1641367581; _MHYUUID=5b230b66-ccb5-491a-8df4-6d572fec519d; _gid=GA1.2.2022069798.1651296521; CNZZDATA1275023096=1526022781-1641359564-https%253A%252F%252Fwww.baidu.com%252F%7C1651373529; ltoken=9g98CgEJyZbFpeq9w4MH6mX6pVKuUadpEqxVriOD; ltuid=252335886; cookie_token=YkHjsucAexunqmsoZTqkikGmz74V7Hhrpy02ExeF; account_id=252335886'

def random_hex(length):
    result = hex(random.randint(0, 16 ** length)).replace('0x', '').upper()
    if len(result) < length:
        result = '0' * (length - len(result)) + result
    return result

def md5(text):
    md5_func = hashlib.md5()
    md5_func.update(text.encode())
    return md5_func.hexdigest()

def get_ds_token(q='', b=None):
    if b:
        br = json.dumps(b)
    else:
        br = ''
    s = 'xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs'
    t = str(int(time.time()))
    r = str(random.randint(100000, 200000))
    c = md5('salt=' + s + '&t=' + t + '&r=' + r + '&b=' + br + '&q=' + q)
    return t + ',' + r + ',' + c


def get_info(uid, ck, server_id='cn_gf01'):
    if uid[0] == '5':
        server_id = 'cn_qd01'
    try:
        req = requests.get(
            url='https://api-takumi.mihoyo.com/game_record/app/genshin/api/index',
            headers={
                'DS'               : get_ds_token('role_id=' + uid + '&server=' + server_id),
                'x-rpc-app_version': mhyVersion,
                'User-Agent'       : 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 ('
                                     'KHTML, like Gecko) miHoYoBBS/2.11.1',
                'x-rpc-client_type': '5',
                'Referer'          : 'https://webstatic.mihoyo.com/',
                'Cookie'           : ck},
            params={
                'role_id': uid,
                'server' : server_id
            }
        )
        data = json.loads(req.text)
        return data
    except requests.exceptions.SSLError:
        try:
            req = requests.get(
                url='https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/index',
                headers={
                    'DS'               : get_ds_token('role_id=' + uid + '&server=' + server_id),
                    'x-rpc-app_version': mhyVersion,
                    'User-Agent'       : 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
                                         '(KHTML, like Gecko) miHoYoBBS/2.11.1',
                    'x-rpc-client_type': '5',
                    'Referer'          : 'https://webstatic.mihoyo.com/',
                    'Cookie'           : ck},
                params={
                    'role_id': uid,
                    'server' : server_id
                }
            )
            data = json.loads(req.text)
            return data
        except json.decoder.JSONDecodeError:
            logger.info('米游社基础信息读取新Api失败！')


klee = '10000029'
def get_character(uid, character_ids, ck, server_id='cn_gf01'):
    if uid[0] == '5':
        server_id = 'cn_qd01'
    try:
        req = requests.post(
            url='https://api-takumi.mihoyo.com/game_record/app/genshin/api/character',
            headers={
                'DS'               : get_ds_token('', {'character_ids': character_ids, 'role_id': uid,
                                                       'server'       : server_id}),
                'Origin'           : 'https://webstatic.mihoyo.com',
                'Cookie'           : ck,
                'x-rpc-app_version': mhyVersion,
                'User-Agent'       : 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                                     'like Gecko) miHoYoBBS/2.11.1',
                'x-rpc-client_type': '5',
                'Referer'          : 'https://webstatic.mihoyo.com/'
            },
            json={'character_ids': character_ids, 'role_id': uid, 'server': server_id}
        )
        data2 = json.loads(req.text)
        return data2
    except requests.exceptions.SSLError:
        try:
            req = requests.post(
                url='https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/character',
                headers={
                    'DS'               : get_ds_token('', {'character_ids': character_ids, 'role_id': uid,
                                                           'server'       : server_id}),
                    'Origin'           : 'https://webstatic.mihoyo.com',
                    'Cookie'           : ck,
                    'x-rpc-app_version': mhyVersion,
                    'User-Agent'       : 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 ('
                                         'KHTML, like Gecko) miHoYoBBS/2.11.1',
                    'x-rpc-client_type': '5',
                    'Referer'          : 'https://webstatic.mihoyo.com/'
                },
                json={'character_ids': character_ids, 'role_id': uid, 'server': server_id}
            )
            data = json.loads(req.text)
            return data
        except json.decoder.JSONDecodeError:
            logger.info('深渊信息读取新Api失败！')
    except Exception as e:
        logger.info('深渊信息读取老Api失败！')
        logger.info(e.with_traceback)


def get_calculate_info(client, uid, char_id, ck, name, server_id='cn_gf01'):
    if uid[0] == '5':
        server_id = 'cn_qd01'
    url = 'https://api-takumi.mihoyo.com/event/e20200928calculate/v1/sync/avatar/detail'
    req = client.get(
        url=url,
        headers={
            'DS'               : get_ds_token('uid={}&avatar_id={}&region={}'.format(uid, char_id, server_id)),
            'x-rpc-app_version': mhyVersion,
            'User-Agent'       : 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 ('
                                 'KHTML, like Gecko) miHoYoBBS/2.11.1',
            'x-rpc-client_type': '5',
            'Referer'          : 'https://webstatic.mihoyo.com/',
            'Cookie'           : ck},
        params={
            'avatar_id': char_id,
            'uid'      : uid,
            'region'   : server_id
        }
    )
    data = req.json()
    data.update({'name': name})
    return data

print(get_calculate_info(requests.Session(),uid,klee,ck,'name'))