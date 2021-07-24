import numpy as np
import tensorflow as tf

def train(x_train, y_train, regressor, noOfUnits, dropout, noOFClass, epochs, batchSize):
    X_train, y_train = np.array(x_train), np.array(y_train)

    # Reshaping
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Part 2 - Building the RNN

    # Importing the Keras libraries and packages
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import LSTM
    from keras.layers import Dropout

    # Adding the first LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units=noOfUnits, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    regressor.add(Dropout(dropout))

    # Adding a second LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units=noOfUnits, return_sequences=True))
    regressor.add(Dropout(dropout))

    # Adding a third LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units=noOfUnits, return_sequences=True))
    regressor.add(Dropout(dropout))

    # Adding a fourth LSTM layer and some Dropout regularisation
    regressor.add(LSTM(units=noOfUnits))
    regressor.add(Dropout(dropout))

    # Adding the output layer
    regressor.add(Dense(units=noOFClass))

    # Compiling the RNN
    regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    # Fitting the RNN to the Training set
    regressor.fit(X_train, y_train, epochs=epochs, batch_size=batchSize)
