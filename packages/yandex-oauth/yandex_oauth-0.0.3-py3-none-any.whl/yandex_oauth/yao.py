"""Модуль функций библиотеки"""

import requests, json, time, random, pickle
from . import __version__

def _safe_request(mode, url, headers=None, body=None, try_number=1):
	"""Функция безопасного запроса на timeout

	:param mode: метод запроса (get,post,patch,delete)
	:type mode: str
	:param url: адрес запроса
	:type url: str
	:param headers: заголовки запроса
	:type headers: dict
	:param body: тело запроса (если предусмотрено)
	:type body: dict
	:param try_number: номер попытки передачи запроса
	:type try_number: int
	:returns: json результат запроса
	"""
	try:
		if mode == 'post': response = requests.post(url, data=body, headers=headers).json()
		if mode == 'get': response = requests.get(url, headers=headers).json()
		if mode == 'patch': response = requests.patch(url, data=body, headers=headers).json()
		if mode == 'delete': response = requests.delete(url, headers=headers).json()

	except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
		time.sleep(2**try_number + random.random()*0.01)
		return _safe_request(mode, url, headers, body, try_number=try_number+1)

	else:
		return response


def get_token_by_code(code, client_id, client_secret):
    """Функция получения токена по коду авторизации

    :param code: код подтверждения
    :type code: str
    :param client_id: id приложения
    :type client_id: str
    :param client_secret: пароль приложения
    :type client_secret: str
    :returns: json токены
	"""

    url = 'https://oauth.yandex.ru/token'
    headers={'Host': 'oauth.yandex.ru', 'Content-type': 'application/x-www-form-urlencoded'}
    body = 'grant_type=authorization_code&code='+str(code)+'&client_id='+str(client_id)+'&client_secret='+str(client_secret)
	
    return _safe_request('post', url, headers, body)

def save_token(path, token):
    """Функция сохранения токенов в pickle хранилище
    
    :param path: путь для сохранения хранилища
    :type path: str
    :param token: словарь токенов
    :type config: dict
    :retunrs: True или False
    """
    try:
        with open(path+'/token.pickle','wb') as f:
            pickle.dump(token, f)
    except:
        return False
    
    return True

def load_token(path):
    """Функция загрузки токенов из хранилища
    
    :param path: путь к хранилищу
    :type path: str
    :returns: config или False, если нет хранилища
    """
    try:
        with open(path+'/token.pickle','rb') as f:
            token = pickle.load(f)
    except:
        return False
    else:
	    return token