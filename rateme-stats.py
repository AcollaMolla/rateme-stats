from user import User
import requests, re, time

def GetAgeSex(post):
	pattern = "[a-zA-Z]\d{2}|\d{2}[a-zA-Z]"
	title = post['title']
	ageAndSex = re.search(pattern, title)
	if ageAndSex is not None:
		return ageAndSex.group(0)
	return "U"

def GetSex(post):
	pattern = "[a-zA-Z]{1}"
	ageAndSex = GetAgeSex(post)
	sex = re.search(pattern, ageAndSex).group(0)
	print(sex)
	print(post['title'])
	if sex == "w" or sex == "W" or sex == "f" or sex == "F":
		return "Female"
	elif sex == "m" or sex == "M":
		return "Male"
	return "None"
	
def GetAge(post):
	return 20
	
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
	

URL = "https://api.pushshift.io/reddit/search/submission/?subreddit=rateme&sort=desc&sort_type=created_utc&before=" + str(CreateTimestamp()) + "&size=5"
users = []
r = requests.get(URL, headers = {'User-agent': 'rateme-stats 1.0'})
data = r.json()
posts = data['data']
id = 0
print("posts length: " + str(len(posts)))
for post in posts:
    user = User(id, GetSex(post), GetAge(post), GetRedditUserId(post), GetRedditPostId(post), CalculateStats(post))
    users.append(user)
    id = id + 1
    exit
