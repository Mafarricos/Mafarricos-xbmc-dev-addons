# Addons resolver
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
# MafaStudios@gmail.com

class link:
	def __init__(self):
		import base64
		self.rato_id = 'plugin.video.ratotv'		
		self.rato_base = base64.urlsafe_b64decode('aHR0cDovL3d3dy5yYXRvdHYubmV0LyVz')
		self.rato_play = base64.urlsafe_b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnJhdG90di8/dXJsPSVzJm1vZGU9NDQmbmFtZT0lcw==')
		self.rato_search = self.rato_base % base64.urlsafe_b64decode('P2RvPXNlYXJjaCZzdWJhY3Rpb249c2VhcmNoJnNlYXJjaF9zdGFydD0xJnN0b3J5PSVz')
		
		self.genesis_id = 'plugin.video.genesis'		
		self.genesis_play = base64.urlsafe_b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLmdlbmVzaXMvP2FjdGlvbj1wbGF5Jm5hbWU9JXMmdGl0bGU9JXMmeWVhcj0lcyZpbWRiPSVzJnVybD0lcw==')
		
		self.sdp_id = 'plugin.video.Sites_dos_Portugas'
		self.sdp_search = base64.urlsafe_b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLlNpdGVzX2Rvc19Qb3J0dWdhcy8/dXJsPUlNREIlc0lNREImbW9kZT05MDAwJm5hbWU9JXM=')
		
		self.wt_id = 'plugin.video.wt'
		self.wt_base = base64.urlsafe_b64decode('aHR0cDovL3d3dy53YXJlenR1Z2EudHYvJXM=')
		self.wt_play = base64.urlsafe_b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnd0Lz91cmw9JXMmbW9kZT01Jm5hbWU9JXM=')
		self.wt_search = base64.urlsafe_b64decode('aHR0cDovL3d3dy53YXJlenR1Z2EudHYvcGFnaW5hdGlvbi5hamF4LnBocD9wPTEmb3JkZXI9ZGF0ZSZ3b3Jkcz0lcyZtZWRpYVR5cGU9bW92aWVz')
		
		self.yts_search = base64.urlsafe_b64decode('aHR0cHM6Ly95dHMucmUvYXBpL2xpc3RpbWRiLmpzb24/aW1kYl9pZD0lcw==')
		
		self.kmediatorrent_id = 'plugin.video.kmediatorrent'
		self.kmediatorrent_play = base64.urlsafe_b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLmtvZGl0b3JyZW50L3BsYXkvJXM=')
		
		self.stream_id = 'plugin.video.stream'
		self.stream_play = base64.urlsafe_b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnN0cmVhbS9wbGF5LyVz')