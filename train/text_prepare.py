import json
import sqlite3
import numpy as np
import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from textblob import TextBlob

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

#write a regex to remove @instagra/snapchat
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
    return clean_arr


def load_data():
    bio_data = clean_data()
    labeled_sents = []
    for user in bio_data:
        for sent in user['bio']:
            tb_data = TextBlob(sent)
            pol = round((tb_data.sentiment.polarity),2)
            if pol != 0.0:
                taged_sent = [sent, pol]
                labeled_sents.append(taged_sent)
    return labeled_sents


def split_data():
    data = load_data()
    test_data = []
    train_data = []
    random.shuffle(data)
    for x in data:
        randomizer = random.randint(1,10)
        if randomizer <= 8:
            train_data.append(x)
        else:
            test_data.append(x)
    return test_data, train_data


def split_labels():
    test_data, train_data = split_data()
    test_labels, train_labels = [], []
    for x in test_data:
        test_labels.append(x[1])
        del x[1]
    for x in train_data:
        train_labels.append(x[1])
        del x[1]
    np.save('working_model/text_data/train_data.npy', train_data)
    np.save('working_model/text_data/train_labels.npy', train_labels)
    np.save('working_model/text_data/test_data.npy', test_data)
    np.save('working_model/text_data/test_labels.npy', test_labels)
    return (train_data, train_labels), (test_data, test_labels)


def get_data(new_data):
    if new_data:
        (train_data, train_labels), (test_data, test_labels) = split_labels()
    else:
       train_data = np.load('working_model/text_data/train_data.npy')
       train_labels = np.load('working_model/text_data/train_labels.npy')
       test_data = np.load('working_model/text_data/test_data.npy')
       test_labels = np.load('working_model/text_data/test_labels.npy')

    return (train_data, train_labels), (test_data, test_labels)



if __name__ == "__main__":
    print("cleans the bio data")
    print("call get_data(new_data=True) from the cnn")
    get_data(new_data=True)
