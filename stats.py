import collections
import math
import sqlite3

import numpy as np


def get_stats(arr):
    arr = np.array(arr).astype(np.float)
    mean = np.nanmean(arr)
    var = np.nanvar(arr, dtype=np.float32)
    std = math.sqrt(var)
    return mean, var, std, arr


def get_query(arr_var):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute("SELECT "+arr_var+" FROM users" )
    rows = c.fetchall()
    arr_var = []
    #could be an easy one liner
    for row in rows:
        arr_var.append(row[0])
    mean, var, std, arr = get_stats(arr_var)
    conn.close()
    return mean, var, std, arr

def get_len():
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    arr = []
    for row in c.fetchall():
        arr.append(row[0])

    return len(arr)


def user_stats(arr_var):
    conn = sqlite3.connect('db/users.db')
    c = conn.cursor()
    c.execute("SELECT "+arr_var+" FROM users")
    arr = []
    string_list = ["uid", "name", "bio", "ig", "gender"]
    if arr_var in string_list:
        for row in c.fetchall():
            if row[0] is not "":
                arr.append(len(row[0]))
    elif arr_var is "photos":
        for row in c.fetchall():
            arr.append(row[0])
    elif arr_var is "school_id":
        for row in c.fetchall():
            if row[0] is not None:
                arr.append(row[0])
    else:
        for row in c.fetchall():
            arr.append(row[0])

    x = "".join([x for x in arr[0]])
    print(list(x))
    arr_counter = collections.Counter(sorted(arr))
    arr_items = list(arr_counter.keys())
    arr_count = list(arr_counter.values())
    mode = arr_items[arr_count.index(max(arr_count))]
    if arr_var is "school_id":
        c.execute("SELECT school_name FROM users WHERE school_id="+mode+"")
        school_name = c.fetchone()[0]
        return school_name
    
    return mode


if __name__ == '__main__':
    print(user_stats("photos"))
    print('This is a helper file')
