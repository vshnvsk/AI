import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageOps, ImageDraw
from sklearn.metrics import pairwise_distances
import numpy as np


class ImageProcessor:
    # change
    def __init__(self, root, vectors_s1_class1_avg, vectors_s1_class2_avg,
                 vector_hopfield_class1, vector_hopfield_class2):
        self.root = root
        self.root.title("Image Processor")

        # Створюємо фрейм для картинки (зліва)
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(column=0, row=0, rowspan=10, padx=10, pady=10)

        # Створюємо фрейм для решти елементів (справа)
        self.right_frame = tk.Frame(root)
        self.right_frame.grid(column=1, row=0, padx=10, pady=10)

        # Додаємо елементи в лівий фрейм (картинка)
        self.image_label = tk.Canvas(self.left_frame, width=700, height=550)
        self.image_label.pack()

        # Додаємо елементи в правий фрейм
        self.upload_button = tk.Button(self.right_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(column=0, row=0)

        # Кнопки для обрізання
        self.crop_button = tk.Button(self.right_frame, text="Crop", command=self.crop_image)
        self.crop_button.grid(column=0, row=1)

        self.threshold_label = tk.Label(self.right_frame, text="Black Threshold:")
        self.threshold_label.grid(column=0, row=2)

        self.threshold_entry = tk.Entry(self.right_frame)
        self.threshold_entry.grid(column=0, row=3)

        self.process_button = tk.Button(self.right_frame, text="Process Image", command=self.process_image)
        self.process_button.grid(column=0, row=6)

        self.feature_vector_label = tk.Label(self.right_frame, text="Feature Vector:")
        self.feature_vector_label.grid(column=0, row=7)

        self.feature_vector_text = tk.Text(self.right_frame, height=3, width=50)
        self.feature_vector_text.grid(column=0, row=8)

        self.class_vector_label = tk.Label(self.right_frame, text="Class Vector:")
        self.class_vector_label.grid(column=0, row=9)

        self.class_vector_text = tk.Text(self.right_frame, height=3, width=55)
        self.class_vector_text.grid(column=0, row=10)

        # self.vector_label_d = tk.Label(self.right_frame, text="Calculated lengths:")
        # self.vector_label_d.grid(column=0, row=11)
        #
        # self.vector_text_d = tk.Text(self.right_frame, height=3, width=55)
        # self.vector_text_d.grid(column=0, row=12)

        self.normalized_vector_label = tk.Label(self.right_frame, text="Normalized Vector:")
        self.normalized_vector_label.grid(column=0, row=13)

        self.normalized_vector_text_s1 = tk.Text(self.right_frame, height=2, width=60)
        self.normalized_vector_text_s1.grid(column=0, row=14)

        self.normalized_vector_text_b = tk.Text(self.right_frame, height=2, width=60)
        self.normalized_vector_text_b.grid(column=0, row=15)

        # self.vector_label_s = tk.Label(self.right_frame, text="Classes vectors S:")
        # self.vector_label_s.grid(column=0, row=16)
        #
        # self.vector_text_s = tk.Text(self.right_frame, height=5, width=60)
        # self.vector_text_s.grid(column=0, row=17)

        self.vector_label_b = tk.Label(self.right_frame, text="Classes binarised vectors:")
        self.vector_label_b.grid(column=0, row=18)

        self.vector_text_b = tk.Text(self.right_frame, height=4, width=70)
        self.vector_text_b.grid(column=0, row=19)

        self.vector_matrix = tk.Label(self.right_frame, text="Normalized Matrix:")
        self.vector_matrix.grid(column=0, row=20)

        self.vector_matrix_text = tk.Text(self.right_frame, height=9, width=70)
        self.vector_matrix_text.grid(column=0, row=21)

        self.image = None
        self.processed_image = None

        # Додаємо змінні для обрізання
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.crop_rectangle = None

        # Встановлюємо обробники для вибору обрізання
        self.image_label.bind("<ButtonPress-1>", self.start_crop)
        self.image_label.bind("<B1-Motion>", self.update_crop)
        self.image_label.bind("<ButtonRelease-1>", self.perform_crop)

        self.vectors_s1_class1_avg = vectors_s1_class1_avg
        self.vectors_s1_class2_avg = vectors_s1_class2_avg

        # hophield
        self.vector_hopfield_class1 = vector_hopfield_class1
        self.vector_hopfield_class2 = vector_hopfield_class2

        self.display_vectors()

    def display_vectors(self):
        # Відображаємо вектори у текстовому полі
        all_vectors_s = {
            "Class 1 Vector S1 Avg": self.vectors_s1_class1_avg,
            "Class 2 Vector S1 Avg": self.vectors_s1_class2_avg
        }

        all_vectors_b = {
            "Class 1 Vector bin": self.vector_hopfield_class1,
            "Class 2 Vector bin": self.vector_hopfield_class2
        }

        # for class_name, vectors in all_vectors_s.items():
        #     self.vector_text_s.insert(tk.END, f"{class_name}: {[round(float(value), 4) for value in vectors]}\n")

        for class_name, vectors in all_vectors_b.items():
            self.vector_text_b.insert(tk.END, f"{class_name}: {[int(value) for value in vectors]}\n")

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

    def display_image(self, image):
        max_width, max_height = 800, 600

        original_width, original_height = image.size
        scaling_factor = min(max_width / original_width, max_height / original_height, 1)

        new_width = int(original_width * scaling_factor)
        new_height = int(original_height * scaling_factor)

        # Змінюємо розмір зображення з урахуванням максимальних розмірів
        img = image.resize((new_width, new_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img)

        self.image_label.delete("all")
        x_offset = (800 - new_width) // 2
        y_offset = (600 - new_height) // 2

        # Display the image centered in the canvas
        self.image_label.create_image(x_offset, y_offset, anchor=tk.NW, image=self.tk_image)
        self.image_label.image = self.tk_image

        # Store the scaling factor for cropping
        self.scaling_factor = scaling_factor

    def start_crop(self, event):
        # Store the initial click coordinates
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.image_label.delete(self.rect_id)
        self.rect_id = None

    def update_crop(self, event):
        if self.rect_id:
            self.image_label.delete(self.rect_id)

        # Create a rectangle for selection
        self.rect_id = self.image_label.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red")

    def perform_crop(self, event):
        end_x = event.x
        end_y = event.y

        # Calculate the offsets to adjust for the centered image
        x_offset = (800 - self.tk_image.width()) // 2
        y_offset = (600 - self.tk_image.height()) // 2

        # Adjust crop rectangle based on the offsets
        adjusted_start_x = int((self.start_x - x_offset) / self.scaling_factor)
        adjusted_start_y = int((self.start_y - y_offset) / self.scaling_factor)
        adjusted_end_x = int((end_x - x_offset) / self.scaling_factor)
        adjusted_end_y = int((end_y - y_offset) / self.scaling_factor)

        # Store the adjusted coordinates for cropping
        self.crop_rectangle = (adjusted_start_x, adjusted_start_y, adjusted_end_x, adjusted_end_y)

    def crop_image(self):
        if self.crop_rectangle and self.image:
            # Обрізаємо зображення за вибраними координатами
            cropped_image = self.image.crop(self.crop_rectangle)
            self.processed_image = cropped_image  # Зберігаємо обрізане зображення для подальшої обробки
            self.display_image(cropped_image)

            if self.rect_id:
                self.image_label.delete(self.rect_id)
                self.rect_id = None

    def process_image(self):
        if self.processed_image is None:
            if self.image is None:
                messagebox.showerror("Error", "No image uploaded or cropped")
                return

            self.processed_image = self.image

        threshold = self.threshold_entry.get()
        if not threshold.isdigit():
            messagebox.showerror("Error", "Invalid threshold value")
            return

        threshold = int(threshold)
        self.processed_image = self.processed_image.convert("L")
        self.processed_image = self.processed_image.point(lambda p: 255 if p > threshold else 0, '1')

        # Створюємо копію для обчислень, без сегментів
        self.image_for_vector_calculation = self.processed_image.copy()

        self.segment_and_draw_sectors()
        self.display_image(self.processed_image)
        self.calculate_feature_vector()
        self.processed_image = None

    def segment_and_draw_sectors(self):
        draw = ImageDraw.Draw(self.processed_image)
        width, height = self.processed_image.size
        center_x, center_y = width - 1, 0

        sectors = 16
        sector_angles = 90 / sectors  # Сектори займають 90 градусів

        for i in range(sectors + 1):
            angle = np.radians(i * sector_angles)

            line_end_x = center_x - int(np.cos(angle) * (max(width, height) * 2))
            line_end_y = center_y + int(np.sin(angle) * (max(width, height) * 2))

            draw.line((center_x, center_y, line_end_x, line_end_y), fill="red", width=2)

    def calculate_feature_vector(self):
        img_array = np.array(self.image_for_vector_calculation)
        height, width = img_array.shape
        total_black_pixels = np.sum(img_array == 0)
        center_x, center_y = width - 1, 0

        sectors = 16
        sector_angles = 90 / sectors

        feature_vector = []

        for i in range(sectors):
            start_angle = i * sector_angles
            end_angle = (i + 1) * sector_angles

            sector_mask = np.zeros_like(img_array, dtype=bool)

            for y in range(height):
                for x in range(width):
                    dx = x - center_x
                    dy = center_y - y
                    angle = (np.degrees(np.arctan2(dy, dx)) + 90) % 90

                    if start_angle <= angle < end_angle:
                        sector_mask[y, x] = True

            sector_black_pixels = np.sum(np.logical_and(img_array == 0, sector_mask))
            feature_vector.append(sector_black_pixels)

        # Очищуємо і виводимо інформацію про вектори
        self.feature_vector_text.delete(1.0, tk.END)
        self.normalized_vector_text_s1.delete(1.0, tk.END)
        self.normalized_vector_text_b.delete(1.0, tk.END)

        # Форматування тексту
        feature_vector_str = ', '.join([f'S{i + 1}: {count}' for i, count in enumerate(feature_vector)])
        self.feature_vector_text.insert(tk.END, feature_vector_str)

        # Нормалізація за сумою (варіант 1)
        normalized_vector_s1 = [x / total_black_pixels if total_black_pixels > 0 else 0 for x in feature_vector]
        normalized_vector_str_s1 = ', '.join(
            [f'(S{i + 1}, {val:.4f})' for i, val in enumerate(normalized_vector_s1)])
        self.normalized_vector_text_s1.insert(tk.END, f"[{normalized_vector_str_s1}]")

        threshold = 0.05
        vector_hopfield = [[1 if value > threshold else -1 for value in normalized_vector_s1]]
        print(vector_hopfield)

        # бінаризація
        normalized_vector_str_b = ', '.join(map(str, vector_hopfield[0]))
        self.normalized_vector_text_b.insert(tk.END, f"[{normalized_vector_str_b}]")

        # change start
        class_vectors = {
            'Class 1': (self.vector_hopfield_class1),
            'Class 2': (self.vector_hopfield_class2)
        }

        # hopfield_distances = []
        # for class_name, class_vector in class_vectors.items():
        #     distance = sum(1 for i in range(len(vector_hopfield[0])) if vector_hopfield[0][i] != class_vector[i])
        #     hopfield_distances.append(distance)

        # Очищуємо і виводимо відстані
        # self.vector_text_d.delete(1.0, tk.END)
        # hopfield_distance_str = ', '.join([f'd{i+1}: {d:.4f}' for i, d in enumerate(hopfield_distances)])
        # self.vector_text_d.insert(tk.END, f"[{hopfield_distance_str}]")

        vectors = [self.vector_hopfield_class1, self.vector_hopfield_class2]
        print("frame", vectors)

        W = self.calculate_normalized_weights(vectors)

        self.vector_matrix_text.delete(1.0, tk.END)
        self.vector_matrix_text.insert(tk.END, f"[{W}]")

        x = vector_hopfield[0]
        recognized = self.hopfield_recognition(W, x)

        best_match = self.find_best_match(recognized, vectors)

        self.class_vector_text.delete(1.0, tk.END)
        self.class_vector_text.insert(tk.END, f"Розпізнаний вектор: {recognized}\n")
        self.class_vector_text.insert(tk.END, best_match)
        # change end

    # change
    def calculate_normalized_weights(self, vectors):
        n = len(vectors[0])
        W = np.zeros((n, n))
        for v in vectors:
            W += np.outer(v, v)
        W /= len(vectors)  # Нормалізація
        np.fill_diagonal(W, 0)
        return W

    def hopfield_recognition(self, W, x, max_iter=10):
        for _ in range(max_iter):
            x_new = np.where(W @ x >= 0, 1, -1)  # уникнення 0
            if np.array_equal(x_new, x):
                break
            x = x_new
        return x

    def find_best_match(self, recognized, vectors):
        distances = [np.sum(np.abs(recognized - v)) for v in vectors]
        best_match_index = np.argmin(distances)  # Меньша сума відмінностей
        return f"Найбільше схожий вектор: {best_match_index + 1}"

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
