from __future__ import print_function

import keras
import numpy as np
from keras import backend as K
from keras.datasets import mnist
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential

import data_prep

batch_size = 256
num_classes = 2
epochs = 5
img_rows, img_cols = 128, 128

(x_train, y_train), (x_test, y_test) = data_prep.load_data(new_data=False)

# Testing on 1k samples 200 validation - 1 epoch
x_train, y_train = x_train[:20000], y_train[:20000]
x_test, y_test = x_test[:4000], y_test[:4000]

# bug here when loading new data - x_train has no shape
# just re-run with false after youve loaded data
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()

# input stem and block 1 
model.add(Conv2D(32, (3, 3), 
            activation='relu', 
            padding='same',
            name="input_conv1",
            input_shape=input_shape))
model.add(Conv2D(32, (3, 3), padding='same', name="block1_conv2", activation='relu'))
model.add(BatchNormalization(name='block1_bn'))
model.add(MaxPooling2D(pool_size=(2, 2), name='block1_pool'))
model.add(Dropout(0.25, name='block1_drop'))

# block 2 
model.add(Conv2D(64, (3, 3), padding='same', activation='relu', name='block2_conv1'))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu', name='block2_conv2'))
model.add(BatchNormalization(name='block2_bn'))
model.add(MaxPooling2D(pool_size=(2, 2), name='block2_pool'))
model.add(Dropout(0.25, name='block2_drop'))

# block 3
model.add(Conv2D(128, (3, 3), padding='same', activation='relu', name='block3_conv1'))
model.add(Conv2D(128, (3, 3), padding='same', activation='relu', name='block3_conv2'))
model.add(BatchNormalization(name='block3_bn'))
model.add(MaxPooling2D(pool_size=(2, 2), name='block3_pool'))
model.add(Dropout(0.25, name='block3_drop'))

# block 4
model.add(Conv2D(256, (3, 3), padding='same', activation='relu', name='block4_conv1'))
model.add(Conv2D(256, (3, 3), padding='same', activation='relu', name='block4_conv2'))
model.add(BatchNormalization(name='block4_bn'))
model.add(MaxPooling2D(pool_size=(2, 2), name='block4_pool'))
model.add(Dropout(0.25, name='block4_drop'))

# Flatten 
model.add(Flatten(name='flatten'))

# Fully connected block
model.add(Dense(512, activation='relu', name='fc1'))
model.add(BatchNormalization(name='fc1_bn'))
model.add(Dropout(0.5, name='fc1_drop'))
model.add(Dense(128, activation='relu', name='fc2'))
model.add(BatchNormalization(name='fc2_bn'))
model.add(Dropout(0.5, name='fc2_drop'))

# softmax 
model.add(Dense(num_classes, activation='softmax', name='predictions'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])
callbacks = [
        keras.callbacks.TensorBoard(log_dir='working_model/logs',
                histogram_freq=2, write_graph=True, write_images=False)]
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          callbacks=callbacks,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
model.summary()
keras.models.save_model(model, 'working_model/model/5conv_model.h5')
print('Test loss:', score[0])
print('Test accuracy:', score[1])
