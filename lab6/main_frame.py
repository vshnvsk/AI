from PIL import Image, ImageDraw, ImageTk
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import frame as main


class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("220x200")

        self.frame = tk.Frame(root)
        self.frame.grid(column=0, row=0, rowspan=10, padx=50, pady=10)

        self.class1_button = tk.Button(self.frame, text="Upload Class 1 Images",
                                       command=lambda: self.set_class(1))
        self.class1_button.grid(column=0, row=1, pady=5)

        self.class1_button = tk.Button(self.frame, text="Upload Class 2 Images",
                                       command=lambda: self.set_class(2))
        self.class1_button.grid(column=0, row=2, pady=5)

        self.class1_button = tk.Button(self.frame, text="Upload Class 3 Images",
                                       command=lambda: self.set_class(3))
        self.class1_button.grid(column=0, row=3, pady=5)

        self.upload_button = tk.Button(self.frame, text="Open Image Processor", command=self.open_image_processor)
        self.upload_button.grid(column=0, row=4, pady=5)

        self.image_paths = []  # List to hold paths of uploaded images
        self.image_labels = []  # List to hold references to image labels for display

        # Vectors for each class (2 vectors per class: sum and max normalization)
        self.vectors_s1_class1 = []
        self.vectors_m1_class1 = []
        self.vectors_s1_class2 = []
        self.vectors_m1_class2 = []
        self.vectors_s1_class3 = []
        self.vectors_m1_class3 = []

        self.vectors_s1_class1_max = []
        self.vectors_s1_class1_min = []
        self.vectors_s1_class2_max = []
        self.vectors_s1_class2_min = []
        self.vectors_s1_class3_max = []
        self.vectors_s1_class3_min = []

        self.vectors_m1_class1_max = []
        self.vectors_m1_class2_min = []
        self.vectors_m1_class2_max = []
        self.vectors_m1_class1_min = []
        self.vectors_m1_class3_max = []
        self.vectors_m1_class3_min = []

    def set_class(self, class_num):
        self.selected_class = class_num
        self.upload_images()  # Call upload images when a class is set

    def open_image_processor(self):
        new_window = tk.Toplevel(self.frame)
        new_window.title("Image Processor")

        image_processor = main.ImageProcessor(new_window,
                                              self.vectors_s1_class1_max,
                                              self.vectors_s1_class1_min,
                                              self.vectors_s1_class2_max,
                                              self.vectors_s1_class2_min,
                                              self.vectors_s1_class3_max,
                                              self.vectors_s1_class3_min,
                                              self.vectors_m1_class1_max,
                                              self.vectors_m1_class2_min,
                                              self.vectors_m1_class2_max,
                                              self.vectors_m1_class1_min,
                                              self.vectors_m1_class3_max,
                                              self.vectors_m1_class3_min)

    def open_image_window(self, image_path):
        self.image_paths = image_path
        images_window = tk.Toplevel(self.root)
        images_window.title("Selected Images")

        # Створюємо Canvas для прокручування
        canvas = tk.Canvas(images_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Додаємо Scrollbar до Canvas
        scrollbar = tk.Scrollbar(images_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Створюємо фрейм всередині Canvas
        images_frame = tk.Frame(canvas)
        images_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=images_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Відображаємо кожне зображення у сітці 3 зображення в рядок
        self.image_labels = []
        row, col = 0, 0
        for index, file_path in enumerate(image_path):
            img = Image.open(file_path)
            img.thumbnail((200, 200))
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(images_frame, image=img_tk)
            label.image = img_tk  # Зберігаємо посилання на зображення
            label.grid(row=row, column=col, padx=5, pady=5)

            self.image_labels.append(label)

            col += 1
            if col == 5:  # Як тільки досягнуто 3 стовпців, перехід на новий рядок
                col = 0
                row += 1

        # Додаємо кнопку для обробки зображень і центруємо її
        self.process_button = tk.Button(images_window, text="Process Image", command=self.process_all_images)
        self.process_button.pack(pady=20)

    def upload_images(self):
        file_paths = filedialog.askopenfilenames(title='Select Images',
                                                 filetypes=[('Image Files', '*.bmp *.jpeg *.png')])

        if len(file_paths) < 5:
            messagebox.showwarning("Insufficient Images", "Please upload at least 5 images.")
        else:
            self.open_image_window(file_paths)

    def print_matrix(self, matrix, label):
        print(f"\n{label}:")
        for row in matrix:
            rounded_row = [round(float(value), 4) for value in row]
            print(rounded_row)

    def find_min_max(self, matrix):
        max_values = []
        min_values = []

        for i in range(len(matrix[0])):
            column = [matrix[j][i] for j in range(len(matrix))]
            max_value = max(column)
            min_value = min(column)
            max_values.append(max_value)
            min_values.append(min_value)

        return max_values, min_values

    def process_all_images(self):
        # Lists to hold normalization vectors
        if self.selected_class == 1:
            vectors_s1 = self.vectors_s1_class1
            vectors_m1 = self.vectors_m1_class1
            vectors_s1_max = self.vectors_s1_class1_max
            vectors_s1_min = self.vectors_s1_class1_min
            vectors_m1_max = self.vectors_m1_class1_max
            vectors_m1_min = self.vectors_m1_class1_min
        elif self.selected_class == 2:
            vectors_s1 = self.vectors_s1_class2
            vectors_m1 = self.vectors_m1_class2
            vectors_s1_max = self.vectors_s1_class2_max
            vectors_s1_min = self.vectors_s1_class2_min
        elif self.selected_class == 3:
            vectors_s1 = self.vectors_s1_class3
            vectors_m1 = self.vectors_m1_class3
            vectors_s1_max = self.vectors_s1_class3_max
            vectors_s1_min = self.vectors_s1_class3_min
        else:
            messagebox.showerror("Error", "No class selected for processing.")
            return

        for file_path in self.image_paths:
            # 1. Convert the image to black and white
            img = Image.open(file_path)
            processed_image = img.convert("L").point(lambda p: 0 if p < 250 else 255, "1")

            # 2. Create a copy for calculations
            image_for_vector_calculation = processed_image.copy()

            # 3. Draw sectors on the processed image
            self.segment_and_draw_sectors(processed_image)

            img_tk = ImageTk.PhotoImage(processed_image)
            index = self.image_paths.index(file_path)  # Get index
            self.image_labels[index].config(image=img_tk)
            self.image_labels[index].image = img_tk

            # 4. Calculate the feature vector for each sector
            feature_vector = self.calculate_feature_vector(image_for_vector_calculation)
            total_black_pixels = np.sum(feature_vector)

            # Normalize the feature vectors
            normalized_vector_s1 = [x / total_black_pixels if total_black_pixels > 0 else 0 for x in feature_vector]
            vectors_s1.append(normalized_vector_s1)

            max_value = max(feature_vector) if feature_vector else 1
            normalized_vector_m1 = [x / max_value if max_value > 0 else 0 for x in feature_vector]
            vectors_m1.append(normalized_vector_m1)

            # Print results for each image
            print(f"\nProcessed {file_path[35:]}:")
            print("Total black pixels:", total_black_pixels)
            print("Feature vector:", feature_vector)

        self.print_matrix(vectors_s1, "Class - Normalized vectors by sum")
        self.print_matrix(vectors_m1, "Class - Normalized vectors by max")

        vectors_s1_max, vectors_s1_min = self.find_min_max(vectors_s1)
        vectors_m1_max, vectors_m1_min = self.find_min_max(vectors_m1)

        print("\nClass - SMax\n", [round(float(value), 4) for value in vectors_s1_max])
        print("Class - SMin\n", [round(float(value), 4) for value in vectors_s1_min])

        print("\nClass - MMax\n", [round(float(value), 4) for value in vectors_m1_max])
        print("Class - MMin\n", [round(float(value), 4) for value in vectors_m1_min])

        if self.selected_class == 1:
            self.vectors_s1_class1_max = vectors_s1_max
            self.vectors_s1_class1_min = vectors_s1_min
            self.vectors_m1_class1_max = vectors_m1_max
            self.vectors_m1_class1_min = vectors_m1_min
        elif self.selected_class == 2:
            self.vectors_s1_class2_max = vectors_s1_max
            self.vectors_s1_class2_min = vectors_s1_min
            self.vectors_m1_class2_max = vectors_m1_max
            self.vectors_m1_class2_min = vectors_m1_min
        elif self.selected_class == 3:
            self.vectors_s1_class3_max = vectors_s1_max
            self.vectors_s1_class3_min = vectors_s1_min
            self.vectors_m1_class3_max = vectors_m1_max
            self.vectors_m1_class3_min = vectors_m1_min

    def segment_and_draw_sectors(self, image):
        draw = ImageDraw.Draw(image)
        width, height = image.size
        center_x, center_y = width - 1, 0

        sectors = 4
        sector_angles = 90 / sectors

        for i in range(sectors + 1):
            angle = np.radians(i * sector_angles)

            line_end_x = center_x - int(np.cos(angle) * (max(width, height) * 2))
            line_end_y = center_y + int(np.sin(angle) * (max(width, height) * 2))

            draw.line((center_x, center_y, line_end_x, line_end_y), fill="red", width=2)

    def calculate_feature_vector(self, img):
        img_array = np.array(img)
        height, width = img_array.shape
        feature_vector = [0] * 4
        center_x, center_y = width - 1, 0
        sectors = 4
        sector_angles = 90 / sectors

        for y in range(height):
            for x in range(width):
                if img_array[y, x] == 0:  # Ensure the correct indexing for height and width
                    dx = x - center_x
                    dy = center_y - y
                    angle = (np.degrees(np.arctan2(dy, dx)) + 90) % 90

                    for i in range(sectors):
                        if (i * sector_angles) <= angle < ((i + 1) * sector_angles):
                            feature_vector[i] += 1

        return feature_vector


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()