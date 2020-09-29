import tkinter as tk
import Logic as Lg

HEIGHT = 300
WIDTH = 500
background_colour_1 = "#DDDDDD"
background_colour_2 = "#CCCCCC"

root = tk.Tk()
root.title('OAST Project nr 1')
root.iconbitmap('logo_PW.ico')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=background_colour_1)
canvas.pack()

"""First frame"""

frame_star_val = tk.Frame(root, bg=background_colour_2, bd=5)
frame_star_val.place(relx=0.05, rely=0.05, relwidth=0.425, relheight=0.9)

"""Influx"""

frame_influx = tk.LabelFrame(frame_star_val, text="Influx from 0.5 to 6", font=16, bg=background_colour_2, padx=5,
                             pady=5)
frame_influx.place(relwidth=1, relheight=0.33)

entry_influx = tk.Entry(frame_influx, font=20, text="1")
entry_influx.insert(0, "1")
entry_influx.place(relwidth=1, relheight=0.9)

"""Time of simulation"""

frame_time = tk.LabelFrame(frame_star_val, text="Time of simulation", font=16, bg=background_colour_2, padx=5, pady=5)
frame_time.place(rely=0.33, relwidth=1, relheight=0.33)

entry_time = tk.Entry(frame_time, font=20)
entry_time.insert(0, "10")
entry_time.place(relwidth=1, relheight=0.9)

"""Type of simulation"""

frame_onoff = tk.LabelFrame(frame_star_val, text="Server state", font=16, bg=background_colour_2, padx=5, pady=5)
frame_onoff.place(rely=0.66, relwidth=1, relheight=0.33)

type_s = tk.BooleanVar()
type_s.set(True)

tk.Radiobutton(frame_onoff, text="Without exlusions", variable=type_s, value=False, bg=background_colour_2, font=18).\
    pack(anchor='w')
tk.Radiobutton(frame_onoff, text="With exlusions", variable=type_s, value=True, bg=background_colour_2, font=18).\
    pack(anchor='w')

"""Second frame"""

frame_calculation = tk.Frame(root, bg=background_colour_2, bd=5)
frame_calculation.place(relx=0.525, rely=0.05, relwidth=0.425, relheight=0.9)

button_calculation = tk.Button(frame_calculation, text="Simulation", bg=background_colour_2, font=20,
                               command=lambda: Lg.sim_var(float(entry_influx.get()), int(entry_time.get()),
                                                          type_s.get()))
button_calculation.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.2)

button_diagram = tk.Button(frame_calculation, text="Diagram", bg=background_colour_2, font=20,
                           command=lambda: Lg.show_diagram(type_s.get()))
button_diagram.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.2)

button_save = tk.Button(frame_calculation, text="Save", bg=background_colour_2, font=20,
                        command=lambda: Lg.save_simulation(type_s.get()))
button_save.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)

root.mainloop()
