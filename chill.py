# -*- coding: Big5 -*-
import os
import tkinter as tk
import json
import requests
import time
import webbrowser
import ttkbootstrap as tb
from ttkbootstrap import *


# =========================Classes=======================================
# 初始化城市資料存放區
class city:
    def __init__(self, index, city_name, hour, tempMin, tempMax):
        self.index = index
        self.city_name = city_name
        self.tempMin = tempMin
        self.tempMax = tempMax
        self.hour = hour

    def Temp_output(self):
        return "{:s}:{:s}小時內最高溫為{:s}度，最低溫為{:s}度\n".format(
            self.city_name, self.hour, self.tempMax, self.tempMin
        )

    def highTemp_output(self):
        return self.tempMax


city_datas = [city(str(i), "NULL", "", "", "") for i in range(22)]
#                              index  name   hr   +-temp


# =========================Functions======================================
# 第一次啟動時建立JSON存放區 (你484以為抓資料不用時間?)
def PC_init():
    if not os.path.exists("CWA_CriticalDataJson.txt"):
        open("CWA_CriticalDataJson.txt", "w")
    if not os.path.exists("CWA_TempDataJson.txt"):
        open("CWA_TempDataJson.txt", "w")


# 由按鈕啟動重新整理
def Total_Refresh():
    refresh_temp_data()
    refresh_critical_data()


# 12/24/36
hour_selection = 0


Temp_time_now_check = "0"
Crit_time_now_check = "0"


def refresh_temp_data():
    day = time.strftime("%Y-%m-%d")
    hour = time.strftime("%H")
    time_now = str(day + " " + hour)
    label1.config(text=time_now)

    global Temp_time_now_check, hour_selection

    # 從cwb(a)讀取資料
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
    # 寫入縣市溫度資料至city_datas
    repeations = 0
    for cities in tempData_refined:
        city_name = cities.get("locationName")

        # 12/24/36小時溫度預報
        city_temp = cities.get("weatherElement")
        # 最低溫
        temp_mins = city_temp[0].get("time")
        temp_min = temp_mins[hour_selection].get("parameter").get("parameterName")
        # 最高溫
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

    # 輸出資料至UI
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
    if lowtemp_warn == 1:
        Critical_Temp_label.config(
            text="!!!!CAUTION : 溫度低下，出外請做好防寒措施。!!!!"
            )
        Critical_Temp_label.grid(row=1)
    elif hightemp_warn == 1:
        Critical_Temp_label.config(
            text="!!!!CAUTION : 溫度過高，出外請注意隨時補充水分。!!!!"
            )
        Critical_Temp_label.grid(row=1)
    else:
        Critical_Temp_label.config(text="")
        Critical_Temp_label.grid_forget()


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


# 不要點連結
def rick():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xs")


# =========================UI stuffs======================================
PC_init()


window = tb.Window(themename="morph")
window.geometry("709x600")
window.title("Stormwatch UI")


TempUI_Frame = tk.Frame(window, bg="#F0F0F0")
textvar = tk.StringVar()
# ================Time=============
label1 = tk.Label(
    TempUI_Frame,
    text="Click that button to refresh data",
    fg="black",
    bg="#F0F0F0",
    font=("微軟正黑體", 13),
    padx=0,
    pady=0,
)
label1.grid(row=0)
# ==========Critical temp info===========
Critical_Temp_label = tb.Label(
    TempUI_Frame, text="", font=("微軟正黑體", 13), bootstyle="inverse-danger"
)

# =========City temp datas=============
tempData_scrollbar = tk.Scrollbar(TempUI_Frame, bg="#F0F0F0")
tempData_scrollbar.grid(row=3, column=1, padx=0, pady=0, sticky="NS")

tempData_text = tk.Text(
    TempUI_Frame,
    fg="black",
    bg="#F0F0F0",
    font=("微軟正黑體", 13),
    height=10,
    width=38,
    bd=0,
    yscrollcommand=tempData_scrollbar.set,
)
tempData_text.grid(row=3, column=0)

tempData_scrollbar["command"] = tempData_text.yview
TempUI_Frame.pack()


SelectUI_Frame = tk.Frame(window, bg="#F0F0F0")
# ========hour selection (12/24/36)========
radio_state = tk.IntVar(value=0)
selection_hour12 = tk.Radiobutton(
    SelectUI_Frame, text="12小時", value=0, variable=radio_state
)
selection_hour24 = tk.Radiobutton(
    SelectUI_Frame, text="24小時", value=1, variable=radio_state
)
selection_hour36 = tk.Radiobutton(
    SelectUI_Frame, text="36小時", value=2, variable=radio_state
)
selection_hour12.grid(row=0)
selection_hour24.grid(row=1)
selection_hour36.grid(row=2)


# ===displayed cities(N/E/Mid/S/Outerlands)====
checkregion_N = tk.IntVar(value=1)
checkregion_E = tk.IntVar()
checkregion_Mid = tk.IntVar()
checkregion_S = tk.IntVar()
checkregion_outerland = tk.IntVar()
checkbutton_N = tk.Checkbutton(SelectUI_Frame, text="北部地區", variable=checkregion_N)
checkbutton_E = tk.Checkbutton(SelectUI_Frame, text="東部地區", variable=checkregion_E)
checkbutton_Mid = tk.Checkbutton(SelectUI_Frame, text="中部地區", variable=checkregion_Mid)
checkbutton_S = tk.Checkbutton(SelectUI_Frame, text="南部地區", variable=checkregion_S)
checkbutton_ol = tk.Checkbutton(
    SelectUI_Frame, text="外島地區", variable=checkregion_outerland
)
checkbutton_N.grid(row=0, column=1)
checkbutton_E.grid(row=1, column=1)
checkbutton_Mid.grid(row=2, column=1)
checkbutton_S.grid(row=3, column=1)
checkbutton_ol.grid(row=4, column=1)

SelectUI_Frame.pack()

# =====The one button that do everything=====
refresh_button = tk.Button(
    window, textvariable=textvar, font=("微軟正黑體", 10), command=Total_Refresh
)
textvar.set("Refresh data")
refresh_button.pack()
# =======The button that rickroll'd you======
rick_button = tk.Button(window, text="???", font=("微軟正黑體", 10), command=rick)
rick_button.pack()

Credit_Label = tk.Label(
    window,
    text="Made by Group 1(6)   ver.0.0.3",
    fg="black",
    bg="#F0F0F0",
    font=("微軟正黑體", 10),
    padx=0,
    pady=0,
)
Credit_Label.pack(side="bottom")

# =The one line command that ALSO do everything=
window.mainloop()