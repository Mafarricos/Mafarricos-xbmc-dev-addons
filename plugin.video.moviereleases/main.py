# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,threading,re,urllib,json
from BeautifulSoup import BeautifulSoup
from resources.libs import links,tmdb,imdb,youtube,basic
AddonsResolver = True
try: import addonsresolver
except BaseException as e:
	basic.log(u"main.AddonsResolver ##Error: %s" % str(e)) 
	AddonsResolver = False

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
cachePath			= os.path.join(dataPath,'cache')
sitesfile 			= os.path.join(os.path.join(addonPath, 'resources'),'sites.txt')
sitecachefile 		= os.path.join(cachePath,'_cache.txt')
getSetting          = xbmcaddon.Addon().getSetting

if not os.path.exists(dataPath): os.makedirs(dataPath)
if not os.path.exists(cachePath): os.makedirs(cachePath)

def MAIN():
	addDir('Latest Releases','Latest Releases',3,'',True,4,'',0,'','','')
	addDir('TMDB','TMDB',6,'',True,4,'',0,'','','')	
	addDir('IMDB','IMDB',4,'',True,4,'',0,'','','')
	addDir('Search Movie','search',7,'',True,4,'',0,'','','')	
	addDir('Tools','Tools',9,'',True,4,'',0,'','','')

def ToolsMenu():
	addDir('Clean Cache','Clean Cache',8,'',False,2,'',0,'','','')
	if AddonsResolver: addDir('AddonsResolver Settings','Settings',10,'',False,2,'',0,'','','')

def IMDBmenu():
	addDir('Top 250','top250',11,'',True,8,'','','','','')
	addDir('Bottom 100','bot100',11,'',True,8,'','','','','')	
	addDir('In Theaters','theaters',11,'',True,8,'','','','','')
	addDir('Comming Soon','comming_soon',11,'',True,8,'','','','','')
	addDir('US Box Office','boxoffice',11,'',True,8,'',1,'','','')
	addDir('Most Voted','most_voted',11,'',True,8,'',1,'','','')
	addDir('Oscars','oscars',11,'',True,8,'',1,'','','')
	addDir('Popular','popular',11,'',True,8,'',1,'','','')
	addDir('Popular by Genre','popularbygenre',11,'',True,8,'',1,'','','')	
	
def TMDBmenu():
	addDir('In Theaters','Theaters',7,'',True,5,'',1,'','','')
	addDir('Upcoming','Upcoming',7,'',True,5,'',1,'','','')
	addDir('Popular','Popular',7,'',True,5,'',1,'','','')
	addDir('Top Rated','TopRated',7,'',True,5,'',1,'','','')
	addDir('Discover by popularity','discoverpop',7,'',True,5,'',1,'','','')	

def TMDBlist(index,url):
	listdirs = []
	if url == 'search':
		keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			encode=urllib.quote(search)
			listdirs = tmdb.listmovies(links.link().tmdb_search % (encode),cachePath)	
	elif url == 'discoverpop': listdirs = tmdb.listmovies(links.link().tmdb_discover % (index),cachePath)
	elif url == 'Theaters': listdirs = tmdb.listmovies(links.link().tmdb_theaters % (index),cachePath)
	elif url == 'Popular': listdirs = tmdb.listmovies(links.link().tmdb_popular % (index),cachePath)
	elif url == 'Upcoming': listdirs = tmdb.listmovies(links.link().tmdb_upcoming % (index),cachePath)
	elif url == 'TopRated': listdirs = tmdb.listmovies(links.link().tmdb_top_rated % (index),cachePath)
	for j in listdirs: addDir(j['label'],j['imdbid'],2,j['poster'],False,len(listdirs)+1,j['info'],'',j['imdbid'],j['year'],j['originallabel'],j['fanart_image'])
	if url <> 'search': addDir('Next>>',url,7,'',True,len(listdirs)+1,'',int(index)+1,'','','')

def IMDBlist2(index,url,originalname):
	listdirs = []
	if url == 'top250': listdirs = imdb.listmovies(links.link().imdb_top250,cachePath)
	elif url == 'bot100': listdirs = imdb.listmovies(links.link().imdb_bot100,cachePath)	
	elif url == 'boxoffice': listdirs = imdb.listmovies(links.link().imdb_boxoffice % (index),cachePath)
	elif url == 'most_voted': listdirs = imdb.listmovies(links.link().imdb_most_voted % (index),cachePath)
	elif url == 'oscars': listdirs = imdb.listmovies(links.link().imdb_oscars % (index),cachePath)
	elif url == 'popular': listdirs = imdb.listmovies(links.link().imdb_popular % (index),cachePath)
	elif url == 'theaters': listdirs = imdb.listmovies(links.link().imdb_theaters,cachePath)
	elif url == 'comming_soon': listdirs = imdb.listmovies(links.link().imdb_comming_soon,cachePath)	
	elif url == 'popularbygenre': 
		if index == '1': originalname = imdb.getgenre(links.link().imdb_genre)
		listdirs = imdb.listmovies(links.link().imdb_popularbygenre % (index,originalname),cachePath)	
	for j in listdirs: addDir(j['label'],j['imdbid'],2,j['poster'],False,len(listdirs)+1,j['info'],'',j['imdbid'],j['year'],j['originallabel'],j['fanart_image'])
	if url <> 'top250' and url <> 'bot100' and url <> 'theaters' and url <> 'comming_soon': 
		if url == 'popularbygenre': addDir('Next>>',url,11,'',True,len(listdirs)+1,'',int(index)+30,'','',originalname,'')
		else: addDir('Next>>',url,11,'',True,len(listdirs)+1,'',int(index)+30,'','','','')
	
def IMDBlist(name,url):
	results = imdb.getlinks(url,[],1,'IMDB')
	populateDir(results,1)
	
def latestreleases(index):
	sites = []
	for i in range(1, 15):
		if getSetting("site"+str(i)+"on") == 'true': sites.append(getSetting("site"+str(i)))
	threads = []
	f = 0	
	results = []
	try: ranging = int(index)+1
	except: 
		ranging = 1
	if ranging ==1: open(sitecachefile, 'w').close()
	for i in range(ranging, ranging+int(getSetting('pages-num'))):
		for site in sites: 
			f = f + 1
			threads.append(threading.Thread(name=site+str(i),target=imdb.getlinks,args=(site+str(i)+'/',results,f*100, )))
	ranging = i
	[i.start() for i in threads]
	[i.join() for i in threads]
	populateDir(results,ranging,True)
	addDir('Next>>','Next>>',3,'',True,1,'',ranging,'','','')		

def populateDir(results,ranging,cache=False):
	unique_stuff = []
	threads2 = []	
	result = []
	order = 0	
	results = sorted(results, key=basic.getKey)
	for order,link in results:
		if link not in str(unique_stuff): unique_stuff.append([order, link])
	chunks=[unique_stuff[x:x+10] for x in xrange(0, len(unique_stuff), 10)]
	for i in range(0,len(chunks)): threads2.append(threading.Thread(name='listmovies'+str(i),target=tmdb.searchmovielist,args=(chunks[i],result,cachePath, )))
	[i.start() for i in threads2]
	[i.join() for i in threads2]
	result = sorted(result, key=basic.getKey)
	basic.log(u"main.populateDir result: %s" % result)
	if cache: linecache= basic.readalllines(sitecachefile)
	for id,lists in result:
		if cache:
			if lists['label'].encode('utf-8') not in str(linecache):
				basic.writefile(sitecachefile,"a",'::pageindex::'+str(ranging)+'::'+lists['label'].encode('utf-8')+'::\n')
				if (getSetting('allyear') == 'true') or ((getSetting('allyear') == 'false') and (int(lists['info']['year']) >= int(getSetting('minyear')) and int(lists['info']['year']) <= int(getSetting('maxyear')))): addDir(lists['label'],lists['imdbid'],2,lists['poster'],False,len(result)+1,lists['info'],ranging,lists['imdbid'],lists['year'],lists['originallabel'],lists['fanart_image'])
			elif '::pageindex::'+str(ranging)+'::'+lists['label'].encode('utf-8') in str(linecache): 
				if (getSetting('allyear') == 'true') or ((getSetting('allyear') == 'false') and (int(lists['info']['year']) >= int(getSetting('minyear')) and int(lists['info']['year']) <= int(getSetting('maxyear')))): addDir(lists['label'],lists['imdbid'],2,lists['poster'],False,len(result)+1,lists['info'],ranging,lists['imdbid'],lists['year'],lists['originallabel'],lists['fanart_image'])
		else:
			if (getSetting('allyear') == 'true') or ((getSetting('allyear') == 'false') and (int(lists['info']['year']) >= int(getSetting('minyear')) and int(lists['info']['year']) <= int(getSetting('maxyear')))): addDir(lists['label'],lists['imdbid'],2,lists['poster'],False,len(result)+1,lists['info'],ranging,lists['imdbid'],lists['year'],lists['originallabel'],lists['fanart_image'])
	
def addDir(name,url,mode,poster,pasta,total,info,index,imdb_id,year,originalname,fanart=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('ascii','xmlcharrefreplace'))+"&originalname="+urllib.quote_plus(originalname.encode('ascii','xmlcharrefreplace'))+"&index="+str(index)+"&imdb_id="+str(imdb_id)+"&year="+str(year)
	ok=True
	context = []
	liz=xbmcgui.ListItem(name, iconImage=poster, thumbnailImage=poster)
	liz.setProperty('fanart_image',fanart)

	try:
		from metahandler import metahandlers
		metaget = metahandlers.MetaData(preparezip=False)
	except: pass
	try:
		playcount = metaget._get_watched('movie', imdb_id, '', '')
		if playcount == 7: info.update({'playcount': 1, 'overlay': 7})
		else: info.update({'playcount': 0, 'overlay': 6})
	except: pass
	try:
		playcount = [i for i in indicators if i['imdb_id'] == imdb_id][0]
		info.update({'playcount': 1, 'overlay': 7})
	except: pass	
		
	if info <> '': 
		liz.setInfo( type="Video", infoLabels=info )
		try:
			trailer = info['trailer'].split('videoid=')[1]
			context.append(('Ver Trailer', 'RunPlugin(%s?mode=1&url=%s&name=%s)' % (sys.argv[0],trailer,originalname)))
		except: pass
		context.append(('Informação', 'Action(Info)'))
	liz.addContextMenuItems(context, replaceItems=False)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	return ok

def whattoplay(originalname,url,imdb_id,year):
	try: url = xbmc.getInfoLabel('ListItem.Trailer').split('videoid=')[1]
	except: url = ''
	if AddonsResolver == False: youtube.playtrailer(url,originalname)
	else:
		if getSetting("playwhat") == 'Trailer': youtube.playtrailer(url,originalname)
		else: addonsresolver.custom_choice(originalname,url,imdb_id,year)
		
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param
      
params=get_params()
url=None
name=None
originalname=None
mode=None
iconimage=None
index=None
imdb_id=None
year=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: originalname=urllib.unquote_plus(params["originalname"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass
try: imdb_id=urllib.unquote_plus(params["imdb_id"])
except: pass
try: year=urllib.unquote_plus(params["year"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "OriginalName: "+str(originalname)
print "Iconimage: "+str(iconimage)
print "Index: "+str(index)
print "imdb_id: "+str(imdb_id)
print "year: "+str(year)

if mode==None or url==None or len(url)<1: MAIN()
elif mode==1: youtube.playtrailer(url,name)
elif mode==2: whattoplay(originalname,url,imdb_id,year)
elif mode==3: latestreleases(index)
elif mode==4: IMDBmenu()
elif mode==5: IMDBlist(name,url)
elif mode==6: TMDBmenu()
elif mode==7: TMDBlist(index,url)
elif mode==8: xbmcgui.Dialog().ok('Cache',basic.removecache(cachePath))
elif mode==9: ToolsMenu()
elif mode==10: basic.settings_open('script.module.addonsresolver')
elif mode==11: IMDBlist2(index,url,originalname)
xbmcplugin.endOfDirectory(int(sys.argv[1]))