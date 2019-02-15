import glob
import os
import sqlite3

import cv2
import imutils
import numpy as np
import requests
import tensorflow as tf
from imutils import face_utils
from textblob import TextBlob

import connect
import dlib

# load in graph/labels
with open('model_out/output_labels.txt', 'r') as label_file:
	labels = [line.strip('\n') for line in label_file]
	labels = labels
with tf.gfile.GFile('model_out/output_graph.pb', 'rb') as graph_file:
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(graph_file.read())
	_ = tf.import_graph_def(graph_def, name='')


def get_tb_data(bio):
	tb_data = TextBlob(str(bio))
	polarity = tb_data.sentiment.polarity
	subjectivity = tb_data.sentiment.subjectivity
	return polarity, subjectivity


def get_tf_data(location, photos, uid):
    location = location + '_imgs/'
    f_clean = glob.glob(location + '*')
    for j in f_clean:
        os.remove(j)
    i = 0
    for img in photos:
        img_data = requests.get(img).content
        img_name = str(uid) + '-' + str(i) + '.jpg'
        i += 1
        with open(location + img_name, 'wb') as img_folder:
            img_folder.write(img_data)
    files = sorted(glob.glob(location + '*'))
    img_list = []
    happy = []
    neutral = []
    for f in files:
        if (os.stat(f).st_size is 0) or (os.stat(f).st_size is 243):
            os.remove(f)
        else:
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
            image = cv2.imread(f)
            image = imutils.resize(image, width=640)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)
            if len(rects) > 0:
                for (i, rect) in enumerate(rects):
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    (x,y,w,h) = face_utils.rect_to_bb(rect)
                    c_image = image[y:y+h, x:x+h]
                    # only writes first faces found
                    try:
                        cv2.imwrite(f, cv2.resize(c_image, (128, 128)))
                    except Exception as e:
                        print(str(e))
                img_list.append(f)
                file_reader = tf.read_file(f, "file_reader")
                image_reader = tf.image.decode_jpeg(
                    file_reader, channels=3, name='jpeg-reader')
                float_caster = tf.cast(image_reader, tf.float32)
                dims_expander = tf.expand_dims(float_caster, 0)
                resized = tf.image.resize_bilinear(dims_expander, [299, 299])
                normalized = tf.divide(tf.subtract(resized, [0]), [255])
                with tf.Session() as sess:
                    c_img = sess.run(normalized)
                    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
                    predictions = sess.run(softmax_tensor, {'Placeholder:0': c_img})
                    prediction = predictions[0].tolist()
                    happy.append(prediction[0])
                    neutral.append(prediction[1])
                    img = cv2.imread(f)
                    if prediction[0] > 0.5:
                        cv2.imwrite('happy_imgs/%s' %os.path.basename(f), img)
                    else:
                        cv2.imwrite('neutral_imgs/%s' %os.path.basename(f), img)
                    os.remove(f)
            else:
                os.remove(f) 
    if len(happy) is 0:
        avg_happy = 0
        avg_neutral = 0
    else:
        avg_happy = sum(happy) / len(happy)
        avg_neutral = sum(neutral) / len(neutral)
    return avg_happy, avg_neutral


if __name__ == '__main__':
	print("This is a helper file, called from the liker and messager")
