import sqlite3
import time

import analyzer
import connect

conn = sqlite3.connect('db/h_t_db.db')
c = conn.cursor()

def make_data_message(name, happy, neutral, pol, subj):
    happy, neutral = str(100*round((happy),2)) + '%', str(100*round((neutral),2)) + "%"
    pol, subj = round((pol), 3), round((subj), 3)
    message = [
u'''Tinder STATS for {0}
    Your photos indicate that you appear {1} happy (smiling)
    You scored {2} on the polarity scale [-1,1]
    You scored {3} on the subjectivity scale [0,1]

Confused by these numbers?

TEXT DATA: 
    Polarity is measure of the negativity vs positivity in your bio
    Subjectivity is a measure of your objectivity vs subjectivty

PHOTO DATA:
    Your "happy" score is based on the amount of smiling faces in your photos

If you want to learn more you can message me; I will respond.
github.com/MMcintre96/tinder_stats_bot'''.format(name, happy, pol, subj)
            ]
    return message

def check_resp(message, uid):
    if message == 'DATA' or message is 'DATA':
        goal_uid = 'uid'
        goal_resp = 'responded'
        # you think someone on tinder will sql inject this? is it possible?
        c.execute("SELECT * FROM matches WHERE "+goal_uid+"=?", (uid,))
        rows = c.fetchall()
        for row in rows:
            resp_var = row[12]
        if resp_var == 0:
            name = row[1]
            happy, neutral = float(row[10]), float(row[11])
            pol, subj = float(row[8]), float(row[9])
            c.execute("UPDATE matches SET responded=1 WHERE uid = ?", (uid,))
            conn.commit()
            data_message = make_data_message(name, happy, neutral, pol, subj)
            return data_message


def m_back():
    matches = connect.session.matches()
    me = connect.session.profile.id
    for match in matches:
        messages = match.messages
        for indx in enumerate(messages):
            if messages[indx[0]].body == 'DATA' or messages[indx[0]].body is 'DATA':
                data_message = check_resp(messages[indx[0]].body, match.user.id)
                # the scarriest function of em all lmao
                if data_message is not None:
                    for i in range(len(data_message)):
                        print(data_message[i])
                        match.message(str(data_message[i]))
            
            else:
                pass
        # this is here to check for new matches
        # absuing recursive functions
        try:
            distance = round((match.user.distance_km * .62317), 2)
            polarity, subjectivity = analyzer.get_tb_data(match.user.bio)
            responded = 0
            c.execute("""INSERT INTO matches
                    (uid, name, age, bio,
                    ig, distance_mi, photos, 
                    gender, polarity, subjectivity, responded)
                    values (?,?,?,?,?,?,?,?,?,?,?)""",
                    (match.user.id, match.user.name,
                    match.user.age, match.user.bio,
                    match.user.instagram_username,
                    distance, str(match.user.photos),
                    match.user.gender,
                    polarity, subjectivity, responded))
            avg_happy, avg_neutral = analyzer.get_tf_data('match', 
                        match.user.photos, str(match.user.id))
            c.execute("""UPDATE matches
                    SET happy = ?,
                        neutral = ?
                    WHERE uid = ?""",
                    (avg_happy, avg_neutral, match.user.id))
            print(match.user.id, match.user.name)
        except Exception as e:
            print(str(e))
        conn.commit()
    m_back()

if __name__ == '__main__':
    m_back()
