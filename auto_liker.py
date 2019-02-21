import sqlite3

import analyzer
import connect


def like_user():
    users = connect.session.nearby_users()
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    for user in users:
        user.distance = round((user.distance_km * .62317), 2)
        polarity, subjectivity = analyzer.get_tb_data(user.bio)
        school_id = list(user.schools.keys())
        school_name = list(user.schools.values())
        job = user.jobs
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
        print(school_name, school_id, job)
        try:
            c.execute("""INSERT INTO users
                    (uid, name, age, bio,
                    ig, distance_mi, photos, 
                    gender, school_name, 
                    school_id, job,
                    polarity, subjectivity)
                    values (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (user.id, user.name, user.age,
                    user.bio, user.instagram_username,
                    user.distance, str(list(user.photos)), user.gender,
                    school_name, school_id, job,
                    polarity, subjectivity))
            avg_happy, avg_neutral = analyzer.get_tf_data('user', list(user.photos), str(user.id))
            c.execute("""UPDATE users
                    SET happy = ?,
                        neutral = ?
                    WHERE uid = ?""",
                    (avg_happy, avg_neutral, user.id))
            user.like()
            print(user.id, user.name, user.like())
        except Exception as e:
            print(str(e))
        conn.commit()
    conn.close()


if __name__ == '__main__':
    like_user()
