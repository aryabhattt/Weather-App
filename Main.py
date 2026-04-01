from logging import root
import tkinter as tk
from tkinter import messagebox
import requests

# OpenWeatherMap API key and base URL
api_key = "292a2d812f670939fcf3bfcd61fcb8dd"
Base_url = "http://api.openweathermap.org/data/2.5/weather"

def weather():
    result_label.config(text="Fetching weather... ⏳")
    root.update()
    city = city_name.get()
    if not city:
        result_label.config(text="Please enter a city name.")
        return
    parameters = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(Base_url, params=parameters)
        response.raise_for_status()
        data = response.json()
        if data["cod"] != 200:
            result_label.config(text=f"Error: {data['message']}")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].lower()
        icon_code = data["weather"][0]["icon"]
        #advise
        if "rain" in description:
            advice = "Don't forget an umbrella ☔"
        elif "clear" in description:
            advice = "It's a sunny day 😎"
        else:
            advice = "Have a nice day!"
        
        # Change background based on weather
        if "clear" in description:
            root.config(bg="lightyellow")
        elif "rain" in description:
            root.config(bg="lightblue")
        else:
            root.config(bg="lightgray")

        # Fetch weather icon (large PNG)
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
        img_data = requests.get(icon_url).content

        # Load directly into Tkinter PhotoImage
        icon_tk = tk.PhotoImage(data=img_data)

        # Update icon label (centered, big)
        icon_label.config(image=icon_tk)
        icon_label.image = icon_tk  # keep reference

        # Update text result below icon
        result_label.config(
            text=f"Temperature: {temp}°C\nHumidity: {humidity}%\nDescription: {description}\n\n{advice}")

    except requests.exceptions.RequestException as e:
        sarcastic_msg = (
            "Epic Fail! The weather gods are on strike again.\n\n"
            f"Details: {e}"
        )
        result_label.config(text=sarcastic_msg)
        messagebox.showerror("Weather App Error", sarcastic_msg)

# Building the GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("420x450")

city_name = tk.StringVar()

# Input bar
city_entry = tk.Entry(root, font=("Arial", 15), justify="center", textvariable=city_name)
city_entry.bind("<Return>", lambda event: weather())
city_entry.pack(pady=10, fill="x", padx=20)

get_weather_button = tk.Button(root, text="Get Weather", command=weather, font=("Arial", 12))
get_weather_button.pack(pady=5)

# Big centered weather icon
icon_label = tk.Label(root, bg=root["bg"])
icon_label.pack(pady=15)

result_label = tk.Label(root, text="", font=("Arial", 14), justify="center", bg=root["bg"])
result_label.pack(pady=10, padx=20, fill="x")
result_label.config(bg=root["bg"])
icon_label.config(bg=root["bg"])
root.mainloop()
