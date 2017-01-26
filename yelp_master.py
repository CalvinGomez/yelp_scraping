import os
from os.path import join, dirname
from dotenv import load_dotenv

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import requests
from time import sleep
import random
import csv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

auth = Oauth1Authenticator(
    consumer_key = os.environ.get("CONSUMER_KEY"),
    consumer_secret = os.environ.get("CONSUMER_SECRET"),
    token = os.environ.get("TOKEN"),
    token_secret = os.environ.get("TOKEN_SECRET")
)

links = []
max_sleep_time = 10
no_of_active_slaves = 13
base_url_first = 'https://yelp-slave-'
base_url_second = '-calvinxgomez.c9users.io/yelpscraping/scrape'
slaves = []
for i in range(1,no_of_active_slaves + 1):
    slaves.append(base_url_first + str(i) + base_url_second)
    
def yelp_search():
	client = Client(auth)
	page_size = 20
	page = 0
	count = 0
	max_page_count = 1     # Can take a max value of 50
	search_term = "Parks"
	city = "New York City"

	print("Page: " + str(page+1) + "\n")
	resp = client.search(term=search_term, location=city, limit=page_size, offset=page * page_size)
	count = count + len(resp.businesses)

	for j in resp.businesses:
		website_link = make_post_requests(j.url)
		if website_link != '0':
			print("Link found.\n")
			links.append([website_link])
		else:
			print("Website link not found.\n")
	
	while resp and page < max_page_count-1:
		page = page + 1
		if page%7 ==0:
			print("\nSleeping for 10 minutes")
			sleep(600)
		print("Page: " + str(page+1))
		resp = client.search(term=search_term, location=city, limit=page_size, offset=page * page_size)
		count = count + len(resp.businesses)

		for j in resp.businesses:
			website_link = make_post_requests(j.url)
			if website_link != '0':
				print("Link found.\n")
				links.append([website_link])
			else:
				print("Website link not found.\n")
	path = search_term + '.csv'
	with open(path, 'w') as outfile:
	    writer = csv.writer(outfile)
	    for row in links:
	      writer.writerow(row)

def make_post_requests(yelp_url):
	sleep_time = random.randint(1, max_sleep_time)
	print("Sleeping for " +str(sleep_time)+ " s")
	sleep(sleep_time)
	
	random_slave = random.randint(1, no_of_active_slaves)
	r = requests.post(slaves[random_slave-1], data = {'url':yelp_url})
	print("Slave " +str(random_slave))
	return r.text

yelp_search()