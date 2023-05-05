import tkinter as tk
from tkinter import Frame
from tkinter import Canvas
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
import io
import pyperclip


# Global color variables
BACKGROUND_COLOR = "#F5F5F5"
TEXT_COLOR = "#36393F"
BUTTON_COLOR = "#4C8BF5"
BUTTON_TEXT_COLOR = "#FFFFFF"
TEXT_BOX_COLOR = "#FFFFFF"

# Additional global variables for dark mode
DARK_BACKGROUND_COLOR = "#36393F"
DARK_TEXT_COLOR = "#F5F5F5"
DARK_BUTTON_COLOR = "#4C8BF5"
DARK_BUTTON_TEXT_COLOR = "#FFFFFF"
DARK_TEXT_BOX_COLOR = "#2C2F33"

is_dark_mode = False

class CopyableText(tk.Frame):
    def __init__(self, master=None, text=None, truck=None, driver=None, phone=None, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(bg=BACKGROUND_COLOR)

        info_label = tk.Label(self, text=f"Truck: {truck} | Driver: {driver} | Phone: {phone}", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        info_label.grid(row=0, column=0, columnspan=5, sticky="nsew")

        self.checkmark_label = tk.Label(self, text="", bg=BACKGROUND_COLOR, fg="green")
        self.checkmark_label.grid(row=0, column=5, sticky="nsew")

        text_box_height = len(text.splitlines()) + 1
        self.text_widget = tk.Text(self, wrap=tk.WORD, width=100)
        self.text_widget.insert(tk.END, text)
        self.text_widget.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.text_widget.configure(height=text_box_height, bg=TEXT_BOX_COLOR, fg=TEXT_COLOR)

        self.copy_button = tk.Button(self, text="Copy", command=self.copy_text, height=text_box_height)
        self.copy_button.grid(row=1, column=5, sticky="nsew")
        self.copy_button.configure(bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)

        self.copy_phone_button = tk.Button(self, text="Copy #", command=lambda: self.copy_phone(phone), height=text_box_height)
        self.copy_phone_button.grid(row=1, column=6, sticky="nsew")
        self.copy_phone_button.configure(bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)

        self.delete_button = tk.Button(self, text="Delete", command=self.delete, height=text_box_height)
        self.delete_button.grid(row=1, column=7, sticky="nsew")
        self.delete_button.configure(bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)

        # Set the column weight for all columns to allow them to expand
        for i in range(8):
            self.columnconfigure(i, weight=1)

    def copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.text_widget.get(1.0, tk.END))
        self.checkmark_label.config(text="✓")

    def copy_phone(self, phone):
        self.clipboard_clear()
        self.clipboard_append(phone.split('+')[-1])

    def delete(self):
        self.grid_forget()
        self.destroy()

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls;*.xlsx")])
    if file_path:
        file_label.config(text=file_path)
        generate_button.config(state="normal")

def generate_sentences():
    file_path = file_label.cget("text")
    with open(file_path, "rb") as f:
        data = f.read()
    process_data(data)

    # Center the content
    center_frame.pack(fill=tk.BOTH, expand=True)
    text_frame.pack(anchor="center", expand=True)

def process_data(data):
    # Read the data into a pandas DataFrame
    df = pd.read_excel(io.BytesIO(data))
    first_column_name = df.columns[0]

    # Count the number of requests for each truck and date combination
    request_counts = df.groupby(['Truck', 'Date']).size().to_dict()

    # Extract the required information
    for index, row in df.iterrows():
        column_a = row[first_column_name]
        truck = row['Truck']
        driver = row['Driver']
        date = row['Date']
        from_location = row['From']
        to_location = row['To']
        phone = row['Phone']

        # Check if Column A starts with "Truck:"
        if str(column_a).startswith("Truck:"):
            continue

        # Generate and display the sentence for each truck
        multiple_requests = request_counts[(truck, date)] > 1
        sentence = generate_sentence(date, from_location, to_location, truck, driver, multiple_requests)
        copyable_text = CopyableText(text_frame, text=sentence, truck=truck, driver=driver, phone=phone)
        copyable_text.grid(sticky="ew")

    # Configure the column weights for the text_frame
    text_frame.columnconfigure(0, weight=1)
    text_frame.columnconfigure(1, weight=1)
    text_frame.columnconfigure(2, weight=1)
    text_frame.columnconfigure(3, weight=1)
    text_frame.columnconfigure(4, weight=1)
    text_frame.columnconfigure(5, weight=1)
    text_frame.columnconfigure(6, weight=1)
    text_frame.columnconfigure(7, weight=1)

    # Set the background color for the text_frame
    text_frame.configure(bg=BACKGROUND_COLOR)

    text_frame.update_idletasks()
    text_canvas.config(scrollregion=text_canvas.bbox("all"))

def generate_sentence(date, from_location, to_location, truck, driver, multiple_requests=False):
    if multiple_requests:
        return f"Good morning, {driver}, For the truck {truck}, can you send me all the ticket's for truck {truck}, from the date {date}, for the job {from_location} to {to_location}."
    else:
        return f"Good morning, {driver}, For the truck {truck}, can you send me the ticket {truck}, from the date {date}, for the job {from_location} to {to_location}."

app = tk.Tk()
app.title("Truck Sentence Generator")
app.minsize(800, 600)  # Set the minimum window size

# Configure the background color of the app
app.configure(bg=BACKGROUND_COLOR)

def toggle_dark_mode():
    global is_dark_mode
    global BACKGROUND_COLOR, TEXT_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR, TEXT_BOX_COLOR
    is_dark_mode = not is_dark_mode

    if is_dark_mode:
        BACKGROUND_COLOR = DARK_BACKGROUND_COLOR
        TEXT_COLOR = DARK_TEXT_COLOR
        BUTTON_COLOR = DARK_BUTTON_COLOR
        BUTTON_TEXT_COLOR = DARK_BUTTON_TEXT_COLOR
        TEXT_BOX_COLOR = DARK_TEXT_BOX_COLOR
    else:
        BACKGROUND_COLOR = "#F5F5F5"
        TEXT_COLOR = "#36393F"
        BUTTON_COLOR = "#4C8BF5"
        BUTTON_TEXT_COLOR = "#FFFFFF"
        TEXT_BOX_COLOR = "#FFFFFF"

    # Apply the new colors
    app.configure(bg=BACKGROUND_COLOR)
    file_label.configure(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    browse_button.configure(bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    generate_button.configure(bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
    dark_mode_button.configure(bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)

    for child in text_frame.winfo_children():
        child.configure(bg=BACKGROUND_COLOR, fg=TEXT_COLOR)

file_label = tk.Label(app, text="No file selected", bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
file_label.pack(pady=5)

browse_button = tk.Button(app, text="Browse", command=browse_file, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
browse_button.pack(pady=5)

generate_button = tk.Button(app, text="Generate", command=generate_sentences, state="disabled", bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
generate_button.pack(pady=5)

dark_mode_button = tk.Button(app, text="Toggle Dark Mode", command=toggle_dark_mode, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR)
dark_mode_button.pack(pady=5)

center_frame = tk.Frame(app, bg=BACKGROUND_COLOR)
text_canvas = tk.Canvas(center_frame, bg=BACKGROUND_COLOR, highlightthickness=0)
text_frame = tk.Frame(text_canvas, bg=BACKGROUND_COLOR)
scrollbar = tk.Scrollbar(center_frame, orient="vertical", command=text_canvas.yview)
text_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
text_canvas.pack(side="left", fill="both", expand=True)
text_canvas.create_window((0, 0), window=text_frame, anchor="nw")

app.mainloop()
