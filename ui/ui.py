import tkinter as tk
from tkinter import ttk, messagebox

# DB functions for testing purposes (to be linked with actual DB code)
def save_username():
    username = entry_username.get()
    if username:
        messagebox.showinfo("Erfolg", f"Benutzer '{username}' wurde ausgewählt!")
        #cursor.execute(...)
    else:
        messagebox.showwarning("Fehler", "Bitte gib einen Namen ein.")

def save_bmi():
    pass

def save_water():
    amount = entry_water.get()
    print(f"Speichere Wasser: {amount}ml")
    #cursor.execute(...)

def save_food():
    name = entry_food_name.get()
    cal = entry_food_cal.get()
    print(f"Speichere Essen: {name} ({cal} kcal)")
    #cursor.execute(...)


#-------- GUI - main window ----------
root = tk.Tk()
root.title("seda - version 0.1.")
root.geometry("600x1000")
#root.minsize(width=250, height=250)
#root.maxsize(width=600, height=600)
#root.resizable(width=False, height=False) #Größensperre

# part1. HEADER (greeting)
tk.Label(root, text="Willkommen bei seda!", font=("roboto", 20, "bold")).pack(pady=20)
tk.Label(root, text="seda hilft dir, deine Gesundheit zu verbessern.", font=("roboto", 12)).pack(pady=10)


# part1a. USER
tk.Label(root, text="Bitte gib unten deinen Benutzernamen ein.", font=("roboto", 12)).pack(pady=10)
user_frame = tk.Frame(root)
user_frame.pack(pady=10)

label_username = tk.Label(user_frame, text="Vorname:", font=("roboto", 12))
label_username.grid(row=0, column=0, padx=5)
entry_username = tk.Entry(user_frame, width=15)
entry_username.grid(row=0, column=1, padx=5)
button_save_username = tk.Button(user_frame, text="Speichern", command=save_username, bg="lightgrey")
button_save_username.grid(row=0, column=2, padx=5)

#horizontal line
separator = ttk.Separator(root, orient='horizontal').pack(fill='x', padx=10, pady=15)

# part 2. BMI-CALCULATOR
tk.Label(root, text="BMI-Rechner", font=("roboto", 20, "bold")).pack(pady=10)
bmi_frame = tk.Frame(root)
bmi_frame.pack(pady=10)

entry_bmi_age = tk.Entry(bmi_frame, width=15)
entry_bmi_age.grid(row=0, column=1, padx=5)
entry_bmi_age.insert(0, " Alter")

entry_bmi_height = tk.Entry(bmi_frame, width=15)
entry_bmi_height.grid(row=0, column=2, padx=5)
entry_bmi_height.insert(0, " Größe in cm")

entry_bmi_weight = tk.Entry(bmi_frame, width=15)
entry_bmi_weight.grid(row=0, column=3, padx=5)
entry_bmi_weight.insert(0, " Gewicht in kg")

button_save_bmi = tk.Button(bmi_frame, text="Berechnen", command=save_bmi, bg="lightgrey")
button_save_bmi.grid(row=0, column=4, padx=5)

tk.Label(root, text="Dein BMI beträgt:", font=("roboto", 12)).pack(pady=10)
#missing: return print BMI value here after calculation

#horizontal line
separator = ttk.Separator(root, orient='horizontal').pack(fill='x', padx=10, pady=15)

# 3. DASHBOARD CONTAINER 
dashboard_frame = tk.Frame(root)
dashboard_frame.pack(pady=10, padx=20, fill="x")

#3.a LEFT COLUMN: WATER-TRACKING
water_frame = tk.LabelFrame(dashboard_frame, text=" Wasser-Tracking ", font=("roboto", 14), padx=15, pady=15)
water_frame.grid(row=0, column=0, padx=10, sticky="nsew")

tk.Label(water_frame, text="Menge (ml):").pack()
entry_water = tk.Entry(water_frame, width=15)
entry_water.pack(pady=5)
tk.Button(water_frame, text="Speichern", command=save_water, bg="lightblue").pack(pady=5)

#3.b RIGHT COLUMN: FOOD
food_frame = tk.LabelFrame(dashboard_frame, text=" Nahrungs-Tracking ", font=("roboto", 14), padx=15, pady=15)
food_frame.grid(row=0, column=1, padx=10, sticky="nsew")

tk.Label(food_frame, text="Name:").pack()
entry_food_name = tk.Entry(food_frame, width=20)
entry_food_name.pack(pady=2)

tk.Label(food_frame, text="Kalorien (kcal):").pack()
entry_food_cal = tk.Entry(food_frame, width=20)
entry_food_cal.pack(pady=2)

tk.Button(food_frame, text="Speichern", command=save_food, bg="lightgreen").pack(pady=10)

# distributing space equally between the two columns
dashboard_frame.columnconfigure(0, weight=1)
dashboard_frame.columnconfigure(1, weight=1)

# 4. STATISTICS & HISTORY
stats_frame = tk.Frame(root, pady=20)
stats_frame.pack(fill="both", expand=True, padx=20)

tk.Label(stats_frame, text="Heute bisher:", font=("Arial", 12, "bold")).pack()
lbl_summary = tk.Label(stats_frame, text="0 / 2000 kcal  |  0 ml Wasser", fg="white")
lbl_summary.pack(pady=5)

#history via listbox (SQLite data)

#tk.Label(stats_frame, text="Letzte Aktivitäten:").pack(anchor="w")
#listbox = tk.Listbox(stats_frame, height=8)
#listbox.pack(fill="x", pady=5)

# 5. Footer
tk.Label(root, text="Tobias Mignat, Sabine Steverding", font=("Arial", 8)).pack(pady=5)

root.mainloop()