class User:
	def __init__(self, id, sex, age, redditUserId, redditPostId, stats):
		self.id = id
		self.sex = sex
		self.age = age
		self.redditUserId = redditUserId
		self.redditPostId = redditPostId
		self.avgRate = stats[0]
		self.stddevRate = stats[1] 
