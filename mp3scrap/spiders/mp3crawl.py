# -*- coding: utf-8 -*-
import scrapy
from ..items import Mp3MovieItem,Mp3SongsItem


class Mp3crawlSpider(scrapy.Spider):
    name = 'mp3'
    #allowed_domains = ['https://www.songs-mp3.net/']
    start_urls = ['https://www.songs-mp3.net/5/indipop-mp3-songs.html']
    domain = 'https://www.songs-mp3.net'

    def parse(self, response):
        sel=scrapy.Selector(response)

        #all_Movies_List,url = zip(sel.css('div#movie_cats ul li a::text').extract(),sel.css('div#movie_cats ul li a::attr(href)').extract())
        # getting the list in alphabatical order
        text=sel.css('div#movie_cats ul li a::text').extract()
        url=sel.css('div#movie_cats ul li a::attr(href)').extract()
        for (t,u) in zip(text,url):
            hit=self.domain+u
            print(t,hit)
            yield scrapy.Request(hit,callback=self.pdata)
    # getting the movie list of each alphabatical order
    def pdata(self,response):
        sel=scrapy.Selector(response)
        Movie_Songs=sel.css('div.list_inside_box ul li a *::attr(href)').extract()
        Movie_Name=sel.css('div.list_inside_box ul li a *::text').extract()
        for (name,url) in zip(Movie_Name,Movie_Songs):
            n=name.replace('Movie Mp3 Songs','').replace('Mp3 Songs','').replace(name[name.find('('):name.find(')')+1],'').replace('.','').strip()
            year = name[name.find('(') + 1:name.find(')')]
            Song_URL = self.domain + url
            # print('Movie Name : ',n,'Released On : ',year,'Songs URL : ',Song_URL)
            yield scrapy.Request(Song_URL, callback=self.sdata, meta={'M_Name': n, 'M_Year': year, 'M_URL': Song_URL})
    # getting songs details of each movie.
    def sdata(self, response):
        sel = scrapy.Selector(response)
        MovieItem=Mp3MovieItem()
        Mov_Details = sel.css('div.movie_details table tbody tr td.m_d_title3')
        Stars = ','.join([a for a in Mov_Details[0].css('a::text').extract()])
        Director = ','.join([a for a in Mov_Details[1].css('a::text').extract()])
        M_Director = ','.join([a for a in Mov_Details[2].css('a::text').extract()])
        Composer = ','.join([a for a in Mov_Details[3].css('a::text').extract()])
        Singer = ','.join([a for a in Mov_Details[4].css('a::text').extract()])
        name = response.meta['M_Name']
        year = response.meta['M_Year']
        url = response.meta['M_URL']
        # print('Movie Name :', name, 'Released On : ', year, 'Songs URL : ', url, 'Stars :', Stars, 'Director(s) :',
        #       Director, 'Music Director(s) :', M_Director, 'Composer :', Composer, 'Singer(s) :', Singer)
        MovieItem['name']=name
        MovieItem['year']=year
        MovieItem['url']=url
        MovieItem['Stars']=Stars
        MovieItem['Director']=Director
        MovieItem['M_Director']=M_Director
        MovieItem['Composer']=Composer
        MovieItem['Singer']=Singer
        yield MovieItem  # Storing movie details into database
        # Songs details item
        song_details = sel.css('div.items')
        SongItem=Mp3SongsItem()
        for song in song_details.css('div.link-item'):
            Song_name = song.css('div.link::text').extract_first()
            Song_URL = self.domain + song.css('a::attr(href)').extract_first()
            Song_Artist = ','.join([a for a in song.css('div.item-artist a::text').extract()])
            Song_Size = song.css('div.item-artist::text').extract_first().split(',')[0].split(':')[1].strip()
            #print('Song Name :', Song_name, 'Song URL :', Song_URL, 'Artist(s)', Song_Artist, 'Size :', Song_Size)
            # print(song.css('*').extract())
            SongItem['Mov_Name']=name
            SongItem['Title']=Song_name
            SongItem['url']=Song_URL
            SongItem['Artist']=Song_Artist
            SongItem['Size']=Song_Size
            yield SongItem  # Storing songs details into database
