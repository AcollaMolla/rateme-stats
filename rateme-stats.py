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
	pattern = "\d+"
	ageAndSex = GetAgeSex(post)
	age = re.search(pattern, ageAndSex)
	if age is not None:
		return age.group(0)
	else:
		return 0
	
def GetRedditUserId(post):
	try:
		redditUserId = post['author_fullname']
	except:
		print(post)
		return "unknown"
	if redditUserId is None or redditUserId == "" or redditUserId == "null":
		return None
	return redditUserId
	
def GetRedditPostId(post):
	try:
		redditPostId = post['id']
	except Exception as e:
		print(e)
		return "unknown"
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
	pattern = "[\d][.]?\d*"
	rating = re.search(pattern, comment)
	if rating is not None:
		#print(comment)
		try:
			rate = float(rating.group(0))
		except Exception as e:
			print(comment)
			print(e)
			return None
		if rate > 10 or rate < 0:
			return None
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
		stats = Stats(sum(rates)/len(rates), len(comments), True)
		return stats
	else:
		stats = Stats(-1, len(comments), False)
		return stats
	return None
	
def CreateTimestamp(time):
	#Fetch posts made at least 1 week ago, letting the post mature in votes and comments
	oneWeekInSeconds = 604800
	today = int(time.time())
	print(today - oneWeekInSeconds)
	return today - oneWeekInSeconds
	
#Unfourtanly Pushshift API only allows retrieving max 100 posts since mid-2020
posts = []
URL = "https://api.pushshift.io/reddit/search/submission/?subreddit=rateme&sort=desc&sort_type=created_utc&before=" + str(int(time.time()) - 604800) + "&size=10"
users = []

for i in range(0,2):
	r = requests.get(URL, headers = {'User-agent': 'rateme-stats 1.0'})
	data = r.json()
	posts.extend(data['data'])
	URL = "https://api.pushshift.io/reddit/search/submission/?subreddit=rateme&sort=desc&sort_type=created_utc&before=" + str(posts[len(posts)-1]['created_utc']) + "&size=10"
	
id = 0
print("posts length: " + str(len(posts)))
for post in posts:
	sex = GetSex(post)
	age = int(GetAge(post))
	redditPostId = GetRedditPostId(post)
	if sex == "None" or age == 0 or redditPostId is None:
		continue
	else:
                stats = CalculateStats(redditPostId)
                if stats is not None:
						user = User(id, sex, age, GetRedditUserId(post), redditPostId, stats)
						users.append(user)
						id = id + 1
                else:
                        continue
print(len(users))
females = []
males = []
unvalidFemales = []
unvalidMales = []
femaleRating = 0
maleRating = 0
for user in users:
        if user.sex == "Female" and user.stats.valid:
                females.append(user)
        elif user.sex == "Female" and not user.stats.valid:
				unvalidFemales.append(user)
        elif user.sex == "Male" and user.stats.valid:
                males.append(user)
        elif user.sex == "Male" and not user.stats.valid:
				unvalidMales.append(user)
if len(females) > 0:
        femaleRating = sum(f.stats.avg for f in females)/len(females)
if len(males) > 0:
        maleRating = sum(m.stats.avg for m in males)/len(males)
print("Females: " + str(len(females)))
print("Males: " + str(len(males)))
print("Female posters with no comments: " + str(len(unvalidFemales)))
print("Male posters with no comments: " + str(len(unvalidMales)))
print("Female avg rating: " + str(femaleRating))
print("Male avg rating: " + str(maleRating))
print("Female avg comment count: " + str(sum(f.stats.commentCount for f in females)/len(females)))
print("Male avg comment count: " + str(sum(m.stats.commentCount for m in males)/len(males)))
females.extend(unvalidFemales)
males.extend(unvalidMales)
print("Average female age: " + str(sum(f.age for f in females)/len(females)))
print("Average male age: " + str(sum(m.age for m in males)/len(males)))
