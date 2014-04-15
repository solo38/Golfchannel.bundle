NAME = "Golf Channel"
DEFAULT_THUMB = "http://resources-cdn.plexapp.com/image/source/com.plexapp.plugins.golfchannel.jpg"

####################################################################################################
def Start():

        ObjectContainer.title1 = NAME
        HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
@handler('/video/golfchannel', NAME)
def MainMenu():
        oc = ObjectContainer()
        
        # See not below as to why this is commented but should stay for now -- Gerk , Feb 9, 2014
        # oc.add(DirectoryObject(key=Callback(FeaturedShows), title="Featured Shows", thumb=DEFAULT_THUMB, summary="Shows currently featured on Gold Channel website.  May or may not have full episodes."))
        oc.add(DirectoryObject(key=Callback(FullEpisodes), title="Shows With Full Episodes", thumb=DEFAULT_THUMB, summary="Shows listed as having full episodes on Golf Channel site."))
        oc.add(DirectoryObject(key=Callback(FeaturedVideos), title="Featured Videos", thumb=DEFAULT_THUMB, summary="Videos featured on the Golf Channel website."))
        oc.add(DirectoryObject(key=Callback(LatestVideos, start=0), title="Latest Videos", thumb=DEFAULT_THUMB, summary="Latest videos posted on the Golf Channel website."))
        oc.add(InputDirectoryObject(key = Callback(Search), title="Search Golfchannel Videos", prompt="Search Videos"))
        return oc

####################################################################################################
@route("/video/golfchannel/fullepisodes")
def FullEpisodes():
	oc = ObjectContainer()
	oc.title2 = "Full Episodes"
	
	page = HTML.ElementFromURL("http://www.golfchannel.com/tv/#allShowsSec")
	
	for show in page.xpath("//div[contains(@class,'view-display-id-all_golf_channel_full_episodes')]//div[contains(@class,'views-field-title')]"):
		title = show.xpath(".//a/text()")[0]
		
		
		if show.xpath(".//a/@href")[0].startswith("http://"):
			url = show.xpath(".//a/@href")[0]
		else:
			url = "http://www.golfchannel.com%s" % show.xpath(".//a/@href")[0]
		
		thumb = show.xpath("..//img/@src")[0]
		summary = show.xpath("../div[contains(@class,'views-field-body')]//div[contains(@class,'field-content')]/text()")[0]

		oc.add(DirectoryObject(
			key = Callback(GetVideos,url=url,show=title),
			title = title,
			#thumb = Resource.ContentsOfURLWithFallback(thumb),
			thumb = thumb,
			summary = summary
		))
		
	return oc

####################################################################################################
# Until they put some sensible data on this page we're going to keep this commented out for now
# currently the data doesn't even give us show titles and to extrapolate from the URL is not a great
# approach, but let's leave this here in case they get it figured out -- Gerk, Feb 9, 2014
# @route("/video/golfchannel/featuredshows")
# def FeaturedShows():
# 	oc = ObjectContainer()
#	oc.title2 = "Featured Shows"
# 	
# 	page = HTML.ElementFromURL("http://www.golfchannel.com/tv/#allShowsSec")
# 	
# 	for show in page.xpath("//div[contains(@class,'view-display-id-all_golf_channel_tv_shows')]//div[contains(@class,'views-field-title')]"):
# 		title = show.xpath(".//a/text()")[0]
# 		
# 		
# 		if show.xpath(".//a/@href")[0].startswith("http://"):
# 			url = show.xpath(".//a/@href")[0]
# 		else:
# 			url = "http://www.golfchannel.com%s" % show.xpath(".//a/@href")[0]
# 		
# 		thumb = show.xpath("..//img/@src")[0]
# 		summary = show.xpath("../div[contains(@class,'views-field-field-schedule')]//div[contains(@class,'field-content')]/text()")[0]
# 
# 		oc.add(DirectoryObject(
# 			key = Callback(GetVideos,url=url,show=title),
# 			title = title, 
#			#thumb = Resource.ContentsOfURLWithFallback(thumb)
# 			thumb = thumb,
# 			summary = summary
# 		))
# 		
# 	return oc

####################################################################################################
@route("/video/golfchannel/featuredvideos")
def FeaturedVideos():
	oc = ObjectContainer()
	oc.title2 = "Featured Videos"

	page = HTML.ElementFromURL("http://www.golfchannel.com/media")
	for show in page.xpath("//div[contains(@class,'featured-video-photos')]//div[contains(@class,'views-row')]"):		
		# now we have to check to make sure this is a video
		# if the video xpath fails it's not a video!
		try: 
			video = show.xpath(".//span[contains(@class,'video')]")[0]		
			title = show.xpath(".//div[contains(@class,'views-field-title')]//a/text()")[0]
			url = "http://www.golfchannel.com%s" % show.xpath(".//a/@href")[0]
			thumb = show.xpath(".//img/@src")[0]
			oc.add(VideoClipObject(
				url = url,
				title = title,
				#thumb = Resource.ContentsOfURLWithFallback(thumb),
				thumb = thumb
			))
		except:
			continue

	return oc

####################################################################################################
@route("/video/golfchannel/latestvideos", start=int)
def LatestVideos(start=0):
	oc = ObjectContainer()
	oc.title2 = "Latest Videos"
	
	page = HTML.ElementFromURL("http://www.golfchannel.com/search/?&q=&submitSearch=&mediatype=Video&start=%i" % start)
	
	for video in page.xpath("//li[contains(@class,'ez-Video')]"):
		Log(video)
		thumb = video.xpath(".//img/@src")[0]
		title = video.xpath("string(.//div[contains(@class,'ez-main')]/a)")
		url = video.xpath(".//div[contains(@class,'ez-main')]/a/@href")[0]
		summary = video.xpath(".//p[contains(@class,'ez-desc')]/text()")[0]
		originally_available_at = Datetime.ParseDate(video.xpath(".//p[contains(@class,'ez-date')]/text()")[0]).date()

		oc.add(VideoClipObject(
			url = url,
			title = title,
			#thumb = Resource.ContentsOfURLWithFallback(thumb),
			thumb = thumb, 
			summary = summary, 
			originally_available_at = originally_available_at
		))
		
	if start < 499:
		oc.add(NextPageObject(key=Callback(LatestVideos, start=int(start+10)), title="Next Page"))

	return oc

####################################################################################################
@route("/video/golfchannel/getvideos")
def GetVideos(url, show):
	oc = ObjectContainer()
	oc.title2 = show
	
	page = HTML.ElementFromURL(url)
	for show in page.xpath("//div[contains(@class,'pane-gfc-tv-shows-individual-carrousels')]//li[contains(@class,'views-row')]//div[contains(@class,'views-field-title')]//a"):		
		# now we have to check to make sure this is a video
		# if the video xpath fails it's not a video!
		try: 
			video = show.xpath("../../..//span[contains(@class,'watermak_video_content_type')]")[0]		
			title = show.xpath("./text()")[0]
			url = "http://www.golfchannel.com%s" % show.xpath("./@href")[0]
			thumb = show.xpath("../../..//img/@src")[0]
			oc.add(VideoClipObject(
				url = url,
				title = title,
				#thumb = Resource.ContentsOfURLWithFallback(thumb)
				thumb = thumb
			))
		except:
			continue
	return oc

####################################################################################################
@route("/video/golfchannel/search")
def Search(query="golf"):
	Log.Debug("Search Query: "+query)
	return SearchVideos(query)
	
####################################################################################################
@route("/video/golfchannel/searchvideos")
def SearchVideos(query):
	oc = ObjectContainer()
	oc.title2 = "Search Golfchannel Videos"
	
	page = HTML.ElementFromURL("http://www.golfchannel.com/search/?&q=%s&submitSearch=+&mediatype=Video" % String.Quote(query, usePlus = True))
	
	for video in page.xpath("//li[contains(@class,'ez-Video')]"):
		thumb = video.xpath(".//img/@src")[0]
		title = video.xpath("string(.//div[contains(@class,'ez-main')]/a)")
		url = video.xpath(".//div[contains(@class,'ez-main')]/a/@href")[0]
		summary = video.xpath(".//p[contains(@class,'ez-desc')]/text()")[0]
		originally_available_at = Datetime.ParseDate(video.xpath(".//p[contains(@class,'ez-date')]/text()")[0]).date()

		oc.add(VideoClipObject(
			url = url,
			title = title,
			thumb = thumb, 
			summary = summary, 
			originally_available_at = originally_available_at
		))

	return oc
