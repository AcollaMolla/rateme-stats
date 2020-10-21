from user import User
from stats import Stats
import requests, re, time

def GetAgeSex(post):
	pattern = "[fFwWmM]\d{2}|\d{2}[fFwWmM]"
	title = post['title']
	ageAndSex = re.search(pattern, title)
	if ageAndSex is not None:
		return ageAndSex.group(0)
	return "U"

def GetSex(post):
	pattern = "[a-zA-Z]{1}"
	ageAndSex = GetAgeSex(post)
	sex = re.search(pattern, ageAndSex).group(0)
	if sex == "w" or sex == "W" or sex == "f" or sex == "F":
		return "Female"
	elif sex == "m" or sex == "M":
		return "Male"
	return "None"
	
def GetAge(post):
	pattern = "[0-9]*"
	ageAndSex = GetAgeSex(post)
	age = re.search(pattern, ageAndSex)
	if age is not None:
		return age.group(0)
	else:
		return 0
	
def GetRedditUserId(post):
	redditUserId = post['author_fullname']
	if redditUserId is None or redditUserId == "" or redditUserId == "null":
		return None
	return redditUserId
	
def GetRedditPostId(post):
	redditPostId = post['id']
	if redditPostId is None or redditPostId == "" or redditPostId == "null":
		return None
	return redditPostId
	
def IsCommentFromMod(comment):
	substring = "Hello /u/"
	substring2 = "[moderators]"
	if substring in comment or substring2 in comment:
		return True
	return False
	
def GetRating(comment):
	if IsCommentFromMod(comment):
		return None
	pattern = "[\d*][.]?\d*"
	rating = re.search(pattern, comment)
	if rating is not None:
		#print(comment)
		try:
			rate = float(rating.group(0))
		except:
			return None
		if rate > 10:
			return None
		print("adding rate: " + str(rate))
		return rate
	return None
	
def CalculateStats(redditPostId):
	print("Fetching comment for " + redditPostId)
	URL = "https://api.pushshift.io/reddit/comment/search/?link_id=" + redditPostId + "&limit=1000"
	r = requests.get(URL, headers = {'User-agent': 'rateme-stats 1.0'})
	comments = r.json()['data']
	rates = []
	for comment in comments:
		rate = GetRating(comment['body'])
		if rate is None:
			continue
		else:
			rates.append(float(rate))
	if len(rates) > 0:
		stats = Stats(sum(rates)/len(rates), len(comments))
		return stats
	return Stats(0, len(comments))
	
def CreateTimestamp():
	#Fetch posts made at least 1 week ago, letting the post mature in votes and comments
	oneWeekInSeconds = 604800
	today = int(time.time())
	print(today - oneWeekInSeconds)
	return today - oneWeekInSeconds
	
#Unfourtanly Pushshift API only allows retrieving max 100 posts since mid-2020
URL = "https://api.pushshift.io/reddit/search/submission/?subreddit=rateme&sort=desc&sort_type=created_utc&before=" + str(CreateTimestamp()) + "&size=5"
users = []
r = requests.get(URL, headers = {'User-agent': 'rateme-stats 1.0'})
data = r.json()
posts = data['data']
id = 0
print("posts length: " + str(len(posts)))
for post in posts:
	sex = GetSex(post)
	age = GetAge(post)
	redditPostId = GetRedditPostId(post)
	if sex == "None" or age == 0 or redditPostId is None:
		continue
	else:
		user = User(id, sex, age, GetRedditUserId(post), redditPostId, CalculateStats(redditPostId))
		print("User avg rate: " + str(user.stats.avg))
		print("Number of comments: " + str(user.stats.commentCount))
		users.append(user)
		id = id + 1
print(len(users))
print("Females: " + str(sum(u.sex == "Female" for u in users)))
print("Males: " + str(sum(u.sex == "Male" for u in users)))
