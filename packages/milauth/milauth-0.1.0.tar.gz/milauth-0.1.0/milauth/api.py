import hashlib
import hmac
import json
import time

import requests

from milauth.milaCoinsError import MilaCoinsError

urls = ["https://sandbox-api.milacoins.com", "https://api.milacoins.com"]


class Api:
    def __init__(self, baseUrl, apiKey, secretKey):
        self.baseUrl = baseUrl
        self.apiKey = apiKey
        self.secretKey = secretKey

        if self.baseUrl not in urls:
            raise Exception("baseUrl have to be one of:" + ' '.join(urls))
        if not self.apiKey:
            raise Exception("api key is required")
        if not self.secretKey:
            raise Exception("secret key is required")

    def request(self, endPoint,method='GET',query={},body={}):
        queryString = ''
        if query:
            queryList = []
            for key in query.keys():
                queryList.append(key+'='+str(query[key]))
            if len(queryList) > 0:
                queryString = '?' + '&'.join(queryList)
        now = int(time.time())
        _method = method.upper()
        path_url = endPoint + queryString  # includes encoded query params
        _body = ''
        if body:
            _body = json.dumps(body, separators=(',', ':'))
           
        data_to_sign = str(now).encode('utf-8') + _method.encode('utf-8') + path_url.encode('utf-8') + _body.encode('utf-8')
        # # hmac needs bytes
        signature = hmac.new(
            self.secretKey.encode('utf-8'),
            data_to_sign,
            digestmod=hashlib.sha256
        )

        headers = {'Content-Type': 'application/json',
                    'Content-Encoding': 'utf-8',
                    'Accept':'application/json',
                    'X-api-key':self.apiKey,
                    'X-time':str(now),
                    'X-Sig':signature.hexdigest()
                    }

        prepared_request = requests.Request(_method, self.baseUrl + path_url,data=body,headers=headers).prepare()
        s = requests.Session()
        response = s.send(prepared_request)
        res = response.json()
        if response.status_code > 399:
            raise MilaCoinsError(res['requestID'],res['name'],res['message'],res['code'])
        return res

        