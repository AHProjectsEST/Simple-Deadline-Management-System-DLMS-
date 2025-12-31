# This program was created for Introduction to programming university course

import tkinter as tk
from datetime import datetime
import os

version_control = "v 1.1" #updated the button colors and deadline layout


#storing all the colors here
blue_color = "#0E0036"
light_blue = "#C1CFFF"
green = "#0D6805"
purple = "#2f0272"




#-----------------------------------#
# defining all my functions to call #
#-----------------------------------#


#----------------------------------------#
# deadline done status updating function #
#----------------------------------------#

def update_status(name, new_status, window=None):
    lines = []
    with open("DLMS.txt") as f:
        for line in f:
            parts = line.strip().split(";")
            if len(parts) == 3:
                if parts[0] == name:
                    parts[2] = str(new_status)
                lines.append(";".join(parts))
    with open("DLMS.txt", "w") as f:
        for l in lines:
            f.write(l + "\n")

    print(f"Updated {name} to {new_status}")

    


#---------------------------#
# deadline viewing function #
#---------------------------#

def deadline_button(window):
    print("Deadlines entered")

    view_deadlines = tk.Toplevel(master)
    view_deadlines.title("Upcoming deadlines")
    view_deadlines.config(bg=blue_color)
    view_deadlines.geometry("+1100+100")
    view_deadlines.minsize(width=700, height=400)
    view_deadlines.protocol(
        "WM_DELETE_WINDOW",
        lambda: quitting(view_deadlines)
    )

    view_label = tk.Label(
        view_deadlines,
        text="Upcoming deadlines:",
        font=("Segoe UI Semibold", 22),
        fg="white",
        bg=blue_color
    )
    view_label.pack(pady=30)

    if window:
        window.destroy()

    deadlines = []

    try:
        with open("DLMS.txt") as file:
            for line in file:
                items = line.strip().split(";")

                date_str = items[1].strip()
                if len(date_str) == 10:
                    date_str += " 23:59"

                if len(items) == 3:
                    try:
                        deadline_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                    except:
                        deadline_dt = None

                    deadlines.append({
                        "name": items[0],
                        "deadline_dt": deadline_dt,
                        "done_status": int(items[2].strip())
                    })
    except:
        print("file not found")

    now = datetime.now()
    deadlines = sorted(
        [d for d in deadlines if d["deadline_dt"]],
        key=lambda d: d["deadline_dt"] - now
    )


    #outer loop for each deadline
    view_deadlines.cb_vars = []

    for d in deadlines:
        try:
            deadline_dt = d["deadline_dt"]
            diff = deadline_dt - now


            #calculating time left
            days = diff.days
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60

            if days < -1 or not d["name"]:
                continue

            if days == 0:
                time_left_str = f"{hours}h, {minutes}min left"
            elif days == 0 and hours == 0:
                time_left_str = f"{minutes}min left"
            else:
                time_left_str = f"{days}d, {hours}h left"
        except:
            time_left_str="Invalid date format"

        text_color = "red" if days <= 1 else "white"
        text_font = ("Segoe UI", 12, "bold") if days <= 1 else ("Segoe UI", 12)



        # will use this for statistics later, currently, its for chekcing values
        for key, value in d.items():
            print(value, key)
            
            
        frame = tk.Frame(
            view_deadlines,
            bg=blue_color,
            padx=8,
            pady=6
        )
        frame.pack(fill="x", padx=25, pady=6)

        cb_var = tk.IntVar(value=d["done_status"])
        view_deadlines.cb_vars.append(cb_var)

        cb = tk.Checkbutton(
            frame,
            text=d["name"],
            variable=cb_var,
            command=lambda n=d["name"], var=cb_var: update_status(n, var.get()),
            indicatoron=False,
            bg=blue_color,                 # not done
            fg="white",
            activebackground=purple,   # prevent flicker
            activeforeground="white",
            selectcolor=green,             # done
            font=("Segoe UI", 12),
            relief="flat",
            anchor="w",
            padx=10,
            pady=6
        )

        # Exam styling — TEXT ONLY
        if "exam" in d["name"].lower():
            cb.config(fg="red", activeforeground="red", font=("Segoe UI", 12, "bold"))

        cb.pack(side=tk.LEFT, fill="x", expand=True)

        if cb_var.get() == 1:
            cb.select()

        time_left = tk.Label(
            frame,
            text=time_left_str,
            fg=text_color,
            bg=blue_color,
            width=14,
            font=text_font
        )
        time_left.pack(side=tk.RIGHT, padx=10)

    exit_butt = tk.Button(
        view_deadlines,
        text="Exit",
        command=lambda: quitting(view_deadlines),
        bg=purple,
        activebackground="darkred",
        fg="white",
        font=("Segoe UI Semibold", 13),
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2"
    )
    exit_butt.pack(pady=(25, 10))

    back_to_add_DL = tk.Button(
        view_deadlines,
        text="Add more deadlines",
        command=lambda: add_DL_button(view_deadlines),
        bg=purple,
        activebackground=green,
        fg="white",
        font=("Segoe UI Semibold", 13),
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2", 
    )
    back_to_add_DL.pack(pady=(0, 25))



#--------------------------#
# deadline saving function #
#--------------------------#
    
def saving_deadline(name, time):
    print("Deadline saved")
    DL_name = name.get()
    DL_time = time.get()
    done_stat = 0
    with open("DLMS.txt", "a") as f:
        f.write(f"{DL_name};{DL_time};{done_stat}\n")
    print("Saved to:", os.path.abspath("DMLS.txt"))
    saved_name = tk.Toplevel(master)
    saved_name.geometry("600x300+1100+100")
    saved_name.config(bg=blue_color)
    saved_name.title("Saved deadline")
    saved_name.protocol("WM_DELETE_WINDOW", lambda: quitting(save_name))
    save_label = tk.Label(saved_name, text=f"Saved upcoming deadline \n'{DL_name}' to date: \n{DL_time}", bg=blue_color, font=("Segoe UI", 16), fg="white")
    save_label.pack(padx=40, pady=40)
    continue_button = tk.Button(saved_name,
                                text="continue", command=saved_name.destroy, activebackground=green, activeforeground="white", 
                                anchor="center", bg=purple, cursor="hand2", disabledforeground="navy", justify="center", fg="white", overrelief="sunken", relief="flat",
                                font=("Segoe UI", 14))
    continue_button.pack(pady=20)
    


#--------------------------#
# deadline adding function #
#--------------------------#

def add_DL_button(window):
    print("Added deadline")
    add_window = tk.Toplevel(master)
    add_window.title("Add Deadline")
    add_window.geometry("700x500+1100+100")
    add_window.config(bg=blue_color)
    if window:
        window.destroy()
    add_window.protocol("WM_DELETE_WINDOW", lambda: quitting(add_window))
    add_label = tk.Label(add_window,
                         text="Enter assigement name:",
                         font=("Segoe UI", 16),
                         bg=blue_color,
                         fg="white")
    add_label.pack(pady=20)
    
    assign_name = tk.Entry(add_window, width=40, font=("Segoe UI", 12), bg=light_blue)
    assign_name.pack(pady=20)
    
    assign_DL_label = tk.Label(add_window,
                         text="Enter deadline (YYYY-MM-DD HH:MM):",
                         bg=blue_color,
                         fg="white",
                         font=("Segoe UI", 14))
    assign_DL_label.pack(pady=10)
    assign_DL = tk.Entry(add_window, width=40, font=("Segoe UI", 12), bg=light_blue)
    assign_DL.pack(pady=30)
    



    save_assig = tk.Button(add_window,
                           text="Save Deadline",
                           command=lambda: saving_deadline(assign_name, assign_DL),
                           activebackground=green,
                           activeforeground="white",
                           anchor="center",
                           bg=purple,
                           cursor="hand2",
                           disabledforeground="navy",
                           justify="center",
                           fg="white", overrelief="sunken", relief="flat",
                           font=("Segoe UI", 14, "bold"))
    save_assig.pack(pady=20)
    button_row = tk.Frame(add_window, bg=blue_color)
    button_row.pack(pady=10)

    exit_save = tk.Button(button_row,
                           text="Exit",
                           command=lambda: quitting(add_window),
                           activebackground="darkred",
                           activeforeground="white",
                           anchor="center",
                           bg=purple,
                           cursor="hand2",
                           disabledforeground="navy",
                           justify="center",
                           fg="white", overrelief="sunken", relief="flat",
                           font=("Segoe UI", 14))
    exit_save.pack(side=tk.LEFT, padx=10, pady=10)
    back_to_main = tk.Button(button_row,
                           text="Back",
                           command= lambda: greet_window(add_window),
                           activebackground=green,
                           activeforeground="white",
                           anchor="center",
                           bg=purple,
                           cursor="hand2",
                           disabledforeground="navy",
                           justify="center", overrelief="sunken", relief="flat",
                           fg="white",
                           font=("Segoe UI", 14))
    back_to_main.pack(side=tk.LEFT, padx=10, pady=10)

    


#-------------------------------#
# quitting the program function #
#-------------------------------#
    
def quitting(window):
    exiting = tk.Toplevel(master)
    exiting.geometry("800x400+1100+100")
    exiting.config(bg=blue_color)
    exiting.title("Exit program")
    
    if window:
        window.destroy()
    exiting.protocol("WM_DELETE_WINDOW", exit)

    exit_label =  tk.Label(exiting,
                    text = "Are you sure that you want to quit?\n Is everything saved?",
                    font = ("Segoe UI", 14, "bold"),
                    fg = "white",
                    bg = blue_color,
                    anchor = "center")
    exit_label.pack(pady=50)
    
    exit_button_frame = tk.Frame(exiting, bg=blue_color)
    exit_button_frame.pack(pady=20)
    
    sure_quit_button = tk.Button(exit_button_frame, 
                   text="Quit", 
                   command=exit,
                   activebackground="darkred", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg=purple,
                   cursor="hand2",
                   disabledforeground="navy",
                   fg="white",
                   font=("Segoe UI", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="sunken", relief="flat",
                   padx=10,
                   pady=5,
                   width=15,
                   wraplength=100)
    sure_quit_button.pack(side=tk.RIGHT, padx=10, pady=10)
    
    dont_quit = tk.Button(exit_button_frame, 
                   text="Back", 
                   command=lambda: greet_window(exiting),
                   activebackground=green, 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg=purple,
                   cursor="hand2",
                   disabledforeground="navy",
                   fg="white",
                   font=("Segoe UI", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="sunken", relief="flat",
                   padx=10,
                   pady=5,
                   width=15,
                   wraplength=100)
    dont_quit.pack(side=tk.RIGHT, padx=10, pady=10)
    
    
    
    
#----------------------#
# Greeting main window #
#----------------------#

def greet_window(window):
    greet_win = tk.Toplevel(master)
    #forcing the greet window to be on top, because i had bugs where it would only display when clicked elsewhere
    greet_win.attributes("-topmost", True)
    greet_win.after(100, lambda: greet_win.attributes("-topmost", False))  
    greet_win.title(f"Deadline management system {version_control}")
    greet_win.config(bg=blue_color)
    greet_win.geometry("700x400+1100+100")
 
    if window and window is not master:
        window.destroy()

    greet_win.protocol("WM_DELETE_WINDOW", lambda: quitting(greet_win))
    greeting = tk.Label(greet_win,
                        text = "Welcome! This is simple deadline manager. \nEnter your upcoming deadlines or view them in a list",
                        font = ("Segoe UI", 14, "bold"),
                        fg = "white",
                        bg = blue_color,
                        anchor = "center")
    greeting.pack(pady=50)

    button_frame = tk.Frame(greet_win, bg=blue_color)
    button_frame.pack(pady=20)

    DL_button = tk.Button(
        button_frame,
        text="View deadlines",
        command=lambda: deadline_button(greet_win), activebackground="blue", 
                    activeforeground="white",
                    anchor="center",
                    bd=3,
                    bg=purple,
                    cursor="hand2",
                    disabledforeground="navy",
                    fg="white",
                    font=("Segoe UI", 12),
                    height=2,
                    highlightbackground="black",
                    highlightcolor="green",
                    highlightthickness=2,
                    justify="center",
                    relief="flat",
                    overrelief="sunken", 
                    padx=12,
                    pady=5,
                    width=10,
                    wraplength=100)


    DL_button.pack(side=tk.LEFT, padx=10, pady=10)

    EDL_button = tk.Button(
        button_frame,
        text="Add deadlines",
        command=lambda: add_DL_button(greet_win),
        activebackground="blue", activeforeground="white", anchor="center", bd=3, bg=purple, cursor="hand2", disabledforeground="navy", fg="white",
        font=("Segoe UI", 12),
        height=2,
        highlightbackground="black",
        highlightcolor="green",
        highlightthickness=2,
        justify="center",
        relief="flat",
        overrelief="sunken",
        padx=10,
        pady=5,
        width=12,
        wraplength=100)

    EDL_button.pack(side=tk.RIGHT, padx=10, pady=10)

    quit_button = tk.Button(
        greet_win,   # attach to greet_win, not master
        text="Quit",
        command=lambda: quitting(greet_win),
        activebackground="darkred", 
                    activeforeground="white",
                    anchor="center",
                    bd=3,
                    bg=purple,
                    cursor="hand2",
                    disabledforeground="navy",
                    fg="white",
                    font=("Segoe UI", 12),
                    height=1,
                    highlightbackground="black",
                    highlightcolor="green",
                    highlightthickness=2,
                    justify="center",
                    relief="flat",
                    overrelief="sunken",
                    padx=4,
                    pady=2,
                    width=10,
                    wraplength=100)
    quit_button.pack(side=tk.TOP, padx=20, pady=20)






master = tk.Tk()
master.tk.call('tk', 'scaling', 1.5)
master.withdraw()

greet_window(master)
master.mainloop()


