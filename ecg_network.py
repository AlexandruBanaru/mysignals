from keras.layers import InputLayer, Conv1D, Dense, Flatten, MaxPool1D, BatchNormalization, Dropout
from keras.models import Sequential
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler, TensorBoard
import numpy as np
from time import time
from math import pow, floor




class NN():

    def __init__(self, dataset, input_shape, learning_rate=0.1, epochs=200, batch_size=1, test_split=0.1):
        #setting the parameters used for training the network, as well as initializing the dataset
        self.epochs = epochs
        self.batch_size = batch_size
        self.input_shape = input_shape
        self.learning_rate = learning_rate
        self.test_split = test_split
        (self.train_x, self.test_x, self.train_y, self.test_y), self.max = dataset  #initializing the dataset


        #normaliztion of data by dividing the values to the maximum one in the dataset
        #there are obtained values in the interval [-1, 1]
        self.train_x /= (self.max * 1)
        self.test_x /= (self.max *1)

        #setting the optimizer and the loss function
        self.optimizer = SGD(lr=self.learning_rate, momentum=0.05, decay=0.001)
        #momentum = accelerates the movement towards a minimum
        #decay = learning rate over each update
        self.loss = 'binary_crossentropy'

        #setting the input layer of the network
        self.model = Sequential()
        self.model.add(InputLayer(input_shape=(input_shape, 1)))

        self._build() #the network is built


    def _build(self):
        #1D convolutional layer with 100 filters, each of dimension 10
        self.model.add(Conv1D(filters=100,
                              kernel_size=10,
                              activation='sigmoid',
                              input_shape=(self.batch_size, self.input_shape)))
        #normalization of the output of the first layer
        self.model.add(BatchNormalization())
        #creating another convolutional layer identical to the previous one for refining the data
        self.model.add(Conv1D(filters=100,
                              kernel_size=10,
                              activation='relu'))
        #creating a max pooling layer to extract the first relevant features from the filters
        self.model.add(MaxPool1D(strides=5))
        #a convolutional layer of 200 filters, each of dimension 10
        #with the previous max pooling layer, there are taken 50 intervals at once
        self.model.add(Conv1D(filters=200,
                              kernel_size=10,
                              activation='relu'))

        self.model.add(Conv1D(filters=200,
                              kernel_size=10,
                              activation='relu'))
        #the previous output is normalized
        self.model.add(BatchNormalization())
        self.model.add(MaxPool1D(strides=2))
        #separating the layers into a fully connected layer
        self.model.add(Flatten())
        #a dropout layer is created to avoid overfitting
        self.model.add(Dropout(rate=0.25))
        #the final (output) layer is created
        self.model.add(Dense(units=2,
                             activation='softmax'))
        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss,
                           metrics=['accuracy'])
        self.model.summary()

    def train(self):

        #setting the step decay for the learning rate
        def step_decay(epoch):
            initial_lrate = self.learning_rate
            drop = 0.1
            epochs_drop = self.epochs // 10
            lrate = initial_lrate * pow(drop,
                                        floor((1 + epoch) / epochs_drop))
            if lrate > 0.03:
                return lrate
            else:
                return 0.03

        #initializing a call back for the adaptive learning rate
        lr = LearningRateScheduler(step_decay)
        #initializing an early stopper for the training process
        es = EarlyStopping(monitor='val_loss',
                           mode='min',
                           min_delta=0.02,
                           patience=self.epochs // 10,
                           verbose=1)
        #initializing a check point to save the best model
        mc = ModelCheckpoint('best_ecg_model_weights.h5',
                             monitor='val_loss',
                             mode='min',
                             save_best_only=True,
                             verbose=1)
        #initializing the graphical logger
        tb = TensorBoard(log_dir='logs_ecg/{}'.format(time()))

        #starting to train the network with the parameters from the __init__ function
        history = self.model.fit(self.train_x,
                                 self.train_y,
                                 batch_size=self.batch_size,
                                 epochs=self.epochs,
                                 validation_data=(self.test_x, self.test_y),
                                 callbacks=[lr, es, mc, tb])

        #after the training process is done, the weights are saved
        self.model.load_weights('best_ecg_model_weights.h5')
        self.model.save('best_ecg_model.h5')

        return history
