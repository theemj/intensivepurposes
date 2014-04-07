import twitter
from ConfigParser import ConfigParser

def idnum(dentification):
	f = open('twitterids', 'w')
	f.write(str(dentification))
	f.close()

def getidnum():
	oldestidnum = None
	try: 
		f=open('twitterids', 'r')
		oldestidnum = long(f.read())
		f.close()
	except:
		print 'Failed to read Twitter IDs.'
	return oldestidnum

	
config = ConfigParser()
config.read("twittercorrector.conf")
api=twitter.Api(consumer_key = config.get("twitter_auth", "consumer_key"),
		consumer_secret = config.get("twitter_auth", "consumer_secret"),
                access_token_key = config.get("twitter_auth", "access_token_key"),
		access_token_secret = config.get("twitter_auth", "access_token_secret"))

statuses = api.GetSearch('intensive purposes', since_id = getidnum(), count = 3)


for s in statuses:
	if not "\"" in s.text and "intents" not in s.text and "intensive purposes" in s.text.lower():
		print 'Currently correcting:'+s.user.screen_name
		try:
			reply = api.PostUpdate('@%s You may have meant "intents and 	purposes."' % s.user.screen_name, in_reply_to_status_id = s.id)
		except twitter.TwitterError, err:		
			print 'Failed to correct user %s' % s.user.screen_name
			print err
if len(statuses)!=0:
	maxid = max([status.id for status in statuses])
	idnum(maxid)
