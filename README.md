# tinder_stats_bot

This bot analyzes a user's tinder profile using two different machine learning methods:
    1. TextBlob uses NLP to get sentiment of text data (user.bio)
    2. CNN trained on tinder faces labeled = ['happy', 'neutral']

The model's architecture is a less deep and less perfected version of VGG-16's
![alt text]('https://github.com/MMcintire96/tinder_stats_bot/tree/master/other/modelpic.png')

Currently using predictions from a transfer learned version of InceptionV3 by google while I get the hyperparams of the model above down.

Coded with love <3, coffee and Lady Gaga

## Run
To run this bot, you need to make the folders
    all_faces/
    -----happy_imgs/
    -----neutral_imgs/
    db/

you will also need the requirements which I cba to write out

1. Call 'connect.py' and use --help to guide you through it. This will make a creds.txt file for you
2. auto_liker.py will like all users and add their data to the DB 
3. auto_mess.py is the message responder, sends new matches their stats

Currently you need to run auto_mess.py all the time, and it will get http errors - working on a fix

## TODO
read notes.txt if you really care

### Creds

Thank You Mary for tinderpro

1. Pynder by charlie/wolf - git clone the repo 
2. Tensorflow - Google
3. TextBlob  

