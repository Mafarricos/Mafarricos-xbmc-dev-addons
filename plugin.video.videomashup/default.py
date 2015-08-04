import xbmcaddon

__plugin__ = 'VideoMashUp'
__author__ = 'Mafarricos'
__svn_url__ = 'http://xbmc-adult.googlecode.com/svn/trunk/plugin.video.videomashup/'
__credits__ = 'sfaxman'
__version__ = '1.7.37'

addon = xbmcaddon.Addon(id='plugin.video.videomashup')
rootDir = addon.getAddonInfo('path')
if rootDir[-1] == ';':
    rootDir = rootDir[0:-1]

class Main:
    def __init__(self):
        self.pDialog = None
        self.curr_file = ''
        self.run()

    def run(self):
        import videomashup
        videomashup.Main()

win = Main()
