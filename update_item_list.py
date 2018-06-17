import json
import urllib.request

# with open('wfm_item_list.json') as wfm_item_list_str:
# 	wfm_item_list_data = json.loads(wfm_item_list_str.read())

# print(wfm_item_list_data)


item_list = json.loads(urllib.request.urlopen("https://api.warframe.market/v1/items").read())['payload']['items']['en']

with open('wfm_item_list.json', 'w') as fout:
	fout.write(json.dumps(item_list))