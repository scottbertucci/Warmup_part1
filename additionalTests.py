"""
Each file that starts with test... in this directory is scanned for subclasses of unittest.TestCase or testLib.RestTestCase
"""

import unittest
import os
import testLib

class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)
	
	def testNoPassword(self):
	    respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user2', 'password' : ''} )
        self.assertResponse(respData, count = 1)
		
	def testNoName(self):
	    respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
		
	def testLongName(self):
	    respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'u'*129 , 'password' : 'password'} )
        self.assertResponse(respData, count = 1, testLib.RestTestCase.ERR_BAD_USERNAME)
		
	def testLongPass(self):
	    respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user3' , 'password' : 'p' *129} )
        self.assertResponse(respData, count = 1, testLib.RestTestCase.ERR_BAD_PASSWORD)
	
	def testDupName(self):
		self.makeRequest("/users/add", method="POST", data = { 'user' : 'user4' , 'password' : 'password'} )
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user4' , 'password' : 'password'} )
        self.assertResponse(respData, count = 1, testLib.RestTestCase.ERR_USER_EXISTS)
		
class TestLoginUser(testLib.RestTestCase):
    """Test logging users"""
	def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)
		
	def testWrongPass(self):
	    self.makeRequest("/users/add", method="POST", data = { 'user' : 'user5' , 'password' : 'password'} )
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user5' , 'password' : 'pass'} )
        self.assertResponse(respData, count = 1, testLib.RestTestCase.ERR_BAD_CREDENTIALS)

	def testNotAdded(self):
		respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user6' , 'password' : 'password'} )
        self.assertResponse(respData, count = 1, testLib.RestTestCase.ERR_BAD_CREDENTIALS)
		
		