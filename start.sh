#!/bin/sh
CLIENTID=""
DEBUG="false"
docker build -t twitch_python python
docker run -it --network=twitch_default --link="twitch_redis_1:redis" --link="twitch_neo_1:neo" -e "CLIENT_ID=$CLIENTID" -e "DEBUG=$DEBUG" twitch_python python twitch.py