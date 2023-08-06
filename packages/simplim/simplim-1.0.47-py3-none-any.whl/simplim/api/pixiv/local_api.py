import requests, _thread, subprocess
import json,simplim,math,os
from bs4 import BeautifulSoup as bs
from simplim.premium import *
from simplim.api import pixiv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

myCookies = ''
# host = '210.140.131.203'
# pximg_host = '210.140.92.138'
try:
	host = socket.gethostbyname('pixiv.com')
except:
	host = '210.140.92.186'
try:
	pximg_host = socket.gethostbyname('pximg.net')
except:
	pximg_host = '210.140.92.143'
test_url='https://'+host+'/artworks/79025298?format=json'
headers = pixiv.headers

def getIllustInfo(pid):
	response = requests.get('https://'+host+'/artworks/'+str(pid), headers={'Host':'www.pixiv.net'},verify=False)
	if response.status_code != 200:
		return
	text = response.text
	soup = bs(text,'lxml')
	#open('h.html','w').write(text)
	content = soup.find('meta',id='meta-preload-data').get('content')
	dict_ = json.loads(content)
	dict_ = simdict(dict_)
	dict_.illust = simdict(dict_.illust[str(pid)])
	dict_.__dict__['manga_urls'] = []
	if dict_.illust.pageCount > 1:
		dict_.__dict__['manga']=True
		for page in range(0, dict_.illust.pageCount):
			s = dict()
			for url in dict_.illust.urls:
				s[url] = dict_.illust.urls[url].replace('p0','p'+str(page))
			dict_.__dict__['manga_urls'].append(s)
	else:
		dict_.__dict__['manga']=False
	return dict_

def getIllustInfoCompatible(pid):
	info = getIllustInfo(pid)
	processed = empty()
	if not info:
		return
	illust = info.illust
	for uid in info.user:
		user = info.user[uid]
	extra = illust.extraData.meta
	processed.info		= info
	processed.title		= illust.illustTitle
	processed.caption	= illust.illustComment
	processed.tags		= [ tag['tag'] for tag in illust.tags.tags ]
	processed.urls		= illust.urls
	processed.mini		= illust.urls.mini
	processed.thumb		= illust.urls.thumb
	processed.small		= illust.urls.small
	processed.regular	= illust.urls.regular
	processed.original	= illust.urls.original
	processed.width		= illust.width
	processed.height	= illust.height
	processed.createDate= illust.createDate
	processed.uploadDate= illust.uploadDate
	processed.age_limit	= illust.xRestrict
	processed.user		= user
	processed.pid		= illust.illustId
	processed.is_manga	= illust.pageCount != 1
	processed.manga		= []
	if processed.is_manga:
		pages	= range(1,illust.pageCount+1)
		for page in pages:
			processed.manga.append(processed.original.replace('p0','p'+str(page)))
	return simdict(processed.__dict__)

def getIllustUrls(pid):
	info = getIllustInfo(pid)
	if not info:
		return
	return info.illust.urls, info.manga_urls, info

def getIllust(pid, path='', use_curl=True, setting='original'):
	info = getIllustInfo(pid)
	if not info:
		return
	title= info.illust.title
	urls, manga_urls = info.illust.urls, info.manga_urls

	if manga_urls:
		print(manga_urls)
		if not path:
			path = title
		if not os.path.exists(path):
			os.mkdir(path)
		cnt=0
		for manga_url in manga_urls:
			ret = simplim.multiThreadDownload(url=manga_url[setting].replace('i.pximg.net',pximg_host),headers=pixiv.headers,path=os.path.join(path,str(cnt)+'.jpg'),verify=False)
			if not ret:
				# d=simplim.download(url=manga_url[setting],headers=pixiv.headers,need_content_length)
				# open(os.path.join(path,str(cnt)+'.jpg'),'wb').write(d.getvalue()).close()
				pixiv.getImg(url=manga_url[setting].replace('i.pximg.net',pximg_host),name=str(cnt),path=path,useCurl=use_curl)
			cnt+=1
	else:
		print(urls)
		if not path:
			path = './'
		ret = simplim.multiThreadDownload(url=urls[setting].replace('i.pximg.net',pximg_host),headers=pixiv.headers,path=os.path.join(path,title+'.jpg'),verify=False)
		if not ret:
			pixiv.getImg(url=urls[setting].replace('i.pximg.net',pximg_host), name=title,path=path,useCurl=use_curl)

def getIllustByUrl(url,path='',use_curl=False):
	# pixiv.getImg(url = url.replace('i.pximg.net',pximg_host),name=simplim.gettemp(),path=path,useCurl=use_curl)
	if use_curl:
		open(path,'wb').write(requests.get(url.replace('i.pximg.net',pximg_host), headers=headers, verify=False).content)
	else:
		simplim.multiThreadDownload(url=url.replace('i.pximg.net',pximg_host),headers=pixiv.headers,path=path,verify=False)

def getUserLikedWorks(pid,use_curl = False):
	headers = {
		'host':'www.pixiv.net',
		'cookie': myCookies
	}
	params = {
		'tag':'',
		'offset': '0',
		'limit': '100',
		'rest':'show',
		'lang':'zh'
	}
	# ?tag=&offset=0&limit=48&rest=show&lang=zh
	response = requests.get('https://'+host+'/ajax/user/'+str(pid)+'/illusts/bookmarks', params = params, headers = headers, verify=False)
	if response.status_code == 200:
		if response.json()['error']:
			return
	else:
		return
	print(response.json())
	sd = simdict(response.json())
	total = sd.body.total
	works = sd.body.works
	limit = int(params['limit'])
	pages = total/limit
	print('\n\n\n'+str(total)+'\n\n\n')
	if pages>1:
		pages = range(0,int(pages))
		offset = 0
		for page in pages:
			offset += limit
			params['offset']=str(offset)
			while 1:
				try:
					response = requests.get('https://'+host+'/ajax/user/'+str(pid)+'/illusts/bookmarks', params = params, headers = headers, verify=False,timeout=10)
					break
				except:
					print('agian')
			sd = simdict(response.json())
			works += sd.body.works
		final = simdict({'works': works})
		final.dump('liked_works.'+str(pid)+'.'+simplim.gettemp()+'.json')
		return final
		# params['limit']=str(total)
		# response = requests.get('https://'+host+'/ajax/user/'+str(pid)+'/illusts/bookmarks', params = params, headers = headers, verify=False)
		# sd = simdict(response.json())
		# sd.dump(str(pid)+'.'+simplim.gettemp()+'.json')
	sd.body.works.dump(str(pid)+'.'+simplim.gettemp()+'.json')
	return sd

def getMainPage(cookie=myCookies):
	headers = {
		'host':'www.pixiv.net',
		'referer':'https://www.pixiv.net',
		'cookie': cookie
	}
	url = 'https://'+host+'/ajax/top/illust?mode=all&lang=zh'
	response=requests.get(url, headers = headers, verify=False)
	print(response.status_code)
	if response.status_code == 200:
		if not response.json()['error']:
			return response.json()

def getUserFollowingUsers(pid):
	headers = {
		'host':'www.pixiv.net',
		'cookie': myCookies,
		'tag':'',
		'offset':'0',
		'limit':'24',
		'rest':'show',
		'lang':'zh'
	}
	# ?offset=0&limit=24&rest=show&tag=&lang=zh
	response=requests.get('https://'+host+'/ajax/user/'+str(pid)+'/following', headers = headers, verify=False)
	text = response.json()
	sd = simdict(text)
	total = sd.body.total
	users = sd.body.users
	limit = headers['limit']
	pages = total/limit
	#open('h.html','w').write(text)
	# content = soup.find('meta',id='meta-preload-data').get('content')
	# dict_ = json.loads(content)
	# dict_ = simdict(dict_)
	return soup

def getRank(mode='daily', page=1, content=''):
	'''
	mode
		daily
		weekly
		monthly
		rookie
		original
		male
		female
	content
		all
			all mode
		illust
			daily - rookie
		ugoira
			daily - weekly
		manga
			daily - rookie
	'''
	valid_mode = {
		'all': ['daily','weekly','monthly','rookie','original','male','female'],
		'illust': ['daily','weekly','monthly','rookie'],
		'ugoira': ['daily','weekly'],
		'manga': ['daily','weekly','monthly','rookie']
	}
	url = 'https://'+host+'/ranking.php'
	params = {
		'mode': mode,
		'p': str(page),
		'format': 'json'
	}
	if content:
		if mode not in valid_mode[content]:
			return
		else:
			params['content'] = content
	response = requests.get(url, params=params, headers={'Host':'www.pixiv.net'}, verify=False)
	if response.status_code == 200:
		if 'error' not in response.json():
			return response.json()

def getIllustRecommend(pid, limit=18):
	url = 'https://'+host+'/ajax/illust/'+str(pid)+'/recommend/init?limit='+str(limit)+'&lang=zh'
	response = requests.get(url, headers={'Host':'www.pixiv.net', 'cookie':myCookies, 'referer':'https://www.pixiv.net/artworks/'+str(pid)}, verify=False)
	if response.status_code == 200:
		if not response.json()['error']:
			return response.json()

def getMuiltiIllustsThumb(ids):
	url='https://'+host+'/ajax/illust/recommend/illusts'
	illust_ids = []
	for pid in ids:
		illust_ids.append('illust_ids%5B%5D='+str(pid))
	print('&'.join(illust_ids))
	url+='?'+'&'.join(illust_ids)+'&lang=zh'
	response = requests.get(url, headers={'Host':'www.pixiv.net'}, verify=False)
	if response.status_code == 200:
		if not response.json()['error']:
			return response.json()

def getLatestIllusts(page=1):
	url='https://'+host+'/bookmark_new_illust.php'
	params = {
		'p': page
	}
	response = requests.get(url,params=params, headers={'Host':'www.pixiv.net', 'cookie':myCookies}, verify=False)
	if response.status_code == 200:
		idname = 'js-mount-point-latest-following'
		text = response.text
		lxml = bs(text.replace('&quot;','\''),'lxml')
		data = lxml.find(id=idname).get('data-items')
		return json.loads(data.replace('\'','\"'))

def search(word,s_type='artworks',order='date_d',mode='all',p=1,s_mode='s_tag',type_='all',lang='zh',wlt=0,hlt=0):
	'''
		word: #url need to replace ' ' to %20
			mainWord -doninclude -anotherDoninclude (include OR anotherInclude)
			
			特殊词汇/标签
			オリジナル 原创
			10000users入り 10000以上收藏
			オリジナル10000users入り 原创10000以上收藏
			# 可以直接做成收藏筛选
			# 也可以做成搜索小提示
		s_type:
			artworks: 所有
			manga: 漫画
				type: manga
			illustrations: 插画，动图（继续用type定义）
				type: illust
					  ugoira
					  illust_and_ugoira

		order:
			date 正序
			date_d/任意 倒序
		mode:
			
		s_mode:
			s_tag
			s_tag_full
			s_tc

		ratio:
			0 正方形
			0.5 横
			-0.5 纵

		wlt: width 最小限制
		hlt: height 最小限制
		wgt: 最大
		hgt: 最大
		tool: 工具
			所有的制图工具
			SAI
			Photoshop
			CLIP STUDIO PAINT
			IllustStudio
			ComicStudio
			Pixia
			AzPainter4
			Painter
			Illustrator
			GIMP
			FireAlpaca
			網上描繪
			AzPainter
			CGillust
			描繪聊天室
			手畫博克
			MS_Paint
			PictBear
			openCanvas
			PaintShopPro
			EDGE
			drawr
			COMICWORKS
			AzDrawing
			SketchBookPro
			PhotoStudio
			Paintgraphic
			MediBang Paint
			NekoPaint
			Inkscape
			ArtRage
			AzDrawing4
			Fireworks
			ibisPaint
			AfterEffects
			mdiapp
			GraphicsGale
			Krita
			kokuban.in
			RETAS STUDIO
			emote
			4thPaint
			ComiLabo
			pixiv Sketch
			Pixelmator
			Procreate
			Expression
			PicturePublisher
			Processing
			Live2D
			dotpict
			Aseprite
			Poser
			Metasequoia
			Blender
			Shade
			3dsMax
			DAZ Studio
			ZBrush
			Comi Po!
			Maya
			Lightwave3D
			六角大王
			Vue
			SketchUp
			CINEMA4D
			XSI
			CARRARA
			Bryce
			STRATA
			Sculptris
			modo
			AnimationMaster
			VistaPro
			Sunny3D
			3D-Coat
			Paint 3D
			VRoid Studio
			筆芯筆
			鉛筆
			原子筆
			毫筆
			顏色鉛筆
			Copic麥克筆
			沾水筆
			透明水彩
			毛筆
			毛筆
			記號筆
			麥克筆
			水溶性彩色铅笔
			涂料
			丙烯顏料
			鋼筆
			粉彩
			噴筆
			顏色墨水
			蠟筆
			油彩
			COUPY-PENCIL
			顏彩
			蠟筆

		scd=2021-02-04 #开始时间 
		ecd=2021-03-05 #结束时间
	'''
	url ='https://'+host+'/ajax/search/'+s_type+'/'+word
	params = {
		'word':word,
		'order':order,
		'mode':mode,
		'p':p,
		's_mode':s_mode,
		'type':type_,
		'lang':lang
	}
	response = requests.get(url, params=params, headers={'Host':'www.pixiv.net'},verify=False)
	return response

# m = getUserLikedWorks(myId)
# m = getUserFollowingUsers(myId)

# z=requests.get('https://210.140.131.203/ajax/user/37265945/illusts/bookmarks?offset=0&limit=24&rest=show&tag=金的&lang=zh', headers={'host':'www.pixiv.net','cookie':myCookies}, verify=False)

# x=getUserLikedWorks(myId,0)
# print(len(x.works))
