# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import urllib2

def open_url(url, encoding='utf-8'):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
		req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		response = urllib2.urlopen(req,timeout=15)
		link=response.read()
		response.close()
		if encoding != 'utf-8': link = link.decode(encoding).encode('utf-8')
		return link
	except BaseException as e: print '##ERROR-addonsresolver:open_url: '+str(url)+' '+str(e)