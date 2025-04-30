import numpy as np

# Навчальні вектори (припустимо, їх 3)
v1 = np.array([-1, -1, -1, 1, 1, -1, 1, -1])
v2 = np.array([-1, -1, -1, 1, 1, 1, 1, -1])

# Вхідний вектор для розпізнавання
x = np.array([-1, -1, -1, 1, 1, -1, 1, -1])

# Функція для створення матриці ваг
def calculate_normalized_weights(vectors):
    n = len(vectors[0])
    W = np.zeros((n, n))
    for v in vectors:
        W += np.outer(v, v)
    W /= len(vectors)  # Нормалізація
    np.fill_diagonal(W, 0)
    return W

# Створюємо матрицю ваг
vectors = [v1, v2]
W = calculate_normalized_weights(vectors)

# Функція для ітеративного оновлення вхідного вектора
def hopfield_recognition(W, x, max_iter=10):
    for _ in range(max_iter):
        x_new = np.where(W @ x >= 0, 1, -1)  # уникнення 0
        if np.array_equal(x_new, x):
            break
        x = x_new
    return x

# Розпізнаємо вхідний вектор
recognized = hopfield_recognition(W, x)

# Порівняння з навчальними векторами
def find_best_match(recognized, vectors):
    distances = [np.sum(np.abs(recognized - v)) for v in vectors]
    best_match_index = np.argmin(distances)  # Меньша сума відмінностей
    return best_match_index

# Визначаємо найбільш схожий вектор
best_match = find_best_match(recognized, vectors)

print("Розпізнаний вектор:", recognized)
print(f"Найбільше схожий вектор: v{best_match + 1}")

# np.set_printoptions(precision=3, suppress=False, floatmode='fixed')
print("Нормалізована матриця ваг W:")
print(W)

