import praw
from get_source import get_source_data
from comment_builder import build_comment, build_footprint

# Setting up PRAW
# You have to enter your own values here. If confused, refer to any PRAW guide.
PARSED_SUBREDDIT = 'loli_tag_bot'
posts_checked = []

def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit(
        'thevexedgermanbot'
    )
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def cook_sauce(image_url, i_submission, posts_checked=[]):
	sauce = get_source_data(image_url)
	bot_reply = build_comment(sauce)
	if type(bot_reply) == str:
		i_submission.reply(bot_reply).mod.distinguish(sticky=True)
		posts_checked.append(i_submission.id)
		posts_checked = posts_checked[-100:]
		print("	Replied: Sauce has been processed [Comment stickied]")
	# else:
	# 	i_submission.reply(build_footprint()).mod.remove()
	# 	print("	Replied: Sauce not found [Comment removed]")


def run_bot():
	#could be made into a main and made to be crash resistant using try main + exception
	for i_submission in reddit.subreddit(PARSED_SUBREDDIT).stream.submissions():
		print("Found {}".format(i_submission.id))
		# replied = False
		#checks whether a thread contains a reply by the bot already. Could be replaced with a local database to reduce reddit requests.
		# for i_comment in i_submission.comments:
		# 	if "View full results" in i_comment.body:
		# 		replied = True
		# 		print("	Ignored: Already replied in this thread")
		# 		break
		if i_submission.id not in posts_checked:
			image_url = i_submission.url
			if image_url[-4:] == '.jpg' or image_url[-4:] == '.png':
				cook_sauce(image_url, i_submission, posts_checked=posts_checked)
			# Handle non-direct imgur links https://imgur.com/... or https://i.imgur.com/...
			# While not as computationally efficient, possibly replace with regex for non s links.
			elif (image_url[8:14] == 'imgur.' and image_url[17:20] != '/a/') or (image_url[8:16] == 'i.imgur.' and image_url[19:22] != '/a/'):
				cook_sauce(image_url+'.jpg', i_submission, posts_checked=posts_checked)
			# else:
			# 	i_submission.reply(build_footprint()).mod.remove()
			# 	print("	Replied: Unsupported submission type [Comment removed]")


def main():
	global reddit
	reddit = authenticate()
	global posts_checked
	posts_checked = get_posts_checked()
	run_bot()


def get_posts_checked():
	return []


if __name__ == '__main__':
    # while True:
    #     try:
    #         main()
    #     except Exception as e:
    #         pass
	main()