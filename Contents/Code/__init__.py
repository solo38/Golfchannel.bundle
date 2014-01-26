NAME="Golf Channel"
DEFAULT_THUMB = "http://resources-cdn.plexapp.com/image/source/com.plexapp.plugins.golfchannel.jpg"

####################################################################################################
def Start():

        ObjectContainer.title1 = NAME
        HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
@handler('/video/golfchannel', NAME)
def MainMenu():
        oc = ObjectContainer()
        
        oc.add(DirectoryObject(key=Callback(FeaturedShows), title="Featured Shows", thumb=DEFAULT_THUMB, summary="Shows currently featured on golfchannel website.  May or may not have full episodes."))
        oc.add(DirectoryObject(key=Callback(FullEpisodes), title="Shows With Full Episodes", thumb=DEFAULT_THUMB, summary="Shows listed as having full episodes on golfchannel site."))
        oc.add(DirectoryObject(key=Callback(FeaturedVideos), title="Featured Videos", thumb=DEFAULT_THUMB, summary="Videos featured on the golfchannel website."))
        oc.add(DirectoryObject(key=Callback(LatestVideos, start=0), title="Latest Videos", thumb=DEFAULT_THUMB, summary="Latest videos posted on the golfchannel website."))
        
        return oc

####################################################################################################
@route("/video/golfchannel/fullepisodes")
def FullEpisodes():
	oc = ObjectContainer()
	
	page = HTML.ElementFromURL("http://www.golfchannel.com")
	
	for show in page.xpath("//h2[contains(.,'Full Episodes') or contains(.,'More full episodes')]/following-sibling::div//li/a"):
		title = show.xpath("./text()")[0]
		url = "http://www.golfchannel.com%s" % show.xpath("./@href")[0]

		oc.add(DirectoryObject(
			key = Callback(GetVideos,url=url,show=title),
			title = title, 
			thumb = DEFAULT_THUMB
		))
		
	return oc

####################################################################################################
@route("/video/golfchannel/featuredshows")
def FeaturedShows():
	oc = ObjectContainer()
	
	page = HTML.ElementFromURL("http://www.golfchannel.com")
	
	for show in page.xpath("//h2[contains(.,'Featured Shows')]/following-sibling::div//li/a"):
		title = show.xpath("./text()")[0]
		url = "http://www.golfchannel.com%s" % show.xpath("./@href")[0]
		
		oc.add(DirectoryObject(
			key = Callback(GetVideos,url=url,show=title),
			title = title, 
			thumb = DEFAULT_THUMB
		))
		
	return oc

####################################################################################################
@route("/video/golfchannel/featuredvideos")
def FeaturedVideos():
	oc = ObjectContainer()

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
				#thumb = Resource.ContentsOfURLWithFallback(thumb)
				thumb = thumb
			))
		except:
			continue

	return oc

####################################################################################################
@route("/video/golfchannel/latestvideos", start=int)
def LatestVideos(start=0):
	oc = ObjectContainer()
	
	page = HTML.ElementFromURL("http://www.golfchannel.com/search/?&q=&submitSearch=+&mediatype=Video&start=%i" % start)
	
	for video in page.xpath("//li[contains(@class,'ez-Video')]"):
		Log(video)
		thumb = video.xpath(".//img/@src")[0]
		title = video.xpath(".//div[contains(@class,'ez-main')]/a/text()")[0]
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
		
	if start < 499:
		oc.add(NextPageObject(key=Callback(LatestVideos, start=int(start+10)), title="Next Page"))

	return oc

####################################################################################################
@route("/video/golfchannel/getvideos")
def GetVideos(url, show):
	oc = ObjectContainer()
	
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