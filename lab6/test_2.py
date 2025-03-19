import numpy as np


class Perceptron:
    def __init__(self, input_size, learning_rate=0.1, epochs=10):
        self.weights = np.random.rand(input_size)
        self.bias = 0.0
        self.learning_rate = learning_rate
        self.epochs = epochs

    def activation_function(self, z):
        return 1 if z >= 0 else -1

    def train(self, X, y):
        for epoch in range(self.epochs):
            for i in range(len(X)):
                z = np.dot(X[i], self.weights) + self.bias
                y_pred = self.activation_function(z)

                if y_pred != y[i]:
                    self.weights += self.learning_rate * (y[i] - y_pred) * X[i]
                    self.bias += self.learning_rate * (y[i] - y_pred)

    def predict(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self.activation_function(z)


# Навчальні дані
X_train = np.array([
    [0.0228, 0.0601, 0.2925, 0.2111, 0.3061, 0.1075],
    [0.0409, 0.2746, 0.0806, 0.3014, 0.1867, 0.1159],
    [0.0816, 0.2465, 0.0968, 0.3149, 0.1635, 0.0967],
    [0.0467, 0.2742, 0.0903, 0.3317, 0.1615, 0.0955],
    [0.0241, 0.2508, 0.115, 0.321, 0.1822, 0.1068],
    [0.0558, 0.1306, 0.2822, 0.2324, 0.1475, 0.1516],
    [0.0591, 0.1454, 0.4453, 0.1453, 0.1037, 0.1011],
    [0.0659, 0.1175, 0.2734, 0.2632, 0.119, 0.161],
    [0.034, 0.1444, 0.3095, 0.2068, 0.1562, 0.1491],
    [0.0825, 0.148, 0.378, 0.1472, 0.1522, 0.0921]
])
y_train = np.array([1, 1, 1, 1, 1, -1, -1, -1, -1, -1])

# Тестовий приклад
X_test = np.array([0.0587, 0.2985, 0.1491, 0.3125, 0.1551, 0.0262])

# Створення і навчання перцептрона
perceptron = Perceptron(input_size=6)
perceptron.train(X_train, y_train)

# Тестування
y_pred = perceptron.predict(X_test)
print("Результат для тестового набору:", y_pred)