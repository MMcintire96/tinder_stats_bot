import math
import numpy as np
import sqlite3


def get_stats(arr):
    arr = np.array(arr).astype(np.float)
    mean = np.mean(arr)
    var = np.var(arr, dtype=np.float32)
    std = math.sqrt(var)
    return mean, var, std 

def get_query(arr_var):
    conn = sqlite3.connect('db/h_t_db.db')
    c = conn.cursor()
    c.execute("SELECT "+arr_var+" FROM users" )
    rows = c.fetchall()
    arr_var = []
    #could be an easy one liner
    for row in rows:
        arr_var.append(row[0])
    mean, var, std = get_stats(arr_var)
    conn.close()
    return mean, var, std


if __name__ == '__main__':
    get_query('happy')
