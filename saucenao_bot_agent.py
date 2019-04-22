import praw
from get_source import get_source_data
from comment_builder import build_comment

#The bot needs posts and flair mod permissions to function
PARSED_SUBREDDIT = 'loli_tag_bot'

def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit(
        'thevexedgermanbot'
    )
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def cook_sauce(image_url, i_submission):
	sauce = get_source_data(image_url)
	bot_reply = build_comment(sauce)
	if type(bot_reply) == str:
		i_submission.reply(bot_reply).mod.distinguish(sticky=True)
		flair_post(i_submission)
		print("	Replied: Sauce has been processed [Comment stickied, post flaired]")


def run_bot():
	for i_submission in reddit.subreddit(PARSED_SUBREDDIT).stream.submissions():
		print("Found {}".format(i_submission.id))
		# Since HentaiSource links get flaired and the volume of requests isn't too high checking flairs should be sufficent for restarts.
		if i_submission.link_flair_text != 'Solved':
			image_url = i_submission.url
			if image_url[-4:] == '.jpg' or image_url[-4:] == '.png' or image_url[-4:] == '.gif':
				cook_sauce(image_url, i_submission)
			# Handle non-direct imgur links https://imgur.com/... or https://i.imgur.com/...
			# While not as computationally efficient, possibly replace with regex for non s links.
			# Needs additional handling for .mp4 and gifv, so regex seems like an option.
			elif (image_url[8:14] == 'imgur.' and image_url[17:20] != '/a/') or (image_url[8:16] == 'i.imgur.' and image_url[19:22] != '/a/'):
				if image_url[-5:] == ".gifv":
					cook_sauce(image_url[:-5]+'.gif', i_submission)
				elif image_url[-4:] == ".mp4":
					cook_sauce(image_url[:-4]+'.gif', i_submission)
				else:
					cook_sauce(image_url+'.jpg', i_submission)
			# elif image_url[8:15] == 'gfycat.':
			# 	cook_sauce('https://giant.'+image_url[8:]+'.gif', i_submission)
			# elif image_url[8:21] == 'giant.gfycat.':
			# 	cook_sauce(image_url+'.gif', i_submission)


def flair_post(i_submission):
	for choice in i_submission.flair.choices():
		if choice['flair_text'] == 'Solved':
			i_submission.flair.select(choice['flair_template_id'])


def main():
	global reddit
	reddit = authenticate()
	run_bot()


if __name__ == '__main__':
    # while True:
    #     try:
    #         main()
    #     except Exception as e:
    #         pass
	main()