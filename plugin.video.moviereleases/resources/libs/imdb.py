# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import re,threading,xbmcgui
import basic,tmdb
from BeautifulSoup import BeautifulSoup

def listmovies(url,cachePath):
	basic.log(u"imdb.listmovies url: %s" % url)
	mainlist = []
	sendlist = [] 
	result = []
	threads = []
	order = 0
	htmlpage = basic.open_url(url)
	found = re.findall('data-tconst="(.+?)"',htmlpage, re.DOTALL)
	for imdb_id in found: 
		order += 1
		sendlist.append([order,imdb_id])
	chunks=[sendlist[x:x+5] for x in xrange(0, len(sendlist), 5)]
	for i in range(0,len(chunks)): threads.append(threading.Thread(name='listmovies'+str(i),target=tmdb.searchmovielist,args=(chunks[i],result,cachePath, )))
	[i.start() for i in threads]
	[i.join() for i in threads]
	result = sorted(result, key=basic.getKey)
	for id,lists in result: mainlist.append(lists)
	basic.log(u"imdb.listmovies mainlist: %s" % mainlist)	
	return mainlist

def getgenre(url):
	genrechoice = xbmcgui.Dialog().select
	htmlpage = basic.open_url(url)	
	found = re.findall('<h3>Top Movies by Genre</h3>.+?</html>',htmlpage, re.DOTALL)
	newfound = re.findall('<a href="/genre/(.+?)\?',found[0], re.DOTALL)
	choose=genrechoice('Seleccione o Género',newfound)
	if choose > -1:	return newfound[choose]
	
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