import json
import sqlite3
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


def fetch_data():
    conn = sqlite3.connect('../db/users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    dirty_arr = []
    for row in c.fetchall():
        user = {
            'bio': row[3],
            'pol': float(row[11]),
            'subj': float(row[12])
        }
        dirty_arr.append(user)
    return dirty_arr


def remove_emoji(bio):
    clean_bio = ""
    for c in bio:
        try:
            c.encode("ascii")
            clean_bio += c
        except UnicodeEncodeError:
            clean_bio += ''
    return clean_bio


# sentence -> tokenize -> remove stopwords ->normalize/leminze
stop_words = set(stopwords.words("english"))
lem = WordNetLemmatizer()
def nltk_bio(bio):
    tokenized_sent = sent_tokenize(bio)
    clean_sent = []
    for w in tokenized_sent:
        if w not in stop_words:
            filtered_sent = w
            lemanized_sent = lem.lemmatize(filtered_sent, 'v')
            tagged_sentence = nltk.tag.pos_tag(lemanized_sent.split())
            cleaned_sent = [word for word,tag in tagged_sentence if tag != 'NNP' or tag != 'NNPS']
            clean_sent.append(' '.join(cleaned_sent))
    return clean_sent


def clean_data():
    dirty_arr = fetch_data()
    clean_arr = []
    i = 0
    for user in dirty_arr:
        if user['pol'] != 0.0 and len(user['bio']) != 0:
            user['bio'] = remove_emoji(user['bio'])
            user['bio'] = nltk_bio(user['bio'])
            clean_arr.append(user)
        i += 1
        print(i)
    f = open('bio_data.txt', 'w')
    print(json.dumps(clean_arr, indent=4), file=f)

def load_data():
    f = open('bio_data.txt', 'r').read()
    bio_data = json.loads(f)
    print(bio_data[1]['bio'][0])


if __name__ == "__main__":
    print("cleans the bio data")
    load_data()
