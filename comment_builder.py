import wrapper.nhentai as nhentai

def build_comment(dic, post):
	output_comment = ''
	is_redacted = False

	# Skip anidb for special handling.
	if not (dic.get('type') == 'anidb' or dic.get('type') == 'fakku'):
		if dic.get('title'):
			output_comment += f"**Title**: {dic.get('title')}\n\n"

	if dic.get('type') == 'nhentai':
		if dic.get('creator'):
			output_comment += f"**Creator(s)**: {dic.get('creator')}\n\n"
		if dic.get('gallery_number'):
			gallery_number = dic.get('gallery_number')
			tags = nhentai.analyseNumber(gallery_number)
			output_comment += "**Gallery Number**: "
			if len(tags) > 1 and tags[-1]:
				is_redacted = True
			if not is_redacted:
				output_comment += f"[{gallery_number}](https://nhentai.net/g/{gallery_number})"
			else:
				output_comment += f"{gallery_number}"
			output_comment += "\n\n"
			if dic.get('page_number'):
				page_number = dic.get('page_number')
				output_comment += "**Page Number**: "
				if not is_redacted:
					output_comment += f"[{page_number}](https://nhentai.net/g/{gallery_number}/{page_number})"
				else:
					output_comment += f"{page_number}"
				output_comment += "\n\n"

	if dic.get('type') == 'anidb':
		if dic.get('title'):
			if dic.get('anidb_link'):
				output_comment += f"**Title**: [{dic.get('title')}]({dic.get('anidb_link')})\n\n"
			else:
				output_comment += f"**Title**: {dic.get('title')}\n\n"
		if dic.get('supplemental_info'):
			output_comment += f"**Details**: {dic.get('supplemental_info')}\n\n"
		if dic.get('japanese_title'):
			output_comment += f"**JP Title**: {dic.get('japanese_title')}\n\n"
		if dic.get('episode'):
			output_comment += f"**EP Name**: {dic.get('episode')}\n\n"
		if dic.get('time_code'):
			output_comment += f"**Est. Time**: {dic.get('time_code')}\n\n"

	if dic.get('type') == 'da':
		if dic.get('da_id'):
			output_comment += f"**dA ID**: [{dic.get('da_id')}]({dic.get('da_link')})\n\n"
		if dic.get('author'):
			output_comment += f"**Author**: [{dic.get('author')}]({dic.get('author_link')})\n\n"
		
	if dic.get('type') == 'pixiv':
		if dic.get('pixiv_id'):
			output_comment += f"**Pixiv ID**: [{dic.get('pixiv_id')}]({dic.get('pixiv_link')})\n\n"
		if dic.get('member'):
			output_comment += f"**Member**: [{dic.get('member')}]({dic.get('member_link')})\n\n"
	
	if dic.get('type') == 'booru':
		if dic.get('creator'):
			output_comment += f"**Creator**: {dic.get('creator')}\n\n"
		if dic.get('material'):
			output_comment += f"**Material**: {dic.get('material')}\n\n"
		link_comment = generate_booru_links(dic)
		if link_comment:
			output_comment += f"**Links**: {link_comment}\n\n"

	if dic.get('type') == 'fakku':
		if dic.get('title'):
			if dic.get('fakku_link'):
				output_comment += f"**Title**: [{dic.get('title')}]({dic.get('fakku_link')})\n\n"
			else:
				output_comment += f"**Title**: {dic.get('title')}\n\n"
		if dic.get('artist'):
			if dic.get('artist_link'):
				output_comment += f"**Artist**: [{dic.get('artist')}]({dic.get('artist_link')})\n\n"
			else:
				output_comment += f"**Artist**: {dic.get('artist')}\n\n"

	if dic.get('type') == 'mangadex':
		if dic.get('artist'):
			output_comment += f"**Artist**: {dic.get('artist')}\n\n"
		if dic.get('author'):
			output_comment += f"**Author**: {dic.get('author')}\n\n"
		link_comment = generate_mangadex_links(dic)
		if link_comment:
			output_comment += f"**Links**: {link_comment}\n\n"
		if dic.get('mangadex_link') and dic.get('mangadex_page_number'):
			output_comment += f"**Mangadex Page**: [{dic.get('mangadex_page_number')}]({dic.get('mangadex_link')}/{dic.get('mangadex_page_number')})\n\n"

	#Add remaining links:
	lesser_links = ''
	if not dic.get('type') == 'anidb':
		if dic.get('anidb_link'):
			lesser_links += f"[AniDB]({dic.get('anidb_link')}) "
	if not dic.get('type') == 'da':
		if dic.get('da_id'):
			lesser_links += f"{generate_seperator_bar(lesser_links)}[DeviantArt]({dic.get('da_link')}) "
	if not dic.get('type') == 'pixiv':
		if dic.get('pixiv_id'):
			lesser_links += f"{generate_seperator_bar(lesser_links)}[Pixiv]({dic.get('pixiv_link')}) "
	if not dic.get('type') == 'booru':
		link_comment = generate_booru_links(dic)
		if link_comment:
			lesser_links += f"{generate_seperator_bar(lesser_links)}{link_comment} "
	if not dic.get('type') == 'fakku':
		if dic.get('fakku_link'):
			lesser_links += f"{generate_seperator_bar(lesser_links)}[FAKKU]({dic.get('fakku_link')}) "
	if not dic.get('type') == 'mangadex':
		link_comment = generate_mangadex_links(dic)
		if link_comment:
			lesser_links += f"{generate_seperator_bar(lesser_links)}{link_comment} "
	
	if lesser_links:
		output_comment += f"**Additional results**: {lesser_links}\n\n"

	# Handle no results
	if not output_comment:
		return False

	output_comment += f"---\n^^[Full results]({dic.get('SauceNAO')}) | [How to SauceNao](https://www.reddit.com/r/HentaiSource/comments/b7h28o/guide_reverse_search_images_cropping_saucenao/) | [Questions?](https://www.reddit.com/message/compose/?to=thevexedgerman&subject=[SauceNAO-Bot]) | [Original Bot](https://www.reddit.com/user/HentaiSauce_Bot) | [Forked GitHub](https://github.com/TheVexedGerman/hsauce_bot) | Bad sauce? [Message the mods](https://www.reddit.com/message/compose?to=%2Fr%2FHentaiSource)".replace(' ', '&#32;')
	output_comment = f"Hey /u/{post.author} the following result was found on SauceNAO [as per rule 10](https://www.reddit.com/r/HentaiSource/comments/bbr4ty/new_rule_10_use_saucenao_rule_11_check_reposts/):\n\n{output_comment}"
	return output_comment


def generate_seperator_bar(link_comment):
	if link_comment:
		return "| "
	return ''

def generate_booru_links(dic):
	danbooru = dic.get('danbooru_link')
	gelbooru = dic.get('gelbooru_link')
	sankaku = dic.get('sankaku_link')
	yandere = dic.get('yandere_link')

	link_comment = ''
	if danbooru or gelbooru or sankaku or yandere:
		if danbooru:
			link_comment += f"[Danbooru]({danbooru}) "
		if gelbooru:
			link_comment += f"{generate_seperator_bar(link_comment)}[Gelbooru]({gelbooru}) "
		if sankaku:
			link_comment += f"{generate_seperator_bar(link_comment)}[Sankaku]({sankaku}) "
		if yandere:
			link_comment += f"{generate_seperator_bar(link_comment)}[Yandere]({yandere}) "
	return link_comment

def generate_mangadex_links(dic):
	mangadex = dic.get('mangadex_link')
	mangaupdates = dic.get('mangaupdates_link')
	mal = dic.get('mal_manga_link')
	
	link_comment = ''
	if mangadex or mangaupdates or mal:
		if mangadex:
			link_comment += f"[MangaDex]({mangadex}) "
		if mangaupdates:
			link_comment += f"{generate_seperator_bar(link_comment)}[Manga Updates]({mangaupdates}) "
		if mal:
			link_comment += f"{generate_seperator_bar(link_comment)}[MAL]({mal}) "
	return link_comment