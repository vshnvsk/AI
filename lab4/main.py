import tkinter as tk
import math

# Initialize constants
SECTOR_ANGLE = 45  # Each sector is 45 degrees (360/8)
NUM_SECTORS = 8
TEXT_PADDING_X = 12  # Horizontal padding in pixels
TEXT_PADDING_Y = 12  # Vertical padding in pixels


def reduce_list(lst):
    return [lst[i] for i in range(len(lst)) if i == 0 or lst[i] != lst[i - 1]]


# Calculate angle between two points
def calculate_angle(p1, p2):
    delta_y = p2[1] - p1[1]
    delta_x = p2[0] - p1[0]
    angle = math.degrees(math.atan2(delta_y, delta_x))
    return angle + 360 if angle < 0 else angle


# Determine sector from angle
def get_sector(angle):
    return int(angle // SECTOR_ANGLE) + 1


# Calculate similarity between two lists
def calculate_similarity(list1, list2):
    matches = sum(1 for a, b in zip(list1, list2) if a == b)
    return (matches / max(len(list1), len(list2))) * 100


class DirectionDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Direction Drawing App")

        # Create two canvases for drawing
        self.canvas1 = tk.Canvas(root, bg="white", width=300, height=300)
        self.canvas2 = tk.Canvas(root, bg="white", width=300, height=300)
        self.canvas1.grid(row=0, column=0, padx=10, pady=10)
        self.canvas2.grid(row=0, column=1, padx=10, pady=10)

        # Variables to store points and directions
        self.points1, self.directions1 = [], []
        self.points2, self.directions2 = [], []

        # Bind mouse events for drawing
        self.canvas1.bind("<Button-1>", self.start_draw1)
        self.canvas1.bind("<B1-Motion>", self.draw1)
        self.canvas2.bind("<Button-1>", self.start_draw2)
        self.canvas2.bind("<B1-Motion>", self.draw2)

        # Label for similarity result
        self.similarity_label_f = tk.Label(root, text="Similarity with full vector: N/A", font=("Century Gothic", 11))
        self.similarity_label_f.grid(row=1, column=0, columnspan=2, pady=5)
        self.similarity_label_s = tk.Label(root, text="Similarity with short vector: N/A", font=("Century Gothic", 11))
        self.similarity_label_s.grid(row=2, column=0, columnspan=2, pady=5)

        # Text widgets to display vectors
        self.vector1_text_f = tk.Text(root, height=4, width=40, font=("Century Gothic", 10), wrap="none")
        self.vector1_text_f.grid(row=3, column=0, padx=10)
        self.vector2_text_f = tk.Text(root, height=4, width=40, font=("Century Gothic", 10), wrap="none")
        self.vector2_text_f.grid(row=3, column=1, padx=10)
        self.vector1_text_s = tk.Text(root, height=4, width=40, font=("Century Gothic", 10), wrap="none")
        self.vector1_text_s.grid(row=4, column=0, padx=10)
        self.vector2_text_s = tk.Text(root, height=4, width=40, font=("Century Gothic", 10), wrap="none")
        self.vector2_text_s.grid(row=4, column=1, padx=10)

        # Button to calculate similarity

        self.px_label = tk.Label(root, text="PX:")
        self.px_label.grid(column=0, row=5)

        self.px_selector = tk.Spinbox(root, from_=10, to=100)
        self.px_selector.grid(column=1, row=5)

        self.compare_button = tk.Button(root, text="Compare", command=self.compare_drawings)
        self.compare_button.grid(row=6, column=0, columnspan=2, pady=10)

    # Start drawing on canvas 1
    def start_draw1(self, event):
        self.canvas1.delete("all")
        self.points1, self.directions1 = [(event.x, event.y)], []
        self.canvas1.delete("text")

    # Draw on canvas 1 with direction tracking
    def draw1(self, event):
        last_point = self.points1[-1]
        new_point = (event.x, event.y)

        # Only draw and record if the distance exceeds STEP_SIZE
        if math.hypot(new_point[0] - last_point[0], new_point[1] - last_point[1]) >= int(self.px_selector.get()):
            self.canvas1.create_line(last_point[0], last_point[1], new_point[0], new_point[1], fill="green", width=2)
            angle = calculate_angle(last_point, new_point)
            sector = get_sector(angle)
            self.directions1.append(sector)
            self.points1.append(new_point)

            # Display sector number on the canvas
            mid_point = ((last_point[0] + new_point[0]) / 2, (last_point[1] + new_point[1]) / 2)
            self.canvas1.create_text(mid_point[0] + TEXT_PADDING_X, mid_point[1] + TEXT_PADDING_Y,
                                     text=str(sector), fill="gray", font=("Arial", 8), tags="text")

    # Start drawing on canvas 2
    def start_draw2(self, event):
        self.canvas2.delete("all")
        self.points2, self.directions2 = [(event.x, event.y)], []
        self.canvas2.delete("text")

    # Draw on canvas 2 with direction tracking
    def draw2(self, event):
        last_point = self.points2[-1]
        new_point = (event.x, event.y)

        if math.hypot(new_point[0] - last_point[0], new_point[1] - last_point[1]) >= int(self.px_selector.get()):
            self.canvas2.create_line(last_point[0], last_point[1], new_point[0], new_point[1], fill="blue", width=2)
            angle = calculate_angle(last_point, new_point)
            sector = get_sector(angle)
            self.directions2.append(sector)
            self.points2.append(new_point)

            # Display sector number on the canvas with padding
            mid_point = ((last_point[0] + new_point[0]) / 2, (last_point[1] + new_point[1]) / 2)
            self.canvas2.create_text(mid_point[0] + TEXT_PADDING_X, mid_point[1] + TEXT_PADDING_Y,
                                     text=str(sector), fill="gray", font=("Arial", 8), tags="text")

    # Display vectors in the text widgets
    def display_vectors(self):
        # Clear previous text
        self.vector1_text_f.delete("1.0", tk.END)
        self.vector2_text_f.delete("1.0", tk.END)
        self.vector1_text_s.delete("1.0", tk.END)
        self.vector2_text_s.delete("1.0", tk.END)

        reduced_list1 = reduce_list(self.directions1)
        reduced_list2 = reduce_list(self.directions2)

        # Insert formatted vectors into text fields
        vector1_str_f = ", ".join(map(str, self.directions1))
        vector2_str_f = ", ".join(map(str, self.directions2))
        vector1_str_s = ", ".join(map(str, reduced_list1))
        vector2_str_s = ", ".join(map(str, reduced_list2))

        self.vector1_text_f.insert(tk.END, f"Full Vector 1:\n{vector1_str_f}")
        self.vector2_text_f.insert(tk.END, f"Full Vector 2:\n{vector2_str_f}")
        self.vector1_text_s.insert(tk.END, f"Reduced Vector 1:\n{vector1_str_s}")
        self.vector2_text_s.insert(tk.END, f"Reduced Vector 2:\n{vector2_str_s}")

    # Compare the drawings
    def compare_drawings(self):
        reduced_list1 = reduce_list(self.directions1)
        reduced_list2 = reduce_list(self.directions2)
        similarity_f = calculate_similarity(self.directions1, self.directions2)
        similarity_s = calculate_similarity(reduced_list1, reduced_list2)

        self.similarity_label_f.config(text=f"Similarity with full vector: {similarity_f:.2f}%")
        self.similarity_label_s.config(text=f"Similarity with short vector: {similarity_s:.2f}%")
        self.display_vectors()


# Run the application
root = tk.Tk()
app = DirectionDrawingApp(root)
root.mainloop()
