# Addons resolver
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
# MafaStudios@gmail.com
import basic,links,re

def playrato(name, url, imdb_id, year):
	ratosearch = basic.open_url(links.link().rato_search % (imdb_id))
	siterato = re.compile('<span class="more-btn"><a href="(.+?)" >Ver Agora</a>').findall(ratosearch)[0]
	if siterato:
		import xbmcgui,xbmc
		item = xbmcgui.ListItem(path=url)
		item.setProperty("IsPlayable", "true")
		xbmc.Player().play(links.link().rato_play % (siterato,name), item)

def playparser(name, url, imdb_id, year):
	import xbmcgui,xbmc
	item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
	xbmc.Player().play(links.link().genesis_play % (name,name,year,imdb_id,url), item)