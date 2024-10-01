import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageOps, ImageDraw
import numpy as np


class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # Створюємо фрейм для картинки (зліва)
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(column=0, row=0, rowspan=10, padx=10, pady=10)

        # Створюємо фрейм для решти елементів (справа)
        self.right_frame = tk.Frame(root)
        self.right_frame.grid(column=1, row=0, padx=10, pady=10)

        # Додаємо елементи в лівий фрейм (картинка)
        self.image_label = tk.Label(self.left_frame)
        self.image_label.pack()

        # Додаємо елементи в правий фрейм
        self.upload_button = tk.Button(self.right_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.grid(column=0, row=0)

        self.threshold_label = tk.Label(self.right_frame, text="Black Threshold:")
        self.threshold_label.grid(column=0, row=1)

        self.threshold_entry = tk.Entry(self.right_frame)
        self.threshold_entry.grid(column=0, row=2)

        self.sector_label = tk.Label(self.right_frame, text="Number of Sectors:")
        self.sector_label.grid(column=0, row=3)

        self.sector_selector = ttk.Spinbox(self.right_frame, from_=2, to=10)
        self.sector_selector.grid(column=0, row=4)

        self.process_button = tk.Button(self.right_frame, text="Process Image", command=self.process_image)
        self.process_button.grid(column=0, row=5)

        self.feature_vector_label = tk.Label(self.right_frame, text="Feature Vector:")
        self.feature_vector_label.grid(column=0, row=6)

        self.feature_vector_text = tk.Text(self.right_frame, height=10, width=50)
        self.feature_vector_text.grid(column=0, row=7)

        self.normalized_vector_label = tk.Label(self.right_frame, text="Normalized Vector (S1):")
        self.normalized_vector_label.grid(column=0, row=8)

        # self.normalized_vector_text_s1 = tk.Text(self.right_frame, height=10, width=50)
        # self.normalized_vector_text_s1.grid(column=0, row=9)

        self.normalized_vector_text_s1 = tk.Text(self.right_frame, height=2, width=50)  # Для нормалізації за сумою
        self.normalized_vector_text_s1.grid(column=0, row=10)

        self.normalized_vector_text_s2 = tk.Text(self.right_frame, height=2, width=50)  # Для нормалізації за модулем
        self.normalized_vector_text_s2.grid(column=0, row=11)

        self.image = None
        self.processed_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

    def display_image(self, image):
        max_width, max_height = 1360, 1080

        original_width, original_height = image.size
        scaling_factor = min(max_width / original_width, max_height / original_height, 1)

        new_width = int(original_width * scaling_factor)
        new_height = int(original_height * scaling_factor)

        # Змінюємо розмір зображення з урахуванням максимальних розмірів
        img = image.resize((new_width, new_height), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        # Відображаємо зображення
        self.image_label.config(image=img)
        self.image_label.image = img

    def process_image(self):
        if self.image is None:
            messagebox.showerror("Error", "No image uploaded")
            return

        threshold = self.threshold_entry.get()
        if not threshold.isdigit():
            messagebox.showerror("Error", "Invalid threshold value")
            return

        threshold = int(threshold)
        self.processed_image = self.image.convert("L")
        self.processed_image = self.processed_image.point(lambda p: 255 if p > threshold else 0, '1')

        # Створюємо копію для обчислень, без сегментів
        self.image_for_vector_calculation = self.processed_image.copy()

        self.segment_and_draw_sectors()
        self.display_image(self.processed_image)
        self.calculate_feature_vector()

    def segment_and_draw_sectors(self):
        draw = ImageDraw.Draw(self.processed_image)
        width, height = self.processed_image.size
        center_x, center_y = width - 1, 0

        sectors = int(self.sector_selector.get())
        sector_angles = 90 / sectors  # Сектори займають 90 градусів

        for i in range(sectors + 1):
            angle = np.radians(i * sector_angles)

            line_end_x = center_x - int(np.cos(angle) * (max(width, height) * 2))
            line_end_y = center_y + int(np.sin(angle) * (max(width, height) * 2))

            draw.line((center_x, center_y, line_end_x, line_end_y), fill="red", width=2)

    def calculate_feature_vector(self):
        # img_array = np.array(self.processed_image)
        img_array = np.array(self.image_for_vector_calculation)
        height, width = img_array.shape
        total_black_pixels = np.sum(img_array == 0)
        center_x, center_y = width - 1, 0

        sectors = int(self.sector_selector.get())
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
        self.normalized_vector_text_s2.delete(1.0, tk.END)

        # Форматування тексту
        feature_vector_str = ', '.join([f'x{i + 1}: {count}' for i, count in enumerate(feature_vector)])
        self.feature_vector_text.insert(tk.END, f"[{feature_vector_str}]")

        # Нормалізація за сумою (варіант 1)
        normalized_vector_s1 = [x / total_black_pixels if total_black_pixels > 0 else 0 for x in feature_vector]
        normalized_vector_str_s1 = ', '.join([f'(S{i + 1}, {val:.4f})' for i, val in enumerate(normalized_vector_s1)])
        self.normalized_vector_text_s1.insert(tk.END, f"[{normalized_vector_str_s1}]")

        # Нормалізація за модулем (варіант 2)
        max_value = max(feature_vector) if feature_vector else 1  # Уникнути ділення на 0
        normalized_vector_s2 = [x / max_value if max_value > 0 else 0 for x in feature_vector]
        normalized_vector_str_s2 = ', '.join([f'(M{i + 1}, {val:.4f})' for i, val in enumerate(normalized_vector_s2)])
        self.normalized_vector_text_s2.insert(tk.END, f"[{normalized_vector_str_s2}]")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
