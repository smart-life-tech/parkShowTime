import tkinter as tk# install all
from PIL import Image, ImageTk, ImageDraw, ImageFont
import requests
import json
import pygame
import os

wait_time=10000# 5 seconds wait time
# Define the URLs for each park
park_urls = [
    "https://queue-times.com/parks/6/queue_times.json",  # Magic Kingdom
    "https://queue-times.com/parks/8/queue_times.json",  # Animal Kingdom
    "https://queue-times.com/parks/5/queue_times.json",  # Epcot
    "https://queue-times.com/parks/7/queue_times.json"   # Hollywood Studios
]

# Function to fetch JSON data from a URL
def get_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}")
        return None

# Define a custom sorting key function
def custom_sort_key(file_name):
    # Extract the first two characters from the file name
    return (file_name[:2])

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
        #self.data=json.loads(self.data)
        self.wait_time_text=""
                # Get the full path to the font file
        script_directory = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_directory, "font.TTF")

        # Create a font with the specified size
        self.font = ImageFont.truetype(font_path, 94)
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

    def get_wait_time_by_name(self,park_data, attraction_name):
        for i in range(3):
            print(park_data[i])
            #json.dumps(park_data[i], indent=2)
            #self.data = json.loads(park_data[i])
            for land in park_data[i].get('lands', []):
                #print(land)
                for ride in land.get('rides', []):
                    #print(ride)
                    if attraction_name.lower() in ride.get('name', '').lower():
                        return ride.get('wait_time', 'N/A')
            return 'Attraction not found'

    def get_wait_time(self,rides, ride_name):
        # List of attraction names from images folder
        for ride in rides:
            if ride["name"] == ride_name:
                self.ride_time=ride["wait_time"]
                self.ride_name=ride_name
                return ride["wait_time"]
        return None

    def update_wait_time(self):
        # Fetch wait times data from the Queue-Times.com API
        try:
            # Fetch JSON data from each park URL
            park_data_list = [get_json_data(url) for url in park_urls]

            # Combine the JSON responses into a single dictionary
            combined_data = {}
            for park_data, park_name in zip(park_data_list, ["Magic Kingdom", "Animal Kingdom", "Epcot", "Hollywood Studios"]):
                combined_data[park_name] = park_data

            # Print or further process the combined data
            #print(json.dumps(combined_data, indent=2))
            response=json.dumps(combined_data, indent=2)
            #response = requests.get("https://queue-times.com/parks/2/queue_times.json")
            self.data = (park_data_list)
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
        image_files= sorted(image_files)
        # Sort the filtered file names based on the custom key
        sorted_files = sorted(image_files, key=custom_sort_key)
        image_files=sorted_files
        #print(sorted_files)
        # Extract names from the image filenames
        image_names = [os.path.splitext(file)[0] for file in image_files]
        # Remove the first two characters from each element in the list
        #image_names = [name[2:] for name in image_names]
        # Display the extracted image names
        #print(image_names)
        ride_names = ["Bavarian Dancers", "Breakout at Bozo's", "Creek Freak Massacre", "Creek Freak Massacre", "Creek Freak Massacre", "Creek Freak Massacre", "Creek Freak Massacre",'Astro Orbiter', 'Buzz Lightyear', 'Carousel of Progress', 'Monsters Inc', 'People Mover', 'Space Mountain', 'Tron']
        #print(len(ride_names))
        if self.image_counter==len(ride_names)-1:
            print("setting to zero")
            self.image_counter=0
        try:
            #print(self.data)
            self.wait_time = self.get_wait_time_by_name(self.data, image_names[self.current_index])
            self.wait_time_text =str(self.wait_time)+ " minutes"
            print(f"Wait time for {image_names[self.current_index]}: {self.wait_time} minutes")

            '''if self.get_wait_time(self.data,image_names[self.image_counter]) != None:
                #self.wait_time_text = f"{self.ride_name}: {self.ride_time} Minutes"
                self.wait_time_text = f"{self.ride_time} Minutes"
            else:
                # Handle the case where the current_ride index is out of bounds
                self.wait_time_text = "No ride information available"
                '''
        except TypeError as r:
            print("error occured : ",r)
            self.wait_time_text = "0 Minutes"
            pass
        # Create the full paths for the sorted image filenames
        image_path = os.path.join(folder_path,sorted_files[self.current_index])# for file_name in sorted_files]

        #image_path = self.image_paths[self.current_index]
        print(self.current_index,image_path)
        
        img = Image.open(image_path)
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)  # Adjust size as needed
        #img = img.resize((1280, 740), Image.Resampling.LANCZOS)  # Adjust size as needed
        # Overlay wait time text
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()  # You can use a custom font if needed
        draw.text((100, 780), self.wait_time_text, fill="white", font=self.font)
        #draw.text((100, 580), self.wait_time_text, fill="white", font=self.font)
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
        self.root.after(wait_time, self.update_slideshow)

if __name__ == "__main__":
    # Replace these paths with the actual paths of your background images and music
    image_folder = "images"
    music_path = "music.mp3"

    root = tk.Tk()
    root.geometry("1920x1080")  # Adjust window size as needed
    #root.attributes("-fullscreen", True)

    app = DisneyWaitTimesApp(root, image_folder, music_path)

    root.mainloop()
