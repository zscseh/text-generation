import os.path

import numpy
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

# load ascii text and convert to lowercase
res_path = 'res'
filename = 'wonderland.txt'
raw_text = open(os.path.join(res_path, filename)).read()
raw_text = raw_text.lower()

# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))

# summerize the dataset
n_chars = len(raw_text)
n_vocab = len(chars)
# print('total characters: ', n_chars)
# print('total vocab: ', n_vocab)

# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length):
    seq_in = raw_text[i : i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print('total patterns: ', n_patterns)

# reshape X to be [samples, timesteps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)

# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# define the checkpoint
checkpoint_path = os.path.join('checkpoints', 'weights-improvement-{epoch:02d}-{loss:.4f}.hdf5')
checkpoint = ModelCheckpoint(checkpoint_path, monitor='loss', verbose=1, save_best_only=True, mode='min')
callback_list = [checkpoint]

model.fit(X, y, epochs=20, batch_size=128, callbacks=callback_list)