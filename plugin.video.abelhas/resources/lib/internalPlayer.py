# -*- coding: utf-8 -*-

""" abelhas.pt
    2015 fightnight"""

import xbmc,xbmcaddon,xbmcgui,os,xbmcvfs,re

addon_id = 'plugin.video.abelhas'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
track = selfAddon.getSetting('track-player')

class Player(xbmc.Player):
	def __init__(self,title):
		xbmc.Player.__init__(self)
		print title
		try: self.title=re.sub('[^-a-zA-Z0-9_\.()\\\/ ]+', ' ',  re.compile("\[COLOR .+?\](.+?)\[/COLOR\]").findall(title)[0])
		except: self.title=re.sub('[^-a-zA-Z0-9_\.()\\\/ ]+', ' ',  title)
		self.playing = True
		self.time = 0
		self.totalTime = 0
		if track == 'true':
			try: self.id = self.title
			except: self.id = None
			if not xbmcvfs.exists(os.path.join(datapath,'trackplayer')): xbmcvfs.mkdir(os.path.join(datapath,'trackplayer'))
			if self.id: self.filemedia = os.path.join(datapath,'trackplayer',str(self.id)+'.txt')
			else: self.filemedia = None

	def onPlayBackStarted(self):
		print 'player Start'
		self.totalTime = self.getTotalTime()
		print 'total time',self.totalTime
		if track == 'true' and self.isPlayingVideo():
			if xbmcvfs.exists(self.filemedia):
				print "Existe um bookmark de visualizacao anterior..."
				tracker=readfile(self.filemedia)
				opcao=xbmcgui.Dialog().yesno("Abelhas", 'Existe um registo de visualização anterior.','Continuar a partir de '+ ' %s?' % (format_time(float(tracker))),'', 'Não', 'Sim')
				if opcao: self.seekTime(float(tracker))

	def onPlayBackStopped(self):
		print 'player Stop'
		self.playing = False
		time = int(self.time)
		print 'self.time/self.totalTime='+str(self.time/self.totalTime)
		if (self.time/self.totalTime > 0.90):
			if track == 'true' and self.isPlayingVideo():
				try: xbmcvfs.delete(self.filemedia)
				except: pass

	def onPlayBackEnded(self):
		self.onPlayBackStopped()

	def track_time(self):
		try:
			if track == 'true' and self.isPlayingVideo():
				self.time = self.getTime()
				save(self.filemedia,str(self.time))
		except: pass

def save(filename, contents):
    try:
        fh = open(filename, 'wb')
        fh.write(contents)  
        fh.close()
    except:
		try:
			fh = xbmcvfs.File(filename, 'w')
			fh.write(str(contents))
			fh.close()
		except: print "Nao gravou os temporarios de: %s" % (filename)

def readfile(filename):
    try:
        f = open(filename, "r")
        string = f.read()
        return string
    except:
        traceback.print_exc()
        print "Nao abriu conteudos de: %s" % filename
        return None

def format_time(seconds):
    minutes,seconds = divmod(seconds, 60)
    if minutes > 60:
        hours,minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else: return "%02d:%02d" % (minutes, seconds)