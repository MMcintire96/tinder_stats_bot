import glob
import os
import random
from random import shuffle

import cv2
import numpy as np

image_dir = 'all_faces'
labels = ['happy', 'neutral']
IMG_ROW, IMG_COL = 128, 128

def clean_data():
    for x in labels:
        for f in glob.glob('all_faces/%s/*'%x):
            f_size_kb = os.stat(f).st_size / 1000
            if os.stat(f).st_size is 0 or os.stat(f).st_size is 243 or f_size_kb > 15:
                os.remove(f) 


def split_data():
    clean_data()
    combined_files = []
    train_path = []
    test_path = []
    for x in labels:
        full_path = image_dir + '/' + x
        for root, dirs, files in os.walk(full_path):
            for f in files:
                path = full_path + '/' + f
                combined_files.append(path)
    shuffle(combined_files)
    for img in combined_files:
       randomizer = random.randint(1,10)
       if randomizer <= 8:
            train_path.append(img)
       else:
           test_path.append(img)
    shuffle(train_path)
    shuffle(test_path)
    f = open('working_model/data/training_img.txt', 'w')
    print(train_path, file=f)
    j = open('working_model/data/testing_imgs.txt', 'w')
    print(test_path, file=j)
    return train_path, test_path


def create_label(img_name):
    if 'happy' in img_name:
        return 1
    elif 'neutral' in img_name:
        return 0


def create_train_data():
    training_data = []
    training_labels = []
    train_path, test_path = split_data()
    for img_name in train_path:
        try:
            img_data = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE) 
            img_data = cv2.resize(img_data, (IMG_ROW, IMG_COL))
            training_data.append(img_data)
            training_labels.append(create_label(img_name))
        except Exception as e:
            print(e)
    np.save('working_model/data/train_data.npy', training_data)
    np.save('working_model/data/train_labels.npy', training_labels)
    return training_data, training_labels


def create_test_data():
    testing_data = []
    testing_labels = []
    train_path, test_path = split_data()
    for img_name in test_path:
        try:
            img_data = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE) 
            img_data = cv2.resize(img_data, (IMG_ROW, IMG_COL))
            testing_data.append(img_data)
            testing_labels.append(create_label(img_name))
        except Exception as e:
            print(e)
    np.save('working_model/data/test_data.npy', testing_data)
    np.save('working_model/data/test_labels.npy', testing_labels)
    return testing_data, testing_labels


def load_data(new_data):
    if new_data:
        train_data, train_labels = create_train_data()
        test_data, test_labels = create_test_data()
    else:
        train_data = np.load('working_model/data/train_data.npy')
        train_labels = np.load('working_model/data/train_labels.npy')
        test_data = np.load('working_model/data/test_data.npy')
        test_labels = np.load('working_model/data/test_labels.npy')
    
    return (train_data, train_labels), (test_data, test_labels)


if __name__ == "__main__":
    print("This is a helper file. Organizes data into training/validation sets")
