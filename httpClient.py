import os
import sys
import json
import requests

class OS_API_CLIENT(object):
	def __init__(self, base_url='', token=None, project_id=None, user_id=None):
		self.os_token = ''
		self.os_host = ''
		self.os_username = ''
		self.os_password = ''
		self.os_tenantName = ''
		self.base_url = base_url
		self.project_id = project_id
		self.user_id = user_id

	def readConfig(self):
		with open('osinput.json') as data_file:
			data = json.load(data_file)
		self.os_host = data["os_host"]
		self.os_username = data["os_username"]
		self.os_tenantName = data["os_tenantName"]
		self.os_password = data["os_password"]
		data_file.close()

	def _update_headers(self, headers):
		if not headers:
			headers = {}

		token = headers.get('x-auth-token', self.os_token)
		if token:
			headers['x-auth-token'] = token

		project_id = headers.get('X-Project-Id', self.project_id)
		if project_id:
			headers['X-Project-Id'] = project_id

		user_id = headers.get('X-User-Id', self.user_id)
		if user_id:
			headers['X-User-Id'] = user_id

		return headers

	def getApiToken(self):
		auth = {}
		auth["auth"] = {}
		auth["auth"]["passwordCredentials"] = {}
		auth["auth"]["passwordCredentials"]["username"] = self.os_username
		auth["auth"]["passwordCredentials"]["password"] = self.os_password
		auth["auth"]["tenantName"] = self.os_tenantName
		hdr = {}
		content_type = hdr.get('content-type', 'application/json')
		hdr['content-type'] = content_type
		url = 'http://' + self.os_host + ':5000/v2.0/tokens'

		r = requests.post(url, data=json.dumps(auth), headers = hdr)
		access = json.loads(r.content)
		self.os_token = access['access']['token']['id']

	def getNeutronNetworks(self):
		hdr = {}
		content_type = hdr.get('content-type', 'application/json')
		hdr['content-type'] = content_type
		x_auth = hdr.get("X-Auth-Token", self.os_token)
		hdr["X-Auth-Token"] = x_auth

		url = 'http://'+self.os_host+':9696/v2.0/networks'

		r = requests.get(url, headers = hdr)
		networks = json.loads(r.content)
		print networks

		out = open("OS_networks.json", 'w+')
		out.write('[')
		f = True
		for net in networks['networks']:
			if not f:
				out.write(',\n')
			out.write('{' +'\t\"name\": \"'+net['name']+'\",\n'+
					  '\t\"provider_segmentation_id\": \"' + str(net['provider:segmentation_id']) + '\",\n' +
					  '\t\"new_vlan\": \"' + '0\"\n'+ '}')
			f = False
		out.write(']')
		out.close()

test = OS_API_CLIENT()
#test.setEnv()
test.readConfig()
test.getApiToken()
test.getNeutronNetworks()
#test.getVlans()

