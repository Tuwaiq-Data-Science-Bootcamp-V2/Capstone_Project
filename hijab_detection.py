import pickle
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import zipfile,os
from tensorflow.keras.utils import load_img
import keras.utils as image1
import numpy as np
from keras.preprocessing import image
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

base_dir = '/Users/shatha_95/Desktop/dataset-5000'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')

train_nonhijab_dir = os.path.join(train_dir, 'nonhijab')
train_hijab_dir = os.path.join(train_dir, 'hijab')

validation_nonhijab_dir = os.path.join(validation_dir, 'nonijab')
validation_hijab_dir = os.path.join(validation_dir, 'hijab')

from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
  rescale=1./255,
  zoom_range=0.2,
  shear_range=0.2,
  horizontal_flip=True)

test_datagen = ImageDataGenerator(
  rescale=1./255,
  zoom_range=0.2,
  shear_range=0.2,
  horizontal_flip=True)

train_generator = train_datagen.flow_from_directory(
  train_dir,
  target_size=(224, 224),
  batch_size=32,
  color_mode='rgb', #
  class_mode='binary',
  shuffle = True,
  seed=42)
validation_generator = test_datagen.flow_from_directory(
  validation_dir,
  target_size=(224, 224),
  batch_size=32,
  color_mode='rgb',
  class_mode='binary',
  shuffle = True,
  seed=42)

sample_images_train, _ = next(train_generator)
sample_images_val, _ = next(validation_generator)

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

result = model.fit(train_generator,
          steps_per_epoch=15,
          epochs=15,
          validation_data=validation_generator,
          validation_steps=5,
          verbose=1)
pickle.dump(model, open("hijab_detection_model.pkl", "wb"))

path = '/Users/shatha_95/Desktop/images_test2.jpg'
img = load_img(path, target_size=(224, 224))
imgplot = plt.imshow(img)
x = image1.img_to_array(img)
x = np.expand_dims(x, axis=0)
classes = model.predict(x, batch_size=32)
if classes == 0:
    print('with hijab')
else:
    print('without hijab')

pickle.dump(model, open("hijab_detection_model.pkl", "wb"))