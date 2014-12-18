# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import basic,re
from BeautifulSoup import BeautifulSoup

def getlinks(url,results,order,Source=None):
	basic.log(u"imdb.getlinks url: %s" % url)
	try:
		html_page = basic.open_url(url)
		soup = BeautifulSoup(html_page)
		if Source == 'IMDB':
			for link in soup.findAll('a', attrs={'href': re.compile("^/title/.+?/\?ref_=.+?_ov_tt")}):
				if '?' in link.get('href'): cleanlink = link.get('href').split("?")[0].split("title")[1].replace('/','')
				else: cleanlink = link.get('href').split("title")[1].replace('/','')
				results.append([order, cleanlink])
				order += 1			
		else:
			for link in soup.findAll('a', attrs={'href': re.compile("^http://.+?/title/")}):
				if '?' in link.get('href'): cleanlink = link.get('href').split("?")[0].split("/title/")[1].replace('/','')
				else: cleanlink = link.get('href').split("title")[1].replace('/','')
				results.append([order, cleanlink])
				order += 1
		basic.log(u"imdb.getlinks results: %s" % results)
		return results
	except BaseException as e: basic.log(u"imdb.getlinks ERROR: %s - %s" % (str(url),str(e)))