#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import datetime
import hmac
import json
import urllib
import uuid
import random
import requests
from walnut.settings import aliyun_sms_app_key, aliyun_sms_app_secret, aliyun_sms_sign_name, aliyun_sms_template_code


def sms_code():
    return str(random.randint(100000, 999999))


def quote(text):
    return urllib.parse.quote(text, safe='~')


def stringify(**kwargs):
    pairs = []
    for k, v in sorted(kwargs.items()):
        pairs.append('{}={}'.format(k, v))
    return '&'.join(pairs)


def canonicalize(**kwargs):
    pairs = []
    for k, v in sorted(kwargs.items()):
        pair = '{}={}'.format(quote(k), quote(v))
        pairs.append(pair)
    return quote('&'.join(pairs))


def sign(text, secret):
    text = text.encode('utf-8')
    key = (secret + '&').encode('utf-8')
    digest = hmac.new(key, text, 'sha1').digest()
    signture = quote(base64.b64encode(digest))
    return signture


class AliSMS(object):
    _defaults = [
        ('action', 'SendSms'),
        ('format', 'JSON'),
        ('region_id', 'cn-hangzhou'),
        ('signature_method', 'HMAC-SHA1'),
        ('signature_version', '1.0'),
        ('sms_version', '2017-05-25'),
        ('domain', 'https://dysmsapi.aliyuncs.com'),
    ]

    def __init__(self, code, phone, app_key=aliyun_sms_app_key, app_secret=aliyun_sms_app_secret,
                 sign_name=aliyun_sms_sign_name,
                 template_code=aliyun_sms_template_code, **settings):
        for k, v in self._defaults:
            setattr(self, k, settings.get(k, v))

        self.app_key = app_key
        self.app_secret = app_secret
        self.sign_name = sign_name
        self.template_code = template_code
        self.template_params = {'code': code}
        self.phone = phone

    def send(self):
        body = self._create_body()
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        res = requests.post(self.domain, data=body, headers=headers)
        return res

    def _create_body(self):
        params = self._create_params()
        text = 'POST&%2F&' + canonicalize(**params)
        signture = sign(text, self.app_secret)
        body = 'Signature={}&{}'.format(signture, stringify(**params))
        return body.encode('utf-8')

    def _create_params(self):
        return {
            'AccessKeyId': self.app_key,
            'Action': self.action,
            'Format': self.format,
            'PhoneNumbers': self.phone,
            'RegionId': self.region_id,
            'SignName': self.sign_name,
            'SignatureMethod': self.signature_method,
            'SignatureNonce': str(uuid.uuid4()),
            'SignatureVersion': self.signature_version,
            'TemplateCode': self.template_code,
            'TemplateParam': json.dumps(self.template_params),
            'Timestamp': datetime.datetime.utcnow().isoformat("T"),
            'Version': self.sms_version,
        }


if __name__ == '__main__':
    sms = AliSMS(code=sms_code(), phone='18949896232')
    resp = sms.send()
    print(type(resp.status_code), resp.json())
