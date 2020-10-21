from user import User
import requests, re, time

def GetAgeSex(post):
	#pattern = "[a-zA-Z]\d{2}|\d{2}[a-zA-Z]|\b([fFwWmM])\b"
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
	#print(sex)
	#print(post['title'])
	#print("----------")
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
	return 123
	
def GetRedditPostId(post):
	return 456
	
def CalculateStats(post):
	stats = []
	stats.append(5)
	stats.append(1.2)
	return stats
	
def CreateTimestamp():
	#Fetch posts made at least 1 week ago, letting the post mature in votes and comments
	oneWeekInSeconds = 604800
	today = int(time.time())
	print(today - oneWeekInSeconds)
	return today - oneWeekInSeconds
	
#Unfourtanly Pushshift API only allows retrieving max 100 posts since mid-2020
URL = "https://api.pushshift.io/reddit/search/submission/?subreddit=rateme&sort=desc&sort_type=created_utc&before=" + str(CreateTimestamp()) + "&size=100"
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
	if sex == "None" and age > 0:
		continue
	else:
		user = User(id, sex, age, GetRedditUserId(post), redditPostId, CalculateStats(post))
		users.append(user)
		id = id + 1
print(len(users))
