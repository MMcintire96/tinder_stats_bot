import sqlite3
import time

import analyzer
import connect
import stats

conn = sqlite3.connect('db/matches.db')
c = conn.cursor()

# clean this up for the love of got
def make_data_message(name, happy, neutral, pol, subj):
    happy, neutral = str(round((100*happy),2)), str(round((neutral*100),2))
    pol, subj = round((pol), 2), round((subj), 2)
    meanhappy, varhappy, stdhappy = stats.get_query('happy')
    meanpol, varpol, stdpol = stats.get_query('polarity')
    meansubj, varsubj, stdsubj = stats.get_query('subjectivity')
    Mhappy, SDhappy = round((100*meanhappy),2), round((100*stdhappy),2)
    Mpol, SDpol = round((meanpol),2), round((stdpol),2)
    Msubj, SDsubj = round((meansubj),2), round((stdsubj),2)
    user_count = stats.get_len()
    mode_name = stats.user_stats('name')
    mode_bio = stats.user_stats('bio')
    mode_school = stats.user_stats('school_id')
    mode_photos = stats.user_stats('photos')
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

For {10} females in your area:
    The most common name is {11}
    The most common bio length is {12} characters
    The most common university is {13}
    The most common amount of photos is {14}
    

If you want to learn more you can message me; I will respond.
Github.com/MMcintire96/tinder_stats_bot'''.format(name, happy, Mhappy, SDhappy, pol, Mpol, SDpol, subj, Msubj, SDsubj, user_count, mode_name, mode_bio, mode_school, mode_photos)]
    return message

def check_resp(uid):
    c.execute("SELECT * FROM matches WHERE uid=?", (uid, ))
    for row in c.fetchall():
        if row[15] == 0:
            name = row[1]
            happy, neutral = float(row[13]), float(row[14])
            pol, subj = float(row[11]), float(row[12])
            c.execute("UPDATE matches SET responded=1 WHERE uid = ?", (uid,))
            conn.commit()
            data_message = make_data_message(name, happy, neutral, pol, subj)
            return data_message


def m_back():
    matches = connect.session.matches()
    for match in matches:
        try:
            distance = round((match.user.distance_km * .62317), 2)
            polarity, subjectivity = analyzer.get_tb_data(match.user.bio)
            responded = 0
            school_id = list(match.user.schools.keys())
            school_name = list(match.user.schools.values())
            job = match.user.jobs
            if len(job) is 0:
                job = None
            else:
                job = job[0]
            if len(school_name) is 0:
                school_name = None
                school_id = None
            else:
                school_name = school_name[0]
                school_id = school_id[0]
            c.execute("""INSERT INTO matches
                    (uid, name, age, bio,
                    ig, distance_mi, photos,
                    school_name, school_id, job,
                    gender, polarity, subjectivity, responded)
                    values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (match.user.id, match.user.name,
                    match.user.age, match.user.bio,
                    match.user.instagram_username,
                    distance, str(list(match.user.photos)),
                    school_name, school_id, job,
                    match.user.gender,
                    polarity, subjectivity, responded))
            avg_happy, avg_neutral = analyzer.get_tf_data(list(match.user.photos), str(match.user.id))
            c.execute("""UPDATE matches
                    SET happy = ?,
                        neutral = ?
                    WHERE uid = ?""",
                    (avg_happy, avg_neutral, match.user.id))
            print(match.user.id, match.user.name)
        except Exception as e:
            pass
        conn.commit()
        data_message = check_resp(match.user.id)
        if data_message is not None:
            print(data_message[0])
            match.message(str(data_message[0]))
    print('No new matches - recalling')
    m_back()

if __name__ == '__main__':
    m_back()
