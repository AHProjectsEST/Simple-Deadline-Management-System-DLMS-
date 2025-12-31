
# **DLMS — Deadline Management System**

DLMS is a lightweight and local **Deadline Management System** designed to help you track tasks, due dates, and upcoming deadlines without relying on cloud services or heavy frameworks.  
It runs as a simple Python application and integrates into your Linux applications menu like a native app.

Deadlines are saved into text file in the same folder where the py file is stored.
Written with native tkinter so no extra library installation is needed.

Current theme is dark blue/violet. Theme choice option will be integrated in the future.

---

## **Features**

- Minimal, fast, and easy to use  
- Local storage — no accounts, no syncing, no data collection  
- Native Linux launcher via `.desktop` integration  
- Automatic scaling support for HiDPI displays  
- Simple installation with one script
- Toggle task done or undone (indicated via green box)  

---

# **Installation (Linux)**

Follow these steps to install DLMS on any Linux system.

### **1. Clone the repository**

```bash
git clone https://github.com/AHProjectsEST/DLMS.git
cd DLMS
```

### **2. Make the installer executable**

```bash
chmod +x install.sh
```

### **3. Run the installer**

```bash
./install.sh
```

This will:

- Copy DLMS into `~/.local/share/DLMS`
- Install a launcher into `~/.local/share/applications`
- Add an icon and menu entry
- Make the app available in your system’s application menu

---

# **Running DLMS**

After installation, you can launch DLMS:

- From your **Applications Menu** (search for *DLMS*)
- Or manually:

```bash
~/.local/share/DLMS/run.sh
```

---

# **Uninstallation**

To remove DLMS:

```bash
rm -rf ~/.local/share/DLMS
rm ~/.local/share/applications/DLMS.desktop
```

You may need to refresh your desktop environment’s application cache or log out and back in.
```bash
xdg-desktop-menu forceupdate
```
---

# **Requirements**

- Python 3  
- Linux desktop environment (GNOME, KDE, XFCE, etc.)

---

# **Windows version installation coming soon**

You can run just the py file on windows meanwhile
