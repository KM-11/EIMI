import dotenv
from pathlib import Path
import re 
import ipaddress
import requests
import json
API_LOCATION='http://ip-api.com/json/'
API_KEY_VT = 'TU-API-KEY'
API_REPORT_VT = 'https://www.virustotal.com/vtapi/v2/file/report'



def load_env_file():
    env_path = Path('..') / '.env'
    dotenv.load_dotenv(dotenv_path=env_path)

def is_ip_valid(ip):
	try:
		ipaddress.ip_address(ip)
		return True
	except:
		return False
		
def find_ip_address(data):
	pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
	matches = re.findall(pattern,data)
	return list(filter(lambda x: is_ip_valid(x),list(matches)))

def get_ip_location(ip):
	
	if is_ip_valid(ip):
		r = requests.get(API_LOCATION+ip)
		return r.text

	return None

def get_report(resource):
	headers = {
  		"Accept-Encoding": "gzip, deflate",
 	}
	global API_KEY
	params = {'apikey': API_KEY_VT , 'resource': resource}

	response = requests.get(API_REPORT_VT, params=params, headers=headers)
	return response.text

def get_av_detection(report_json):
	av = []
	for i in report_json['scans']:
		if report_json['scans'][i]['detected'] == True:
			av_name = i
			label = report_json['scans'][i]['result']
			av.append((av_name,label))
	return av

report_json = json.loads(get_report('ed63ebefb0fe0631547e7c50d4b66c6e45956e17b4f00be4970b7dbf71a29ef1'))
list_av_detection= get_av_detection(report_json)

print(list_av_detection)
print(report_json['total'])
print(report_json['positives'])


