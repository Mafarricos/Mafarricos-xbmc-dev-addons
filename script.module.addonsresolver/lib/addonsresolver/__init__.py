# Addons resolver
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
# MafaStudios@gmail.com

def playparser(name, url, imdb_id, year):
	import xbmcgui,xbmc
	item = xbmcgui.ListItem(path=url)
	item.setProperty("IsPlayable", "true")
	xbmc.Player().play('plugin://plugin.video.genesis/?action=play&name='+name+'&title='+name+'&year='+year+'&imdb='+imdb_id+'&url='+url, item)