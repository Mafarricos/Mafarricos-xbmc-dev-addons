# -*- coding: UTF-8 -*-
# by Mafarricos
# email: MafaStudios@gmail.com
# This program is free software: GNU General Public License

class link:
	def __init__(self):
		import base64
		self.omdbapi_info = 'http://www.omdbapi.com/?plot=short&r=json&i=%s'
		
		self.tmdb_base = 'http://api.themoviedb.org/3/movie/%s'
		self.tmdb_image = 'http://image.tmdb.org/t/p/%s'
		self.tmdb_key = base64.urlsafe_b64decode('ODFlNjY4ZTdhMzdhM2Y2NDVhMWUyMDYzNjg3ZWQ3ZmQ=')
		self.tmdb_info = self.tmdb_base % ('%s?language=%s&api_key='+self.tmdb_key)
		self.tmdb_info_default = self.tmdb_base % ('%s?append_to_response=trailers,credits&api_key='+self.tmdb_key)
		self.tmdb_info_default_alt = self.tmdb_base % ('%s?language=ge&append_to_response=trailers,credits&api_key='+self.tmdb_key)
		self.tmdb_theaters = self.tmdb_base % ('now_playing?page=%s&api_key='+self.tmdb_key)
		self.tmdb_upcoming = self.tmdb_base % ('upcoming?page=%s&api_key='+self.tmdb_key)
		self.tmdb_popular = self.tmdb_base % ('popular?page=%s&api_key='+self.tmdb_key)
		self.tmdb_top_rated = self.tmdb_base % ('top_rated?page=%s&api_key='+self.tmdb_key)			
		self.tmdb_backdropbase = self.tmdb_image % ('original%s')
		self.tmdb_posterbase = self.tmdb_image % ('w500%s')
		self.tmdb_discover = 'http://api.themoviedb.org/3/discover/movie?page=%s&sort_by=popularity.desc&api_key='+self.tmdb_key
		self.tmdb_search ='http://api.themoviedb.org/3/search/movie?include_adult=false&query=%s&api_key='+self.tmdb_key
		self.youtube_trailer_search = 'http://gdata.youtube.com/feeds/api/videos?q=%s-trailer&start-index=1&max-results=1&v=2&alt=json&hd'
		self.youtube_plugin = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'
		
		self.imdb_top250 = 'http://akas.imdb.com/chart/top'
		self.imdb_bot100 = 'http://akas.imdb.com/chart/bottom'
		self.imdb_theaters = 'http://www.imdb.com/movies-in-theaters/'
		self.imdb_comming_soon = 'http://www.imdb.com/movies-coming-soon/'	
		self.imdb_popular = 'http://akas.imdb.com/search/title?sort=moviemeter,asc&title_type=feature,tv_movie&count=30&start=%s'
		self.imdb_popularbygenre = 'http://akas.imdb.com/search/title?sort=moviemeter,asc&title_type=feature,tv_movie&count=30&start=%s&genres=%s'
		self.imdb_boxoffice = 'http://akas.imdb.com/search/title?sort=boxoffice_gross_us&title_type=feature,tv_movie&count=30&start=%s'
		self.imdb_most_voted = 'http://akas.imdb.com/search/title?sort=num_votes&title_type=feature,tv_movie&count=30&start=%s'
		self.imdb_oscars = 'http://akas.imdb.com/search/title?count=30&groups=oscar_best_picture_winners&sort=year,desc&start=%s'
		self.imdb_amazon = 'http://rss.imdb.com/list/ls002595589'
		self.imdb_dvd = 'http://rss.imdb.com/list/ls075513547'
		self.imdb_api_search = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s'
		self.imdb_years = 'http://akas.imdb.com/search/title?title_type=feature,tv_movie&sort=boxoffice_gross_us&count=30&start=%s&year=%s,%s'
		self.imdb_genre = 'http://www.imdb.com/chart/'