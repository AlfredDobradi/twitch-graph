import pprint
import os

import userqueue
import asktwitch
import neorepository


pp = pprint.PrettyPrinter(indent=4)

try:
    client_id = os.environ["CLIENT_ID"]
except KeyError:
    print("Usage: CLIENT_ID=<twitch client id> python twitch.py")
    raise SystemExit

debug = False
if os.environ.get("DEBUG") == "true":
    debug = True

queue = userqueue.UserQueue("redis", "6379")
twitch = asktwitch.AskTwitch(client_id, debug)
neorepository = neorepository.Neorepository()

# workflow

userid = twitch.GetUserIdByName("barveyhirdman")

userinfo = twitch.GetUserInfo(userid)
if userinfo is not None:
    added = queue.AddEntry(userinfo["_id"])
    if added is True:
        user = {
            "_id": userinfo["_id"],
            "name": userinfo["name"]
        }
        neorepository.findOrCreateUser(user)

queue.RefreshQueue()
stop = False

i = 0

while len(queue.queue) > 0 and stop is not True:
    for key in queue.queue:
        i += 1
        id = key.decode('utf8').replace('User-', '')
        userinfo = twitch.GetUserInfo(id)
        if userinfo is not None:
            user_from = neorepository.findOrCreateUser({
                "_id": userinfo["_id"],
                "name": userinfo["name"]
            })
            print("{0} - Parsing "
                  "channels {1} follows".format(i, userinfo["name"]))
            following = twitch.GetUserFollowing(id)
            print("Found {0} channels".format(len(following)))
            subset = 0
            for userid in following:
                subset += 1
                user_to = neorepository.findOrCreateUser({
                    "_id": following[userid]["_id"],
                    "name": following[userid]["name"]
                })

                neorepository.findOrCreateRelation(user_from, user_to)
                queue.AddEntry(userid)
                if subset % 15 == 0 and subset != 0:
                    print("Progress: {0}".format(subset))

        queue.MarkParsed(id)
    queue.RefreshQueue()


# following = t.GetUserFollowing(userid)

# items = following.items()

# i = 0

# for key, value in items:
#     added = q.AddEntry(key)
#     if added is False:
#         continue

# print(i)

# 1. Get initial user's id or if not supplied check queue
#   user_to_parse = os.environ["USER"] # naming duh

# 2. Parse user, save data, get followers

# 3. Iterate through followers, loop while there's followers
