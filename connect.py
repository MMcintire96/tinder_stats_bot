import argparse
import re
import sqlite3

import pynder
import requests
import robobrowser

MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', type=str,
                    help='Enter your email that you use to login to facebook')
    parser.add_argument('--pwd', type=str, help='Enter your facebook password')
    args = parser.parse_args()
    if type(args.email) is str and type(args.pwd) is str:
        with open('creds.txt', 'w') as f:
            f.write(args.email + '\n')
            f.write(args.pwd + '\n')
            f.write(get_access_token(args.email, args.pwd) + '\n')
        f.close()
        args.email, args.pwd, auth = [line.rstrip() for line in open('creds.txt')]
    else:
        args.email, args.pwd, auth = [line.rstrip() for line in open('creds.txt')]
    return args.email, args.pwd, auth


def get_access_token(email, password):
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser='lxml')
    s.open(FB_AUTH)
    f = s.get_form()
    f["pass"] = password
    f["email"] = email
    s.submit_form(f)
    f = s.get_form()
    try:
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
    except Exception as e:
        print("Bad login credentials -- try again")
        get_args()
        return
    access_token = re.search(r"access_token=([\w\d]+)",
                        s.response.content.decode()).groups()[0]
    return access_token

def make_db():
    try:
        conn = sqlite3.connect("db/h_t_db.db")
        c = conn.cursor()
        c.execute(""" CREATE TABLE matches
                (uid data_type TEXT UNIQUE,
                name data_type TEXT,
                age data_type TEXT,
                bio data_type TEXT,
                ig data_type TEXT,
                distance_mi data_type TEXT,
                photos data_type TEXT,
                gender data_type TEXT,
                polarity data_type TEXT,
                subjectivity data_type TEXT,
                happy data_type TEXT,
                neutral data_type TEXT)""")
        c.execute(""" CREATE TABLE users
                (uid data_type TEXT UNIQUE,
                name data_type TEXT,
                age data_type TEXT,
                bio data_type TEXT,
                ig data_type TEXT,
                distance_mi data_type TEXT,
                photos data_type TEXT,
                gender data_type TEXT,
                polarity data_type TEXT,
                subjectivity data_type TEXT,
                happy data_type TEXT,
                neutral data_type TEXT)""")
        conn.commit()
        conn.close()
    except Exception as e:
        print(str(e))
        print("If you are looking for help connecting, use --help")

email, password, auth = get_args()
if len(auth) > 0:
    session = pynder.Session(auth)
else:
    session = pynder.Session(facebook_token=get_access_token(email, password))

if __name__ == '__main__':
    make_db()
