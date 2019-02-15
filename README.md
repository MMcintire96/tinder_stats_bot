# tinder_stats_bot

A bot that returns user data for their tinder profile using tensorflow and textblob

## Run
To run this bot, you need to make the folder
1. user_imgs
2. match_imgs
3. happy_imgs
4. neutral_imgs
5. db

Call 'connect.py' and user --help to guide you through it. This will make a creds.txt file for you
auto_liker.py will like all users and add their data to the DB 
auto_mess.py is the message responder, it waits for a specific message 'DATA' and then responseds with stats

## TODO
1. fix db lock issue
