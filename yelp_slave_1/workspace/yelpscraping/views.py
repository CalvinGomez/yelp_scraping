from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib
from bs4 import BeautifulSoup
import re
import urllib2
import random

user_agents = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko', 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.58.494 Chrome/11.0.696.71 Safari/534.24', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A', 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+', 'Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54', 'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02']

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def scrape(request):
	yelp_url = request.POST['url']
	req = urllib2.Request(yelp_url)
	
	random_user_agent = random.randint(0, len(user_agents)-1)
	req.add_header('User-Agent', user_agents[random_user_agent])
	print("\n" + user_agents[random_user_agent])
	htmlfile = urllib2.urlopen(req)
	htmltext = htmlfile.read()
	
	soup = BeautifulSoup(htmltext, "html.parser")
	span_biz_website = soup.find_all("span", class_="biz-website")

	if len(span_biz_website)==0:
		return HttpResponse("0")

	else:
		ahref = span_biz_website[0].a["href"]
		website_link = re.findall('url=(.*?)&website', ahref, re.DOTALL)
		website_link[0] = website_link[0].replace('%3A',':')
		website_link[0] = website_link[0].replace('%2F','/')
		return HttpResponse(website_link[0])