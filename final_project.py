# -*- coding: latin-1 -*-
import os, json, requests, time, webbrowser, customtkinter
from tkinter import *
from dotenv import load_dotenv
from pprint import pprint
import tkinter as tk

load_dotenv() # load API keys

#24 hours weather rear_end start

#-------------class-------------

class city:
    def __init__(self, index, city_name, hour, tempMin, tempMax):
        self.index = index
        self.city_name = city_name
        self.tempMin = tempMin
        self.tempMax = tempMax
        self.hour = hour
    def Temp_output(self):
        return "{:s}           highest temp: {:s}C              lowest temp: {:s}C\n".format(
            self.city_name,self.tempMax, self.tempMin
        )
    def highTemp_output(self):
        return self.tempMax
    
#--------------------------------

city_datas = [city(str(i), "NULL", "", "", "") for i in range(22)]

#----------hour_setting----------

hour_selection = 0
Temp_time_now_check = "0"
Crit_time_now_check = "0"

#--------------------------------

#--function_for_24hour_weather---

def PC_init():
    if not os.path.exists("CWA_CriticalDataJson.txt"):
        open("CWA_CriticalDataJson.txt", "w")
    if not os.path.exists("CWA_TempDataJson.txt"):
        open("CWA_TempDataJson.txt", "w")



def Total_Refresh():
    tempData_text.configure(state="normal")
    refresh_temp_data()
    refresh_critical_data()
    tempData_text.configure(state="disabled")

# 12/24/36
hour_selection = 0


Temp_time_now_check = "0"
Crit_time_now_check = "0"


def refresh_temp_data():
    day = time.strftime("%Y-%m-%d")
    hour = time.strftime("%H")
    time_now = str(day + " " + hour)

    global Temp_time_now_check, hour_selection

    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-152E5251-7018-4A9D-BA92-6ACFB08EDC08&elementName=MinT,MaxT&sort=time"
    with open("CWA_TempDataJson.txt", "r+", encoding="UTF-8") as CWA_DataJson:
        if time_now == Temp_time_now_check:
            print("Refresh : Offline mode")
            r = CWA_DataJson.read()
            tempDatas_rough = json.loads(r)
        else:
            print("Refresh : Request network data")
            CWA_DataJson.mode = "w+"
            r = requests.get(url)
            CWA_DataJson.truncate(0)
            CWA_DataJson.write(r.text)
            tempDatas_rough = json.loads(r.text)

    Temp_time_now_check = time_now
    tempData_refined = tempDatas_rough.get("records").get("location")
    hour_selection = radio_state.get()

    repeations = 0
    for cities in tempData_refined:
        city_name = cities.get("locationName")


        city_temp = cities.get("weatherElement")

        temp_mins = city_temp[0].get("time")
        temp_min = temp_mins[hour_selection].get("parameter").get("parameterName")
        temp_maxs = city_temp[1].get("time")
        temp_max = temp_maxs[hour_selection].get("parameter").get("parameterName")

        city_datas[repeations].city_name = city_name
        city_datas[repeations].tempMin = temp_min
        city_datas[repeations].tempMax = temp_max

        if hour_selection == 0:
            city_datas[repeations].hour = "12"
        elif hour_selection == 1:
            city_datas[repeations].hour = "24"
        elif hour_selection == 2:
            city_datas[repeations].hour = "36"
        repeations += 1

    tempData_word = ""
    """
    City_N = (18, 7, 1, 5, 3, 4, 13)
    City_E = (10, 12)
    City_Mid = (8, 11, 9, 20, 14)
    City_S = (0, 2, 6, 15, 17)
    City_OL = (16, 19, 21)
    """
    tempData_text.delete("1.0", "end")
    L1 = []
    for k in range(5):
        T2 = (
            (18, 7, 1, 5, 3, 4, 13),
            (10, 12),
            (8, 11, 9, 20, 14),
            (0, 2, 6, 15, 17),
            (16, 19, 21),
        )
        if (
            checkregion_N.get(),
            checkregion_E.get(),
            checkregion_Mid.get(),
            checkregion_S.get(),
            checkregion_outerland.get(),
        )[k]:
            for i in range(len(T2[k])):
                L1.append(T2[k][i])
    for i in L1:
        tempData_text.insert("insert", city_datas[i].Temp_output())
    for i in range(1, 23):
        tempData_text.tag_add("tag" + str(i * 2), str(i) + ".13", str(i) + ".15")
        tempData_text.tag_config("tag" + str(i * 2), foreground="red")
        tempData_text.tag_add("tag" + str(i * 2 + 1), str(i) + ".21", str(i) + ".23")
        tempData_text.tag_config("tag" + str(i * 2 + 1), foreground="blue")
    lowtemp_warn = 0
    hightemp_warn = 0
    for i in range(21):
        if int(city_datas[i].tempMax) < 23:
            lowtemp_warn = 1
        if int(city_datas[i].tempMin) > 28:
            hightemp_warn = 1
    


def refresh_critical_data():
    day = time.strftime("%Y-%m-%d")
    hour = time.strftime("%H")
    time_now = str(day + " " + hour)

    global Crit_time_now_check

    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0033-002?Authorization=CWA-152E5251-7018-4A9D-BA92-6ACFB08EDC08"
    with open("CWA_CriticalDataJson.txt", "r+", encoding="UTF-8") as CWA_DataJson:
        if time_now == Crit_time_now_check:
            print("CRefresh : Offline mode")
            r = CWA_DataJson.read()
            CritDatas_rough = json.loads(r)
        else:
            print("CRefresh : Request network data")
            CWA_DataJson.mode = "w+"
            r = requests.get(url)
            CWA_DataJson.truncate(0)
            CWA_DataJson.write(r.text)
            CritDatas_rough = json.loads(r.text)

    Crit_time_now_check = time_now
    CritDatas_Refined = CritDatas_rough.get("records").get("record")
    for CritDatas in CritDatas_Refined:
        CritData = CritDatas.get("contents").get("content").get("contentText")
        print(CritData[17:-17])

#--------------------------------

PC_init()

#24 hours weather rear_end end

#rear_end start

def get_current_weather(city):
    #get weathehr by api url
    request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=imperial'
    weather_data = requests.get(request_url).json()
    return weather_data

def click_handler():
    city = entry.get()
    weather_data = get_current_weather(city)
    title = weather_data["name"]
    status = weather_data["weather"][0]["description"].capitalize()
    temp = f"{(((weather_data['main']['temp']) - 32) / 1.8):.1f}"
    feels_like=f"{(((weather_data['main']['feels_like']) - 32) / 1.8):.1f}"
    current_weather_label.configure(text=f"{title} city")
    current_weather_labe2.configure(text=f"It's {status} right now!")
    current_weather_labe3.configure(text=f"{temp} C rights now")
    current_weather_labe4.configure(text=f"It feel's like {feels_like} C")

def init(city):
    weather_data = get_current_weather(city)
    title = weather_data["name"]
    status = weather_data["weather"][0]["description"].capitalize()
    temp = f"{(((weather_data['main']['temp']) - 32) / 1.8):.1f}"
    feels_like=f"{(((weather_data['main']['feels_like']) - 32) / 1.8):.1f}"
    current_weather_label.configure(text=f"{title} city")
    current_weather_labe2.configure(text=f"It's {status} right now!")
    current_weather_labe3.configure(text=f"{temp} C rights now")
    current_weather_labe4.configure(text=f"It feel's like {feels_like} C")

#rear_end end

main = Tk()
main.title("getWeather")
main.iconbitmap(".\main.ico")
main.configure(bg="#FAF6F0")


#window giometry of main start

width = 900
height = 520
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
screen_width = int((screen_width - 900) / 2)
screen_height = int((screen_height - 520) / 2)
main.geometry(f"{width}x{height}+{screen_width}+{screen_height}")
main.resizable(False, False)

#window giometry of main end

#section satrt

section1 = customtkinter.CTkFrame(main, fg_color="#F4DFC8", border_color="#F4DFC8")
section2 = customtkinter.CTkFrame(main, fg_color="#F4DFC8", border_color="#F4DFC8", width=620, height=100)
section3 = customtkinter.CTkFrame(main, fg_color="#F4DFC8", border_color="#F4DFC8", width=200, height=50)
section4 = customtkinter.CTkFrame(main, fg_color="#F4DFC8", border_color="#F4DFC8", width=200, height=50)
section5 = customtkinter.CTkFrame(main, fg_color="#F4DFC8", border_color="#F4DFC8", width=860, height=65)
section6 = customtkinter.CTkFrame(main, fg_color="#F4DFC8", border_color="#F4DFC8", width=860, height=220)
section1.place(x=25, y=30)
section2.place(x=265, y=30)
section3.place(x=265, y=144)
section4.place(x=480, y=144)
section5.place(x=25, y=207)
section6.place(x=25, y=280)

#section end

#widgets start

TempUI_Frame = tk.Frame(main, bg="#F0F0F0")
textvar = tk.StringVar()

section1_title = customtkinter.CTkLabel(
    master = section1,
    text="Weather search!",
    fg_color="transparent",
    text_color="Black",
    font=("Time news romen", 20, "bold")
)

current_weather_label = customtkinter.CTkLabel(
    master= main,
    text="",
    text_color="Black",
    font=("Time news romen", 40, "bold"),
    bg_color="#F4DFC8"
)

current_weather_labe2 = customtkinter.CTkLabel(
    master= main,
    text="",
    text_color="Black",
    font=("Time news romen", 20, "bold"),
    bg_color="#F4DFC8"
)

current_weather_labe3 = customtkinter.CTkLabel(
    master= main,
    text="test",
    text_color="Black",
    font=("Time news romen", 20, "bold"),
    bg_color="#F4DFC8"
)

current_weather_labe4 = customtkinter.CTkLabel(
    master= main,
    text="test",
    text_color="Black",
    font=("Time news romen", 20, "bold"),
    bg_color="#F4DFC8"
)

recent_24hr_label = customtkinter.CTkLabel(
    master=main,
    text="Recent 24 Hours weather",
    text_color="Black",
    font=("Time new roman", 25, "bold"),
    bg_color="#F4DFC8",
)

recent_fresh_btn = customtkinter.CTkButton(
    master=main,
    text="Refresh data",
    text_color="Black",
    fg_color="#F4EAE0", 
    hover_color="#FAF6F0",
    border_color="Black",
    border_width=2,
    corner_radius=5,
    width=120,
    command=Total_Refresh
)

click = customtkinter.CTkButton(
    section1, 
    text="Search",
    fg_color="#F4EAE0", 
    text_color="Black",
    border_color="Black",
    hover_color="#FAF6F0",
    border_width=2,
    corner_radius=5,
    width=80,
    command=click_handler
)

entry = customtkinter.CTkEntry(
    section1,
    placeholder_text="Enter city's name",
    fg_color="#F4EAE0",
    border_color="Black",
    corner_radius=5,
    width=150
)

#----------set_time--------------

radio_state = tk.IntVar(value=1)

#--------------------------------

tempData_text = customtkinter.CTkTextbox(
    TempUI_Frame,
    fg_color="#F4DFC8",
    font=("Time news romen", 20),
    height=200,
    width=500
)
tempData_text.grid(row=3, column=0)

TempUI_Frame.place(x=40, y=290)

#--------set_time_value----------

SelectUI_Frame = tk.Frame(main, bg="#F0F0F0")
checkregion_N = tk.IntVar(value=1)
checkregion_E = tk.IntVar()
checkregion_Mid = tk.IntVar()
checkregion_S = tk.IntVar()
checkregion_outerland = tk.IntVar()

#--------------------------------

checkbutton_N = customtkinter.CTkCheckBox(
    master=main,
    text="North", 
    text_color="Black",
    bg_color="#F4DFC8",
    variable=checkregion_N,
)

checkbutton_E = customtkinter.CTkCheckBox(
    master=main,
    text="East",
    text_color="Black",
    bg_color="#F4DFC8",
    variable=checkregion_E
)

checkbutton_Mid = customtkinter.CTkCheckBox(
    master=main, 
    text="Middle", 
    text_color="Black",
    bg_color="#F4DFC8",
    variable=checkregion_Mid
)

checkbutton_S = customtkinter.CTkCheckBox(
    master=main,
    text="South",
    text_color="Black",
    bg_color="#F4DFC8", 
    variable=checkregion_S
)

#widgets end


init("Taipei")

section1_title.pack(anchor="s", expand=True, pady=10, padx=30)
entry.pack(anchor="s", expand=True, pady=10, padx=30)
click.pack(anchor="n", expand=True, pady=20, padx=20)
current_weather_label.place(x=280,y=40)
current_weather_labe2.place(x=282,y=88)
current_weather_labe3.place(x=282,y=154)
current_weather_labe4.place(x=495,y=154)

recent_24hr_label.place(x=40, y=223)
recent_fresh_btn.place(x=360, y=225)

checkbutton_N.place(x=500, y=225)
checkbutton_E.place(x=570, y=225)
checkbutton_Mid.place(x=640, y=225)
checkbutton_S.place(x=720, y=225)
 
SelectUI_Frame.pack()


main.mainloop()