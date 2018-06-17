import json
import urllib.request
from pprint import pprint
import time
import random
import numpy as np
from operator import itemgetter

# Items which have below this many transactions per 90 day interval on wfm have their plat values penalized
LOW_VOLUME_THRESHOLD = 2000
# If below the volume threshold, the plat price is multiplied by this.
LOW_VOLUME_MULT = 0.5

with open('wfm_item_list.json') as item_list_file:
	item_list = json.loads(item_list_file.read())

prime_item_list = [x for x in item_list if "Prime" in x['item_name'] and not "Set" in x['item_name']]

random_item = prime_item_list[random.randint(1,len(prime_item_list))-1]
random_item_name = random_item['item_name']

##### Getting buy orders #####
# example_item_orders = json.loads(urllib.request.urlopen("https://api.warframe.market/v1/items/{0}/orders".format(random_item['url_name'])).read())['payload']['orders']
# time.sleep(0.4)

# # pprint(example_item_orders)

# buy_orders = [x for x in example_item_orders if x['order_type'] == 'buy' and x['user']['status'] == 'ingame']

# # pprint(buy_orders)


##### Getting stats #####
stats = json.loads(urllib.request.urlopen("https://api.warframe.market/v1/items/{0}/statistics".format(random_item['url_name'])).read())['payload']['statistics']['90days']
time.sleep(0.4)
pprint(stats)

print(random_item_name)
median_price = np.median([x['median'] for x in stats])
print(median_price)
total_volume = np.sum([x['volume'] for x in stats])
print(total_volume)



with open('unvaulted_drop_table.json') as drop_table_file:
	drop_table = json.loads(drop_table_file.read())

# print(drop_table)

# relic_values = {}
# for name, drops in drop_table.items():
# 	value = 0
# 	for drop in drops:
# 		item = None
# 		for i in prime_item_list:
# 			if i['item_name'] == drop['name']:
# 				item = i
# 				break
# 		if item:
# 			stats = json.loads(urllib.request.urlopen("https://api.warframe.market/v1/items/{0}/statistics".format(item['url_name'])).read())['payload']['statistics']['90days']
# 			time.sleep(0.4)
# 			median_price = np.median([x['median'] for x in stats])
# 			value += median_price * drop['chance']
# 	relic_values[name] = value
# pprint(relic_values)

# with open('radiant_unvaulted_drop_table.json') as drop_table_file:
# 	drop_table = json.loads(drop_table_file.read())

# relic_values = {}
# for name, drops in drop_table.items():
# 	value = 0
# 	for drop in drops:
# 		item = None
# 		for i in prime_item_list:
# 			if i['item_name'] == drop['name']:
# 				item = i
# 				break
# 		if item:
# 			stats = json.loads(urllib.request.urlopen("https://api.warframe.market/v1/items/{0}/statistics".format(item['url_name'])).read())['payload']['statistics']['90days']
# 			time.sleep(0.4)
# 			median_price = np.median([x['median'] for x in stats])
# 			value += median_price * drop['chance']
# 	relic_values[name] = value
# pprint(relic_values)


# with open('unvaulted_drop_table.json') as drop_table_file:
# 	drop_table = json.loads(drop_table_file.read())

# relic_values = {}
# for name, drops in drop_table.items():
# 	value = 0
# 	for drop in drops:
# 		item = None
# 		for i in prime_item_list:
# 			if i['item_name'] == drop['name']:
# 				item = i
# 				break
# 		if item:
# 			stats = json.loads(urllib.request.urlopen("https://api.warframe.market/v1/items/{0}/statistics".format(item['url_name'])).read())['payload']['statistics']['90days']
# 			time.sleep(0.4)
# 			median_price = np.median([x['median'] for x in stats])
# 			value += median_price * drop['chance']
# 	relic_values[name] = value
# pprint(relic_values)


plat_by_relic = {}
for name, drops in drop_table.items():

	# Assign values to drops based on median of daily medians from last 90 days on warframe.market.
	for drop in drops:
		item = None
		for i in prime_item_list:
			if i['item_name'] == drop['name']:
				item = i
				break
		if item:
			stats = json.loads(urllib.request.urlopen("https://api.warframe.market/v1/items/{0}/statistics".format(item['url_name'])).read())['payload']['statistics']['90days']
			time.sleep(0.4)
			median_price = np.median([x['median'] for x in stats])
			volume = np.sum([x['volume'] for x in stats])
			if volume < LOW_VOLUME_THRESHOLD:
				drop['value'] = median_price*LOW_VOLUME_MULT
			else:
				drop['value'] = median_price
		else:
			drop['value'] = 0.0

	# Calculate average plat return from a run where all players pick the relic in question
	plat = 0.0
	sorted_drops = sorted(drops, key=itemgetter('value'), reverse=True)
	for i, drop in enumerate(sorted_drops):
		total_chance = np.sum([x['chance'] for index, x in enumerate(sorted_drops) if index >= i])
		chance_of_getting_higher = np.sum([x['chance_with_4'] for index, x in enumerate(sorted_drops) if index < i])
		sorted_drops[i]['chance_with_4'] = (1.0 - (1.0 - drop['chance']/total_chance)**4) - chance_of_getting_higher
		plat += drop['value'] * drop['chance_with_4']
	plat_by_relic[name] = plat

pprint(plat_by_relic)