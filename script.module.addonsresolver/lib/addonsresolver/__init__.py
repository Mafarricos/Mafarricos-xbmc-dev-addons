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

def ytssearch(imdb_id):
	qualitychoice = xbmcgui.Dialog().select
	quality = []
	magnet = []
	yts = basic.open_url(links.link().yts_search % (imdb_id))
	jtys = json.loads(yts)
	for j in jtys["MovieList"]:
		quality.append(j["Quality"])
		magnet.append(j["TorrentMagnetUrl"])
	choose=qualitychoice('Seleccione a Qualidade',quality)
	if choose > -1:
		return magnet[choose]
	
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
	item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
	if 'genesis' in addon: xbmc.Player().play(links.link().genesis_play % (name,name,year,imdb_id,url), item)
	elif 'rato' in addon: xbmc.Player().play(links.link().rato_play % (url,name), item)
	elif 'wt' in addon: 
		print links.link().wt_play % (urllib.quote_plus(url),urllib.quote_plus(name))
		xbmc.Player().play(links.link().wt_play % (urllib.quote_plus(url),urllib.quote_plus(name)), item)	
	if 'portugas' in addon.lower():	xbmc.executebuiltin('activatewindow(video,'+links.link().sdp_search % (imdb_id,urllib.quote_plus(name.split("(")[0].strip()))+')')
	
def custom_choice(name,url,imdb_id,year):
	if getSetting("pref_addon") <> '-':
		if 'rato' in getSetting("pref_addon").lower(): url = ratosearch(imdb_id)
		if 'wt' in getSetting("pref_addon").lower(): url = wtsearch(name)		
		if url: playparser(name,url,imdb_id,year,getSetting("pref_addon").lower())
	else:
		addonchoice = xbmcgui.Dialog().select
		addons = []
		see = 'Ver no %s'
		if getSetting("genesis_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().genesis_id)): addons.append(see % (links.link().genesis_id.split('.')[2]))
		if getSetting("rato_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().rato_id)):
			siterato = ratosearch(imdb_id)
			if siterato: addons.append(see % (links.link().rato_id.split('.')[2]))
		if getSetting("wt_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().wt_id)):
			sitewt = wtsearch(name)
			if sitewt: addons.append(see % (links.link().wt_id.split('.')[2]))			
		if getSetting("sdp_enabled") == 'true' and os.path.exists(os.path.join(installfolder,links.link().sdp_id)): addons.append(see % (links.link().sdp_id.split('.')[2]))
		choose=addonchoice('Seleccione o addon',addons)
		if choose > -1:
			if 'rato' in addons[choose]: url = siterato
			if 'wt' in addons[choose]: url = sitewt			
			playparser(name,url,imdb_id,year,addons[choose])
	