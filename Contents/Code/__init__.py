NAME="Golf Channel"

####################################################################################################
def Start():

        ObjectContainer.title1 = NAME
        HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
@handler('/video/golfchannel', NAME)
def MainMenu():
        return ShowList()

####################################################################################################
@route("/video/golfchannel/getshows")
def ShowList():
	oc = ObjectContainer()
	
	page = HTML.ElementFromURL("http://www.golfchannel.com/tv")
	
	for show in page.xpath("//div[contains(@class,'view-display-id-all_golf_channel_full_episodes')]//div[contains(@class,'views-row')]"):
		thumb = show.xpath(".//img/@src")[0]
		url = "http://www.golfchannel.com%s" % show.xpath(".//a/@href")[0]
		Log("url: "+url)
		title = show.xpath(".//div[contains(@class,'views-field-title')]//a/text()")[0]
		summary = show.xpath(".//div[contains(@class,'views-field-body')]/div[contains(@class,'field-content')]/text()")[0]
		Log("show: "+title)
		oc.add(DirectoryObject(
			key = Callback(GetVideos,url=url,show=title),
			title = title, 
			thumb = Resource.ContentsOfURLWithFallback(thumb),
			summary=summary
			
		))
		
	return oc
####################################################################################################
@route("/video/golfchannel/getvideos")
def GetVideos(url, show):
	oc = ObjectContainer()
	
	page = HTML.ElementFromURL(url)
	for show in page.xpath("//div[contains(@class,'pane-gfc-tv-shows-individual-carrousels')]//li[contains(@class,'views-row')]//div[contains(@class,'views-field-title')]//a"):		
		# now we have to check to make sure this is a video
		# watermak_video_content_type
		# if the video xpath fails it's not a video!
		try: 
			video = show.xpath("../../..//span[contains(@class,'watermak_video_content_type')]")[0]		
			title = show.xpath("./text()")[0]
			url = "http://www.golfchannel.com%s" % show.xpath("./@href")[0]
			thumb = show.xpath("../../..//img/@src")[0]
			oc.add(VideoClipObject(
				url = url,
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(thumb)
			))
		except:
			continue
	return oc