
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
        try:
            c.execute("""INSERT INTO users
                    (uid, name, age, bio,
                    ig, distance_mi, photos, 
                    gender, polarity, subjectivity)
                    values (?,?,?,?,?,?,?,?,?,?)""",
                    (user.id, user.name, user.age,
                    user.bio, user.instagram_username,
                    user.distance, str(user.photos), user.gender,
                    polarity, subjectivity))
            avg_happy, avg_neutral = analyzer.get_tf_data('user', user.photos, str(user.id))
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
