import time
import connect
import sqlite3
import matplotlib.pyplot as plt
import collections

def graph():
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    age_arr = []
    name_arr = []
    bio_arr = []
    for row in c.fetchall():
        age_arr.append(row[2])
        name_arr.append(row[1])
        bio_arr.append(len(row[3]))
   
    plt.style.use('dark_background')

    fig1 = plt.figure(1)
    age_counter = collections.Counter(sorted(age_arr))
    plt.bar(list(age_counter.keys()), list(age_counter.values()))
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.title("Age by frequency of occurence")
    fig1.show()

    fig2 = plt.figure(2)
    name_counter = collections.Counter(sorted(name_arr))
    name_keys = [x[0] for x in name_counter.most_common(15)]
    value_keys = [y[1] for y in name_counter.most_common(15)]
    plt.bar(name_keys, value_keys)
    plt.xlabel("Names")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.title("Top 15 Names by frequency of occurence")
    fig2.show()
   
    fig3 = plt.figure(3)
    bio_counter = collections.Counter(sorted(bio_arr))
    bio_keys = [x[0] for x in bio_counter.most_common(50)]
    bio_values = [x[1] for x in bio_counter.most_common(50)]
    plt.bar(bio_keys, bio_values)
    plt.xlabel("Letter length")
    plt.ylabel("Count")
    plt.title("Top 50 bio lengths (letters) by frequency of occurence")
    fig3.show()

    input()


def update_users():
    users = connect.session.nearby_users()
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    for user in users:
        time.sleep(1)
        uid = user.id
        school_name = list(user.schools.values())
        school_id = list(user.schools.keys())
        job = user.jobs
        if len(job) is 0:
            job = None
        else:
            job =job[0]
        if len(school_name) is 0:
            school_name = None
            school_id = None
        else:
            school_name = school_name[0]
            school_id = school_id[0]
        print(user.name, school_name, school_id, job, uid)
        try:
            c.execute("""UPDATE users
                    SET school_name = ?,
                        school_id = ?,
                        job = ?
                    WHERE uid = ?""",
                    (school_name, school_id, job, uid))
        except Exception as e:
            print(str(e))
        conn.commit()
    conn.close()


if __name__ == '__main__':
    #update_users()
    graph()
