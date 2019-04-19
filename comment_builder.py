import wrapper.nhentai as nhentai

def build_comment(dic):
	output_comment = ''
	is_redacted = False

	# Skip anidb for special handling.
	if not (dic.get('type') == 'anidb'):
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
				pass
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
		danbooru = dic.get('danbooru_link')
		gelbooru = dic.get('gelbooru_link')
		sankaku = dic.get('sankaku_link')
		yandere = dic.get('yandere_link')

		if danbooru or gelbooru or sankaku or yandere:
			link_comment = ''
			if danbooru:
				link_comment += f"[Danbooru]({danbooru}) "
			if gelbooru:
				link_comment += f"{generate_seperator_bar(link_comment)}[Gelbooru]({gelbooru}) "
			if sankaku:
				link_comment += f"{generate_seperator_bar(link_comment)}[Sankaku]({sankaku}) "
			if yandere:
				link_comment += f"{generate_seperator_bar(link_comment)}[Yandere]({yandere}) "
			output_comment += f"**Links**: {link_comment}\n\n"




	# if dic.get('Title') is not None:
	# 	output_comment += '**Title:** {0}\n\n'.format(dic.get('Title'))

	# if (dic.get('Creator') or dic.get('Member') or dic.get('Author')) is not None:
	# 	output_comment += '**Creator:** '
	# 	if dic.get('Creator') is not None: output_comment += dic.get('Creator').title()+' | '
	# 	if dic.get('Member') is not None:
	# 		output_comment += dic.get('Member')
	# 		if dic.get('Pixiv_art') is not None: output_comment += ' [^({{on Pixiv}})]({0})'.format(dic.get('Pixiv_art'))
	# 		output_comment += ' | '
	# 	if dic.get('Author') is not None and dic.get('Member') is None:
	# 		output_comment += dic.get('Author')
	# 		if dic.get('DeviantArt_art') is not None: output_comment +=' [^({{on DeviantArt}})]({0})'.format(dic.get('DeviantArt_art'))
	# 		output_comment += ' | '
	# 	output_comment += '\n\n'

	# if dic.get('Material') is not None:
	# 	output_comment += '**Material:** '+dic.get('Material').title()
	# 	if dic.get('Material') != 'original':
	# 		output_comment += ' [^({{Google it!}})](http://www.google.com/search?q={0}) [^({{Hentify it!}})](https://gelbooru.com/index.php?page=post&s=list&tags={1})'.format('+'.join(dic.get('Material').split(' ')), '_'.join(dic.get('Material').split(' ')))
	# 	output_comment += '\n\n'

	# if (dic.get('Pixiv_src') or dic.get('Gelbooru') or dic.get('Danbooru') or dic.get('Sankaku') or dic.get('DeviantArt_src') or dic.get('gallery_number')) is not None:
	# 	output_comment += '**Image links:** '
	# 	#TODO make it pretty
	# 	if dic.get('gallery_number') is not None:
	# 		output_comment += '[nHentai](https://nhentai.net/g/{0}/'.format(dic.get('gallery_number'))
	# 		if dic.get('page_number') is not None:
	# 			output_comment += "{0}/".format(dic.get('page_number'))
	# 		output_comment += ') | '
	# 	if dic.get('Pixiv_src') is not None: output_comment += '[Pixiv]({0}) | '.format(dic.get('Pixiv_src'))
	# 	if dic.get('Gelbooru') is not None: output_comment += '[Gelbooru]({0}) | '.format(dic.get('Gelbooru'))
	# 	if dic.get('Danbooru') is not None: output_comment += '[Danbooru]({0}) | '.format(dic.get('Danbooru'))
	# 	if dic.get('Sankaku') is not None: output_comment += '[Sankaku]({0}) | '.format(dic.get('Sankaku'))
	# 	if dic.get('DeviantArt_src') is not None: output_comment += '[DeviantArt]({0}) | '.format(dic.get('DeviantArt_src'))
	# 	output_comment += '\n\n'	

	# Handle no results
	if output_comment == '':
		return False

	output_comment += f"---\n^^[Full results]({dic.get('SauceNAO')}) | [How to SauceNao](https://www.reddit.com/r/HentaiSource/comments/b7h28o/guide_reverse_search_images_cropping_saucenao/) | [Questions?](https://reddit.com/user/Kicken) | [Original GitHub](https://github.com/MistressMamiya/hsauce_bot) | [Forked GitHub](https://github.com/TheVexedGerman/hsauce_bot) | Bad sauce? [Message the mods](https://www.reddit.com/message/compose?to=%2Fr%2FHentaiSource)".replace(' ', '&#32;')

	return output_comment

def build_footprint():
	return 'Submission is not an image or sauce could not be found!\n\n---\n^(View full results) ^| [^(Message creator)](https://reddit.com/user/Mistress_Mamiya)'

def generate_seperator_bar(link_comment):
	if link_comment:
		return "| "
	return ''