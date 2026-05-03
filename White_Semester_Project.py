import tkinter as tk
from tkinter import messagebox
import requests

#base class to handle the api logic
#it just stores the key and builds the url
class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_data(self, city):
        #params for the request, units=metric gives us celsius
        #if we want fahrenheit we would change metric to imperial
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

#subclass for the actual app functionality
#this inherits from the service class to satisfy the project specs
class WeatherApp(WeatherService):
    def __init__(self, root, api_key):
        #calling the parent constructor
        super().__init__(api_key)
        self.root = root
        self.root.title("Weather Finder")
        self.root.geometry("400x300")

        #setting up the gui components
        self.label = tk.Label(root, text="enter city name:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.city_entry = tk.Entry(root, font=("Arial", 12))
        self.city_entry.pack(pady=5)

        self.search_btn = tk.Button(root, text="get weather", command=self.display_weather)
        self.search_btn.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
        self.result_label.pack(pady=20)

    def display_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showwarning("error", "type a city first dude")
            return

        #fetching data using the inherited method
        data = self.get_data(city)

        #checking if the api call actually worked
        if data.get("cod") != 200:
            messagebox.showerror("error", "city not found or api issue")
            return

        #parsing the json response
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        feels_like = data['main']['feels_like']

        #formatting the output string for the label
        report = (
            f"city: {city.title()}\n"
            f"temp: {temp}°c\n"
            f"feels like: {feels_like}°c\n"
            f"sky: {desc}\n"
            f"humidity: {humidity}%"
        )
        self.result_label.config(text=report)

#main execution block
if __name__ == "__main__":
    #setting api key here
    API_KEY = "085b777188931a771bcb816c9923f12e"
    
    root = tk.Tk()
    app = WeatherApp(root, API_KEY)
    
    #keeping the window open
    root.mainloop()
