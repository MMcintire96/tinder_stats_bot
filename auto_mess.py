import sqlite3
import time
import stats
import analyzer
import connect

conn = sqlite3.connect('db/matches.db')
c = conn.cursor()

def make_data_message(name, happy, neutral, pol, subj):
    happy, neutral = str(100*round((happy),2)), str(100*round((neutral),2))
    pol, subj = round((pol), 2), round((subj), 2)
    meanhappy, varhappy, stdhappy, arr = stats.get_query('happy')
    meanpol, varpol, stdpol, arr = stats.get_query('polarity')
    meansubj, varsubj, stdsubj, arr = stats.get_query('subjectivity')
    Mhappy, SDhappy = round((100*meanhappy),2), round((100*stdhappy),2)
    Mpol, SDpol = round((meanpol),2), round((stdpol),2)
    Msubj, SDsubj = round((meansubj),2), round((stdsubj),2)
    message = [
u'''Tinder Stats for {0}:

Happy: 

== {1} ==

    -M: {2} -SD: {3} -R: [0,100]

Polarity:

== {4} ==
    
    -M: {5} -SD: {6} -R: [-1,1]

Subjectivity: 

== {7} == 
    
    -M: {8} -SD: {9} -R: [0,1]

Key: M=mean, SD=Standard Deviation, R=Range

Confused by these numbers?
    "Polarity" is measure of the [negativity vs positivity] in your bio
    "Subjectivity" is a measure of your [objectivity vs subjectivty] in your bio
    "Happy" is a measure of the quality & frequency of smiling faces in your photos
    Mean and standard deviation are based on a sample of the tinder population

If you want to learn more you can message me; I will respond.
Github.com/MMcintire96/tinder_stats_bot'''.format(name, happy, Mhappy, SDhappy, pol, Mpol, SDpol, subj, Msubj, SDsubj)
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
            if messages[indx[0]].body == 'DATA' or messages[indx[0]].body is '"DATA"':
                data_message = check_resp(messages[indx[0]].body, match.user.id)
                if data_message is not None:
                    for j in enumerate(data_message):
                        print(data_message[j[0]])
                        match.message(str(data_message[j[0]]))
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
            pass
        conn.commit()
    print('No new messages, recalling')
    m_back()

if __name__ == '__main__':
    m_back()
