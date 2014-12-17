# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import links,json,basic,re

def searchmovie(id):
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
	trailer = ''
	year = ''
	jsonpage = basic.open_url(links.link().omdbapi_info % (id))
	jdef = json.loads(jsonpage)
	title = jdef['Title']		
	poster = jdef['Poster']
	fanart = poster
	genre = jdef['Genre']
	plot = jdef['Plot']
	tagline = plot
	year = jdef['Year']
	listcast = jdef['Actors'].split(', ')
	director = jdef['Director']
	writer = jdef['Writer']
	duration = re.findall('(\d+) min', jdef['Runtime'], re.DOTALL)
	if duration: dur = duration[0]
	duration = re.findall('(\d) h', jdef['Runtime'], re.DOTALL)
	if duration: dur = int(duration[0])*60	
	return {
        "label": '%s (%s)' % (title,year),
        "poster": poster,
		"fanart_image": fanart,
		"imdbid": id,
		"year": year,
		"info":{
			"genre": genre, 
			"year": year,
			"rating": jdef['imdbRating'], 
			"cast": listcast,
			"director": director,
			"plot": plot,
			"plotoutline": plot,
			"title": title,
			"originaltitle": title,
			"duration": duration,
			"tagline": tagline,
			"writer": writer,
			"code": id,
			"votes": jdef['imdbVotes'],
			}
		}