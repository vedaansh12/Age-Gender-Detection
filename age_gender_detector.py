# Importing Necessary Libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model
from keras.metrics import MeanAbsoluteError  # Fix for 'mae'

# Load the Model and Handle Custom Metrics
custom_objects = {"mae": MeanAbsoluteError()}
model = load_model('model\Age_Sex_Detection.h5', custom_objects=custom_objects)

# Initialize the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age & Gender Detector')
top.configure(background='#CDCDCD')

# Initialize Labels (for displaying results)
label1 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
sign_image = Label(top)

# Function to Detect Age and Gender
def Detect(file_path):
    try:
        # Load and preprocess the image
        image = Image.open(file_path)
        image = image.resize((48, 48))  # Resize image to match the model's input
        image = np.expand_dims(image, axis=0)
        image = np.array(image)
        image = np.resize(image, (48, 48, 3))
        image = np.array([image]) / 255.0  # Normalize image

        # Predict using the model
        pred = model.predict(image)
        age = int(np.round(pred[1][0]))  # Age prediction
        sex = int(np.round(pred[0][0]))  # Gender prediction

        # Display results
        sex_f = ["Male", "Female"]
        print("Predicted Age:", age)
        print("Predicted Gender:", sex_f[sex])
        label1.configure(foreground="#011638", text=f"Predicted Age: {age}")
        label2.configure(foreground="#011638", text=f"Predicted Gender: {sex_f[sex]}")
    except Exception as e:
        print(f"Error during detection: {e}")

# Function to Display Detect Button
def show_Detect_button(file_path):
    Detect_b = Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Function to Upload Image
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_Detect_button(file_path)
    except Exception as e:
        print(f"Error during upload: {e}")

# Create Upload Button
upload = Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)

# Add Components to the Window
sign_image.pack(side='bottom', expand=True)
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", expand=True)
heading = Label(top, text="Age and Gender Detector", pady=20, font=('arial', 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

# Run the Application
top.mainloop()

