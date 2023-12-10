# -*- coding: latin-1 -*-
import os, json, requests, time, webbrowser, customtkinter
from tkinter import *
from dotenv import load_dotenv
from pprint import pprint
import tkinter as tk

load_dotenv() # load API keys

main = Tk()
main.title("Current Weather")
main.iconbitmap(".\icon.ico")
main.configure(bg="#F6F1F1")

#function start




#function end

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


nav_current = customtkinter.CTkButton(
    master=main,
    text="Current weather",
    text_color="BLACK",
    fg_color="#19A7CE",
    corner_radius=0,
    border_color="#19A7CE",
    width=150,
    height=30,
)


nav_hours = customtkinter.CTkButton(
    master=main,
    text="Hours temp",
    text_color="BLACK",
    fg_color="#19A7CE",
    corner_radius=0,
    border_color="#19A7CE",
    width=150,
    height=30,
)


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


#navbar end

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

checkbutton_N = customtkinter.CTkCheckBox(
    master=main,
    text="North", 
    text_color="Black",
    bg_color="#AFD3E2"
)


checkbutton_E = customtkinter.CTkCheckBox(
    master=main,
    text="East",
    text_color="Black",
    bg_color="#AFD3E2"
)


checkbutton_Mid = customtkinter.CTkCheckBox(
    master=main, 
    text="Middle", 
    text_color="Black",
    bg_color="#AFD3E2"
)


checkbutton_S = customtkinter.CTkCheckBox(
    master=main,
    text="South",
    text_color="Black",
    bg_color="#AFD3E2"
)

hours_label = customtkinter.CTkLabel(
    master=main,
    text_color="BLACK",
    text="Hours select",
    font=("Sylfaen", 14),
    bg_color="#AFD3E2"
)

checkbutton_12 = customtkinter.CTkCheckBox(
    master=main,
    text="12h",
    text_color="Black",
    bg_color="#AFD3E2",
)

checkbutton_24 = customtkinter.CTkCheckBox(
    master=main,
    text="24h",
    text_color="Black",
    bg_color="#AFD3E2"
)

checkbutton_36 = customtkinter.CTkCheckBox(
    master=main,
    text="36h",
    text_color="Black",
    bg_color="#AFD3E2"
)
navbar.place(x=30, y=50)
nav_current.place(x=17, y=80)
nav_hours.place(x=17, y=140)
nav_deathclock.place(x=17, y=200)
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






main.mainloop()