# This program was created for Introduction to programming university course

import tkinter as tk
from datetime import datetime
import os

version_control = "v 1.1" #updated the button colors and deadline layout
version_control = "v 1.2" #Added theme options and corrected button borders


# ---------------------- #
# Theme configuration    #
# ---------------------- #

def save_theme(theme_name):
    with open("theme.cfg", "w") as f:
        f.write(theme_name)

def load_theme():
    try:
        with open("theme.cfg") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Dark Blue"
    
def change_theme(new_theme, window):
    global current_theme
    current_theme = new_theme
    save_theme(new_theme)

    # Rebuild the greet window with the new theme
    window.destroy()
    greet_window(master)

    

themes = {
    "Dark Blue": {
        "bg": "#0E0036",
        "fg": "white",
        "accent": "#2f0272",
        "highlight": "#8F7EEC",
        "success": "#0D6805",
        "danger": "darkred",
        "text": "#C0B5FF"
    },
    "Dark Green": {
        "bg": "#002b00",
        "fg": "white",
        "accent": "#004d00",
        "highlight": "#09d309",
        "success": "#00aa00",
        "danger": "#660000",
        "text": "#AEDAB9"
    },
    "Light Mellow": {
        "bg": "#eee6da",
        "fg": "black",
        "accent": "#f1e5e5",
        "highlight": "#c49600",
        "success": "#008000",
        "danger": "#cc0000",
        "text": "#000000"
    },
    "Midnight Purple": { 
        "bg": "#1E1B2E", 
        "fg": "#E0E0E0", 
        "accent": "#3A2F5F", 
        "highlight": "#A68BFF", 
        "success": "#4CAF50", 
        "danger": "#D32F2F", 
        "text": "#CFC3FF" 
        },

    "Slate Gray": {
        "bg": "#2B2B2B",
        "fg": "#F2F2F2",
        "accent": "#3C3F41",
        "highlight": "#6EA4FF",
        "success": "#4CAF50",
        "danger": "#E53935",
        "text": "#D9D9D9"
    },

    "Solarized Light": {
        "bg": "#FDF6E3",
        "fg": "#657B83",
        "accent": "#EEE8D5",
        "highlight": "#B58900",
        "success": "#859900",
        "danger": "#DC322F",
        "text": "#586E75"
    },

    "Sunset Orange": {
        "bg": "#61300F",
        "fg": "#FFEDE6",
        "accent": "#7C3316",
        "highlight": "#FF8A50",
        "success": "#66BB6A",
        "danger": "#FF5252",
        "text": "#FFD6C9"
    },

    "Forest Mist": {
        "bg": "#E3EDE5",
        "fg": "#1F2E1F",
        "accent": "#C8D6CC",
        "highlight": "#6BAF7A",
        "success": "#2E7D32",
        "danger": "#B71C1C",
        "text": "#1A261A"
    },
    "Pastel Blossom": {
        "bg": "#F8E8EE",
        "fg": "#4A3F45",
        "accent": "#F2D3D8",
        "highlight": "#E7A9B9",
        "success": "#7BB661",
        "danger": "#D46A6A",
        "text": "#4A3F45"
    },
    "Pastel Mint": {
        "bg": "#E8FFF5",
        "fg": "#2F4F4F",
        "accent": "#D6F5E3",
        "highlight": "#A0E8CC",
        "success": "#4CAF50",
        "danger": "#D9534F",
        "text": "#2F4F4F"
    },
    "Cyberpunk Neon": {
        "bg": "#0A0014",
        "fg": "#E0E0FF",
        "accent": "#2A0055",
        "highlight": "#C800FF",
        "success": "#00FF9C",
        "danger": "#FF0055",
        "text": "#D8BFFF"
    },
    "Cyber Grid Blue": {
        "bg": "#000814",
        "fg": "#CFE8FF",
        "accent": "#001D3D",
        "highlight": "#00A8E8",
        "success": "#4EFFA1",
        "danger": "#FF3864",
        "text": "#A8D8FF"
    }

}

current_theme = load_theme()

def T(key):
    return themes[current_theme][key]


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
    view_deadlines.config(bg=T("bg"))
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
        fg=T("fg"),
        bg=T("bg")
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

        text_color = "red" if days <= 1 else T("text")
        text_font = ("Segoe UI", 12, "bold") if days <= 1 else ("Segoe UI", 12)



        # will use this for statistics later, currently, its for chekcing values
        for key, value in d.items():
            print(value, key)
            
            
        frame = tk.Frame(
            view_deadlines,
            bg=T("bg"),
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
            bg=T("bg"),                 # not done
            fg=T("text"),
            activebackground=T("highlight"),   # prevent flicker
            activeforeground="white",
            highlightthickness=1,
            highlightbackground="black",
            highlightcolor=T("success"),
            selectcolor=T("success"),             # done
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
            bg=T("bg"),
            width=14,
            font=text_font
        )
        time_left.pack(side=tk.RIGHT, padx=10)

    exit_butt = tk.Button(
        view_deadlines,
        text="Exit",
        command=lambda: quitting(view_deadlines),
        bg=T("accent"),
        activebackground=T("danger"),
        highlightthickness=1,
        highlightbackground="black",
        highlightcolor=T("success"),
        fg=T("text"),
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
        bg=T("accent"),
        activebackground=T("success"),
        highlightthickness=1,
        highlightbackground="black",
        highlightcolor=T("success"),
        fg=T("text"),
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
    saved_name.config(bg=T("bg"))
    saved_name.title("Saved deadline")
    saved_name.protocol("WM_DELETE_WINDOW", lambda: quitting(saved_name))
    save_label = tk.Label(saved_name, text=f"Saved upcoming deadline \n'{DL_name}' to date: \n{DL_time}", bg=T("bg"), font=("Segoe UI", 16), fg=T("text"))
    save_label.pack(padx=40, pady=40)
    continue_button = tk.Button(saved_name,
                                text="continue", 
                                command=saved_name.destroy, 
                                activebackground=T("success"), 
                                activeforeground="white",
                                highlightthickness=1,
                                highlightbackground="black",
                                highlightcolor=T("success"), 
                                anchor="center", 
                                bg=T("accent"), 
                                cursor="hand2", 
                                disabledforeground="navy", 
                                justify="center", 
                                fg=T("text"), 
                                overrelief="sunken", 
                                relief="flat",
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
    add_window.config(bg=T("bg"))
    if window:
        window.destroy()
    add_window.protocol("WM_DELETE_WINDOW", lambda: quitting(add_window))
    add_label = tk.Label(add_window,
                         text="Enter assigement name:",
                         font=("Segoe UI", 16, "bold"),
                         bg=T("bg"),
                         fg=T("text"))
    add_label.pack(pady=20)
    
    assign_name = tk.Entry(add_window, width=40, font=("Segoe UI", 14, "bold"), bg=T("highlight"))
    assign_name.pack(pady=20)
    
    assign_DL_label = tk.Label(add_window,
                         text="Enter deadline (YYYY-MM-DD HH:MM):",
                         bg=T("bg"),
                         fg=T("text"),
                         font=("Segoe UI", 14, "bold"))
    assign_DL_label.pack(pady=10)
    assign_DL = tk.Entry(add_window, width=40, font=("Segoe UI", 14, "bold"), bg=T("highlight"))
    assign_DL.pack(pady=30)
    



    save_assig = tk.Button(add_window,
                           text="Save Deadline",
                           command=lambda: saving_deadline(assign_name, assign_DL),
                           activebackground=T("success"),
                           activeforeground=T("text"),
                           highlightthickness=1,
                           highlightbackground="black",
                           highlightcolor=T("success"),
                           anchor="center",
                           bg=T("accent"),
                           cursor="hand2",
                           disabledforeground="navy",
                           justify="center",
                           fg=T("text"), overrelief="sunken", relief="flat",
                           font=("Segoe UI", 14, "bold"))
    save_assig.pack(pady=20)
    button_row = tk.Frame(add_window, bg=T("bg"))
    button_row.pack(pady=10)

    exit_save = tk.Button(button_row,
                           text="Exit",
                           command=lambda: quitting(add_window),
                           activebackground=T("danger"),
                           activeforeground=T("text"),
                           anchor="center",
                           bg=T("accent"),
                           cursor="hand2",
                           highlightthickness=1,
                           highlightbackground="black",
                           highlightcolor=T("danger"),
                           disabledforeground="navy",
                           justify="center",
                           fg=T("text"), overrelief="sunken", relief="flat",
                           font=("Segoe UI", 14))
    exit_save.pack(side=tk.LEFT, padx=10, pady=10)
    back_to_main = tk.Button(button_row,
                           text="Back",
                           command= lambda: greet_window(add_window),
                           activebackground=T("success"),
                           activeforeground=T("text"),
                           highlightthickness=1,
                           highlightbackground="black",
                           highlightcolor=T("success"),
                           anchor="center",
                           bg=T("accent"),
                           cursor="hand2",
                           disabledforeground="navy",
                           justify="center", overrelief="sunken", relief="flat",
                           fg=T("text"),
                           font=("Segoe UI", 14))
    back_to_main.pack(side=tk.LEFT, padx=10, pady=10)

    


#-------------------------------#
# quitting the program function #
#-------------------------------#
    
def quitting(window):
    exiting = tk.Toplevel(master)
    exiting.geometry("800x400+1100+100")
    exiting.config(bg=T("bg"))
    exiting.title("Exit program")
    
    if window:
        window.destroy()
    exiting.protocol("WM_DELETE_WINDOW", exit)

    exit_label =  tk.Label(exiting,
                    text = "Are you sure that you want to quit?\n Is everything saved?",
                    font = ("Segoe UI", 14, "bold"),
                    fg = T("text"),
                    bg = T("bg"),
                    anchor = "center")
    exit_label.pack(pady=50)
    
    exit_button_frame = tk.Frame(exiting, bg=T("bg"))
    exit_button_frame.pack(pady=20)
    
    sure_quit_button = tk.Button(exit_button_frame, 
                   text="Quit", 
                   command=exit,
                   activebackground=T("danger"), 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg=T("accent"),
                   cursor="hand2",
                   disabledforeground="navy",
                   fg=T("text"),
                   font=("Segoe UI", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=1,
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
                   activebackground=T("success"), 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg=T("accent"),
                   cursor="hand2",
                   fg=T("text"),
                   font=("Segoe UI", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor=T("success"),
                   highlightthickness=1,
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
    greet_win.config(bg=T("bg"))
    greet_win.geometry("700x500+1100+100")
 
    if window and window is not master:
        window.destroy()

    greet_win.protocol("WM_DELETE_WINDOW", lambda: quitting(greet_win))
    

    
    greeting = tk.Label(greet_win,
                        text = "Welcome! This is simple deadline manager. \nEnter your upcoming deadlines or view them in a list",
                        font = ("Segoe UI", 14, "bold"),
                        fg = T("text"),
                        bg = T("bg"),
                        anchor = "center")
    greeting.pack(pady=50)
    

    button_frame = tk.Frame(greet_win, bg=T("bg"))
    button_frame.pack(pady=20)


    DL_button = tk.Button(
        button_frame,
        text="View deadlines",
        command=lambda: deadline_button(greet_win), activebackground=T("highlight"), 
                    activeforeground="white",
                    anchor="center",
                    bd=3,
                    bg=T("accent"),
                    cursor="hand2",
                    disabledforeground="navy",
                    fg=T("text"),
                    font=("Segoe UI", 12),
                    height=2,
                    highlightbackground="black",
                    highlightcolor=T("success"),
                    highlightthickness=1,
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
        activebackground=T("highlight"), activeforeground="white", anchor="center", bd=3, bg=T("accent"), cursor="hand2", fg=T("text"),
        font=("Segoe UI", 12),
        height=2,
        highlightbackground="black",
        highlightcolor=T("success"),
        highlightthickness=1,
        justify="center",
        relief="flat",
        overrelief="sunken",
        padx=10,
        pady=5,
        width=12,
        wraplength=100)

    EDL_button.pack(side=tk.RIGHT, padx=10, pady=10)

    quit_frame = tk.Frame(greet_win, bg=T("bg"))
    quit_frame.pack(pady=10)

    theme_var = tk.StringVar(value=current_theme)

    theme_menu = tk.OptionMenu(
        quit_frame,
        theme_var,
        *themes.keys(),
        command=lambda choice: change_theme(choice, greet_win)
    )
    theme_menu.config( bg=T("accent"), 
                      fg=T("text"), 
                      activebackground=T("highlight"), 
                      activeforeground=T("fg"), 
                      highlightthickness=1,
                      highlightbackground="black", 
                      bd=0, 
                      font=("Segoe UI", 12), pady=5 )
    
    menu = theme_menu["menu"] 
    menu.config( bg=T("accent"), 
                fg=T("text"), 
                activebackground=T("highlight"), 
                activeforeground=T("fg"), 
                font=("Segoe UI", 12),
                bd=0 ) 



    quit_button = tk.Button(
        quit_frame,   # attach to greet_win, not master
        text="Quit",
        command=lambda: quitting(greet_win),
        activebackground="darkred", 
                    activeforeground="white",
                    anchor="center",
                    bd=0,
                    bg=T("accent"),
                    cursor="hand2",
                    fg=T("text"),
                    font=("Segoe UI", 12),
                    height=1,
                    highlightbackground="black",
                    highlightcolor=T("danger"),
                    highlightthickness=1,
                    justify="center",
                    relief="flat",
                    overrelief="sunken",
                    padx=4,
                    pady=5,
                    width=10,
                    wraplength=100)
    quit_button.pack(side=tk.LEFT, padx=20, pady=20)
    theme_menu.pack(side=tk.RIGHT, pady=2, padx=10)









master = tk.Tk()
master.tk.call('tk', 'scaling', 1.5)
master.withdraw()

greet_window(master)
master.mainloop()


