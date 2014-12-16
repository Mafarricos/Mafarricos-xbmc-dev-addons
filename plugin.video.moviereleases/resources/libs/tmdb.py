# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import basic,links,json

LANG = basic.get_api_language()

def listmovies(url):
	mainlist = []
	jsonpage = basic.open_url(url)
	j = json.loads(jsonpage)
	for list in j['results']: mainlist.append(searchmovie(list['id']))
	return mainlist
	
def searchmovie(id):
	listgenre = []
	fanart = ''
	poster = ''
	genre = ''
	title = ''
	plot = ''
	tagline = ''
	director = ''
	writer = ''
	credits = ''
	listcast = []
	listcastr = []
	jsonpage = basic.open_url(links.link().tmdb_info_default % (id))
	jdef = json.loads(jsonpage)
	if LANG <> 'en':	
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
		
	if title == '': title = jdef['title']
	if fanart == '': fanart = links.link().tmdb_backdropbase % (jdef["backdrop_path"])
	if poster == '': poster = links.link().tmdb_posterbase % (jdef["poster_path"])
	if genre == '':
		for g in jdef['genres']: listgenre.append(g['name'])
		genre = ', '.join(listgenre)
	if plot == '': plot = jdef['overview']
	if tagline == '': tagline = jdef['tagline']
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
	return {
        "label": '%s (%s)' % (title,year),
        "poster": links.link().tmdb_posterbase % (j["poster_path"]),
		"fanart_image": links.link().tmdb_backdropbase % (j["backdrop_path"]),
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
			"duration": jdef['runtime'],
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