# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License
import links,json,basic,re,xbmcaddon,os

getSetting          = xbmcaddon.Addon().getSetting

def listmovies(url,cachePath):
	basic.log(u"omdbapi.listmovies url: %s" % url)
	mainlist = []
	sendlist = [] 
	result = []
	threads = []
	order = 0
	jsonpage = basic.open_url(url)
	j = json.loads(jsonpage)
	for list in j['results']: 
		order += 1
		sendlist.append([order,list['id']])
	chunks=[sendlist[x:x+5] for x in xrange(0, len(sendlist), 5)]
	for i in range(0,len(chunks)): threads.append(threading.Thread(name='listmovies'+str(i),target=searchmovielist,args=(chunks[i],result,cachePath, )))
	[i.start() for i in threads]
	[i.join() for i in threads]
	result = sorted(result, key=basic.getKey)
	for id,lists in result: mainlist.append(lists)
	basic.log(u"omdbapi.listmovies mainlist: %s" % mainlist)	
	return mainlist

def searchmovielist(list,result,cachePath):
	basic.log(u"omdbapi.searchmovielist list: %s" % list)
	for num,id in list: 
		moviedata = searchmovie(id,cachePath)
		if moviedata: result.append([num,moviedata])
	basic.log(u"omdbapi.searchmovielist result: %s" % result)
	
def searchmovie(id,cachePath,cache=True):
	basic.log(u"omdbapi.searchmovie id: %s" % id)
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
	if cache:
		videocache = os.path.join(cachePath,str(id))
		if os.path.isfile(videocache): return json.loads(basic.readfiletoJSON(videocache))	
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
	response = {
		"label": '%s (%s)' % (title,year),
		"originallabel": '%s (%s)' % (title,year),
		"poster": poster,
		"fanart_image": fanart,
		"imdbid": id,
		"year": year,
		"info":{
			"genre": genre, 
			"year": year,
			"rating": jdef['imdbRating'], 
			"cast": listcast,
			"castandrole": director,
			"director": plot,
			"plot": plot,
			"plotoutline": plot,
			"title": title,
			"originaltitle": title,
			"duration": duration,
			"studio": '',
			"tagline": tagline,
			"writer": writer,
			"premiered": '',
			"code": id,
			"credits": '',
			"votes": jdef['imdbVotes'],
			"trailer": ''
			}
		}
	if cache:
		if getSetting("cachesites") == 'true': basic.writefile(videocache,'w',json.dumps(response))
	return response		
