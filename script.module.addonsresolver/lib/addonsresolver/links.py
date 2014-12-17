# Addons resolver
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
# MafaStudios@gmail.com

class link:
	def __init__(self):
		import base64
		self.rato_base = base64.urlsafe_b64decode('aHR0cDovL3d3dy5yYXRvdHYubmV0LyVz')
		self.rato_play = base64.urlsafe_b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnJhdG90di8/dXJsPSVzJm1vZGU9NDQmbmFtZT0lcw==')
		self.rato_search = self.rato_base % base64.urlsafe_b64decode('P2RvPXNlYXJjaCZzdWJhY3Rpb249c2VhcmNoJnNlYXJjaF9zdGFydD0xJnN0b3J5PSVz')
		
		self.genesis_play = base64.urlsafe_b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLmdlbmVzaXMvP2FjdGlvbj1wbGF5Jm5hbWU9JXMmdGl0bGU9JXMmeWVhcj0lcyZpbWRiPSVzJnVybD0lcw==')