import requests
import json


class AskTwitch:
    debug = None
    client_id = None
    headers = None

    def __init__(self,
                 client_id=None,
                 debug=None):
        if debug is True:
            self.debug = True

        if client_id is None:
            return False

        self.client_id = client_id

        self.headers = {
            "Accept": "application/vnd.twitchtv.v5+json",
            "Client-ID": client_id
        }

    def GetUserIdByName(self, name):
        r = requests.get('https://api.twitch.tv/kraken'
                         '/users?login={0}'.format(name),
                         headers=self.headers)
        response = json.loads(r.text)
        if response is not None and response['_total'] > 0:
            user_id = response['users']
            return user_id[0]['_id']
        else:
            return None

    def GetUserInfo(self, id):
        r = requests.get('https://api.twitch.tv/kraken'
                         '/users/{0}'.format(id),
                         headers=self.headers)
        response = json.loads(r.text)
        if response is not None:
            return response
        return

    def GetUserFollowing(self, id):
        following = {}
        limit = 25
        url = (
            'https://api.twitch.tv/kraken'
            '/users/{0}/follows/channels?limit={1}'.format(id, str(limit))
        )
        r = requests.get(url, headers=self.headers)
        response = json.loads(r.text)
        total = response["_total"]
        following.update(self.ProcessFollowing(response["follows"]))
        current = 25
        while current < total:
            tempUrl = url + "&offset=" + str(current)
            if self.debug is True:
                print(tempUrl)
            r = requests.get(tempUrl, headers=self.headers)
            response = json.loads(r.text)
            following.update(self.ProcessFollowing(response["follows"]))
            current += limit

        return following

    def ProcessFollowing(self, following):
        response = {}
        for record in following:
            id = str(record["channel"]["_id"])
            channel = {
                "_id": record["channel"]["_id"],
                "views": record["channel"]["views"],
                "followers": record["channel"]["followers"],
                "name": record["channel"]["name"]
            }

            response[id] = channel

        return response
