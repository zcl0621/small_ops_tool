# -*- coding=utf-8 -*-
from ldap3 import Server, Connection, LEVEL, ALL_ATTRIBUTES
from collections import Iterable
import re
from walnut.settings import ldap_user, ldap_password, ldap_host, ldap_search_base


class PublicLdap(object):
    """
        :argument
        host ldap的主机地址
        user ldap的管理员账户名 例如xxx
        password ldap的管理员密码
        find_username 需要查找的用户的用户名
        new_password 当需要修改密码时传入
        :return
        cn 查找用户的中文名
        telephoneNumber 查找用户的电话好吗
        mail 查找用户的邮箱
        dn 查找用户的base_dn
    """

    def __init__(self, find_username, host=ldap_host, user=ldap_user, password=ldap_password,
                 search_base=ldap_search_base, new_password=None):
        self.host = host
        self.user = user
        self.password = password
        self.search_base = search_base
        self.find_username = find_username
        self.new_password = new_password
        self.connection = Connection(server=Server(self.host, use_ssl=True), user=self.user, password=self.password,
                                     auto_bind=True)
        self.connection.search(search_base=self.search_base,
                               search_filter='(sAMAccountName=%s)' % self.find_username,
                               search_scope=LEVEL,
                               attributes=ALL_ATTRIBUTES,
                               paged_size=100)
        self.search_out = self.connection.response
        if new_password is None:
            self.connection.unbind()

    def __getattr__(self, key):
        if not isinstance(self.search_out, Iterable):
            return {'status': False, 'code': '用户不存在或信息缺失'}
        try:
            if key in self.search_out[0]['attributes']:
                return self.search_out[0]['attributes'][key]
            return super(PublicLdap, self).__getattribute__(key)
        except Exception as e:
            print(e)
            return {'status': False, 'code': '用户不存在或信息缺失'}

    def modify_password(self):
        try:
            if self.check_password() is not True:
                return self.check_password()
            dn = self.connection.response[0]['dn']
            modify_password_out = self.connection.extend.microsoft.modify_password(user=dn,
                                                                                   new_password=self.new_password)
            enable_user_out = self.connection.modify(dn,
                                                     {'userAccountControl': [('MODIFY_REPLACE', 512)]})
            if modify_password_out and enable_user_out:
                return {'status': True, 'data': '修改密码成功'}
            else:
                print(self.connection.result())
                self.connection.unbind()
                return {'status': False, 'data': '修改密码失败'}
        except Exception as e:
            return {'status': False, 'data': e}

    def check_password(self):
        if re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$", self.new_password) and len(self.new_password) >= 6:
            return True
        else:
            return {'status': False, 'data': '密码复杂度不合规 大小写数字符号并且6位以上'}
