import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time
import threading
import winsound


def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A, %d %B %Y")
    time_label.config(text=f"Time: {current_time}")
    date_label.config(text=f"Date: {current_date}")
    app.after(1000, update_time)


def check_alarms():
    while True:
        now = datetime.now().strftime("%H:%M")
        for alarm in alarms:
            if alarm["time"] == now and alarm["active"]:
                ring_alarm(alarm)
        time.sleep(1)


def ring_alarm(alarm):
    def stop_alarm():
        alarm_popup.destroy()
        alarm["active"] = False

    alarm_popup = tk.Toplevel(app)
    alarm_popup.title("Alarm Ringing!")
    tk.Label(alarm_popup, text=f"Alarm set for {alarm['time']} is ringing!", font=("Helvetica", 14)).pack(pady=10)
    tk.Button(alarm_popup, text="Dismiss", command=stop_alarm, bg="red", fg="white", width=10).pack(pady=5)
    tk.Button(alarm_popup, text="Snooze (5 mins)", command=lambda: snooze_alarm(alarm, alarm_popup), bg="blue", fg="white", width=10).pack(pady=5)
    
    for _ in range(5): 
        winsound.Beep(1000, 500)
        time.sleep(0.5)


def snooze_alarm(alarm, alarm_popup):
    alarm_popup.destroy()
    snooze_time = datetime.now() + timedelta(minutes=5)
    alarm["time"] = snooze_time.strftime("%H:%M")
    messagebox.showinfo("Snoozed", "Alarm snoozed for 5 minutes.")


def add_alarm():
    alarm_time = alarm_time_entry.get()
    if alarm_time:
        alarms.append({"time": alarm_time, "active": True})
        update_alarm_list()
        alarm_time_entry.delete(0, tk.END)


def toggle_alarm(index):
    alarms[index]["active"] = not alarms[index]["active"]
    update_alarm_list()


def update_alarm_list():
    alarm_list.delete(0, tk.END)
    for index, alarm in enumerate(alarms):
        status = "On" if alarm["active"] else "Off"
        alarm_list.insert(tk.END, f"{alarm['time']} - {status}")


app = tk.Tk()
app.title("Alarm Clock")
app.geometry("400x500")


alarms = []


time_label = tk.Label(app, text="", font=("Helvetica", 16))
time_label.pack(pady=10)
date_label = tk.Label(app, text="", font=("Helvetica", 12))
date_label.pack(pady=5)

tk.Label(app, text="Set Alarm Time (HH:MM):", font=("Helvetica", 12)).pack(pady=10)
alarm_time_entry = tk.Entry(app, font=("Helvetica", 12), width=10)
alarm_time_entry.pack(pady=5)

tk.Button(app, text="Add Alarm", command=add_alarm, bg="green", fg="white", width=10).pack(pady=5)

tk.Label(app, text="Alarms List:", font=("Helvetica", 12, "bold")).pack(pady=10)
alarm_list = tk.Listbox(app, font=("Helvetica", 12), height=10, width=30)
alarm_list.pack(pady=10)

tk.Button(app, text="Toggle Alarm", command=lambda: toggle_alarm(alarm_list.curselection()[0]), bg="orange", fg="white", width=12).pack(pady=5)

update_time()
threading.Thread(target=check_alarms, daemon=True).start()


app.mainloop()
