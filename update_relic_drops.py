import csv
import json
import requests
from pprint import pprint
import io
import re

relics_url = "https://docs.google.com/feeds/download/spreadsheets/Export?gid=983656373&key=1iyuQXUaWcIr1-DrYsFgsPsGuGANTwWDEK9Fy_fzFfLU&exportFormat=csv"
drop_table_url = "https://docs.google.com/feeds/download/spreadsheets/Export?gid=0&key=1iyuQXUaWcIr1-DrYsFgsPsGuGANTwWDEK9Fy_fzFfLU&exportFormat=csv"

data_str = requests.get(relics_url).text

drop_table_str = requests.get(drop_table_url).text

data_list = data_str.split("\n")
for i, element in enumerate(data_list):
	data_list[i] = element.split(",")

drop_table_list = drop_table_str.split("\n")
for i, element in enumerate(drop_table_list):
	drop_table_list[i] = element.split(",")


# print(data_list[:20])
# print(drop_table_list[:20])

unvaulted = []
for i in drop_table_list:
	if "Relic" in i[0]:
		unvaulted.append(i[0][0:-6])
# print(unvaulted[:10])

data_dict = {}
item_name = ""
for i, element in enumerate(data_list):
	if i % 8 == 0:
		item_name = element[0]
		if "Relic (Intact)" in item_name:
			item_name = item_name[0:-15]
			data_dict[item_name] = []
			relic = True
		else:
			relic = False
	elif relic and element[0]:
		data_dict[item_name].append({'name': element[0],'chance': float(re.sub('[^\d\.]', '', element[1]))/100.0})
# print(data_dict)

radiant_data_dict = {}
item_name = ""
for i, element in enumerate(data_list):
	if i % 8 == 0:
		item_name = element[0]
		if "Relic (Radiant)" in item_name:
			item_name = item_name[0:-16]
			radiant_data_dict[item_name] = []
			relic = True
		else:
			relic = False
	elif relic and element[0]:
		radiant_data_dict[item_name].append({'name': element[0],'chance': float(re.sub('[^\d\.]', '', element[1]))/100.0})

unvaulted_dict = {}
vaulted_dict = {}
for name in data_dict.keys():
	if name in unvaulted:
		unvaulted_dict[name] = data_dict[name]
	else:
		vaulted_dict[name] = data_dict[name]

radiant_unvaulted_dict = {}
radiant_vaulted_dict = {}
for name in radiant_data_dict.keys():
	if name in unvaulted:
		radiant_unvaulted_dict[name] = radiant_data_dict[name]
	else:
		radiant_vaulted_dict[name] = radiant_data_dict[name]

with open('unvaulted_drop_table.json','w') as fileOut:
	fileOut.write(json.dumps(unvaulted_dict))

with open('vaulted_drop_table.json','w') as fileOut:
	fileOut.write(json.dumps(vaulted_dict))

with open('radiant_unvaulted_drop_table.json', 'w') as fileOut:
	fileOut.write(json.dumps(radiant_unvaulted_dict))

with open('radiant_vaulted_drop_table.json', 'w') as fileOut:
	fileOut.write(json.dumps(radiant_vaulted_dict))