import numpy as np


def validate(x_test,regressor):
    # Part 3 - Making the predictions and visualising the results
    x_test  = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predicted_output = regressor.predict(x_test)
    return predicted_output