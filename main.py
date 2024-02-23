from predict_library import predict_label_from_url
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os

#directory path
dir_path = os.getcwd()

# Create a window
root = tk.Tk()
root.title("Birdwatcher")
root.geometry('800x600')

# Configure column to expand horizontally
root.columnconfigure(0, weight=1)

#add form frame
form_frame = tk.LabelFrame(root, padx=20, pady=20, bd=0)
form_frame.grid(columnspan=2, row=0, column=0, sticky="ew")

#image frame
image_frame = tk.LabelFrame(root, padx=20, pady=20, bd=0)
image_frame.grid(columnspan=2, row=2, column=0, sticky="ew")

#equal coluns
image_frame.columnconfigure(0, weight=1)
image_frame.columnconfigure(1, weight=1)

# Configure column to expand horizontally
form_frame.columnconfigure(0, weight=1)

#button func
def myClick():
    url = inputField.get()

    #clean inputField
    inputField.delete("0", "end")

    #update predict label
    predicted_label = predict_label_from_url(url)
    predictLabel.config(text=f"Predicted label: {predicted_label}")

    #get url image
    response = requests.get(url)
    urlImage = Image.open(BytesIO(response.content))

    #resize url image if necessary
    max_width = 350
    max_height = 300
    if urlImage.width > max_width or urlImage.height > max_height:
        urlImage.thumbnail((max_width, max_height))

    #update url image label
    url_tk_image = ImageTk.PhotoImage(urlImage)
    url_imageLabel.config(image=url_tk_image)
    url_imageLabel.image = url_tk_image  # Keep a reference to prevent garbage collection

    #get prediction image
    pre_image = Image.open(f"{dir_path}/label_images/{predicted_label}.jpg")

    #resize pre image
    max_width = 350
    max_height = 300
    if pre_image.width > max_width or pre_image.height > max_height:
        pre_image.thumbnail((max_width, max_height))

    #update url image label
    pre_tk_image = ImageTk.PhotoImage(pre_image)
    pre_imageLabel.config(image=pre_tk_image)
    pre_imageLabel.image = pre_tk_image

    #image frame label texts
    image_frameLabel1.config(text="Your image")
    image_frameLabel2.config(text="Prediction image")

    #set label text
    with open(f"{dir_path}/label_texts/{predicted_label}.txt", "r") as file:
        labelText = file.read()

    # Insert text
    textLabel.config(text=labelText)

#enter func
def on_enter(event):
    myClick()

#entry
inputField = tk.Entry(form_frame, width=50)
#inputField.insert(0, "Enter url")
inputField.grid(row=1, column=0, sticky="ew")

#submit button
submitButton = tk.Button(form_frame, text="Enter", command=myClick)
submitButton.grid(row=1, column=1, sticky="ew")

# Bind the <Return> or <KP_Enter> event to the button action function
root.bind("<Return>", on_enter)
root.bind("<KP_Enter>", on_enter)

formLabel = tk.Label(form_frame, text="Enter Bird Image URL:")
formLabel.grid(row=0, column=0, sticky="w")

# Add a label to display the predicted label
predictLabel = tk.Label(root, text="")
predictLabel.grid(row=1, column=0, columnspan=2)

#url image label
url_imageLabel = tk.Label(image_frame)
url_imageLabel.grid(row=1, column=0, sticky="ew")

#prediction image label
pre_imageLabel = tk.Label(image_frame)
pre_imageLabel.grid(row=1, column=1, sticky="ew")

#image frame labels
image_frameLabel1 = tk.Label(image_frame, text="")
image_frameLabel1.grid(row=0, column=0)

image_frameLabel2 = tk.Label(image_frame, text="")
image_frameLabel2.grid(row=0, column=1)

# Text widget for long paragraph
textLabel = tk.Label(root, text="", width=700, wraplength=700, justify="left")
textLabel.grid(row=3, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()

#url = input("Enter image URL: ")
#predicted_label = predict_label_from_url(url)
#print(f"Predicted label: {predicted_label}")