from bs4 import BeautifulSoup
import requests, re
from comment_builder import build_comment

MINIMUM_SIMILARITY_PERCENTAGE = 57
MAX_DELTA = 20

def create_link_dictionary(soup):
	dic = {}
	first = True
	top_similarity_percentage = 0.0
	# Creator - boorus; Material - boorus; Author - DeviantArt; Member - Pixiv
	
	# Filters to only show relevant results.
	results = soup.find_all('div', class_='result')
	# print(results)
	if not results:
		return dic
	
	# print(results)
	# for idx, val in enumerate(ints): use to find first entry
	# print(results)
	for result in results:
		# print(result)
		# with open("reslut.html", "a", encoding="utf-8") as f:
		# 	f.write(f"{result}\n")
		# Skip "hidden results" result
		if result.get('id') is not None:
			continue
		
		if first:
			top_similarity_percentage = float(result.find(class_='resultsimilarityinfo').text[:-1])
			first = False
		# Skip all further results if they are low quality matches
		similarity_percentage = float(result.find(class_='resultsimilarityinfo').text[:-1])
		if similarity_percentage < MINIMUM_SIMILARITY_PERCENTAGE or top_similarity_percentage-MAX_DELTA>similarity_percentage:
			break

		# print(similarity_percentage)

		# Make assumption about content based on preview image url /frames/ = anidb, /dA/ = deviantart, /res/pixiv/ = pixiv, /booru/ = danbooru/gelbooru, /res/nhentai = nhentai
		image_url = result.table.tr.td.div.a.img.get('src')
		if re.search(r'/res/nhentai/', image_url):
		#nHentai Block
			if not dic.get('type'):
				dic.update({'type': 'nhentai'})
			gallery_number = re.search(r'(?<=\/nhentai\/)\d+', image_url)
			if gallery_number:
				dic.update({'gallery_number': gallery_number.group(0)})
			page_number = re.search(r'(?<=\/)\d+(?=\.jpg)', image_url)
			if page_number:
				dic.update({'page_number': page_number.group(0)})
			title = result.find('div', class_='resulttitle').strong.text
			if title and dic.get('title') == None:
				dic.update({'title': title})
			creator = results[0].table.tr.find('div', class_='resultcontentcolumn')
			creator = re.search(r'(?<=Creator\(s\): <\/strong>).*?(?=<br\/>)', str(creator))
			if creator and dic.get('creator') == None:
				dic.update({'creator': creator.group(0)})
			continue

		if re.search(r'/frames/', image_url):
			#aniDB block
			if not dic.get('type'):
				dic.update({'type': 'anidb'})
			title_candidate = result.find('div', class_='resulttitle')
			#TODO fix supplemental info
			title = title_candidate.strong.text
			if title and dic.get('title') == None:
				dic.update({'title': title})
			supplemental_info = re.sub(r'\<strong\>.*?\<\/strong\>', '', title_candidate.text.replace('<small>', '').replace('</small>', ''))
			if supplemental_info and dic.get('supplemental_info') == None:
				dic.update({'supplemental_info': supplemental_info})

			japanese_title = re.search(r'(?<=<strong>Title: </strong>).*?(?=<)', str(result))
			if japanese_title and dic.get('japanese_title') == None:
				dic.update({'japanese_title': japanese_title.group(0)})
			episode = re.search(r'(?<=<strong>Name: </strong>).*?(?=<)', str(result))
			if episode and dic.get('episode') == None:
				dic.update({'episode': episode.group(0)})
			time_code = re.search(r'(?<=<strong>Est Time: </strong>).*?(?=<)', str(result))
			if time_code and dic.get('time_code') == None:
				dic.update({'time_code': time_code.group(0)})
			anidb_link = result.find('div', class_='resultmiscinfo').a.get('href')
			if anidb_link and dic.get('anidb_link') == None:
				dic.update({'anidb_link': anidb_link})
			continue

		if re.search(r'/res/dA/', image_url):
			#DeviantArt block
			if not dic.get('type'):
				dic.update({'type': 'da'})
			title = result.find('div', class_='resulttitle')
			if title and dic.get('title') == None:
				dic.update({'title': title.strong.text})
			resultcontentcolumn = result.find('div', class_='resultcontentcolumn').find_all('a')
			if len(resultcontentcolumn) == 2:
				if dic.get('da_link') == None:
					dic.update({'da_link': resultcontentcolumn[0].get('href')})
				if dic.get('da_id') == None:
					dic.update({'da_id': resultcontentcolumn[0].text})
				if dic.get('author_link') == None:
					dic.update({'author_link': resultcontentcolumn[1].get('href')})
				if dic.get('author') == None:
					dic.update({'author': resultcontentcolumn[1].text})
			continue

		if re.search(r'/res/pixiv/', image_url):
			# Pixiv block
			if not dic.get('type'):
				dic.update({'type': 'pixiv'})
			title = result.find('div', class_='resulttitle')
			if title and dic.get('title') == None:
				dic.update({'title': title.strong.text})
			resultcontentcolumn = result.find('div', class_='resultcontentcolumn').find_all('a')
			if len(resultcontentcolumn) == 4:
				if dic.get('pixiv_link') == None:
					dic.update({'pixiv_link': resultcontentcolumn[0].get('href')})
				if dic.get('pixiv_id') == None:
					dic.update({'pixiv_id': resultcontentcolumn[0].text})
				if dic.get('member_link') == None:
					dic.update({'member_link': resultcontentcolumn[2].get('href')})
				if dic.get('member') == None:
					dic.update({'member': resultcontentcolumn[2].text})
			continue
				
		if re.search(r'/booru/', image_url):
			# 'Booru block
			if not dic.get('type'):
				dic.update({'type': 'booru'})
			creator = result.find('div', class_='resulttitle')
			if creator:
				creator = re.search(r'(?<=Creator: <\/strong>).*?(?=<)', str(creator))
				if creator and dic.get('creator') == None:
					dic.update({'creator': creator.group(0)})
			# print(creator)
			material = result.find('div', class_='resultcontentcolumn')
			if material:
				material1 = re.search(r'(?<=Material: <\/strong>).*?(?=<)', str(material))
				if material1 and dic.get('material') == None:
					dic.update({'material': material1.group(0)})
				material = re.search(r'(?<=Source: </strong>).*?(?=<)', str(material))
				if material and dic.get('material') == None:
					dic.update({'material': material.group(0)})
			for link in result.find('div', class_='resultmiscinfo').find_all('a'):
				link = link.get('href')
				# print(link)
				if link[8:17] == 'danbooru.':
					if dic.get('danbooru_link') == None:
						dic.update({'danbooru_link': link})
						continue
				if link[8:17] == 'gelbooru.':
					if dic.get('gelbooru_link') == None:
						dic.update({'gelbooru_link': link})
						continue
				if link[8:28] == 'chan.sankakucomplex.':
					if dic.get('sankaku_link') == None:
						dic.update({'sankaku_link': link})
						continue
				if link[8:16] == 'yande.re':
					if dic.get('yandere_link') == None:
						dic.update({'yandere_link': link})
						continue
			continue

		# print(title)
	return dic


def get_source_data(picture_url):
	print(picture_url)
	resp = requests.get('http://saucenao.com/search.php?db=999&url='+picture_url)
	# Needs to be parsed as xml since html parser adds inconvenient closing tags (pip install lxml)
	soup = BeautifulSoup(resp.content, features='xml')
	dic = create_link_dictionary(soup)
	dic.update({'SauceNAO': 'http://saucenao.com/search.php?db=999&url='+picture_url})
	
	return dic

if __name__ == "__main__":
	# print("This is also a standalone program. You can put the image url in the line below.")
	# sauce = get_source_data('https://i.imgur.com/GH0Dofm.jpg')
	# print(sauce)
	# Hits
	# sauces = ["https://i.imgur.com/y1cJcOl.jpg", "https://i.imgur.com/Z13SC8H.png", "https://i.imgur.com/62IVnsr.png", "https://i.imgur.com/uHcgE42.jpg", "https://i.imgur.com/DHbGpl1.jpg"]
	# Misses
	# sauces = ["https://i.imgur.com/GH0Dofm.jpg", "https://i.imgur.com/h3VhC7x.jpg", "https://i.imgur.com/LKxb5tS.png", "https://i.imgur.com/i9rH5bq.jpg", "https://i.imgur.com/er8mMZj.jpg"]
	# Crashes
	sauces = ["https://img2.gelbooru.com//images/7b/9f/7b9f93b720c8f4e559400d3100ad4c58.gif", "https://i.redd.it/p4oyfybedwr21.jpg", "https://i.imgur.com/MDKuBSQ.mp4", "https://i.imgur.com/MDKuBSQ.gif", "https://i.redd.it/nxlbtrgqvyq21.jpg"]
	sauces = ["https://i.imgur.com/Z13SC8H.png"]
	for sauce in sauces:
		print(get_source_data(sauce))