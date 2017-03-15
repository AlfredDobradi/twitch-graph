import requests
import json

class AskTwitch:
	client_id = None
	headers = None

	def __init__(self, client_id = None):
		if client_id is None:
			return false

		self.client_id = client_id
		
		self.headers = {
			"Accept": "application/vnd.twitchtv.v5+json",
			"Client-ID": client_id
		}

	def GetUserIdByName(self, name):
		r = requests.get("https://api.twitch.tv/kraken/users?login=" + name, headers=self.headers)
		response = json.loads(r.text)
		if response is not None and response['_total'] > 0:
			user_id = response['users']
			return user_id[0]['_id']
		else:
			return None

	def GetUserInfo(self, id):
		r = requests.get("https://api.twitch.tv/kraken/users/" + id, headers=self.headers)
		response = json.loads(r.text)
		if response is not None:
			return response
		return None

	def GetUserFollowing(self, id):
		# url = "https://api.twitch.tv/kraken/users/" + id + "/follows/channels"
		# r = requests.get(url, headers=self.headers)
		# response = json.loads(r.text)
		# total = response["_total"]
		# if total < 25
		return None
