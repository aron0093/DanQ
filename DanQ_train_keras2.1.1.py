'''
06/12/2017 15:22

DanQ modified by Revant Gupta to work with keras 2.1.1. (later versions are not guaranteed as keras updates can be backward incompatible)

'''
import numpy as np
import h5py
import scipy.io
np.random.seed(1337) # for reproducibility

from keras.preprocessing import sequence
from keras.optimizers import RMSprop
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.constraints import maxnorm
from keras.layers.recurrent import LSTM
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Bidirectional


print('loading data')
trainmat = h5py.File('data/train.mat')
validmat = scipy.io.loadmat('data/valid.mat')
testmat = scipy.io.loadmat('data/test.mat')

X_train = np.transpose(np.array(trainmat['trainxdata']),axes=(2,0,1))
y_train = np.array(trainmat['traindata']).T

#X_train = np.ones((500,1000,4))
#y_train = np.zeros((500,919))


lstm = LSTM(units=320, return_sequences=True)
brnn = Bidirectional(lstm)

print('building model')

model = Sequential()
model.add(Conv1D(320, 26, input_shape=(1000,4)))

model.add(MaxPooling1D(strides=13, pool_size=13))

model.add(Dropout(0.2))

model.add(brnn)

model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(925))
model.add(Activation('relu'))

model.add(Dense(919))
model.add(Activation('sigmoid'))

print('compiling model')
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics = ['accuracy'])

print('running at most 60 epochs')

earlystopper = EarlyStopping(monitor='val_loss', patience=5, verbose=1)

model.fit(X_train, y_train, batch_size=100, epochs=60, shuffle=True, verbose=2,
          validation_data=(np.transpose(validmat['validxdata'],axes=(0,2,1)), validmat['validdata']),
          callbacks=[earlystopper]
          )

tresults = model.evaluate(np.transpose(testmat['testxdata'],axes=(0,2,1)), testmat['testdata'])

print("Results")

print (tresults)

