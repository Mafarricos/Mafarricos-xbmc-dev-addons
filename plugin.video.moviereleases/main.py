# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

import xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,threading,urllib2,re,json,urllib,base64
from BeautifulSoup import BeautifulSoup

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
dataPath            = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo("profile")).decode("utf-8")
cachePath			= os.path.join(dataPath,'cache')
sitesfile 			= os.path.join(os.path.join(addonPath, 'resources'),'sites.txt')
sitecachefile 		= os.path.join(cachePath,'_cache.txt')
getSetting          = xbmcaddon.Addon().getSetting
sites 				= ['http://irfree.com/movies/page/','http://sceper.ws/category/movies/page/','http://www.scnsrc.me/category/films/page/']

if not os.path.exists(dataPath): os.makedirs(dataPath)
if not os.path.exists(cachePath): os.makedirs(cachePath)

def MAIN(index):
	addDir('Latest Releases','Latest Releases',3,'',True,1,'','','','')
	addDir('IMDB','IMDB',4,'',True,1,'','','','')

def IMDBmenu():
	addDir('In Theaters','http://www.imdb.com/movies-in-theaters/',5,'',True,1,'','','','')
	addDir('Comming Soon','http://www.imdb.com/movies-coming-soon/',5,'',True,1,'','','','')
def IMDBlist(name,url):
	xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	results = getimdblinks(url,[],1,'IMDB')
	populateDir(results,1)
	
def latestreleases(index):
	xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	threads = []	
	results = []
	try: ranging = int(index)+1
	except: 
		ranging = 1
		open(sitecachefile, 'w').close()
	for i in range(ranging, ranging+int(getSetting('pages-num'))):
		for site in sites: threads.append(threading.Thread(name=site+str(i),target=getimdblinks,args=(site+str(i)+'/',results,i*100, )))
	ranging = i
	[i.start() for i in threads]
	[i.join() for i in threads]
	populateDir(results,ranging)
	addDir('Next>>','Next>>',3,'',True,1,'',ranging,'','')		

def populateDir(results,ranging):
	unique_stuff = []
	threads2 = []	
	list = []
	order = 0	
	results = sorted(results, key=getKey)
	for order,link in results:
		if link not in str(unique_stuff): unique_stuff.append([order, link])
	chunks=[unique_stuff[x:x+10] for x in xrange(0, len(unique_stuff), 10)]
	for i in range(0,len(chunks)): threads2.append(threading.Thread(name='chunks'+str(i),target=populatelist,args=(chunks[i],list, )))
	[i.start() for i in threads2]
	[i.join() for i in threads2]
	list = sorted(list, key=getKey)
	linecache= readalllines(sitecachefile)
	for order,title,poster,information,imdb_id,year in list:
		if title not in str(linecache):
			writefile(sitecachefile,"a",'::pageindex::'+str(ranging)+'::'+title.encode('ascii', 'xmlcharrefreplace')+'::\n')
			addDir(title,title,2,poster,False,len(list),information,ranging,imdb_id,year)
		elif '::pageindex::'+str(ranging)+'::'+title.encode('ascii', 'xmlcharrefreplace') in str(linecache): addDir(title,title,2,poster,False,len(list),information,ranging,imdb_id,year)

def populatelist(results,list):
	for index,link in results:
		dur = ''
		ttcode = re.findall('tt(\d+)', link, re.DOTALL)
		try:
			tmdb_image = 'http://image.tmdb.org/t/p/w500'		
			tmdb_key = base64.urlsafe_b64decode('ODFlNjY4ZTdhMzdhM2Y2NDVhMWUyMDYzNjg3ZWQ3ZmQ=')
			tmdb_info = 'http://api.themoviedb.org/3/movie/tt'+str(ttcode[0])+'?language=en&api_key='+tmdb_key
			jsonpage = abrir_url(tmdb_info)
			jsondata = json.loads(jsonpage)
			Year = re.findall('(\d+)-\d+-\d+', jsondata['release_date'], re.DOTALL)
			listgenre = []
			for genre in jsondata['genres']: listgenre.append(genre['name'])
			strgenre = ', '.join(listgenre)
			liststudios = []
			for studios in jsondata['production_companies']: liststudios.append(studios['name'])
			try: strstudios = liststudios[0]
			except: strstudios = ''
			informacao = {"code": jsondata['imdb_id'], "title": jsondata['title'], "originaltitle": jsondata['original_title'], "year": Year[0], "rating": jsondata['vote_average'], "plot": jsondata['overview'] , "genre": strgenre, "votes": jsondata['vote_count'], "duration": jsondata['runtime'], "studio": strstudios}
			if getSetting('allyear') == 'true': list.append([index,jsondata['title']+' ('+Year[0]+')',tmdb_image+jsondata['poster_path'],informacao,ttcode[0],Year[0]])
			elif int(Year[0]) >= int(getSetting('minyear')) and int(Year[0]) <= int(getSetting('maxyear')): list.append([index,jsondata['title']+' ('+Year[0]+')',tmdb_image+jsondata['poster_path'],informacao,ttcode[0],Year[0]])
		except:
			jsonpage = abrir_url('http://www.omdbapi.com/?plot=short&r=json&i=tt'+str(ttcode[0]))
			jsondata = json.loads(jsonpage)
			actors = jsondata['Actors'].split(', ')
			duration = re.findall('(\d+) min', jsondata['Runtime'], re.DOTALL)
			if duration: dur = duration[0]
			duration = re.findall('(\d) h', jsondata['Runtime'], re.DOTALL)
			if duration: dur = int(duration[0])*60
			informacao = {"code": jsondata['imdbID'], "title": jsondata['Title'], "originaltitle": jsondata['Title'], "year": jsondata['Year'], "rating": jsondata['imdbRating'], "plot": jsondata['Plot'] , "genre": jsondata['Genre'], "director": jsondata['Director'], "writer": jsondata['Writer'], "cast": actors, "votes": jsondata['imdbVotes'], "mpaa": jsondata['Rated'], "duration": dur}
			if getSetting('allyear') == 'true': list.append([index,jsondata['Title']+' ('+jsondata['Year']+')',jsondata['Poster'],informacao,ttcode[0],jsondata['Year']])
			elif int(jsondata['Year']) >= int(getSetting('minyear')) and int(jsondata['Year']) <= int(getSetting('maxyear')): list.append([index,jsondata['Title']+' ('+jsondata['Year']+')',jsondata['Poster'],informacao,ttcode[0],jsondata['Year']])

def getimdblinks(url,results,order,Source=None):
	try:
		html_page = abrir_url(url)
		soup = BeautifulSoup(html_page)
		if Source == 'IMDB':
			for link in soup.findAll('a', attrs={'href': re.compile("^/title/.+?/\?ref_=.+?_ov_tt")}):
				results.append([order, link.get('href').replace('?ref_=ttmd_md_nm','')])
				order += 1			
		else:
			for link in soup.findAll('a', attrs={'href': re.compile("^http://.+?/title")}):
				results.append([order, link.get('href').replace('?ref_=ttmd_md_nm','')])
				order += 1
		return results
	except BaseException as e: print '##ERROR-##getimdblinks: '+url+' '+str(e)

def readalllines(file):
	f = open(file,"r")
	lines = f.readlines()
	f.close()
	return lines

def writefile(file,mode,string):
	writes = open(file, mode)
	writes.write(string)
	writes.close()
	
def abrir_url(url, encoding='utf-8'):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:10.0a1) Gecko/20111029 Firefox/10.0a1')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	if encoding != 'utf-8': link = link.decode(encoding).encode('utf-8')
	return link
	
def addDir(name,url,mode,iconimage,pasta,total,informacao,index,imdb_id,year):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('ascii', 'xmlcharrefreplace'))+"&index="+str(index)+"&imdb_id="+str(imdb_id)+"&year="+str(year)
	ok=True
	context = []
	context.append(('Ver Trailer', 'RunPlugin(%s?mode=1&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image',iconimage)
	if informacao <> '': liz.setInfo( type="Video", infoLabels=informacao )	
	liz.addContextMenuItems(context, replaceItems=False)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

def getKey(item):
	return item[0]

def playparser(name, url, imdb_id, year):
	item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
	xbmc.Player().play('plugin://plugin.video.genesis/?action=play&name='+name+'&title='+name+'&year='+year+'&imdb='+imdb_id+'&url='+url, item)

#trailer,sn
def trailer(name, url):
	url = trailer2().run(name, url)
	if url == None: return
	item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
	xbmc.Player().play(url, item)

class trailer2:
    def __init__(self):
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_query = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def run(self, name, url):
        try:
            if url.startswith(self.youtube_base):
                url = self.youtube(url)
                if url == None: raise Exception()
                return url
            elif not url.startswith('http://'):
                url = self.youtube_watch % url
                url = self.youtube(url)
                if url == None: raise Exception()
                return url
            else:
                raise Exception()
        except:
            url = self.youtube_query + name + ' trailer'
            url = self.youtube_search(url)
            if url == None: return
            return url

    def youtube_search(self, url):
        try:
            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url= url.split('[/B]')[0].replace('[B]','')
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url, timeout='10').result
            result = parseDOM(result, "entry")
            result = parseDOM(result, "id")
			
            for url in result[:5]:
                url = url.split("/")[-1]	
                url = self.youtube_watch % url
                url = self.youtube(url)
                if not url == None: return url
        except: return

    def youtube(self, url):
        try:
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(self.youtube_info % id, timeout='10').result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(self.youtube_watch % id, timeout='10').result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='5'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

def parseDOM(html, name=u"", attrs={}, ret=False):
    if isinstance(name, str): # Should be handled
        try:  name = name #.decode("utf-8")
        except: pass

    if isinstance(html, str):
        try: html = [html.decode("utf-8")] # Replace with chardet thingy
        except: html = [html]
    elif isinstance(html, unicode): html = [html]
    elif not isinstance(html, list): return u""

    if not name.strip(): return u""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item: item = item.replace(match, match.replace("\n", " "))

        lst = _getDOMElements(item, name, attrs)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                lst2 += _getDOMAttributes(match, name, ret)
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                temp = _getDOMContent(item, name, match, ret).strip()
                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    return ret_lst

def _getDOMContent(html, name, match, ret):  # Cleanup

    endstr = u"</" + name  # + ">"

    start = html.find(match)
    end = html.find(endstr, start)
    pos = html.find("<" + name, start + 1 )

    while pos < end and pos != -1:  # Ignore too early </endstr> return
        tend = html.find(endstr, end + len(endstr))
        if tend != -1:
            end = tend
        pos = html.find("<" + name, pos + 1)

    if start == -1 and end == -1:
        result = u""
    elif start > -1 and end > -1:
        result = html[start + len(match):end]
    elif end > -1:
        result = html[:end]
    elif start > -1:
        result = html[start + len(match):]

    if ret:
        endstr = html[end:html.find(">", html.find(endstr)) + 1]
        result = match + result + endstr

    return result

def _getDOMAttributes(match, name, ret):
    lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
    if len(lst) == 0:
        lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
    ret = []
    for tmp in lst:
        cont_char = tmp[0]
        if cont_char in "'\"":

            # Limit down to next variable.
            if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

            # Limit to the last quotation mark
            if tmp.rfind(cont_char, 1) > -1:
                tmp = tmp[1:tmp.rfind(cont_char)]
        else:
            if tmp.find(" ") > 0:
                tmp = tmp[:tmp.find(" ")]
            elif tmp.find("/") > 0:
                tmp = tmp[:tmp.find("/")]
            elif tmp.find(">") > 0:
                tmp = tmp[:tmp.find(">")]

        ret.append(tmp.strip())

    return ret

def _getDOMElements(item, name, attrs):
    lst = []
    for key in attrs:
        lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
        if len(lst2) == 0 and attrs[key].find(" ") == -1:  # Try matching without quotation marks
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

        if len(lst) == 0:
            lst = lst2
            lst2 = []
        else:
            test = range(len(lst))
            test.reverse()
            for i in test:  # Delete anything missing from the next list.
                if not lst[i] in lst2:
                    del(lst[i])

    if len(lst) == 0 and attrs == {}:
        lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
        if len(lst) == 0:
            lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

    return lst
#trailer,en
	
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
mode=None
iconimage=None
index=None
imdb_id=None
year=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
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
print "Iconimage: "+str(iconimage)
print "Index: "+str(index)
print "imdb_id: "+str(imdb_id)
print "year: "+str(year)

if mode==None or url==None or len(url)<1: MAIN(index)
elif mode==1: trailer(name,url)
elif mode==2: playparser(name,url,imdb_id,year)
elif mode==3: latestreleases(index)
elif mode==4: IMDBmenu()
elif mode==5: IMDBlist(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))