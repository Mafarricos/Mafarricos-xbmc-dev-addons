# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import basic,links,json,omdbapi,threading,xbmcaddon,os

LANG = basic.get_api_language()
getSetting          = xbmcaddon.Addon().getSetting

def listmovies(url,cachePath):
	mainlist = []
	sendlist = [] 
	result = []
	threads = []
	order = 0
	jsonpage = basic.open_url(url)
	j = json.loads(jsonpage)
	#for list in j['results']: mainlist.append(searchmovie(list['id']))
	for list in j['results']: 
		order += 1
		sendlist.append([order,list['id']])
	##single thread
	#searchmovielist(sendlist,result)
	##mult thread
	chunks=[sendlist[x:x+5] for x in xrange(0, len(sendlist), 5)]
	for i in range(0,len(chunks)): threads.append(threading.Thread(name='listmovies'+str(i),target=searchmovielist,args=(chunks[i],result,cachePath, )))
	[i.start() for i in threads]
	[i.join() for i in threads]
	result = sorted(result, key=basic.getKey)
	for id,lists in result: mainlist.append(lists)
	return mainlist

def searchmovielist(list,result,cachePath):
	for num,id in list: result.append([num,searchmovie(id,cachePath)])

def searchmovie(id,cachePath):
	listgenre = []
	listcast = []
	listcastr = []	
	genre = ''
	title = ''
	plot = ''
	tagline = ''
	director = ''
	writer = ''
	credits = ''
	poster = ''
	fanart = ''
	duration = ''
	videocache = os.path.join(cachePath,str(id))
	if os.path.isfile(videocache): return json.loads(basic.readfiletoJSON(videocache))
	jsonpage = basic.open_url(links.link().tmdb_info_default % (id))
	if not jsonpage: jsonpage = basic.open_url(links.link().tmdb_info_default_alt % (id))
	try: jdef = json.loads(jsonpage)
	except: jdef = ''
	if LANG <> 'en':
		try:
			jsonpage = basic.open_url(links.link().tmdb_info % (id,LANG))
			j = json.loads(jsonpage)
			title = j['title']
			fanart = links.link().tmdb_backdropbase % (j["backdrop_path"])
			poster = links.link().tmdb_posterbase % (j["poster_path"])
			for g in j['genres']: listgenre.append(g['name'])
			genre = ', '.join(listgenre)
			try: plot = j['overview']
			except: pass
			try: tagline = j['tagline']
			except: pass
			fanart = j["backdrop_path"]
			poster = j["poster_path"]
		except: pass
	if not title: title = jdef['title']		
	if not poster: poster = jdef['poster_path']
	if not fanart: fanart = jdef['backdrop_path']
	if not fanart: fanart = poster
	if fanart: fanart = links.link().tmdb_backdropbase % (fanart)
	if poster: poster = links.link().tmdb_posterbase % (poster)	
	if genre == '':
		for g in jdef['genres']: listgenre.append(g['name'])
		genre = ', '.join(listgenre)
	if not plot: plot = jdef['overview']
	if not tagline: tagline = jdef['tagline']
	try: trailer = "plugin://plugin.video.youtube/?action=play_video&videoid=%s" % (jdef['trailers']['youtube'][0]['source'])
	except: trailer = ''
	try: year = jdef["release_date"].split("-")[0]
	except: year = ''
	try: studio = jdef['production_companies'][0]['name']
	except: studio = ''
	for listc in jdef['credits']['cast']: 
		listcastr.append(listc['name']+'|'+listc['character'])
		listcast.append(listc['name'])
	for crew in jdef['credits']['crew']:
		if crew['job'] == 'Director': director = crew['name']
		break
	for crew in jdef['credits']['crew']:
		if crew['job'] == 'Story': credits = crew['name']
		break		
	for crew in jdef['credits']['crew']:
		if crew['job'] == 'Writer': 
			writer = crew['name']
			break
		if crew['job'] == 'Novel': 
			writer = crew['name']
			break
		if crew['job'] == 'Screenplay': 
			writer = crew['name']
			break
	duration = jdef['runtime']
	if not poster and jdef['imdb_id']:
		altsearch = omdbapi.searchmovie(jdef['imdb_id'])
		poster = altsearch['poster']
		if not fanart: fanart = poster
		if not plot: plot = altsearch['info']['plot']
		if not tagline: tagline = altsearch['info']['plot']	
		if not listcast: 
			listcast = altsearch['info']['cast']
			listcastr = []
		if not duration: duration = altsearch['info']['duration']
		if not writer: writer = altsearch['info']['writer']
		if not director: director = altsearch['info']['director']		
		if not genre: genre = altsearch['info']['genre']
	response = {
        "label": '%s (%s)' % (title,year),
        "originallabel": '%s (%s)' % (jdef['original_title'],year),		
        "poster": poster,
		"fanart_image": fanart,
		"imdbid": jdef['imdb_id'],
		"year": year,
		"info":{
			"genre": genre, 
			"year": year,
			"rating": jdef['vote_average'], 
			"cast": listcast,
			"castandrole": listcastr,
			"director": director,
			"plot": plot,
			"plotoutline": plot,
			"title": title,
			"originaltitle": jdef['original_title'],
			"duration": duration,
			"studio": studio,
			"tagline": tagline,
			"writer": writer,
			"premiered": jdef['release_date'],
			"code": jdef['imdb_id'],
			"credits": credits,
			"votes": jdef['vote_count'],
			"trailer": trailer
			}
		}
	if getSetting("cachesites") == 'true': basic.writefile(videocache,'w',json.dumps(response))
	return response