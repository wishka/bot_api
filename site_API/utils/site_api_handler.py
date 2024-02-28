from typing import Dict

import requests


def _make_response(method: str, url: str, headers: Dict, params: Dict, timeout: int, success=200):
    response = requests.request(
        method,
        url,
        headers=headers,
        params=params,
        timeout=timeout,
    )
    status_code = response.status_code
    
    if status_code == success:
        return response
    return status_code


def _get_forecast_weather(method: str, url: str, headers: Dict, params: Dict, timeout: int, func=_make_response):
    url = "{0}/forecast.json".format(url)
    response = func(method, url, headers=headers, params=params, timeout=timeout)
    return response
    

def _get_word(method: str, url: str, headers: Dict, word: str, timeout: int, func=_make_response):
    url = "{0}/words/%7B{1}%7D".format(url, word)
    response = func(method, url, headers=headers, timeout=timeout)
    return response


def _get_definitions(method: str, url: str, headers: Dict, definition: str, timeout: int, func=_make_response):
    url = "{0}/words/{1}/definitions".format(url, definition)
    response = func(method, url, headers=headers, timeout=timeout)
    return response


class SiteApiInterface:
    @staticmethod
    def get_forecast_weather(method: str, url: str, headers: Dict, params: Dict, timeout: int, func=_make_response):
        url = "{0}/forecast.json".format(url)
        response = func(method, url, headers=headers, params=params, timeout=timeout)
        return response
    
    @staticmethod
    def get_word():
        return _get_word
    
    @staticmethod
    def get_definitions():
        return _get_definitions


if __name__ == "__main__":
    _make_response()
    _get_forecast_weather()
    _get_word()
    _get_definitions()
    SiteApiInterface()