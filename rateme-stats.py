from user import User
import requests

URL = "https://reddit.com/r/rateme/top/.json"
users = []
r = requests.get(URL, headers = {'User-agent': 'rateme-stats 1.0'})
data = r.json()
posts = data['data']['children']
for post in posts:
	print("post")
