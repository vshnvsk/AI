import numpy as np


class Perceptron(object):

    def __init__(self, eta=0.01, n_iter=10):
        self.eta = eta
        self.n_iter = n_iter

    def weighted_sum(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return np.where(self.weighted_sum(X) >= 0.0, 1, -1)

    def fit(self, X, y):

        # initializing the weights to 0
        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        print("Weights:", self.w_)

        # training the model n_iter times
        for _ in range(self.n_iter):
            error = 0

            # loop through each input
            for xi, target in zip(X, y):
                # 1. calculate ŷ (the predicted value)
                y_pred = self.predict(xi)

                # 2. calculate Update
                # update = η * (y - ŷ)
                update = self.eta * (target - y_pred)

                # 3. Update the weights
                # Wi = Wi + Δ(Wi)   where  Δ(Wi) = η * (y - ŷ) = update * Xi
                self.w_[1:] = self.w_[1:] + update * xi
                print("Updated Weights:", self.w_[1:])

                # Update the bias (Xo = 1)
                self.w_[0] = self.w_[0] + update

                # if update != 0, it means that ŷ != y
                error += int(update != 0.0)

            self.errors_.append(error)

        return self

#
# X = np.array([
#     # class 1
#     [0.0494, 0.3259, 0.3694, 0.2552],
#     [0.1451, 0.2508, 0.4214, 0.1826],
#     [0.1963, 0.2286, 0.4079, 0.1671],
#     [0.1496, 0.2616, 0.4325, 0.1563],
#     [0.0643, 0.3257, 0.4368, 0.1733],
#     # class 2
#     [0.1014, 0.4046, 0.4099, 0.0841],
#     [0.1602, 0.334, 0.3398, 0.166],
#     [0.0609, 0.3291, 0.4317, 0.1783],
#     [0.251, 0.3213, 0.3302, 0.0974],
#     [0.1469, 0.3519, 0.3541, 0.1471]
# ])
#
# ppn = Perceptron(eta=0.1, n_iter=10)
# y = np.array([1, 1, 1, 1, 1, -1, -1, -1, -1, -1])
#
# ppn.fit(X, y)
#
# test_vector = np.array([0.251, 0.4046, 0.4317, 0.1783])
#
# predicted_class = ppn.predict(test_vector)
#
# print("Predicted class:", predicted_class)