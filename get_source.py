from bs4 import BeautifulSoup
import requests, re
from comment_builder import build_comment

def create_link_dictionary(soup):
	dic = {}

	# Creator - boorus; Material - boorus; Author - DeviantArt; Member - Pixiv

	results = soup.find_all(class_='result')
	# print(results)
	# print(results[0]['id'])
	if results[0].get('id') is None:
		image_url = results[0].table.tr.td.div.a.img.get('src')
		# print(image_url)
		gallery_number = re.search(r'(?<=\/nhentai/)\d+', image_url)
		if gallery_number:
			dic.update({'gallery_number': gallery_number.group(0)})
		page_number = re.search(r'(?<=\/)d+(?=\.jpg)', image_url)
		if page_number:
			dic.update({'page_number': page_number.group(0)})

		title = results[0].table.tr.find('div', class_='resulttitle').strong.text
		if title and title != 'Creator: ':
			dic.update({'Title': title})
		creator = results[0].table.tr.find('div', class_='resultcontentcolumn')
		creator = re.search(r'(?<=Creator\(s\): <\/strong>).*?(?=<br\/>)', str(creator))
		if creator:
			dic.update({'Creator': creator.group(0)})

	creator = re.search(r"Creator: <\/strong>([\w\d\s\-_.*()\[\]]*)<br\/>", str(soup))
	if creator and dic.get('Creator') == None:
		dic.update({'Creator': creator.group(1)})
	material = re.search(r"Material: <\/strong>([\w\d\s\-_.*()\[\]]*)<br\/>", str(soup))
	if material and dic.get('Material') == None:
		dic.update({'Material': material.group(1)})
	author = re.search(r'Author: <\/strong><[\w\s\d="\-_\.\/\?:]*>([\w\d\s\-_.*()\[\]]*)<\/a>', str(soup))
	if author and dic.get('Author') == None:
		dic.update({'Author': author.group(1)})
	member = re.search(r'Member: <\/strong><[\w\s\d="\-_\.\/\?:]*>([\w\d\s\-_.*()\[\]]*)<\/a>', str(soup))
	if member and dic.get('Member') == None:
		dic.update({'Member': member.group(1)})

	for link in soup.find_all('a'):
		pg = link.get('href')
		if re.search(r"[\w]+\.deviantart\.com", pg) and dic.get('DeviantArt_art') == None:
			dic.update({'DeviantArt_art': pg})
		elif re.search(r"deviantart\.com\/view\/", pg) and dic.get('DeviantArt_src') == None:
			dic.update({'DeviantArt_src': pg})
		elif re.search(r"pixiv\.net\/member\.", pg) and dic.get('Pixiv_art') == None:
			dic.update({'Pixiv_art': pg})
		elif re.search(r"pixiv\.net\/member_illust", pg) and dic.get('Pixiv_src') == None:
			dic.update({'Pixiv_src': pg})
		elif re.search(r"gelbooru\.com\/index\.php\?page", pg) and dic.get('Gelbooru') == None:
			dic.update({'Gelbooru': pg})
		elif re.search(r"danbooru\.donmai\.us\/post\/", pg) and dic.get('Danbooru') == None:
			dic.update({'Danbooru': pg})
		elif re.search(r"chan\.sankakucomplex\.com\/post", pg) and dic.get('Sankaku') == None:
			dic.update({'Sankaku': pg})

	return dic


def get_source_data(picture_url):
	resp = requests.get('http://saucenao.com/search.php?db=999&url='+picture_url)
	txt = resp.text.split('Low similarity results')[0] # Get rid of the low similarity results
	soup = BeautifulSoup(txt, 'html.parser')
	dic = create_link_dictionary(soup)
	dic.update({'SauceNAO': 'http://saucenao.com/search.php?db=999&url='+picture_url})
	
	return dic

if __name__ == "__main__":
	print("This is also a standalone program. You can put the image url in the line below.")
	# sauce = get_source_data('https://i.imgur.com/GH0Dofm.jpg')
	# print(sauce)
	sauces = ["https://i.imgur.com/y1cJcOl.jpg", "https://i.imgur.com/Z13SC8H.png", "https://i.imgur.com/62IVnsr.png", "https://i.imgur.com/uHcgE42.jpg", "https://i.imgur.com/DHbGpl1.jpg"]
	for sauce in sauces:
		print(get_source_data(sauce))

	# with open('comm', 'w') as ot:
	# 	for line in build_comment(sauce):
	# 		ot.write(line)

	# print("\n\n")
	# print("Overwiev:\n")
	# print("Creator: "+sauce.get('Creator', ''))
	# print("Material: "+sauce.get('Material', ''))
	# print("Author: "+sauce.get('Author', ''))
	# print("Member: "+sauce.get('Member', ''))
	# print("\nLinks:\n")
	# print("DeviantArt_art: "+sauce.get('DeviantArt_art', ''))
	# print("DeviantArt_src: "+sauce.get('DeviantArt_src', ''))
	# print("Pixiv_art: "+sauce.get('Pixiv_art', ''))
	# print("Pixiv_src: "+sauce.get('Pixiv_src', ''))
	# print("Gelbooru: "+sauce.get('Gelbooru', ''))
	# print("Danbooru: "+sauce.get('Danbooru', ''))
	# print("Sankaku: "+sauce.get('Sankaku', ''))
	# print("\n\n")