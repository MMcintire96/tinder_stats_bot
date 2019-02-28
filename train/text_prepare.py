import json
import sqlite3
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

conn = sqlite3.connect('../db/users.db')
c = conn.cursor()
c.execute("SELECT * FROM users")
dirty_arr= []
for row in c.fetchall():
    user = {
        'bio': row[3],
        'pol': float(row[11]),
        'subj': float(row[12])
    }
    dirty_arr.append(user)

# sentence -> tokenize -> remove stopwords ->normalize/leminze
stop_words = set(stopwords.words("english"))
lem = WordNetLemmatizer()

# wait could this be 1 loop? sure looks like it
def prep_bio(bio):
    for user in clean_arr:
        tokenized_sent = sent_tokenize(user['bio'])
        filtered_sent = []
        for w in tokenized_sent:
            if w not in stop_words:
                filtered_sent.append(w)
        lematized_sent = []
        for sent in filtered_sent:
            lematized_sent.append(lem.lemmatize(sent, 'v'))
        pos_removed_sent = []
        for sent in lematized_sent:
            tagged_sentence = nltk.tag.pos_tag(sent.split())
            cleaned_sent = [word for word,tag in tagged_sentence if tag != 'NNP' or tag != 'NNPS']
            pos_removed_sent.append(' '.join(cleaned_sent))
    return bio


def remove_emoji(bio):
    clean_bio = ""
    for c in bio:
        try:
            c.encode("ascii")
            clean_bio += c
        except UnicodeEncodeError:
            clean_bio += ''
    return clean_bio


clean_arr = []
i = 0
for user in dirty_arr:
    user['bio'] = remove_emoji(user['bio'])
    user['bio'] = prep_bio(user['bio'])
    i += 1
    print(i)
    if user['pol'] != 0.0:
        clean_arr.append(user)
f = open('bio_data.txt', 'w')
print(json.dumps(clean_arr, indent=4), file=f)

