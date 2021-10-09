# -*- coding: utf-8

from unittest import mock
import unittest
import requests



class MockLoginTest(unittest.TestCase):
    def setUp(self):
        self.url='http://localhost:12306'

    def tearDown(self):
        pass

    def getUrl(self,path):
        return self.url+path

    def getToken(self):
        """get token"""
        data={
            "username":"admin",
            "password":"admin",
            "roleID":22
        }
        r=requests.post(self.getUrl('/login'),json=data)
        #print("token----------",r.json()['token'])
        return r.json()['token']

    def test_login(self):
        """验证登录的接口"""
        data={
            "username":"admin",
            "password":"admin",
            "roleID":22
        }

        r=requests.post(self.getUrl("/login"),json=data)
        #print("username---------",r.json()['username'])
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json()['username'],'xiaolizi')

if __name__=='__main__':
    unittest.main(verbosity=2)