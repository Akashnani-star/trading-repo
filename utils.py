import requests
import json

def get_random_cp(instruments):
	cp_list = []
	if len(instruments) != 0:
		request_url = "http://192.168.29.229:5000/SL"
		fetch = requests.get(request_url)
		data = json.loads(fetch.text)
		for i in instruments:
			cp_list.append((i,int(data)))
	return cp_list	
