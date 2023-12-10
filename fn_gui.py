# -*- coding: latin-1 -*-
import os
import json
import requests
import time
import webbrowser
from tkinter import *
from dotenv import load_dotenv
from pprint import pprint
import tkinter as tk
import customtkinter


load_dotenv() # load API keys

main = Tk()
main.title("Hours Weather")
main.iconbitmap(".\icon.ico")
main.configure(bg="#F6F1F1")

#function start

state = 1   # 0 => current 1 => hours 2=> death
def get_current_weather(city):
    #get weathehr by api url
    request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=imperial'
    weather_data = requests.get(request_url).json()
    return weather_data

def click_handler():
    city = entry_cityname.get()
    weather_data = get_current_weather(city)
    title = weather_data["name"]
    status = weather_data["weather"][0]["description"].capitalize()
    temp = f"{(((weather_data['main']['temp']) - 32) / 1.8):.1f}"
    feels_like=f"{(((weather_data['main']['feels_like']) - 32) / 1.8):.1f}"
    city_label.configure(text=f"{title} city")
    feels_label.configure(text=f"It's {status} right now!")
    temperature_label.configure(text=f"{temp} C rights now")
    temperature_label2.configure(text=f"It feel's like {feels_like} C")

def init(city):
    weather_data = get_current_weather(city)
    title = weather_data["name"]
    status = weather_data["weather"][0]["description"].capitalize()
    temp = f"{(((weather_data['main']['temp']) - 32) / 1.8):.1f}"
    feels_like=f"{(((weather_data['main']['feels_like']) - 32) / 1.8):.1f}"
    city_label.configure(text=f"{title} city")
    feels_label.configure(text=f"It's {status} right now!")
    temperature_label.configure(text=f"{temp} C rights now")
    temperature_label2.configure(text=f"It feel's like {feels_like} C")

def nav_current_handler():
    global state
    if state == 1:
        main.title("Current Weather")
        section_hourstemp.place_forget()
        section_content.place_forget()
        main_label.place_forget()
        region_label.place_forget()
        checkbutton_N.place_forget()
        checkbutton_E.place_forget()
        checkbutton_Mid.place_forget()
        checkbutton_S.place_forget()
        hours_label.place_forget()
        checkbutton_12.place_forget()
        checkbutton_24.place_forget()
        checkbutton_36.place_forget()
        TempUI_Frame.place_forget()
        section_currentweather.place(x=250, y=50)
        current_label.place(x=348, y=120)
        cityname_label.place(x=340, y=180)
        entry_cityname.place(x=333, y=210)
        submit_btn.place(x=336, y=260)
        section_put_weather1.place(x=250, y=350)
        section_put_weather2.place(x=490, y=350)
        section_put_weather3.place(x=490, y=400)
        city_label.place(x=268, y=365)
        feels_label.place(x=272, y=403)
        temperature_label.place(x=500, y=357)
        temperature_label2.place(x=500, y=405)
        state = 0
    if state == 2:
        main.title("Current Weather")
        section_currentweather.place(x=250, y=50)
        current_label.place(x=348, y=120)
        cityname_label.place(x=340, y=180)
        entry_cityname.place(x=333, y=210)
        submit_btn.place(x=336, y=260)
        section_put_weather1.place(x=250, y=350)
        section_put_weather2.place(x=490, y=350)
        section_put_weather3.place(x=490, y=400)
        city_label.place(x=268, y=365)
        feels_label.place(x=272, y=403)
        temperature_label.place(x=500, y=357)
        temperature_label2.place(x=500, y=405)
        state = 0

def nav_hours_handler():
    global state
    if state == 0:
        main.title("Hours Weather")
        section_currentweather.place_forget()
        current_label.place_forget()
        cityname_label.place_forget()
        entry_cityname.place_forget()
        submit_btn.place_forget()
        section_put_weather1.place_forget()
        section_put_weather2.place_forget()
        section_put_weather3.place_forget()
        city_label.place_forget()
        feels_label.place_forget()
        temperature_label.place_forget()
        temperature_label2.place_forget()
        section_hourstemp.place(x=250, y=40)
        section_content.place(x=250, y=290)
        main_label.place(x=407, y=80)
        region_label.place(x=340, y=130)
        checkbutton_N.place(x=340, y=165)
        checkbutton_E.place(x=412, y=165)
        checkbutton_Mid.place(x=480, y=165)
        checkbutton_S.place(x=565, y=165)
        hours_label.place(x=340, y=197)
        checkbutton_12.place(x=340, y=227)
        checkbutton_24.place(x=440, y=227)
        checkbutton_36.place(x=540, y=227)
        TempUI_Frame.place(x=276, y=300)
        state = 1
    if state == 2:
        main.title("Hours Weather")
        section_hourstemp.place(x=250, y=40)
        section_content.place(x=250, y=290)
        main_label.place(x=407, y=80)
        region_label.place(x=340, y=130)
        checkbutton_N.place(x=340, y=165)
        checkbutton_E.place(x=412, y=165)
        checkbutton_Mid.place(x=480, y=165)
        checkbutton_S.place(x=565, y=165)
        hours_label.place(x=340, y=197)
        checkbutton_12.place(x=340, y=227)
        checkbutton_24.place(x=440, y=227)
        checkbutton_36.place(x=540, y=227)
        TempUI_Frame.place(x=276, y=300)
        state = 1

#function end


#rear end start


#-------------class-------------

class city_1:
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

city_datas = [city_1(str(i), "NULL", "", "", "") for i in range(22)]

#----------hour_setting----------

hour_selection = 0
Temp_time_now_check = "0"

#--------------------------------

#--function_for_24hour_weather---

def PC_init():
    if not os.path.exists("CWA_CriticalDataJson.txt"):
        open("CWA_CriticalDataJson.txt", "w")
    if not os.path.exists("CWA_TempDataJson.txt"):
        open("CWA_TempDataJson.txt", "w")


# 12/24/36
hour_selection = 0


Temp_time_now_check = "0"
Crit_time_now_check = "0"


def refresh_temp_data():
    day = time.strftime("%Y-%m-%d")
    hour = time.strftime("%H")
    time_now = str(day + " " + hour)

    global Temp_time_now_check, hour_selection

    # ±qcwb(a)Åª¨ú¸ê®Æ
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-152E5251-7018-4A9D-BA92-6ACFB08EDC08&elementName=MinT,MaxT&sort=time"
    with open("CWA_TempDataJson.txt", "r+", encoding="UTF-8") as CWA_DataJson:
        if time_now == Temp_time_now_check and CWA_DataJson.read(1):
            print("Refresh : Offline mode")
            CWA_DataJson.seek(0)
            r = CWA_DataJson.read()
            tempDatas_rough = json.loads(r)
        else:
            print("Refresh : Request network data")
            r = requests.get(url)
            CWA_DataJson.seek(0)
            CWA_DataJson.truncate()
            CWA_DataJson.write(r.text)
            tempDatas_rough = json.loads(r.text)

    Temp_time_now_check = time_now
    tempData_refined = tempDatas_rough.get("records").get("location")
    hour_selection = radio_state.get()
    # ¼g¤J¿¤¥«·Å«×¸ê®Æ¦Ücity_datas
    repeations = 0
    for cities in tempData_refined:
        city_name = cities.get("locationName")

        # 12/24/36¤p®É·Å«×¹w³ø
        city_temp = cities.get("weatherElement")
        # ³Ì§C·Å
        temp_mins = city_temp[0].get("time")
        temp_min = temp_mins[hour_selection].get("parameter").get("parameterName")
        # ³Ì°ª·Å
        temp_maxs = city_temp[1].get("time")
        temp_max = temp_maxs[hour_selection].get("parameter").get("parameterName")

        city_datas[repeations].city_name = city_name
        city_datas[repeations].tempMin = temp_min
        city_datas[repeations].tempMax = temp_max
        if hour_selection == 0:
            city_datas[repeations].hour = " 0-12"
        elif hour_selection == 1:
            city_datas[repeations].hour = "12-24"
        elif hour_selection == 2:
            city_datas[repeations].hour = "24-36"
        repeations += 1

    # ¿é¥X¸ê®Æ¦ÜUI
   
    tempData_word = ""
    """
    City_N = (18, 7, 1, 5, 3, 4, 13)
    City_E = (10, 12)
    City_Mid = (8, 11, 9, 20, 14)
    City_S = (0, 2, 6, 15, 17)
    City_OL = (16, 19, 21)
    """
    L1 = []
    City_Index = ((18, 7, 1, 5, 3, 4, 13),(10, 12),(8, 11, 9, 20, 14),(0, 2, 6, 15, 17),(16, 19, 21))
    for k in range(5):
        if (checkregion_N.get(),checkregion_E.get(),checkregion_Mid.get(),checkregion_S.get(),checkregion_outerland.get())[k]:
            for i in range(len(City_Index[k])):
                L1.append(City_Index[k][i])
    tempData_text.configure(state="normal")
    tempData_text.delete('1.0', 'end')

    lowtemp_warn = 0
    hightemp_warn = 0

    for i in L1:
        tempData_text.insert("insert", city_datas[i].Temp_output())
        if int(city_datas[i].tempMax) < 23:
            lowtemp_warn = 1
        if int(city_datas[i].tempMin) > 28:
            hightemp_warn = 1
    for i in range(1, 23):
        tempData_text.tag_add("tag" + str(i * 2), str(i) + ".16", str(i) + ".18")
        tempData_text.tag_config("tag" + str(i * 2), foreground="red")
        tempData_text.tag_add("tag" + str(i * 2 + 1), str(i) + ".24", str(i) + ".26")
        tempData_text.tag_config("tag" + str(i * 2 + 1), foreground="blue")
    tempData_text.configure(state="disable")
    

#--------------------------------

PC_init()

#rear end end


#geometry start
width = 900
height = 500
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
screen_width = int((screen_width - 900) / 2)
screen_height = int((screen_height - 520) / 2)
main.geometry(f"{width}x{height}+{screen_width}+{screen_height}")
main.resizable(False, False)

#geometry end

#navbar

navbar = customtkinter.CTkFrame(
    master=main,
    fg_color="#19A7CE",
    width=4,
    height=400
)
navbar.place(x=30, y=50)

nav_current = customtkinter.CTkButton(
    master=main,
    text="Current weather",
    text_color="BLACK",
    fg_color="#19A7CE",
    corner_radius=0,
    border_color="#19A7CE",
    width=150,
    height=30,
    command=nav_current_handler
)
nav_current.place(x=17, y=80)

nav_hours = customtkinter.CTkButton(
    master=main,
    text="Hours temp",
    text_color="BLACK",
    fg_color="#19A7CE",
    corner_radius=0,
    border_color="#19A7CE",
    width=150,
    height=30,
    command=nav_hours_handler
)
nav_hours.place(x=17, y=140)

nav_deathclock = customtkinter.CTkButton(
    master=main,
    text="Death clock",
    text_color="BLACK",
    fg_color="#19A7CE",
    corner_radius=0,
    border_color="#19A7CE",
    width=150,
    height=30,
)
nav_deathclock.place(x=17, y=200)

#navbar end

section_currentweather = customtkinter.CTkFrame(
    master=main,
    fg_color="#AFD3E2",
    width=400,
    height=290,
)


current_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="Current Weather",
    font=("Time news romen", 26, "bold"),
    bg_color="#AFD3E2"
)

cityname_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="Cityname",
    font=("Sylfaen", 14),
    bg_color="#AFD3E2"
)

entry_cityname = customtkinter.CTkEntry(
    master=main,
    width=250,
    placeholder_text="your cityname",
    fg_color="#AFD3E2",
    border_color="#AFD3E2",
    corner_radius=0,
    text_color="Black"
)


submit_btn = customtkinter.CTkButton(
    master=main,
    text="SUBMIT",
    text_color="BLACK",
    fg_color="#19A7CE",
    corner_radius=0,
    border_color="#19A7CE",
    width=230,
    height=30,
    command=click_handler
)


section_put_weather1 = customtkinter.CTkFrame(
    master=main,
    fg_color="#AFD3E2",
    width=230,
    height=90
)


section_put_weather2 = customtkinter.CTkFrame(
    master=main,
    fg_color="#AFD3E2",
    width=160,
    height=40
)

section_put_weather3 = customtkinter.CTkFrame(
    master=main,
    fg_color="#AFD3E2",
    width=160,
    height=40
)

city_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="Taipei City",
    font=("Time news romen", 24, "bold"),
    bg_color="#AFD3E2"
)

feels_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="It Few clouds right now",
    font=("Time news romen", 16),
    bg_color="#AFD3E2"
)


temperature_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="19.4 C rights now",
    font=("Time news romen", 15, "bold"),
    bg_color="#AFD3E2"
)

temperature_label2 = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="It feels like 19.2 C",
    font=("Time news romen", 15, "bold"),
    bg_color="#AFD3E2"
)

section_hourstemp = customtkinter.CTkFrame(
    master=main,
    fg_color="#AFD3E2",
    width=500,
    height=240,
)

section_content = customtkinter.CTkFrame(
    master=main,
    fg_color="#AFD3E2",
    width=500,
    height=190,
)


main_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="Hours Weather",
    font=("Time news romen", 26, "bold"),
    bg_color="#AFD3E2"
)

region_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="Region select",
    font=("Sylfaen", 14),
    bg_color="#AFD3E2"
)

checkregion_N = tk.IntVar(value=1)
checkregion_E = tk.IntVar()
checkregion_Mid = tk.IntVar()
checkregion_S = tk.IntVar()
checkregion_outerland = tk.IntVar()

checkbutton_N = customtkinter.CTkCheckBox(
    master=main,
    text="North", 
    text_color="Black",
    bg_color="#AFD3E2",
    variable=checkregion_N, 
    command=refresh_temp_data
)


checkbutton_E = customtkinter.CTkCheckBox(
    master=main,
    text="East",
    text_color="Black",
    bg_color="#AFD3E2",
    variable=checkregion_E, 
    command=refresh_temp_data
)


checkbutton_Mid = customtkinter.CTkCheckBox(
    master=main, 
    text="Middle", 
    text_color="Black",
    bg_color="#AFD3E2",
    variable=checkregion_Mid, 
    command=refresh_temp_data
)


checkbutton_S = customtkinter.CTkCheckBox(
    master=main,
    text="South",
    text_color="Black",
    bg_color="#AFD3E2",
    variable=checkregion_S, 
    command=refresh_temp_data
)

hours_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="Hours select",
    font=("Sylfaen", 14),
    bg_color="#AFD3E2"
)

radio_state = tk.IntVar(value=3)

checkbutton_12 = customtkinter.CTkCheckBox(
    master=main,
    text="12h",
    text_color="Black",
    bg_color="#AFD3E2",
    variable=radio_state, 
    onvalue=0,
    offvalue=0,
    command=refresh_temp_data
)

checkbutton_24 = customtkinter.CTkCheckBox(
    master=main,
    text="24h",
    text_color="Black",
    bg_color="#AFD3E2",
    variable=radio_state, 
    onvalue=1,
    offvalue=0,
    command=refresh_temp_data
)

checkbutton_36 = customtkinter.CTkCheckBox(
    master=main,
    text="36h",
    text_color="Black",
    bg_color="#AFD3E2",
    variable=radio_state, 
    onvalue=2,
    offvalue=0,
    command=refresh_temp_data
)

TempUI_Frame = tk.Frame(main, bg="#F0F0F0")
textvar = tk.StringVar()
tempData_scrollbar = tk.Scrollbar(TempUI_Frame, bg="#F0F0F0")
tempData_scrollbar.grid(row=3, column=1, padx=0, pady=0, sticky="NS")
tempData_text = tk.Text(
    TempUI_Frame,
    fg="black",
    bg="#AFD3E2",
    font=("·L³n¥¿¶ÂÅé", 13),
    height=10,
    width=53,
    bd=0,
    yscrollcommand=tempData_scrollbar.set,
)
tempData_text.grid(row=3, column=0)
tempData_text.configure(state="disabled")
tempData_scrollbar["command"] = tempData_text.yview


section_hourstemp.place(x=250, y=40)
section_content.place(x=250, y=290)
main_label.place(x=407, y=80)
region_label.place(x=340, y=130)
checkbutton_N.place(x=340, y=165)
checkbutton_E.place(x=412, y=165)
checkbutton_Mid.place(x=480, y=165)
checkbutton_S.place(x=565, y=165)
hours_label.place(x=340, y=197)
checkbutton_12.place(x=340, y=227)
checkbutton_24.place(x=440, y=227)
checkbutton_36.place(x=540, y=227)
TempUI_Frame.place(x=276, y=300)

main.mainloop()