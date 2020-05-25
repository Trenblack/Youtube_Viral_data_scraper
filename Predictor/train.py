import os
import cv2
from sklearn.model_selection import train_test_split
import numpy as np
from keras.utils import to_categorical

from architecture import CNN

input_shape = (160, 160, 3)
epochs = 50
batch_size = 32

model = CNN(3, input_shape).get_model()

X = []
y = []

dataset_path = os.path.join(os.getcwd(), "Dataset")

paths = os.listdir(dataset_path)
counter = 0
for folder in paths:
    images_path = os.path.join(dataset_path, folder)
    images_list = os.listdir(images_path)
    for image in images_list:
        img = cv2.imread(os.path.join(images_path, image))
        img = cv2.resize(img, (160, 160))
        img = img.astype('float') / 255.0
        X.append(img)
        y.append(counter)
    counter = counter + 1
y = to_categorical(y, num_classes=3)
X = np.array(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, shuffle='true',
          validation_data=(X_test, y_test))
model.save('NN.h5')
