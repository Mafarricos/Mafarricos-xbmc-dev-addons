# Addons resolver
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
# MafaStudios@gmail.com
import re,xbmcgui,xbmcaddon,xbmc,os,urllib,json
import basic,links

addon_id 		= 'script.module.addonsresolver'
selfAddon 		= xbmcaddon.Addon(id=addon_id)
getSetting 		= selfAddon.getSetting
installfolder 	= xbmc.translatePath('special://home/addons')

def ytssearch(imdb_id,returnmagnets=False):
	quality = []
	magnet = []
	yts = basic.open_url(links.link().yts_search % (imdb_id))
	jtys = json.loads(yts)
	if 'No movies found' in str(jtys): return '',''
	for j in jtys["MovieList"]:
		quality.append('%s (Seeds: %s Peers: %s Size: %s)' %(j["Quality"],j["TorrentSeeds"],j["TorrentPeers"],j["Size"]))
		magnet.append(j["TorrentMagnetUrl"])
	if returnmagnets == False:
		qualitychoice = xbmcgui.Dialog().select		
		choose=qualitychoice('Seleccione a Qualidade',quality)
		if choose > -1:
			return magnet[choose]
	else:
		return quality,magnet
		
def ratosearch(imdb_id):
	ratos = basic.open_url(links.link().rato_search % (imdb_id))
	try: siterato = re.compile('<span class="more-btn"><a href="(.+?)" >Ver Agora</a>').findall(ratos)[0]
	except: siterato = False
	return siterato

def wtsearch(name):
	wt = basic.open_url(links.link().wt_search % (urllib.quote_plus(name)))
	try: 
		sitewt = re.compile('<a href="(.+?)" class="movie-name">').findall(wt)[0]
		sitewt = links.link().wt_base % (sitewt)
	except: sitewt = False
	return sitewt
	
def playparser(name, url, imdb_id, year, addon):
	if 'kmediatorrent' or 'stream' in addon: item = xbmcgui.ListItem(path=imdb_id)
	else: item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
	if 'genesis' in addon: xbmc.Player().play(links.link().genesis_play % (name,name,year,imdb_id,url), item)
	elif 'rato' in addon: xbmc.Player().play(links.link().rato_play % (url,name), item)
	elif 'wt' in addon: 
		xbmc.Player().play(links.link().wt_play % (urllib.quote_plus(url),urllib.quote_plus(name)), item)	
	elif 'portugas' in addon.lower(): xbmc.Player().play(links.link().sdp_search % (imdb_id,urllib.quote_plus(name.replace('('+year+')',''))))
	elif 'kmediatorrent' in addon.lower():
		qualitychoice = xbmcgui.Dialog().select
		q = []
		m = []
		for qual,magnet in url:
			q = qual
			m = magnet
		choose=qualitychoice('Seleccione a Qualidade',q)
		url = links.link().kmediatorrent_play % (urllib.quote_plus(m[choose]))
		if choose > -1:	xbmc.Player().play(url,item)		
	elif 'stream' in addon.lower():
		qualitychoice = xbmcgui.Dialog().select
		q = []
		m = []
		for qual,magnet in url:
			q = qual
			m = magnet
		choose=qualitychoice('Seleccione a Qualidade',q)
		url = links.link().stream_play % (urllib.quote_plus(m[choose]))
		if choose > -1:	xbmc.Player().play(url,item)

def custom_choice(name,url,imdb_id,year):
	if getSetting("pref_addon") <> '-':
		if 'rato' in getSetting("pref_addon").lower(): url = ratosearch(imdb_id)
		if 'wt' in getSetting("pref_addon").lower(): url = wtsearch(name)
		if 'kmediatorrent' or 'stream' in getSetting("pref_addon").lower(): url = ytssearch(imdb_id)
		if url: playparser(name,url,imdb_id,year,getSetting("pref_addon").lower())
	else:
		addonchoice = xbmcgui.Dialog().select
		addons = []
		siterato = ''
		sitewt = ''
		magnet = ''
		see = 'Ver no %s'
		if getSetting("genesis_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().genesis_id)): addons.append(see % (links.link().genesis_id.split('.')[2]))
		if getSetting("rato_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().rato_id)):
			siterato = ratosearch(imdb_id)
			if siterato: addons.append(see % (links.link().rato_id.split('.')[2]))
		if getSetting("wt_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().wt_id)):
			sitewt = wtsearch(name)
			if sitewt: addons.append(see % (links.link().wt_id.split('.')[2]))
		if (getSetting("kmediatorrent_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().kmediatorrent_id))) or (getSetting("stream_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().stream_id))):
			qual,magnet = ytssearch(imdb_id,True)
			if magnet: 
				addons.append(see % (links.link().kmediatorrent_id.split('.')[2]))
				addons.append(see % (links.link().stream_id.split('.')[2]))				
		if getSetting("sdp_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().sdp_id)): addons.append(see % (links.link().sdp_id.split('.')[2]))
		choose=addonchoice('Seleccione o addon',addons)
		if choose > -1:
			if 'rato' in addons[choose]: url = siterato
			if 'wt' in addons[choose]: url = sitewt
			if 'kmediatorrent' in addons[choose] or 'stream' in addons[choose]: 
				url = []
				url.append([qual,magnet])			
			playparser(name,url,imdb_id,year,addons[choose])