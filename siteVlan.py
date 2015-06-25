import os
import sys
import json
import requests

class OS_API_CLIENT(object):
	def __init__(self):
		self.os_token = ''
		self.os_host = ''
		self.os_username = ''
		self.os_password = ''
		self.os_tenantName = ''

	def readConfig(self):
		with open('osinput.json') as data_file:
			data = json.load(data_file)
		self.os_host = data["os_host"]
		self.os_username = data["os_username"]
		self.os_tenantName = data["os_tenantName"]
		self.os_password = data["os_password"]
		data_file.close()

	def getApiToken(self):
		auth = {}
		auth["auth"] = {}
		auth["auth"]["passwordCredentials"] = {}
		auth["auth"]["passwordCredentials"]["username"] = self.os_username
		auth["auth"]["passwordCredentials"]["password"] = self.os_password
		auth["auth"]["tenantName"] = self.os_tenantName
		with open('credentials.json', 'w+') as fp:
			json.dump(auth, fp)
		fp.close()

		cmd = ['curl', '-d', '@credentials.json', '-H', "Content-Type:application/json",
			   'http://'+self.os_host+':35357/v2.0/tokens']

		of = open("/tmp/OS_auth.json", 'w+')
		p = subprocess.call(cmd, stdout=of, stderr=subprocess.PIPE)

		of.flush()
		with open("/tmp/OS_auth.json") as of:
			data = json.load(of)
		self.os_token = data['access']['token']['id']
		of.close()

	def getNeutronNetworks(self):
		cmd = ['curl', '-H', "X-Auth-Token:"+self.os_token,
			   'http://'+self.os_host+':9696/v2.0/networks']
		of = open("/tmp/OS_networks.json", 'w+')
		p = subprocess.call(cmd, stdout=of, stderr=subprocess.PIPE)
		of.flush()
		with open("/tmp/OS_networks.json") as of:
			data = json.load(of)
		of.close()
		print data

		out = open("OS_networks.json", 'w+')
		out.write('[')
		f = True
		for net in data['networks']:
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

