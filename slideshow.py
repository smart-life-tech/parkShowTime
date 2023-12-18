import tkinter as tk# install all
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
import json
import time
import pygame
import os

class DisneyWaitTimesApp:
    def __init__(self, root, image_folder, music_path):
        self.root = root
        self.image_paths = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        self.current_index = 0
        self.music_path = music_path
        self.current_ride=1
        self.ride_name=""
        self.ride_time=""
        self.image_counter = 0  # Counter variable for image
        with open('json.json', 'rb') as f:
            self.data=f.read()
        self.data=json.loads(self.data)
        self.wait_time_text=""
                # Get the full path to the font file
        script_directory = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_directory, "font.TTF")

        # Create a font with the specified size
        self.font = ImageFont.truetype(font_path, 54)
        # Get all image files from the specified folder
        
        # Initialize pygame mixer
        pygame.mixer.init()
        #pygame.mixer.init(driver='alsa', device='hw:0,0')  # Replace with your HDMI audio device
        # Set up background music
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(0.5)  # Adjust volume as needed

        # Create a label for the image
        self.label = tk.Label(root)
        self.label.pack()

        # Fetch initial data
        self.update_wait_time()

        # Start slideshow with music
        self.update_slideshow()

    def get_wait_time(self,rides, ride_name):
        for ride in rides:
            if ride["name"] == ride_name:
                self.ride_time=ride["wait_time"]
                self.ride_name=ride_name
                return ride["wait_time"]
        return None

    def update_wait_time(self):
        # Fetch wait times data from the Queue-Times.com API
        try:
            response = requests.get("https://queue-times.com/parks/2/queue_times.json")
            self.data = json.loads(response.text)
        except Exception as e:

            print(f"Error fetching ride data: {e}")
            self.wait_time_text = "Error fetching ride data"


    def update_slideshow(self):
        # Load the current background image
                 # Check if the current_ride index is within the bounds of the rides_data list
            # Example list of ride names
        # Specify the path to the "images" folder
        folder_path = "images"
        # Get a list of all files in the folder
        image_files = os.listdir(folder_path)

        # Filter only files with certain image extensions (e.g., '.jpg', '.png')
        image_files = [file for file in image_files if file.lower().endswith(('.jpg', '.png', '.jpeg'))]

        # Extract names from the image filenames
        image_names = [os.path.splitext(file)[0] for file in image_files]
        # Remove the first two characters from each element in the list
        image_names = [name[2:] for name in image_names]
        # Display the extracted image names
        print(image_names)
        ride_names = ["Bavarian Dancers", "Breakout at Bozo's", "Creek Freak Massacre", "Creek Freak Massacre", "Creek Freak Massacre", "Creek Freak Massacre", "Creek Freak Massacre"]
        print(len(ride_names))
        if self.image_counter>=len(ride_names):
            print("setting to zero")
            self.image_counter=0
        try:
            if self.get_wait_time(self.data["rides"],ride_names[self.image_counter]) != None:
                #self.wait_time_text = f"{self.ride_name}: {self.ride_time} Minutes"
                self.wait_time_text = f"{self.ride_time} Minutes"
            else:
                # Handle the case where the current_ride index is out of bounds
                self.wait_time_text = "No ride information available"
        except TypeError as r:
            print("error occured : ",r)
            self.wait_time_text = "0 Minutes"
            pass
        image_path = self.image_paths[self.current_index]
        img = Image.open(image_path)
        img = img.resize((1280, 740), Image.Resampling.LANCZOS)  # Adjust size as needed

        # Overlay wait time text
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()  # You can use a custom font if needed
        draw.text((100, 580), self.wait_time_text, fill="white", font=self.font)

        # Display the image
        img = ImageTk.PhotoImage(img)
        self.label.config(image=img)
        self.label.image = img

        # Play music if not already playing
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

        # Move to the next image after 15 seconds (adjust as needed)
        self.image_counter += 1


        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.root.after(1000, self.update_slideshow)

if __name__ == "__main__":
    # Replace these paths with the actual paths of your background images and music
    image_folder = "images"
    music_path = "music.mp3"

    root = tk.Tk()
    root.geometry("1920x1080")  # Adjust window size as needed
    root.attributes("-fullscreen", True)

    app = DisneyWaitTimesApp(root, image_folder, music_path)

    root.mainloop()
