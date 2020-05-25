from keras.layers import Dense, Conv2D, BatchNormalization, Activation, Dropout, Flatten, MaxPooling2D, MaxPool2D
from keras.models import Sequential
from keras.optimizers import SGD


class CNN:
    def __init__(self, num_classes, input_shape):
        self.model = Sequential()
        self.num_classes = num_classes
        self.input_shape = input_shape

    def get_model(self):
        self.model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='Same',
                              activation='relu', input_shape=self.input_shape))
        self.model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='Same',
                              activation='relu'))
        self.model.add(MaxPool2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='Same',
                              activation='relu'))
        self.model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='Same',
                              activation='relu'))
        self.model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Flatten())
        self.model.add(Dense(256, activation="relu"))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(self.num_classes, activation="softmax"))

        sgd = SGD(lr=0.0005, decay=0, nesterov=True)

        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        return self.model
