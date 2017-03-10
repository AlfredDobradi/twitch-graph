# Twitch-graph

## What does it do?

Parses channel followers from Twitch API, then saves the channel, followers and their relationship (which is currently only :FOLLOW) in Neo4j

## Usage

To run, you'll need Docker and Python. (I might create a Docker container for the Python script, but for now it seemed moot)

First create the container
```
docker build . -t twitchgraph
```

Fire it up
```
docker run -p7474:7474 -p7687:7687 twitchgraph
```
(Neo4j will use the ```./data``` directory to store you know... data.)

When you start Neo4j the first time, check the web interface at ```http://localhost:7474``` and change your password. You'll have to change it in the script in this line:
```
neo = Graph(user="twitch", password="twitch")
```

Once Neo4j is up and running you can actually run the script:
```
CLIENT_ID=<twitch client id> CHANNEL=<twitch channel> python code/twitch.py
```

It will take a bit of time to parse the followers, depending on how many the channel has.  

After it's finished, you can check your DB via the browser interface, run queries and all.

## Neo4j examples

### Count your nodes labeled 'User':
```
MATCH (u:User)
RETURN COUNT(u)
```

### Return your users ordered by the number of saved Channels they follow
```
MATCH (u:User)-[r:FOLLOW]->(c:Channel)
RETURN n, COUNT(r) AS rel_count
ORDER BY rel_count DESC
```

## Plans

* Viral discovery (channel -> followers -> their followed channels -> start again)
* Web based "analytics" using the data
* Refactor

## Links

Docker Hub: http://hub.docker.com  
Neo4j: http://www.neo4j.com  
Twitch Developers: http://dev.twitch.tv