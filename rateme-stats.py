from user import User
import requests, re

def GetSex(post):
	pattern = "^[a-zA-Z]\d{2}"
	title = post['data']['title']
	sex = re.search(pattern, title)
	if sex is not None:
		print(sex.group(0))
	print(title)
	print("------")
	return "female"
	
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
	

URL = "https://reddit.com/r/rateme/top/.json"
users = []
r = requests.get(URL, headers = {'User-agent': 'rateme-stats 1.0'})
data = r.json()
posts = data['data']['children']
id = 0
for post in posts:
	user = User(id, GetSex(post), GetAge(post), GetRedditUserId(post), GetRedditPostId(post), CalculateStats(post))
	users.append(user)
	id = id + 1
	exit
